'''
@Author: Stephen.Gao
@Date: 2022-04-07
@Description: HDC2080 sensor driver

Copyright 2022 - 2022 quectel
'''
from machine import I2C
import utime as time
from usr.common_except import CustomError

# I2C Address
HDC2080_ADDRESS =                       0x40    # 1000000 
# Registers
HDC2080_TEMPERATURE_L =          0x00
HDC2080_TEMPERATURE_H =          0x01
HDC2080_HUMIDITY_L =             0x02
HDC2080_HUMIDITY_H =             0x03
HDC2080_DRDYANDINT =             0x04
HDC2080_INT_ENABLE =             0x07
HDC2080_RESET =                  0x0E
HDC2080_MEASURE_CONF =           0x0F
HDC2080_MANUID_L =               0xFC
HDC2080_MANUID_H =               0xFD

class Hdc2080(object):
    '''
    HDC2080温湿度传感器类
    '''
    def __init__(self,i2c,addr=HDC2080_ADDRESS):
        self._i2c = i2c
        self._i2c_addr = addr

        time.sleep_ms(15)
        manu_id = (self._read_data(HDC2080_MANUID_H,1)[0] << 8) | self._read_data(HDC2080_MANUID_L,1)[0]
        # print(manu_id)
        if manu_id != 0x5449:
            raise CustomError("HDC2080 manu id err.")

        self._write_data(HDC2080_MEASURE_CONF,[0x00])
        time.sleep_ms(15)
        print("sensor init complete.")

    def _write_data(self, reg, data):
        '''
        i2c写数据
        '''
        self._i2c.write(self._i2c_addr,
                           bytearray([reg]), len([reg]),
                           bytearray(data), len(data))

    def _read_data(self,reg, length):
        '''
        i2c读数据
        '''
        r_data = [0x00 for i in range(length)]
        r_data = bytearray(r_data)
        ret = self._i2c.read(self._i2c_addr,
                          bytearray([reg]), len([reg]),
                          r_data, length,
                          0)
        return list(r_data)

    def _read_data_delay(self,reg, length):
        '''
        i2c延时读数据
        '''
        r_data = [0x00 for i in range(length)]
        r_data = bytearray(r_data)
        ret = self._i2c.read(self._i2c_addr,
                          bytearray([reg]), len([reg]),
                          r_data, length,
                          50)
        return list(r_data)

    def reset(self):
        self._write_data(HDC2080_RESET, [0x80])

    def read_temperature(self):
        '''
        读温度
        '''
        tem_h = self._read_data_delay(HDC2080_TEMPERATURE_H, 1)[0]
        tem_l = self._read_data_delay(HDC2080_TEMPERATURE_L, 1)[0]
        tem_data = (tem_h << 8) | tem_l
        tem = (tem_data / 65536) * 165 - 40.5
        return tem

    def read_humidity(self):
        '''
        读湿度
        '''
        hum_h = self._read_data_delay(HDC2080_HUMIDITY_H,1)[0]
        hum_l = self._read_data_delay(HDC2080_HUMIDITY_L,1)[0]
        hum_data = (hum_h << 8) | hum_l
        hum = (hum_data / 65536) * 100
        return hum

    def read(self):
        self._write_data(HDC2080_MEASURE_CONF,[0x01]) #MEAS_TRIG bit
        while 1:
            drdy = self._read_data(HDC2080_DRDYANDINT,1)[0] & 0x80 #data ready
            if drdy:
                tem = self.read_temperature()
                hum = self.read_humidity()
                return (hum,tem)

if __name__ == "__main__":
    i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
    hdc=Hdc2080(i2c_dev)
    for i in range(10):
        print("test %d begin." % (i + 1))
        hum, tem = hdc.read()
        print("current humidity is {0}%RH,current temperature is {1}°C".format(hum, tem))
        print("test %d end." % (i + 1))
        time.sleep(1)
