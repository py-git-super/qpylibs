# 导入移远云SDK
import quecIot


class QuecthingModule(object):
    '''
    Quecthing SDK
    '''
    def __init__(self, pk, ps, server, lifetime=120, mode=0):
        '''
        pk:产品标识
        ps:产品密钥
        server:服务地址
        lifetime:心跳
        mode: 0 lwM2M; 1 MQTT
        '''
        self.__pk = pk
        self.__ps = ps
        self.__server = server
        self.__lifeTime = lifetime
        self.__mode = mode

    def cloudInit(self):
        # 初始化连接
        self.__setCallback()
        self.__setProductinfo()
        self.__setServer()
        self.__setLifetime()

    def __setCallback(self):
        # 注册消息回调
        state = quecIot.setEventCB(self.__callback)
        print("quecthing set callback state:{}".format(state))
        return state

    def __setProductinfo(self):
        # 设置产品PK, PS
        state = quecIot.setProductinfo(self.__pk, self.__ps)
        print("quecthing set productinfo state:{}".format(state))
        return state

    def __setServer(self):
        # 设置服务地址 默认连接MQTT生产服务器
        state = quecIot.setServer(self.__mode, self.__server)
        print("quecthing set server state:{}".format(state))
        return state

    def __setLifetime(self):
        # 设置保活心跳 默认120
        state = quecIot.setLifetime(self.__lifeTime)
        print("quecthing set lifetime state:{}".format(state))
        return state

    @staticmethod
    def connect():
        # 发起连接
        state = quecIot.setConnmode(1)
        print("quecthing connect state:{}".format(state))
        return state

    @staticmethod
    def disconnect():
        # 注销连接
        state = quecIot.setConnmode(0)
        print("quecthing disconnect state:{}".format(state))
        return state

    @staticmethod
    def send(mode, data, pgid=None, qos=0):
        '''
        mode: 0 向云平台发送透传数据
              1 向云平台发送物模型数据
              2 向云平台应答物模型数据
        '''
        if mode == 0:
            state = quecIot.passTransSend(qos, data)
        elif mode == 1:
            state = quecIot.phymodelReport(qos, data)
        elif mode == 2 and pgid:
            state = quecIot.phymodelAck(qos, pgid, data)
        else:
            raise ValueError("The send api parameter is incorrect")
        print("quecthing send msg state :{}".format(state))
        return state

    def __callback(self, data):
        # 消息回调
        print("quecthing callback recv data :{}".format(data))
        event = data[0]
        eventCode = data[1]
        if event == 4:
            if eventCode == 10210:
                print("quecthing sent con msg is successfully")
            elif eventCode == 10310:
                print("quecthing sent con msg is fail")
            else:
                print("quecthing sent con msg is fail")
        elif (event == 3) and (eventCode == 10200):
            print("Device Registration succeeded")
        elif (event == 9) and (eventCode == 10200):
            print("Connection restored successfully")
        elif event == 7:  # OTA事件
            if eventCode == 0:
                quecIot.otaAction(1)  # 0 拒绝升级 ，1确认升级
            elif eventCode == 10701:
                print('Module download begins')
            elif eventCode == 10702:
                print('Package download')
            elif eventCode == 10703:
                print('[Package download completed')
            elif eventCode == 10704:
                print('Package in the update')
            elif eventCode == 10705:
                print('Firmware update completed')
            elif eventCode == 10706:
                print('Failed to update firmware')
        else:
            pass