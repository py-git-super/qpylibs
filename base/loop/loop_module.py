import _thread
import utime
import gc

type_gen = type((lambda: (yield))())
DEFAUT_TIME = 150
MAX_CYCLE = 12 * 60 * 60 * 1000
MAX_CYCLE_SECONDS = 12 * 60 * 60
SERVICES_STARTED = False


class CTask(object):
    def __init__(self, fun, long, *args, **kwargs):
        self.long = long
        self.fun = fun
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.fun(*self.args, **self.kwargs)


def task(long=False):
    def wrap(fun):
        def _warp(*args, **kwargs):
            t = CTask(fun, long, *args, **kwargs)
            return t

        return _warp

    return wrap


def cticks_diff(start, end):
    r = start - end
    if abs(r) > MAX_CYCLE:
        return -1
    return r


def cticks_ms():
    return utime.ticks_ms()


def default_except_handler(e):
    # sys.print_exception(e)
    # print( e)
    raise e


def ph_meld(h1, h2):
    if h1 is None:
        return h2
    if h2 is None:
        return h1
    lt = cticks_diff(h1.ph_key, h2.ph_key) < 0
    # lt = (h1.ph_key - h2.ph_key) < 0
    if lt:
        if h1.ph_child is None:
            h1.ph_child = h2
        else:
            h1.ph_child_last.ph_next = h2
        h1.ph_child_last = h2
        h2.ph_next = None
        h2.ph_rightmost_parent = h1
        return h1
    else:
        h1.ph_next = h2.ph_child
        h2.ph_child = h1
        if h1.ph_next is None:
            h2.ph_child_last = h1
            h1.ph_rightmost_parent = h2
        return h2


# pairing-heap pairing operation; amortised O(log N)
def ph_pairing(child):
    heap = None
    while child is not None:
        n1 = child
        child = child.ph_next
        n1.ph_next = None
        if child is not None:
            n2 = child
            child = child.ph_next
            n2.ph_next = None
            n1 = ph_meld(n1, n2)
        heap = ph_meld(heap, n1)
    return heap


# pairing-heap delete of a node; stable, amortised O(log N)
def ph_delete(heap, node):
    if node is heap:
        child = heap.ph_child
        node.ph_child = None
        return ph_pairing(child)
    # Find parent of node
    parent = node
    while parent.ph_next is not None:
        parent = parent.ph_next
    parent = parent.ph_rightmost_parent
    # Replace node with pairing of its children
    if node is parent.ph_child and node.ph_child is None:
        parent.ph_child = node.ph_next
        node.ph_next = None
        return heap
    elif node is parent.ph_child:
        child = node.ph_child
        next = node.ph_next
        node.ph_child = None
        node.ph_next = None
        node = ph_pairing(child)
        parent.ph_child = node
    else:
        n = parent.ph_child
        while node is not n.ph_next:
            n = n.ph_next
        child = node.ph_child
        next = node.ph_next
        node.ph_child = None
        node.ph_next = None
        node = ph_pairing(child)
        if node is None:
            node = n
        else:
            n.ph_next = node
    node.ph_next = next
    if next is None:
        node.ph_rightmost_parent = parent
        parent.ph_child_last = node
    return heap


class ASYTask:
    def __init__(self, coro):
        self.coro = coro  # Coroutine of this Task
        self.data = None  # General data for queue it is waiting on
        self.state = True  # None, False, True or a TaskQueue instance
        self.ph_key = 0  # Pairing heap
        self.ph_child = None  # Paring heap
        self.ph_child_last = None  # Paring heap
        self.ph_next = None  # Paring heap
        self.ph_rightmost_parent = None  # Paring heap

    def __str__(self):
        return str(self.coro)


# TaskQueue class based on the above pairing-heap functions.
class TaskQueue:
    def __init__(self):
        self.heap = None

    def peek(self):
        return self.heap

    def push_sorted(self, v, key):
        v.data = None
        v.ph_key = key
        v.ph_child = None
        v.ph_next = None
        self.heap = ph_meld(v, self.heap)

    def push_head(self, v):
        self.push_sorted(v, cticks_ms())  # 添加任务

    def pop_head(self):
        v = self.heap
        if self.heap:
            self.heap = ph_pairing(self.heap.ph_child)
        return v

    def remove(self, v):
        self.heap = ph_delete(self.heap, v)


_tasks = TaskQueue()
cur_task = None


