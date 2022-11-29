### aw8377a

**类引用：**

```python
from usr.aw8733_module import Aw8733a
```

**实例化参数：**

| 名称 | 必填 | 类型    | 说明                             |
| ---- | ---- | ------- | -------------------------------- |
| pin  | 是   | Pin对象 | 单gpio，direction为OUT，控制芯片 |

```python
pin1 = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_DISABLE, 0)
pa = Aw8377a(pin1)
```

**接口函数：**

l **pa_enable(gain)**

使能AW8733A，并设置增益大小，增益模式1-4。

参数：

| 名称 | 必填 | 类型 | 说明                      |
| ---- | ---- | ---- | ------------------------- |
| gain | 是   | int  | 大于4则循环，如5表示模式1 |

返回值：

无。

l **pa_disable()**

使AW8733A进入关断模式。

参数：

无。

返回值：

无。