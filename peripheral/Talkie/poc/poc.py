import net
import sim
import poc
from usr.common_except import CustomError

class Poc(object):
    def __init__(self,init_cb=None):
        '''
        初始化对讲机，先确保sim卡及网络状态正常。
        :param init_cb: 初始化回调函数
        '''
        if sim.getStatus() != 1:
            raise CustomError("sim not ready.")
        if net.getState() == -1:
            raise CustomError("net conn not ready.")
        if init_cb == None:
            self._cb = self.cb
        else:
            self._cb = init_cb
        poc.init(self._cb)

    def cb(self,*args):
        pass

    def log_en(self,enable=0):
        '''
        log使能
        :param enable: 0：关闭，1：开启，默认0
        '''
        poc.log(enable)

    def login(self,login_cb):
        '''
        登录
        :param login_cb:登录状态回调函数，参数：1表示成功，2表示失败
        :return: 0:成功 -1：失败
        '''
        if poc.login(login_cb):
            return -1
        return 0

    def logout(self):
        poc.logout()

    def joingroup(self,gid):
        '''
        加入组
        :param gid: 组id
        :return: 0：成功 -1：失败
        '''
        if poc.joingroup(gid):
            return -1
        return 0

    def leavegroup(self):
        '''
        离开组
        '''
        poc.leavegroup()

    def speak(self,value):
        '''
        呼叫组内用户
        :param value:1：呼叫 0：退出呼叫
        :return:0：成功 -1：失败
        '''
        if poc.speak(value):
            return -1
        return 0

    def calluser(self,uid,cb):
        '''
        呼叫uid的用户
        :param uid: 呼叫的用户id
        :param cb: 回调函数，参数：1表示成功，0表示失败
        :return:
        '''
        if poc.calluser(uid,cb):
            return -1
        return 0

    def group_getbyindex(self,index):
        '''
        按索引查询群组信息
        :param index:索引号
        :return:列表：（群组id,群组名，群组类型，群组索引号）
        '''
        return poc.group_getbyindex(index)

    def group_getbyid(self,gid):
        '''
        按gid查询群组信息
        :param index:索引号
        :param gid:组id
        :return:列表：（群组id,群组名，群组类型，群组索引号）
        '''
        return poc.group_getbyid(gid)

    def member_getbyid(self,uid):
        '''
        查询用户信息
        :param uid: 用户id
        :return: 列表：（用户id, 用户名，在线状态，索引号）,在线状态：1，在线 	2，离线	3，在线在组
        '''
        return poc.member_getbyid(uid)

    def get_loginstate(self):
        '''
        查询当前用户在线状态
        :return:1，在线 	2，离线	3，在线在组
        '''
        return poc.get_loginstate()

    def get_groupcount(self):
        '''
        查询组群数
        :return: 组群数
        '''
        return poc.get_groupcount()

    def get_grouplist(self,index_begin, count):
        '''
        查询组群信息
        :param index_begin: 查询的索引起始值
        :param count:计划查询的个数
        :return:群组id,群组名，群组类型，群组索引号）  -1：失败
        '''
        return poc.get_grouplist(index_begin, count)

    def get_audiostate(self):
        '''
        获取当前音频状态
        :return:0：空闲
                1：开始通话
                2：通话中
                3：停止通话
                4：开始接听
                5：接听中
                6：停止接听
                7：开始播放tts
                8：停止播放tts
                9：开始播放提示音
                10：停止播放提示音
                11：开始录音
                12：结束录音
        '''
        return poc.get_audiostate()

    def set_tts_enable(self,enable):
        '''
        使能tts
        :param enable: 1:使用 0:不使用
        :return:0:成功 其他失败
        '''
        return poc.set_tts_enable(enable)

    def play_tts(self,tts_str,interrupt):
        '''
        播放tts
        :param tts_str:播放的内容
        :param interrupt:可否中断
        :return:0:成功 其他失败
        '''
        return poc.play_tts(tts_str,interrupt)

    def ping(self):
        '''
        ping服务器
        :return: 0:成功 其他失败
        '''
        return poc.send_ping()

    def register_audio_cb(self,audio_cb):
        '''
        注册音频回调
        :param audio_cb:音频回调函数
        回调参数：列表（state，uid, name，flag）
                state:当前语音状态:收听/讲话/TTS/TONE
                uid：当前操作用户uid，讲话/TTS/TONE时为0
                name:当前操作用户名字，讲话/TTS/TONE时为NULL
                flag:如果state为BND_LISTEN_START,flag==1表示本机可以打断对方讲话,flag==0表示本机不能打断对方讲话
        '''
        poc.register_audio_cb(audio_cb)

    def register_join_group_cb(self,cb):
        '''
        注册入组回调
        :param cb:进组回调,触发源包括主动进组和被动进组
        回调参数：列表（groupname，gid）
                groupname:当前群组的名字
                gid：当前群组gid
        '''
        poc.register_join_group_cb(cb)

    def register_listupdate_cb(self,cb):
        '''
        注册数据变化的回调
        :param cb:数据变化的回调
        回调参数：1：群组列表变化， 2：成员列表变化
        '''
        poc.register_listupdate_cb(cb)

    def register_upgrade_cb(self,cb):
        '''
        注册是否升级回调
        :param cb:升级回调
        回调参数：1：需要升级， 0：不需要升级
        '''
        poc.register_upgrade_cb(cb)

    def set_notify_mode(self,flags):
        '''
        通知模式
        :param flags:通知模式
        '''
        poc.set_notify_mode(flags)

    def get_init_status(self):
        '''
        获取初始化状态
        '''
        return poc.get_init_status()

    def set_solution(self, solution):
        '''
        设置方案
        :param solution:方案
        '''
        return poc.set_solution(solution)

    def set_solution_version(self, version):
        '''
        设置solution版本
        :param version:版本
        '''
        return poc.set_solution_version(version)

    def set_productInfo(self,info):
        '''
        设置产品信息
        '''
        return poc.set_productInfo(info)

    def set_manufacturer(self,info):
        '''
        设置制造商信息
        '''
        return poc.set_manufacturer(info)

def init_cb(args):
    print('cb ',args)

def ui_upgrade_status_cb(args):
    print("upgrade", args)

def ui_login_status_cb(args):
    print("ui_login_status", args)

def ui_join_group_cb(args):
    print("ui_join_group gid", args[0])
    print("ui_join_group groupname", args[1])

def ui_audio_cb(args):
    print("audio state:", args[0], "uid", args[1], "name", args[2], "falg", args[3])

def ui_listupdate_cb(args):
    print("ui_listupdate_cb", args)

if __name__ == "__main__":
    mypoc = Poc(init_cb)                            #初始化对象
    mypoc.get_init_status()                         #获取初始化状态
    mypoc.set_notify_mode(1)                        #通知模式
    mypoc.set_solution("HF")                        #设置方案
    mypoc.set_solution_version("1208")              #设置方案版本
    mypoc.set_productInfo("HF")                     #设置产品信息
    mypoc.set_manufacturer("HF")                    #设置制造商信息

    print("ping .",mypoc.ping())
    mypoc.login(ui_login_status_cb)                 #登录
    mypoc.register_upgrade_cb(ui_upgrade_status_cb) #注册是否升级回调
    mypoc.register_join_group_cb(ui_join_group_cb)  #注册入组回调
    mypoc.register_audio_cb(ui_audio_cb)            #注册音频回调
    mypoc.register_listupdate_cb(ui_listupdate_cb)  #注册数据变化的回调

    mypoc.set_tts_enable(1)                         #使能tts
    mypoc.play_tts("hello",0)                       #播放tts