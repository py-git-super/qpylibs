# GPIO

#### 介绍
GPIO 读写操作，以及中断开发


#### 参数说明

> **gpio = Pin(GPIOn, direction, pullMode, level)**

| 参数      | 类型 | 说明                                                         |
| :-------- | :--- | ------------------------------------------------------------ |
| GPIOn     | int  | 引脚号<br />EC100YCN平台引脚对应关系如下（引脚号为外部引脚编号）：<br />GPIO1 – 引脚号22<br />GPIO2 – 引脚号23<br />GPIO3 – 引脚号38<br />GPIO4 – 引脚号53<br />GPIO5 – 引脚号54<br />GPIO6 – 引脚号104<br />GPIO7 – 引脚号105<br />GPIO8 – 引脚号106<br />GPIO9 – 引脚号107<br />GPIO10 – 引脚号178<br />GPIO11 – 引脚号195<br />GPIO12 – 引脚号196<br />GPIO13 – 引脚号197<br />GPIO14 – 引脚号198<br />GPIO15 – 引脚号199<br />GPIO16 – 引脚号203<br />GPIO17 – 引脚号204<br />GPIO18 – 引脚号214<br />GPIO19 – 引脚号215<br />EC600SCN/EC600NCN平台引脚对应关系如下（引脚号为模块外部引脚编号）：<br />GPIO1 – 引脚号10<br />GPIO2 – 引脚号11<br />GPIO3 – 引脚号12<br />GPIO4 – 引脚号13<br />GPIO5 – 引脚号14<br />GPIO6 – 引脚号15<br />GPIO7 – 引脚号16<br />GPIO8 – 引脚号39<br />GPIO9 – 引脚号40<br />GPIO10 – 引脚号48<br />GPIO11 – 引脚号58<br />GPIO12 – 引脚号59<br />GPIO13 – 引脚号60<br />GPIO14 – 引脚号61<br />GPIO15 – 引脚号62<br/>GPIO16 – 引脚号63<br/>GPIO17 – 引脚号69<br/>GPIO18 – 引脚号70<br/>GPIO19 – 引脚号1<br/>GPIO20 – 引脚号3<br/>GPIO21 – 引脚号49<br/>GPIO22 – 引脚号50<br/>GPIO23 – 引脚号51<br/>GPIO24 – 引脚号52<br/>GPIO25 – 引脚号53<br/>GPIO26 – 引脚号54<br/>GPIO27 – 引脚号55<br/>GPIO28 – 引脚号56<br/>GPIO29 – 引脚号57<br />GPIO30 – 引脚号2<br />GPIO31 – 引脚号66<br />GPIO32 – 引脚号65<br />GPIO33 – 引脚号67<br />GPIO34 – 引脚号64<br />GPIO35 – 引脚号4<br />GPIO36 – 引脚号31<br />GPIO37 – 引脚号32<br />GPIO38 – 引脚号33<br />GPIO39 – 引脚号34<br />GPIO40 – 引脚号71<br />GPIO41 – 引脚号72<br />EC600UCN平台引脚对应关系如下（引脚号为模块外部引脚编号）<br />GPIO1 – 引脚号61<br />GPIO2 – 引脚号58<br />GPIO3 – 引脚号34<br />GPIO4 – 引脚号60<br />GPIO5 – 引脚号69<br />GPIO6 – 引脚号70<br />GPIO7 – 引脚号123<br />GPIO8 – 引脚号118<br />GPIO9 – 引脚号9<br />GPIO10 – 引脚号1<br />GPIO11 – 引脚号4<br />GPIO12 – 引脚号3<br />GPIO13 – 引脚号2<br />GPIO14 – 引脚号54<br />GPIO15 – 引脚号57<br/>GPIO16 – 引脚号56<br/>EC200UCN平台引脚对应关系如下（引脚号为模块外部引脚编号）<br />GPIO1 – 引脚号27<br />GPIO2 – 引脚号26<br />GPIO3 – 引脚号24<br />GPIO4 – 引脚号25<br />GPIO5 – 引脚号13<br />GPIO6 – 引脚号135<br />GPIO7 – 引脚号136<br />GPIO8 – 引脚号133<br />GPIO9 – 引脚号3<br />GPIO10 – 引脚号40<br />GPIO11 – 引脚号37<br />GPIO12 – 引脚号38<br />GPIO13 – 引脚号39<br />GPIO14 – 引脚号5<br />GPIO15 – 引脚号141<br/>GPIO16 – 引脚号142<br/>EC800NCN平台引脚对应关系如下（引脚号为模块外部引脚编号）<br />GPIO1 – 引脚号30<br />GPIO2 – 引脚号31<br />GPIO3 – 引脚号32<br />GPIO4 – 引脚号33<br />GPIO5 – 引脚号49<br />GPIO6 – 引脚号50<br />GPIO7 – 引脚号51<br />GPIO8 – 引脚号52<br />GPIO9 – 引脚号53<br />GPIO10 – 引脚号54<br />GPIO11 – 引脚号55<br />GPIO12 – 引脚号56<br />GPIO13 – 引脚号57<br />GPIO14 – 引脚号58<br />GPIO15 – 引脚号80<br/>GPIO16 – 引脚号81<br/>GPIO17 – 引脚号76<br/>GPIO18 – 引脚号77<br/>GPIO19 – 引脚号82<br/>GPIO20 – 引脚号83<br/>GPIO21 – 引脚号86<br/>GPIO22 – 引脚号87<br/>GPIO23 – 引脚号66<br/>GPIO24 – 引脚号67<br/>GPIO25 – 引脚号17<br/>GPIO26 – 引脚号18<br/>GPIO27 – 引脚号19<br/>GPIO28 – 引脚号20<br/>GPIO29 – 引脚号21<br />GPIO30 – 引脚号22<br />GPIO31 – 引脚号23<br />GPIO32 – 引脚号28<br />GPIO33 – 引脚号29<br />GPIO34 – 引脚号38<br />GPIO35 – 引脚号39<br />GPIO36 – 引脚号16<br />GPIO37 – 引脚号78<br />BC25PA平台引脚对应关系如下（引脚号为模块外部引脚编号）<br />GPIO1 – 引脚号3<br />GPIO2 – 引脚号4<br />GPIO3 – 引脚号5<br />GPIO4 – 引脚号6<br />GPIO5 – 引脚号16<br />GPIO6 – 引脚号20<br />GPIO7 – 引脚号21<br />GPIO8 – 引脚号22<br />GPIO9 – 引脚号23<br />GPIO10 – 引脚号25<br />GPIO11 – 引脚号28<br />GPIO12 – 引脚号29<br />GPIO13 – 引脚号30<br />GPIO14 – 引脚号31<br />GPIO15 – 引脚号32<br/>GPIO16 – 引脚号33<br/>GPIO17 – 引脚号2<br/>GPIO18 – 引脚号8<br/> |
| direction | int  | 0 - IN – 输入模式，1 - OUT – 输出模式                                |
| pullMode  | int  | 0 - PULL_DISABLE – 浮空模式<br />1 - PULL_PU – 上拉模式<br />2 - PULL_PD – 下拉模式 |
| level     | int  | 0 - 设置引脚为低电平, 1 - 设置引脚为高电平                    |

