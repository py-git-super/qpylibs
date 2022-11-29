'''
@Author: Stephen.Gao
@Date: 2022-03-25
@Description: LIS2DH12 sensor driver

Copyright 2022 - 2022 quectel
'''
import utime
import _thread
from machine import I2C
from machine import Pin

# 寄存器地址
LIS2DH12_OUT_X_L = 0x28
LIS2DH12_OUT_X_H = 0x29
LIS2DH12_OUT_Y_L = 0x2A
LIS2DH12_OUT_Y_H = 0x2B
LIS2DH12_OUT_Z_L = 0x2C
LIS2DH12_OUT_Z_H = 0x2D
LIS2DH12_FIFO_CTRL_REG = 0x2E

# 控制寄存器
LIS2DH12_CTRL_REG1 = 0x20
LIS2DH12_CTRL_REG2 = 0x21
LIS2DH12_CTRL_REG3 = 0x22
LIS2DH12_CTRL_REG4 = 0x23
LIS2DH12_CTRL_REG5 = 0x24
LIS2DH12_CTRL_REG6 = 0x25
LIS2DH12_REFERENCE_REG = 0x26
LIS2DH12_STATUS_REG = 0x27

# 状态寄存器
LIS2DH12_STATUS_REG_AUX = 0x7

# 中断寄存器
LIS2DH12_INT1_CFG = 0x30
LIS2DH12_INT1_SRC = 0x31
LIS2DH12_INT1_THS = 0x32
LIS2DH12_INT1_DURATION = 0x33

LIS2DH12_INT2_CFG = 0x34
LIS2DH12_INT2_SRC = 0x35
LIS2DH12_INT2_THS = 0x36
LIS2DH12_INT2_DURATION = 0x37

# 身份寄存器
LIS2DH12_WHO_AM_I = 0x0F

# 单击有关的寄存器
LIS2DH12_CLICK_CFG = 0x38
LIS2DH12_CLICK_SRC = 0x39
LIS2DH12_CLICK_THS = 0x3A
LIS2DH12_TIME_LIMIT = 0x3B
LIS2DH12_TIME_LATENCY = 0x3C
LIS2DH12_TIME_WINDOW = 0x3D

#重力加速度
STANDARD_GRAVITY = 9.806

#中断种类
#单击
X_SINGLE_CLICK_INT = 0x01
Y_SINGLE_CLICK_INT = 0x04
Z_SINGLE_CLICK_INT = 0x10
XYZ_SINGLE_CLICK_INT = 0x15
#双击
X_DOUBLE_CLICK_INT = 0x02
Y_DOUBLE_CLICK_INT = 0x08
Z_DOUBLE_CLICK_INT = 0x20
XYZ_DOUBLE_CLICK_INT = 0x2A
#惯性中断
POSI_CHANGE_RECOGNIZE = 0xFF
X_POSI_CHANGE_RECOGNIZE = 0x83
Y_POSI_CHANGE_RECOGNIZE = 0x8C
Z_POSI_CHANGE_RECOGNIZE = 0xB0
MOVE_RECOGNIZE = 0x7F
X_MOVE_RECOGNIZE = 0x03
Y_MOVE_RECOGNIZE = 0x0C
Z_MOVE_RECOGNIZE = 0x30
#自由落体中断
FF_RECOGNIZE = 0x95  #and zl yl xl

