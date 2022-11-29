# 导入onenet平台连接套件
from nb import ONENET


class OnenetModule(object):

    def __init__(self):
        '''
        接入配置信息,创建通信套件实例
        '''
        self.__onenet = ONENET

    def setConfig(self, config_list, config_flag):
        '''
        接入配置信息
        配置 Bootstrap(引导接口)模式和引导服务器地址或者 LwM2M 服务器地址，也可以用于
        设置 CoAP 协议中的 ACK_TIMEOUT,还可以用来配置是否自动响应 OneNET 平台或者应用服务器的订
        阅请求、存活周期即将到期时是否会自动更新，以及是否使能 OneNET 深睡眠唤醒保存参数和状态功能.
        config_list: [0, '0', 0, 10, 0, 0, 0]
        0 模式是否使能,当不配置时选择0
        1 服务器地址,当不配置时选择'0'
        2 端口号是,当不配置时选择0
        3 应答超时,默认2s,当不配置时选择0
        4 是否自动响应 OneNET 平台或者应用服务器,当不配置时选择0
        5 是否使能在存活周期即将到期时，自动更新存活周期,当不配置时选择0
        6 模块连接 OneNET 后进入深度睡眠是否保存已配置参数和状态功能,当不配置时选择0
        config_flag:
        配置内容指示
        0: 服务器地址配置 
        2: 应答超时配置 
        3: 自动响应 OneNET 平台或者应用服务器 
        4: OneNET 深睡眠唤醒保存参数和状态功能
        '''
        state = self.__onenet.config(config_list, config_flag)
        state = True if state == 0 else False
        return state 

    def createCommunicationInstance(self):
        '''创建通信套件实例'''
        self.__instance_id = self.__onenet.create()
        return self.__instance_id
        
    def addLwM2mObject(self, obj_list):
        '''
        添加LwM2M对象 
        obj_list: LwM2M 对象配置列表 [0, 3303, 2, "11", 6,1]
        0 instance_id(通信实例id)
        1 objId(LwM2M 对象 ID)
        2 insCount(实例数量)
        3 insBitmap(实例位图，字符串型，需标注双引号。例如，若共有 4 个实例,ID 分别为 0、1、2、3,那么<insCount>值为4,
          同时<insBitmap>="1101" 表示实例 ID 0、1、3 将被注册，而实例 ID 2 不会被注册。)
        4 attrCount(属性个数，表示可读和/或可写资源个数)
        5 intactCount(动作个数，表示可执行的资源个数)      
        '''
        state = self.__onenet.add_object(obj_list)
        state = True if state == 0 else False
        return state 

    def connect(self, instance_id, lifetime):
        '''
        连接平台，进行设备注册请求，同时注册回调函数用于接收平台消息  
        instance_id 通信套件的实例ID
        lifetime 设备存活周期 单位秒
        '''
        state = self.__onenet.connect(instance_id, lifetime, self.__callback)
        state = True if state == 0 else False
        return state 

    def __observerResp(self, observe_resp_list):
        '''
        当自动响应订阅请求功能被禁用后，此命令用来手动响应 OneNET 平台或应用服务器发来的订阅请求
        observe_resp_list: 
        0 instance_id(通信套件的实例 ID)
        1 msgId(数据包 消息 ID,由消息“+MIPLOBSERVE”中获取)
        2 result(订阅结果,默认1, 表示成功,其他请参考BC25 ONENET应用指导V1.1)
        '''
        state = self.__onenet.observer_resp(observe_resp_list)
        state = True if state == 0 else False
        return state 

    def __discoverResp(self, discover_resp_list):
        '''
        响应来自 OneNET 平台的发现资源请求
        discover_resp_list: 发现资源请求应答参数列表
        0 instance_id(通信套件的实例 ID)
        1 msgId(数据包 消息 ID,由消息“+MIPLOBSERVE”中获取)
        2 result(资源结果,默认1, 表示成功,其他请参考BC25 ONENET应用指导V1.1)
        3 length(参数<valuestring>的长度)
        4 valuestring(字符串类型（需标记双引号），包含对象的属性，每个属性之间用分号隔开)
        '''
        state = self.__onenet.discover_resp(discover_resp_list)
        state = True if state == 0 else False
        return state 

    def __readResp(self, read_resp_list):
        '''
        响应从 OneNET 平台或者应用服务器发来的读取请求  
        read_resp_list: 读取请求应答参数列表
        0 instance_id(通信套件的实例 ID)
        1 msgId(数据包 消息 ID,由消息“+MIPLOBSERVE”中获取)
        2 result(资源结果,默认1, 表示成功,其他请参考BC25 ONENET应用指导V1.1)
        3 objId(对象 ID)由 URC“+MIPLREAD”中获取)
        4 insId(实例 ID,由 URC“+MIPLREAD”中获取)
        5 resId(资源 ID,由 URC“+MIPLREAD”中获取)
        6 valueType(<value>值的类型。1: String 2: Opaque 3: Integer 4: Float 5: Boolean
        7 len(参数<value>值的长度)
        8 value(数据内容)
        9 index(消息序号)
        10 flag(消息指示),默认0
        '''
        state = self.__onenet.read_resp(read_resp_list)
        state = True if state == 0 else False
        return state 

    def disconnect(self, instance_id):
        '''
        向 OneNET 平台发送注销请求
        instance_id(通信套件的实例 ID)
        '''
        state = self.__onenet.close(instance_id)
        return state

    def send(self, data, ack_flag):
        '''
        数据上报 [0,-1,3303,0,5700,4,4,'25.7',0,0]
        data :list,数据上报参数列表
            0 instance_id(通信套件的实例 ID)
            1 result(资源结果,默认1, 表示成功,其他请参考BC25 ONENET应用指导V1.1)
            2 objId(对象 ID)由 URC“+MIPLREAD”中获取)
            3 insId(实例 ID,由 URC“+MIPLREAD”中获取)
            4 resId(资源 ID,由 URC“+MIPLREAD”中获取)
            5 valueType(<value>值的类型。1: String 2: Opaque 3: Integer 4: Float 5: Boolean
            6 len(参数<value>值的长度,最大1026)
            7 value(数据内容)
            8 index(消息序号) ,默认0
            9 flag(消息指示),默认0
            10 ackid(消息确认id),默认0
        ack_flag: 应答标志
        如果发送Opaque不透明数据,数据为16进制字符串,长度为实际数据长度的一半。
        '''
        state = self.__onenet.notify(data, ack_flag)
        state = True if state == 0 else False
        return state
    
    def updateLwM2MObject(self, instance_id, lifetime, obj_flag, raimode):
        '''
        更新LwM2M 对象
        instance_id:通信套件的实例ID
        lifetime:设备存活周期 单位秒
        obj_flag:是否更新对象列表。0 不使用.1 使用
        raiMode: 用于指定消息传输携带的快速释放标记 RAI(Release Assistant Indication释放辅助提示),该标记
                 用于指示核心网释放与模块的 RRC 连接
                 0: 无指示 
                 1: 指示该包上行数据后不期望有进一步的上行或者下行数据, 核心网可立即释放 
                 2: 指示该包上行数据后期望有对应的单个下行数据包回复，核心网在下发后立即释放  
        '''
        state = self.__onenet.update(instance_id, lifetime, obj_flag, raimode)
        state = True if state == 0 else False
        return state

    def deleteLwM2MObject(self, instance_id, obj_id):
        '''
        删除LwM2M 对象
        instance_id:通信套件的实例ID
        objId:LwM2M 对象 ID,若对象 ID 不存在，则返回错误
        '''
        state = self.__onenet.delete_object(instance_id, obj_id)
        state = True if state == 0 else False
        return state

    def deleteInstance(self, instance_id):
        '''
        删除 OneNET 通信套件中的实例
        instance_id:通信套件的实例ID
        '''
        state = self.__onenet.destroy(instance_id)
        state = True if state == 0 else False
        return state

    def __callback(self, data):
        '''
        消息回调
        data: 平台下发事件
        '''
        print("onenet callback recv data :{}".format(data))