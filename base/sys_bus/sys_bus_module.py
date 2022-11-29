import sys_bus
import utime 
def cb_callback(topic, msg):
    print(topic, msg)
# 支持一个topic 可以注册多个订阅函数
sys_bus.subscribe("topic1", cb_callback)
sys_bus.subscribe("topic2", cb_callback)
sys_bus.subscribe("topic3", cb_callback)


"发布后订阅者会收到消息"
sys_bus.publish("topic1", " 此处打印的是topic1的发布消息")
utime.sleep(2)
sys_bus.publish("topic2", " 此处打印的是topic2的发布消息")
utime.sleep(2)
sys_bus.publish("topic3", " 此处打印的是topic3的发布消息")
utime.sleep(2)

print(sys_bus.sub_table())
# 返回 {"topic1": set(cb_callback...)}
utime.sleep(2)
print(sys_bus.sub_table("topic1"))
# 返回 set(cb_callback...)

sys_bus.unsubscribe("topic1", cb_callback)
#由于上面取消了订阅callback,所以下面的发布不会进入之前的callback，即：此时仍可以收到订阅消息，但是没有callback
sys_bus.publish("topic1", " 此处打印的是topic1的发布消息")

sys_bus.unsubscribe("topic1")
#由于上面取消了topic1的订阅,所以下面的发布不会收到任何消息
sys_bus.publish("topic1", " 此处打印的是topic1的发布消息")
