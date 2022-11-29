### lis2dh12

默认初始化2G量程。

**类引用：**

```python
from usr.lis2dh12_module import Lis2dh12
```

 

**实例化参数：**

| 名称          | 必填 | 类型    | 说明                                      |
| ------------- | ---- | ------- | ----------------------------------------- |
| i2c_dev       | 是   | i2c对象 | 如I2C(I2C.I2C1,  I2C.STANDARD_MODE)       |
| int_pin       | 是   | Pin对象 | 如Pin(Pin.GPIO1, Pin.IN,  Pin.PULL_PU, 0) |
| slave_address | 否   | int     | 默认0x19                                  |

```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
int_pin = Pin(Pin.GPIO1, Pin.IN, Pin.PULL_PU, 0)    #600U
dev = Lis2dh12(i2c_dev,int_pin)
```

**接口函数：**

l **sensor_reset ()**

重置传感器。

参数：

​    无。

返回值：

​    无。

l **int_enable(int_type,int_ths,time_limit,time_latency,time_window,duration)**

​	中断使能。

参数：

| 名称         | 必填 | 类型 | 说明                                                         |
| ------------ | ---- | ---- | ------------------------------------------------------------ |
| int_type     | 是   | int  | 中断类型（可配单双击中断，自由落体中断）<br />x单击：0x01，y单击：0x04，z单击：0x10，三轴单击：0x15<br />x双击：0x02，y双击：0x08，z双击：0x20，三轴双击：0x2A<br />自由落体：0x95 |
| int_ths      | 是   | int  | 中断阈值，所有中断均需设置                                   |
| time_limit   | 否   | int  | 时间限制（单双击事件），默认0x18                             |
| time_latency | 否   | int  | 延时(双击事件设置),默认0x12                                  |
| time_window  | 否   | int  | 时间窗口(双击事件设置)，双击得在该段时间内完成,默认0x55      |
| duration     | 否   | int  | 延续时间，惯性中断设置，默认0x03                             |

返回值：

​       无

l **start_sensor ()**

​	启动传感器（使能xyz轴）。

参数：

​    无。

返回值：

​       无

l **read_acceleration()**

​	循环读取 STATUS_REG寄存器，有新数据则输出三轴加速度。

参数：

​    无。

返回值：

| 名称    | 类型  | 说明                  |
| ------- | ----- | --------------------- |
| (x,y,z) | tuple | x, y, z轴加速度,单位G |

 

l **int_processing_data ()**

​	中断检测。（int1脚）

参数：

​    无。

返回值：

| 名称 | 类型 | 说明                                        |
| ---- | ---- | ------------------------------------------- |
| ret  | int  | 1----检测到中断信号； 0----未检测到中断信号 |