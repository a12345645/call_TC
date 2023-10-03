class tx_cmd:
    command = ''
    illustrate = ''
    def __init__(self):
        pass
    def info(self, data):
        return b''
    def Iscmd(self, cmd):
        return self.command == cmd.upper()


class cmd_0F42(tx_cmd):
    command = '0F42'
    def info(self, data):
        return b'\x0f\x42'
    
class cmd_5F4C(tx_cmd):
    command = '5F4C'
    def info(self, data):
        return b'\x5f\x4C'

class cmd_5F46(tx_cmd):
    command = '5F46'
    def info(self, data):
        if (len(data) != 2):
            print('5F46 need SegmentType and WeekDay.')
            return b''
        return b'\x5f\x46' + int(data[0]).to_bytes(1, 'big') + int(data[1]).to_bytes(1, 'big')

# 目前控制策略管理
# 全動態是 16 自動是 1
class cmd_5F10(tx_cmd):
    command = '5F10'
    def info(self, data):
        if (len(data) < 1):
            print('5f10 need ControlStrategy.')
            return b''
        ret = b'\x5f\x10' + int(data[0]).to_bytes(1, 'big')
        if len(data) == 2:
            return ret + int(data[1]).to_bytes(1, 'big')
        else:
            return ret + b'\x78'
    
class cmd_5F18(tx_cmd):
    command = '5F18'
    def info(self, data):
        if (len(data) < 1):
            print('5f18 need planId.')
            return b''
        return b'\x5f\x18' + int(data[0]).to_bytes(1, 'big')

class cmd_5F1E(tx_cmd):
    command = '5F1E'
    def info(self, data):
        if (len(data) < 6):
            print('5f18 need Direct(2) and (Hour+Min)(2).')
            return b''
        ret = b'\x5f\x1E' 
        for i in range(6):
            ret += data[i].to_bytes(1, 'big')
        return ret

class cmd_5F63(tx_cmd):
    command = '5F63'
    def info(self, data):
        if (len(data) != 2):
            print('5f63 need ChildNo and PlanId')
            return b''
        return b'\x5f\x63' + int(data[0]).to_bytes(1, 'big') + int(data[1]).to_bytes(1, 'big')

class cmd_0F43(tx_cmd):
    command = '0F43'
    def info(self, data):
        return b'\x0f\x43'

# 查詢路口時制計畫的基本參數
class cmd_5F44(tx_cmd):
    command = '5F44'
    def info(self, data):
        if (len(data) != 1):
            print('5f44 need PlanId')
            return b''
        return b'\x5f\x44' + int(data[0]).to_bytes(1, 'big')

class cmd_5F13(tx_cmd):
    command = '5F13'
    def info(self, data):
        if (len(data) <= 4):
            print('5f13 need PhaseOrder SignalMap SignalCount SubPhaseCount ')
            return b''
        command = b'\x5f\x13' + int(data[0]).to_bytes(1, 'big') + int(data[1]).to_bytes(1, 'big') + \
            int(data[2]).to_bytes(1, 'big') + int(data[3]).to_bytes(1, 'big')
        SignalCount = int(data[2])
        SubPhaseCount = int(data[3])
        for i in range(SubPhaseCount):
            for j in range(SignalCount):
                command += int(data[4 + i * SignalCount + j])
        return b'\x5f\x13' + int(data[0]).to_bytes(1, 'big')

# 時相或步階變換控制
class cmd_5F1C(tx_cmd):
    command = '5F1C'
    def info(self, data):
        if (len(data) != 3):
            print('5F1C need SubPhaseID StepID EffectTime')
            return b''
        return b'\x5f\x1c' + int(data[0]).to_bytes(1, 'big') + int(data[1]).to_bytes(1, 'big') + int(data[2]).to_bytes(1, 'big')

txcmds = [cmd_5F4C(), cmd_5F10(), cmd_5F18(), cmd_0F42(), cmd_5F46(), cmd_5F63(), cmd_0F43(), cmd_5F44(), cmd_5F13(), cmd_5F1C()]
