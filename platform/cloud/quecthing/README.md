# quecthing



#### 介绍

qpy平台使用quecthing连接套件代码说明







#### 使用说明

1. 实例1

```python
from usr.quecthing import QuecthingModule

# 输入移远云产品PK
pk = ""  
# 输入移远云产品PS
ps = ""
# 输入移远云平台连接地址
server = ""
# 创建移远云连接对象
quecthing_obj = QuecthingModule(pk, ps, server)
# 初始化连接属性
quecthing_obj.cloudInit()
# 发起注册请求
quecthing_obj.connect()
```

