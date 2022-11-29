### mcp23017

**类引用：**

```python
from usr.mcp23017_module import Mcp23017
```

 

**实例化参数：**

| 名称          | 必填 | 类型    | 说明                                       |
| ------------- | ---- | ------- | ------------------------------------------ |
| i2c_dev       | 是   | i2c对象 | 如I2C(I2C.I2C1,  I2C.STANDARD_MODE)        |
| slave_address | 否   | int     | 默认0x20                                   |
| bank          | 否   | int     | 默认1，与寄存器地址有关，为0则本类接口失效 |

```python
i2c = I2C(I2C.I2C1, I2C.STANDARD_MODE)
mcp = mcp23017.Mcp23017(i2c)
```

**接口函数：**

**16位property方法接口**

l **mode**

​	gpio方向。

**demo**：

```python
mcp = mcp23017.Mcp23017(i2c, address=0x20)
mcp.mode = 0xffff
```

 

**set**：

​    mcp_obj.mode = 0xffff为all_in

​    mcp_obj.mode = 0x0000为all_out

l **gpio**

设置高低电平。

demo：

```python
mcp = mcp23017.Mcp23017(i2c, address=0x20)
mcp.mode = 0xfffe
mcp.gpio = 0x0001 #15号脚（PA7）输出高电平
```

 

**set：**

​    mcp_obj.mode = 0xffff为all_in

​    mcp_obj.mode = 0x0000为all_out

**8位property方法接口**

l **mode**

​	gpio方向。

**demo**：

```python
mcp = mcp23017.Mcp23017(i2c, address=0x20)
mcp.porta.mode = 0xfe
mcp.portb.mode = 0xff
```

 

**set**：

​    和16位一样

 

l **gpio**

​	设置高低电平。

**demo**：

```python
mcp = mcp23017.Mcp23017(i2c, address=0x20)
mcp.porta.gpio = 0x01
mcp.portb.gpio = 0x02
```

**set：**

​    同16位

 

**函数方法接口**

l **pin(pin, mode, value, pullup, polarity, interrupt_enable, interrupt_compare_default, default_value)**

​	设置0-15号pin脚。

参数：

| 名称     | 必填 | 类型 | 说明                                      |
| -------- | ---- | ---- | ----------------------------------------- |
| pin      | 是   | int  | io脚，0-15可选                            |
| mode     | 否   | int  | in还是out，默认None（寄存器初始化all in） |
| value    | 否   | int  | 0或1，默认None（初始值）                  |
| pullup   | 否   | int  | True或False，默认None（初始值）           |
| polarity | 否   | int  | 0或1，极性，默认None（初始值）            |

返回值：

​       无

**demo**：

```python
mcp = mcp23017.Mcp23017(i2c, address=0x20)
mcp.pin(0, mode=1)
mcp.pin(1, mode=1, pullup=True)
mcp.pin(1)
mcp.pin(2, mode=0, value=1)
mcp.pin(3, mode=0, value=0)
```

