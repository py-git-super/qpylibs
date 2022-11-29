# loop

#### 介绍
qpy平台任务调度器,不接触平台底层实现周期任务和创建线程。
例如创建线程只需要用装饰器task(long=True)就能创建线程：

```
@task(long=True)
def long_task():
   print("我是新建线程")
```


#### 使用说明
note：方法或者函数必须使用装饰器task才能成为任务

# 实例：

```
from  usr.loop import current ,task,csleep_ms,csleep
import utime

@task()
def task1():
    print("i am run once")

@task()
def task2(cycle):
    '''
    每五秒运行一次
    :return:
    '''
    print("周期为：",cycle)
    print("当前的时间为：",utime.time())

current.schedule_once(task1())#schedule_once(task, later=0) later为什么时候运行，小于0马上运行，大于0则later秒后运行
current.schedule_once(task1(),later=10)# 十秒之后运行task1()
schedule_interval_5 =  current.schedule_interval(task2(5),cycle=5)# schedule_interval( task, cycle=0),cycle小于等于0，马上运行，相当于schedule_once，cycle大于0是周期为cycle的周期任务
schedule_interval_10 = current.schedule_interval(task2(10),cycle=10)#创建周期为10s的任务

@task(long=True)
def long_task():
    '''
    创建线程
    :return:
    '''
    while True:
        print("我是长期运行的任务")
        utime.sleep(5)


long_task = current.create_task(long_task())
@task()
def control_exactly():
'''
   如果想对任务进行精细的控制 可以用yield from
   csleep_ms(ms) :毫秒
   csleep(s)：秒
   yield from csleep_ms(100)任务暂停100毫秒
   yield from csleep(10)任务暂停10s

'''
    print("run after 1s")
    yield from csleep_ms(100)  # 暂停一百毫秒
    print("going on ")



@task()
def close_loop():
    '''
    关闭循环
    :return:
    '''
    import gc
    current.close()#关闭调度器


@task()
def cancle_task():
    current.cancel_task(schedule_interval_5)#取消任务
    current.cancel_task(schedule_interval_10)#取消任务
    current.cancel_task(long_task)#取消任务
    print("一分钟后停止loop", )
    current.schedule_once(close_loop(),later=60)# 60秒后运行

current.create_task(control_exactly())
current.schedule_once(cancle_task(),later=120)# 120秒后运行
current.run_forever()#一定要记得调用，否则任务不运行



```


