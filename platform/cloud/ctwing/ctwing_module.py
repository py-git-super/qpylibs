# 导入ctwing平台连接套件
from nb import AEP
import pm


class CtwingModule(object):
    '''
    Ctwing 连接套件
    '''
    def __init__(self, server, port, mode=1, psk=None):
        '''
        server:服务地址
        port: 服务端口
        mode: 下行数据接收模式,默认为1
              0 缓存模式,接收到新数据无URC上报
              1 直吐模式,接收到新数据通过URC立即上报
              2 缓存模式,接收到新数据仅上报URC提示
        psk: 十六进制字符串, 用于加密设备的密钥,可在平台配置,可选参数
        '''
        self.__aep = AEP(server, port, mode, psk) if psk else AEP(server, port, mode)
        self.__setCallback()

    def connect(self, timeout=30000):
        '''
        发起连接
        timeout : 超时时间,单位(ms),不输入参数则默认30s
        '''
        state = self.__aep.connect(timeout)
        return state

    def disconnect(self):
        '''
        注销连接
        '''
        state = self.__aep.close()
        return state

    def send(self, len, data, mode=0):
        '''
        len: 发送的数据长度
        data: 待发送数据,最大支持1024字节数据
        mode: 0-发送 NON 数据并将模块发送数据所携带的 RAI 辅助释放标记设置为 0
              1-发送 NON 数据并将模块发送数据所携带的 RAI 辅助释放标记设置为 1
              2-发送 NON 数据并将模块发送数据所携带的 RAI 辅助释放标记设置为 2
              100-发送 CON 数据并将模块发送数据所携带的 RAI 辅助释放标记设置为 0
              101-发送 CON 数据并将模块发送数据所携带的 RAI 辅助释放标记设置为 1
              102-发送 CON 数据并将模块发送数据所携带的 RAI 辅助释放标记设置为 2
        '''
        state = self.__aep.send(len, data, mode)
        return state

    def recv(self, data_len, data, timeout=30):
        '''
        data_len: 期望读取的数据长度,非阻塞
        data:存储接收到的数据
        timeout: 超时时间,单位ms,默认为30s
        '''
        self.__aep.recv(data_len, data, timeout * 1000)

    def __checkMsgNum(self):
        '''检查云平台待读取的数据条数'''
        msg_num = self.__aep.check()
        return msg_num

    def __setCallback(self):
        '''
        注册消息回调
        '''
        self.__aep.set_event_callcb(self.__callback)

    def __callback(self, data):
        '''
        消息回调
        data: 平台下发事件
        '''
        print("ctwing callback recv data :{}".format(data))
        event = data[0]
        eventCode = data[1]
        if event == 23:  # 深休眠唤醒
            if eventCode == 6: # 恢复连接成功
                print("Connection restored successfully")
            else:
                print("Connection restored fail")
        elif event == 24 and eventCode == 8: # OTA请求
            pm.autosleep(0)  # 升级期间不允许设备进入休眠
            print("OTA upgrade")
        elif event == 25 and eventCode == 0: # 收到RST事件，设备需要重新跟云端建立连接
            print("RST, please re-establish the connection")
        elif event == 22:  # CON数据ACK确认
            if eventCode == 4:
                print("ctwing sent con msg is successfully")
            else:
                print("ctwing sent con msg is fail")
        elif event == 27 and eventCode == 0: # mode为1的情况下接收到平台消息
            print("revc cloud msg")
            msg = data[2]
            msg_len = data[3]
            print(msg, msg_len)
        elif event == 28 and eventCode == 0: # mode为2的情况下接收到新消息提示
            print("revc cloud msg, mode is 0")
        else:
            pass