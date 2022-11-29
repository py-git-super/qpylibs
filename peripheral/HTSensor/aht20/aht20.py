'''
File: aht20.py
Project: i2c
File Created: Monday, 28th December 2020 5:17:28 pm
Author: chengzhu.zhou
-----
Last Modified: Tuesday, 15th March 2022 1:50:35 pm
Modified By: Stephen.Gao
-----
Copyright 2022 - 2022 quectel
'''

from machine import I2C
import utime as time
from usr.htsensor import HtSensor


# API  手册 http://qpy.quectel.com/wiki/#/zh-cn/api/?id=i2c
# AHT20 说明书
# https://server4.eca.ir/eshop/AHT20/Aosong_AHT20_en_draft_0c.pdf

class Aht20(HtSensor):
    '''
    AHT20类
    '''

    # Initialization command
    AHT20_CALIBRATION_CMD = 0xE1
    # Trigger measurement
    AHT20_START_MEASURMENT_CMD = 0xAC
    # reset
    AHT20_RESET_CMD = 0xBA

    def __init__(self,addre=0x38):
        super().__init__(self)
        self._aht20_init(addre)       

    def _aht20_init(self, addre):
        '''
        根据数据手册的描述来转化湿度和温度
        '''
        self.i2c_dev = I2C(I2C.I2C1, I2C.FAST_MODE)  # 返回i2c对象 i2c类功能：用于设备之间通信的双线协议
        self.i2c_addre = addre
        self.init_data = [0x08, 0x00]

        print("sensor init begin.")

        super()._write_data([self.AHT20_CALIBRATION_CMD], self.init_data)
        time.sleep_ms(300)  # at last 300ms

        print("sensor init complete.")

    def _aht20_transfor_data(self, data):
        '''
        根据数据手册的描述来转化湿度和温度
        '''
        r_data = data
        #湿度
        humidity = (r_data[0] << 12) | (
            r_data[1] << 4) | ((r_data[2] & 0xF0) >> 4)
        humidity = (humidity/(1 << 20)) * 100.0
        print("current humidity is {0}%".format(humidity))
        #温度
        temperature = ((r_data[2] & 0xf) << 16) | (
            r_data[3] << 8) | r_data[4]
        temperature = (temperature * 200.0 / (1 << 20)) - 50
        print("current temperature is {0}°C".format(temperature))
        return (humidity,temperature)

    def read(self):
        data = super()._trigger_measure()
        return self._aht20_transfor_data(data)

    def aht20_test(self,count):

        # 测试十次
        for i in range(count):
            print("test %d begin." % (i+1))
            data = super()._trigger_measure()
            self._aht20_transfor_data(data)
            print("test %d end." % (i+1))
            super().ht_sensor_reset()
            time.sleep(1)



if __name__ == "__main__":
    aht_dev=Aht20()
    hum,tem=aht_dev.read()
    print("current humidity is {0}%,current temperature is {1}°C".format(hum,tem))
