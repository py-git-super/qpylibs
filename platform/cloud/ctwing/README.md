# ctwing

#### 介绍

qpy平台ctwing连接代码说明





#### 使用说明



1. 实例1

   ```python
   from usr.ctwing import CtwingModule
   
   # ctwing平台连接地址
   server = "221.229.214.202"
   # ctwing 平台连接端口
   port = "5683"
   
   # 初始化连接对象
   ctwing_obj = CtwingModule(server, port)
   # 发起连接请求
   connect_sta = ctwing_obj.connect()
   print("connect sta is {}".format(connect_sta))
   ```