class SingletonGenerator:
    def __init__(self):
        self.state = None
        self.exc = StopIteration()

    def __iter__(self):
        return self

    def __next__(self):
        if self.state is not None:
            # print(cur_task)
            _tasks.push_sorted(cur_task, self.state)
            self.state = None
            return None
        else:
            self.exc.__traceback__ = None
            raise self.exc


def csleep_ms(t, sgen=SingletonGenerator()):
    assert sgen.state is None
    sgen.state = cticks_ms() + max(0, t)
    return sgen


def csleep(t):
    return csleep_ms(t * 1000)


class Loop(object):
    def __init__(self):

        self._exception_handler = default_except_handler
        self._flag = True
        self.service_started = False
        self.tasks_lock_add = _thread.allocate_lock()
        self.tasks_lock_del = _thread.allocate_lock()

    def create_task(self, task):
        if task.long:
            return _thread.start_new_thread(self.exec_long_task, (task,None))
        else:
            result = task()
            if isinstance(result, type_gen):
                # self._tasks.put(task)
                self.tasks_lock_add.acquire()
                t = ASYTask(result)
                _tasks.push_head(t)
                self.tasks_lock_add.release()
                return t

    def cancel_task(self, task):
        if not isinstance(task, (ASYTask, int)):
            return
        if isinstance(task, ASYTask):
            self.tasks_lock_del.acquire()
            if cticks_diff(task.ph_key, cticks_ms()) > 0:
                _tasks.remove(task)
            self.tasks_lock_del.release()
        else:
            try:
                _thread.stop_thread(task)
            except Exception as e:
                print(e)

    def is_done(self, task):
        return cticks_diff(task.ph_key, cticks_ms()) < 0

    def exec_long_task(self,task,cycle):
        print("创建线程.................")
        try:
            if cycle == 0 or cycle is None:
                task()
            else:
                while True:
                    utime.sleep(cycle)
                    task()
        except Exception as e:
            self._exception_handler(e)

    def loop2init(self):
        global _tasks
        self._flag = True
        self.service_started = False
        while _tasks.pop_head():
            utime.sleep(1)
            continue

    def close(self):
        self._flag = False
        while _tasks.pop_head():
            pass

    def set_exception_handler(self, fun):
        self._exception_handler = fun

    def schedule_interval(self, task, cycle=0):
        if task.long or cycle > MAX_CYCLE_SECONDS:
            return _thread.start_new_thread(self.exec_long_task, (task,cycle,))
        else:
            if cycle <= 0:
                result = task()
            else:
                def _warp_task():
                    while True:
                        yield from csleep(cycle)
                        task()

                result = _warp_task()
            if isinstance(result, type_gen):
                # self._tasks.put(task)
                self.tasks_lock_add.acquire()
                t = ASYTask(result)
                _tasks.push_head(t)
                self.tasks_lock_add.release()
                return t

    def schedule_once(self, task, later=0):
        if task.long:
            return _thread.start_new_thread(self.exec_long_task, (task,))
        else:
            if later <= 0:
                result = task()
            else:
                def _warp_task():
                    yield from csleep(later)
                    task()
                result = _warp_task()
            if isinstance(result, type_gen):
                # self._tasks.put(task)
                self.tasks_lock_add.acquire()
                t = ASYTask(result)
                _tasks.push_head(t)
                self.tasks_lock_add.release()
                return t

    def run_forever(self):
        self.service_started = True
        global cur_task
        while self._flag:
            try:
                dt = 1
                while dt > 0:
                    dt = -1
                    t = _tasks.peek()
                    if t:
                        # A task waiting on _task_queue; "ph_key" is time to schedule task at
                        # dt = max(0, t.ph_key-utime.time())
                        dt = max(0, cticks_diff(t.ph_key, cticks_ms()))
                        # print(t, t.ph_key,dt)

                        utime.sleep_ms(20)
                t = _tasks.pop_head()
                if not t:
                    utime.sleep_ms(20)
                    continue
                cur_task = t
                t.coro.send(None)
            except StopIteration:
                pass
            except Exception as e:
                self._exception_handler(e)
        else:
            self.loop2init()


current = Loop()


# @task()
# def free_mem():
#     '''
#     垃圾回收
#     '''
#     cycle = 2 * 60
#     while True:
#         yield from csleep(cycle)
#         cur_mem = gc.mem_free()
#         gc.collect()
#         print("释放内存：", gc.mem_free() - cur_mem)
#
#
# current.create_task(free_mem())
