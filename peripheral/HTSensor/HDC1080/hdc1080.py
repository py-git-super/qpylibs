'''
@Author: Stephen.Gao
@Date: 2022-04-06
@Description: HDC1080 sensor driver

Copyright 2022 - 2022 quectel
'''
from machine import I2C
import utime as time
from usr.common_except import CustomError

# I2C Address
HDC1080_ADDRESS =                       0x40    # 1000000 
# Registers
HDC1080_TEMPERATURE_REGISTER =          0x00
HDC1080_HUMIDITY_REGISTER =             0x01
HDC1080_CONFIGURATION_REGISTER =        0x02
HDC1080_MANUFACTURERID_REGISTER =       0xFE
HDC1080_DEVICEID_REGISTER =         0xFF
HDC1080_SERIALIDHIGH_REGISTER =         0xFB
HDC1080_SERIALIDMID_REGISTER =          0xFC
HDC1080_SERIALIDBOTTOM_REGISTER =       0xFD

class Hdc1080(object):
    '''
    HDC1080温湿度传感器类
    '''
    def __init__(self,i2c,addr=HDC1080_ADDRESS):
        self._i2c = i2c
        self._i2c_addr = addr

        time.sleep_ms(15)
        manu_id = self._read_data(HDC1080_MANUFACTURERID_REGISTER,2)
        manu_id = (manu_id[0] << 8) | manu_id[1]
        # print(manu_id)
        if manu_id != 0x5449:
            raise CustomError("HDC1080 manu id err.")

        self._write_data(HDC1080_CONFIGURATION_REGISTER,[0x10,0x00])
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
        self._write_data(HDC1080_CONFIGURATION_REGISTER, [0x10, 0x00])

    def read_temperature(self):
        '''
        读温度
        '''
        tem_data = self._read_data_delay(HDC1080_TEMPERATURE_REGISTER,2)
        tem_data = (tem_data[0] << 8) | tem_data[1]
        tem = (tem_data / 65536) * 165 - 40
        return tem

    def read_humidity(self):
        '''
        读湿度
        '''
        hum_data = self._read_data_delay(HDC1080_HUMIDITY_REGISTER,2)
        hum_data = (hum_data[0] << 8) | hum_data[1]
        hum = (hum_data / 65536) * 100
        return hum

    def read(self):
        tem = self.read_temperature()
        time.sleep_ms(15)
        hum = self.read_humidity()
        return (hum,tem)

if __name__ == "__main__":
    i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
    hdc=Hdc1080(i2c_dev)
    for i in range(10):
        print("test %d begin." % (i + 1))
        hum, tem = hdc.read()
        print("current humidity is {0}%RH,current temperature is {1}°C".format(hum, tem))
        print("test %d end." % (i + 1))
        time.sleep(1)
