'''
@Author: Stephen.Gao
@Date: 2022-04-01
@Description: AW8733 driver

Copyright 2022 - 2022 quectel
'''
from machine import Pin
import utime

#AW8733A增益模式
CM_AW8733A_GAIN_12DB = 1        #12dB，没有防破音功能
CM_AW8733A_GAIN_16DB = 2        #16dB，开启防破音功能
CM_AW8733A_GAIN_24DB = 3        #24dB，没有防破音功能
CM_AW8733A_GAIN_27_5DB = 4      #27.5dB，开启防破音功能

class Aw8377a(object):
    """
    aw8377a功放类
    开放接口：pa_enable(gain),pa_disable()
    """
    def __init__(self,pin):
        '''
        初始化功放
        :param pin: Pin对象(输出模式)
        '''
        self._pin = pin
        self.pa_enable(1)

    def _sleep_ms(self,n):
        utime.sleep_ms(n)

    def _sleep_us(self, n):
        pass

    def pa_enable(self,gain):
        '''
        使能AW8733A，并设置增益大小。
        :param gain: 模式(1-4),循环模式
        '''
        gain = gain % 4
        gain = gain if gain else 4
        for i in range(gain):
            self._pin.write(0)
            self._sleep_us(2)
            self._pin.write(1)
            self._sleep_us(2)

    def pa_disable(self):
        '''
        AW8733A进入关断模式
        '''
        self._pin.write(0)
        self._sleep_us(500)

def aw8733_test():
    pin1 = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_DISABLE, 0)
    pa = Aw8377a(pin1)
    pa.pa_enable(4)
    print(pin1.read())
    #开播放音乐线程

if __name__ == "__main__":
    aw8733_test()