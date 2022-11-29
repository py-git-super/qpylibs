# onenet



#### 介绍

qpy平台使用onenet连接套件代码说明







#### 使用说明

1. 实例1

```python
from usr.onenet import OnenetModule

# 创建onenet连接对象
onenet_obj = OnenetModule()
# 配置文件
config_list = [0, '0', 0, 10, 0, 0, 0]
# 配置标识
config_flag = 2
# lwm2m实例参数
obj_list = [0, 3303, 2, "11", 6,1]
# 设置连接引导配置
sta = onenet_obj.setConfig(config_list, config_flag)
print("setConfig sta = {}".format(sta))
# 创建通信连接实例，返回实例id
instance_id = onenet_obj.createCommunicationInstance()
print("createCommunicationInstance instance_id = {}".format(instance_id))
# 添加lwm2m实例
sta = onenet_obj.addLwM2mObject(obj_list)
print("addLwM2mObject sta = {}".format(sta))
# 发起注册连接请求
sta = onenet_obj.connect(instance_id, 360)
print("connect sta = {}".format(sta))
```

