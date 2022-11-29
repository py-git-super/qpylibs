# -*- coding: UTF-8 -*-
from machine import SPI
import utime


spi_obj = SPI(0, 0, 1)


if __name__ == '__main__':
    r_data = bytearray(5)  # 创建接收数据的buff
    data = b"world"  # 写入测试数据
    spi_obj.write(data, 5) # 写入数据
    spi_obj.read(r_data, 5) # 读取数据

    ret = spi_obj.write_read(r_data, data, 5)  # 写入数据并接收