> **Pin.write(value)**

| 参数  | 类型 | 说明                                                         |
| ----- | ---- | ------------------------------------------------------------ |
| value | int  | 0 - 当PIN脚为输出模式时，设置当前PIN脚输出低;  <br />1 - 当PIN脚为输出模式时，设置当前PIN脚输出高 |

#### 使用说明

1.  实例1
 

```
from machine import Pin

# gpio = GPIO(1, 1, 0, 0)
gpio = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_DISABLE, 0)
gpio.write(1)
0
gpio.read()
1
```


# ExtInt

#### 介绍
类功能：用于配置I/O引脚在发生外部事件时中断。


#### 参数说明

> **extint = ExtInt(GPIOn, mode, pull, callback)**

| 参数     | 类型 | 说明                                                         |
| :------- | :--- | ------------------------------------------------------------ |
| GPIOn    | int  | 需要控制的GPIO引脚号，参照Pin模块的定义                      |
| mode     | int  | 设置触发方式<br /> IRQ_RISING – 上升沿触发<br /> IRQ_FALLING – 下降沿触发<br /> IRQ_RISING_FALLING – 上升和下降沿触发 |
| pull     | int  | PULL_DISABLE – 浮空模式<br />PULL_PU – 上拉模式 <br />PULL_PD  – 下拉模式 |
| callback | int  | 中断触发回调函数                                             |

#### 使用说明

1.  实例1

```python
>>> from machine import ExtInt
>>> def fun(args):
        print('### interrupt  {} ###'.format(args))
>>> extint = ExtInt(ExtInt.GPIO1, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, fun)
>>> extint.enable()  # 使能中断
>>> extint.disable() # 关闭中断
>>> extint.line()    # 读取引脚映射行号
>>> extint.read_count(is_reset)   # 读取中断数
>>> extint.count_reset()   # 清空中断数
```