# 将其和外部的中断引脚绑定到一起。
class Lis2dh12(object):
    '''
    lis2dh12传感器类
    开放接口：sensor_reset(),int_processing_data(),resolution属性,
    int_enable(int_type,int_ths,time_limit,time_latency,duration),read_acceleration属性
    '''
    def __init__(self, i2c_dev,int_pin,slave_address=0x19):
        '''
        初始化
        :param i2c_dev: i2c对象
        :param int_pin: 中断引脚对象
        :param slave_address: 设备地址
        '''
        self._address = slave_address
        self._i2c_dev = i2c_dev
        self._int_pin = int_pin  # 中断引脚, 根据硬件连接不同而改变
        self._sensor_init()

    def _read_data(self, regaddr, datalen):
        '''
        i2c读数据
        :param regaddr: 寄存器地址
        :param datalen: 读取的长度
        :return: 列表类型的data
        '''
        r_data = bytearray(datalen)
        reg_addres = bytearray([regaddr])
        self._i2c_dev.read(self._address, reg_addres, 1, r_data, datalen, 1)
        ret_data = list(r_data)
        return ret_data

    def _write_data(self, regaddr, data):
        '''
        i2c写数据
        :param regaddr: 寄存器地址
        :param datalen: 写入的数据
        '''
        addr = bytearray([regaddr])
        w_data = bytearray([data])
        self._i2c_dev.write(self._address, addr, len(addr), w_data, len(w_data))

    def sensor_reset(self):
        '''
        传感器重置
        '''
        # 重置chip
        self._write_data(LIS2DH12_CTRL_REG5, 0x80)

        # print('reboot already. {}'.format(self._read_data(LIS2DH12_CTRL_REG5,1)))
        utime.sleep_ms(100)
        r_data = self._read_data(LIS2DH12_WHO_AM_I, 1)
        # 确定重启成功
        while r_data[0] != 0x33:
            r_data = self._read_data(LIS2DH12_WHO_AM_I, 1)
            utime.sleep_ms(5)

    def _sensor_init(self):
        self.sensor_reset()  # 1. 重置设备
        # 2. 初始化传感器
        self._write_data(LIS2DH12_CTRL_REG1, 0x77)  # 设置ODR 400HZ ,enable XYZ.
        utime.sleep_ms(20)  # (7/ODR) = 18ms
        self._write_data(LIS2DH12_CTRL_REG4, 0x08)  # ±2g， 高分辨率模式

        self._write_data(LIS2DH12_CLICK_CFG, 0)  # 清click_cfg
        self._write_data(LIS2DH12_INT1_CFG, 0)  # 清int1_cfg
        self._write_data(LIS2DH12_INT2_CFG, 0)  # 清int2_cfg


    def int_enable(self,int_type,int_ths,time_limit=0x18,time_latency=0x12,time_window=0x55,duration=0x03):
        '''
        中断使能
        单击中断，双击中断，惯性改变中断
        :param int_type: 中断类型
        :param int_ths: 阈值
        :param time_limit: 单双击事件传此参数，时间窗口限制
        :param time_latency: 单双击事件传此参数，设置延时
        :param duration: 惯性改变事件传此参数，设置duration
        '''
        #单击中断
        if int_type in (XYZ_SINGLE_CLICK_INT, X_SINGLE_CLICK_INT, Y_SINGLE_CLICK_INT, Z_SINGLE_CLICK_INT):
            self._write_data(LIS2DH12_CTRL_REG2, 0x07)  # 为点击功能启用高通过滤波器。
            self._write_data(LIS2DH12_CTRL_REG3, 0x80)  # 将中断引到INT1引脚上面， 默认高电平有效
            self._write_data(LIS2DH12_CLICK_CFG, int_type)  # 使能 单双击中断
            self._write_data(LIS2DH12_CLICK_THS, int_ths)  # 设置阈值
            self._write_data(LIS2DH12_TIME_LIMIT, time_limit)  # 设置时间限制(limit内恢复阈值以内)
        #双击中断
        elif int_type in (XYZ_DOUBLE_CLICK_INT, X_DOUBLE_CLICK_INT, Y_DOUBLE_CLICK_INT, Z_DOUBLE_CLICK_INT):
            self._write_data(LIS2DH12_CTRL_REG2, 0x07)  # 为点击功能启用高通过滤波器。
            self._write_data(LIS2DH12_CTRL_REG3, 0x80)  # 将中断引到INT1引脚上面， 默认高电平有效
            self._write_data(LIS2DH12_CLICK_CFG, int_type)  # 使能 单双击中断
            self._write_data(LIS2DH12_CLICK_THS, int_ths)  # 设置阈值
            self._write_data(LIS2DH12_TIME_LIMIT, time_limit)  # 设置时间窗口限制
            self._write_data(LIS2DH12_TIME_LATENCY, time_latency)  # 设置延时
            self._write_data(LIS2DH12_TIME_WINDOW, time_window)  #设置时间窗口，双击得在该段时间内完成
        #方向，运动改变中断
        elif int_type in (MOVE_RECOGNIZE, X_MOVE_RECOGNIZE, Y_MOVE_RECOGNIZE, Z_MOVE_RECOGNIZE,POSI_CHANGE_RECOGNIZE,
                          X_POSI_CHANGE_RECOGNIZE,Y_POSI_CHANGE_RECOGNIZE,Z_POSI_CHANGE_RECOGNIZE,FF_RECOGNIZE):
            self._write_data(LIS2DH12_CTRL_REG2, 0x00)  # 关闭高通过滤波器。
            self._write_data(LIS2DH12_CTRL_REG3, 0x40)  # 将中断引到INT1引脚上面， 默认高电平有效
            self._write_data(LIS2DH12_CTRL_REG5, 0x08)  # INT1已锁存
            self._write_data(LIS2DH12_INT1_CFG, int_type)  # 使能 6d中断
            self._write_data(LIS2DH12_INT1_THS, int_ths)  # 设置阈值
            self._write_data(LIS2DH12_INT1_DURATION, duration)  # 设置duration


    def start_sensor(self):
        '''
        启动传感器
        '''
        self._write_data(LIS2DH12_CTRL_REG1, 0x77)  # 设置ODR 100HZ ,enable XYZ.
        utime.sleep_ms(20)  # (7/ODR) = 18ms

    def process_xyz(self):
        '''
        读取大小端配置及out寄存器，并转换x,y,z数据
        :return: x,y,z数据的三元组
        '''
        data = []
        ctl4 = self._read_data(LIS2DH12_CTRL_REG4, 1)[0] #CTRL_REG4 中的 BLE(第七bit) 位为 0，小端模式，数字的低位字节存储在存储器的最低地址中，高位字节存储在最高地址中。
        big_endian = ctl4 & 0x40
        #读xl,xh,yl,yh,zl,zh
        for i in range(6):
            r_data = self._read_data(LIS2DH12_OUT_X_L + i, 1)
            data.append(r_data[0])

        if big_endian:          #大端
            x = data[0] * 256 + data[1]
            y = data[2] * 256 + data[3]
            z = data[4] * 256 + data[5]
        else:                   #小端 默认
            x = data[1] * 256 + data[0]
            y = data[3] * 256 + data[2]
            z = data[5] * 256 + data[4]

        return (x, y, z)

    def int_processing_data(self):
        '''
        中断检测
        :return: 1----检测到中断信号； 0----未检测到中断信号
        '''
        value = self._int_pin.read()

        if value == 1:  # 检测到中断信号了
            #acc = self.read_acceleration()
            int_src = self._read_data(LIS2DH12_INT1_SRC,1)  #读取INT1_SRC，清除中断请求
            utime.sleep_ms(100)
            return 1
        else:
            return 0

    @property
    def _resolution(self):
        """
        加速度计的range.
        :return: range_2_G, range_4_G, range_8_G,, range_16_G.
        """
        ctl4 = self._read_data(LIS2DH12_CTRL_REG4,1)[0]
        return (ctl4 >> 4) & 0x03

    @property
    def _acceleration(self):
        """
        计算三轴加速度
        :return: x,y,z轴的加速度三元组，单位重力加速度G
        """
        divider = 1
        accel_range = self._resolution
        if accel_range == 3:        #range_16_G
            divider = 2048
        elif accel_range == 2:      #range_8_G
            divider = 4096
        elif accel_range == 1:      #range_4_G
            divider = 8192
        elif accel_range == 0:      #range_2_G
            divider = 16384

        x, y, z = self.process_xyz()

        x = x / divider
        y = y / divider
        z = z / divider

        if accel_range == 3:        #range_16_G
            # print('16g 精度下')
            x = x if x <= 16 else x - 32
            y = y if y <= 16 else y - 32
            z = z if z <= 16 else z - 32
        elif accel_range == 2:      #range_8_G
            # print('8g 精度下')
            x = x if x <= 8 else x - 16
            y = y if y <= 8 else y - 16
            z = z if z <= 8 else z - 16
        elif accel_range == 1:      #range_4_G
            # print('4g 精度下')
            x = x if x <= 4 else x - 8
            y = y if y <= 4 else y - 8
            z = z if z <= 4 else z - 8
        elif accel_range == 0:      #range_2_G
            # print('2g 精度下')
            x = x if x <= 2 else x - 4
            y = y if y <= 2 else y - 4
            z = z if z <= 2 else z - 4

        # convert from Gs to m / s ^ 2 and adjust for the resolution
        # x = (x / divider) * STANDARD_GRAVITY
        # y = (y / divider) * STANDARD_GRAVITY
        # z = (z / divider) * STANDARD_GRAVITY
        return (x, y, z)

    def read_acceleration(self):
        '''
        循环读取 STATUS_REG，有数据则输出三轴加速度
        :return: x,y,z轴的加速度三元组，单位m/s2
        '''

        while 1:
            status = self._read_data(LIS2DH12_STATUS_REG,1)[0]
            xyzda = status & 0x08   #三轴皆有新数据则置1
            xyzor = status & 0x80
            if not xyzda:
                continue
            else:
                x,y,z = self._acceleration
                #print("x = %0.3f G, y = %0.3f G, z = %0.3f G" % (x, y, z))
                return (x, y, z)


def is2dh12_thread(state, delay, retryCount):

    i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
    #int_pin = Pin(Pin.GPIO3, Pin.IN, Pin.PULL_PU, 0)    #600s 12号引脚
    int_pin = Pin(Pin.GPIO1, Pin.IN, Pin.PULL_PU, 0)    #600U

    dev = Lis2dh12(i2c_dev,int_pin)
    dev.int_enable(XYZ_DOUBLE_CLICK_INT,0x12)     # 配置中断类型
    dev.start_sensor()

    while True:
        if state == 1:
            if dev.int_processing_data() == 1:  #中断检测处理
                retryCount -= 1
            utime.sleep_ms(10)
        elif state == 0:
            acc = dev.read_acceleration()
            utime.sleep_ms(delay)
            retryCount -= 1
        if retryCount == 0:
            break
    print("检测结束退出")


if __name__ == "__main__":
    _thread.start_new_thread(is2dh12_thread, (1, 1000, 10))


