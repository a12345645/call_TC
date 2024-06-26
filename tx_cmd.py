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
            print('5f13 need PhaseOrder SignalMap SignalCount SubPhaseCount')
            return b''
        command = b'\x5f\x13' + int(data[0], 16).to_bytes(1, 'big') + int(data[1], 16).to_bytes(1, 'big') + \
            int(data[2]).to_bytes(1, 'big') + int(data[3]).to_bytes(1, 'big')
        SignalCount = int(data[2])
        SubPhaseCount = int(data[3])
        for i in range(SubPhaseCount):
            for j in range(SignalCount):
                command += int(data[4 + i * SignalCount + j], 16).to_bytes(1, 'big')
        return command

class cmd_5F2F(tx_cmd):
    command = '5F2F'
    def info(self, data):
        if (len(data) <= 4):
            print('5F2F need PhaseOrder SignalMap SignalCount SubPhaseCount')
            return b''
        command = b'\x5f\x2F' + int(data[0]).to_bytes(1, 'big') + int(data[1], 16).to_bytes(1, 'big') + \
            int(data[2]).to_bytes(1, 'big') + int(data[3]).to_bytes(1, 'big')
        SignalCount = int(data[2])
        SubPhaseCount = int(data[3])
        idx = 4
        for i in range(SubPhaseCount):
            StepCount = int(data[idx])
            idx += 1
            for k in range(StepCount):
                for j in range(SignalCount):
                    command += int(data[idx], 16).to_bytes(1, 'big')
                    idx += 1
        return command

# 時相或步階變換控制
class cmd_5F1C(tx_cmd):
    command = '5F1C'
    def info(self, data):
        if (len(data) != 3):
            print('5F1C need SubPhaseID StepID EffectTime')
            return b''
        return b'\x5f\x1c' + int(data[0]).to_bytes(1, 'big') + int(data[1]).to_bytes(1, 'big') + int(data[2]).to_bytes(1, 'big')


# 一般日時段型態管理, 先用 5F46 查詢在使用
class cmd_5F16(tx_cmd):
    command = '5F16'
    def info(self, data):
        if (len(data) <= 2):
            print('5F16 need SegmentType SegmentCount')
            return b''
        segmentType = int(data[0])
        segmentCount = int(data[1])
        command = b'\x5f\x16' + segmentType.to_bytes(1, 'big') + segmentCount.to_bytes(1, 'big')
        index = 2
        for i in range(segmentCount):
            command += int(data[index]).to_bytes(1, 'big') # Hour
            command += int(data[index + 1]).to_bytes(1, 'big') # Min
            command += int(data[index + 2]).to_bytes(1, 'big') # PlanID
            index += 3
        numWeekDay = int(data[index])
        command += int(data[index]).to_bytes(1, 'big')
        for i in range(numWeekDay):
            command += int(data[index + i + 1]).to_bytes(1, 'big')
        return command

class cmd_5F16(tx_cmd):
    command = '5F16'
    def info(self, data):
        if (len(data) <= 2):
            print('5F16 need SegmentType SegmentCount')
            return b''
        segmentType = int(data[0])
        segmentCount = int(data[1])
        command = b'\x5f\x16' + segmentType.to_bytes(1, 'big') + segmentCount.to_bytes(1, 'big')
        index = 2
        for i in range(segmentCount):
            command += int(data[index]).to_bytes(1, 'big') # Hour
            command += int(data[index + 1]).to_bytes(1, 'big') # Min
            command += int(data[index + 2]).to_bytes(1, 'big') # PlanID
            index += 3
        numWeekDay = int(data[index])
        command += int(data[index]).to_bytes(1, 'big')
        for i in range(numWeekDay):
            command += int(data[index + i + 1]).to_bytes(1, 'big')
        return command

# 時相或步階變換控制
class cmd_5F43(tx_cmd):
    command = '5F43'
    def info(self, data):
        if (len(data) != 1):
            print('5F43 need PhaseOrder')
            return b''
        return b'\x5f\x43' + int(data[0], 16).to_bytes(1, 'big')

class cmd_0F11(tx_cmd):
    command = '0F11'
    def info(self, data):
        return b'\x0f\x11'

class cmd_5F3F(tx_cmd):
    command = '5F3F'
    def info(self, data):
        if (len(data) != 2):
            print('5F3F need TransmitType TransmitCylce')
            return b''
        return b'\x5f\x3f' + int(data[0]).to_bytes(1, 'big') + int(data[1]).to_bytes(1, 'big')

class cmd_0F14(tx_cmd):
    command = '0F14'
    def info(self, data):
        if (len(data) != 1):
            print('0F14 need HardwareCylce')
            return b''
        return b'\x0f\x14' + int(data[0]).to_bytes(1, 'big')

class cmd_0F41(tx_cmd):
    command = '0F41'
    def info(self, data):
        return b'\x0f\x41'

class cmd_5F14(tx_cmd):
    command = '5F14'
    def info(self, data):
        if (len(data) <= 2):
            print('5F14 need SegmentType SegmentCount')
            return b''
        segmentType = int(data[0])
        segmentCount = int(data[1])
        command = b'\x5f\x16' + segmentType.to_bytes(1, 'big') + segmentCount.to_bytes(1, 'big')
        index = 2
        for i in range(segmentCount):
            command += int(data[index]).to_bytes(1, 'big') # Hour
            command += int(data[index + 1]).to_bytes(1, 'big') # Min
            command += int(data[index + 2]).to_bytes(1, 'big') # PlanID
            index += 3
        numWeekDay = int(data[index])
        command += int(data[index]).to_bytes(1, 'big')
        for i in range(numWeekDay):
            command += int(data[index + i + 1]).to_bytes(1, 'big')
        return command

class cmd_5F15(tx_cmd):
    command = '5F15'
    def info(self, data):
        if (len(data) <= 4):
            print('5F15 need PlanID Direct PhaseOrder SubPhaseCount')
            return b''
        planID = int(data[0])
        direct = int(data[1])
        phaseOrder = int(data[2], 16)
        subPhaseCount = int(data[3])
        command = b'\x5f\x15' + planID.to_bytes(1, 'big') + direct.to_bytes(1, 'big') + phaseOrder.to_bytes(1, 'big') + subPhaseCount.to_bytes(1, 'big')
        index = 4
        for i in range(subPhaseCount):
            command += int(int(data[index]) / 256).to_bytes(1, 'big') # Green
            command += int(int(data[index]) % 256).to_bytes(1, 'big')
            index += 1
        

        command +=  int(int(data[index]) / 256).to_bytes(1, 'big') + int(int(data[index]) % 256).to_bytes(1, 'big')
        command +=  int(int(data[index + 1]) / 256).to_bytes(1, 'big') + int(int(data[index + 1]) % 256).to_bytes(1, 'big')
        return command

class cmd_5F45(tx_cmd):
    command = '5F45'
    def info(self, data):
        if (len(data) < 1):
            print('5F45 need PlanID')
            return b''
        command = b'\x5f\x45' + int(data[0]).to_bytes(1, 'big')
        return command

class cmd_5F48(tx_cmd):
    command = '5F48'
    def info(self, data):
        return b'\x5f\x48'

txcmds = [cmd_5F4C(), cmd_5F10(), cmd_5F18(), cmd_0F42(), cmd_5F46(), cmd_5F63(), cmd_0F43(),
    cmd_5F44(), cmd_5F13(), cmd_5F1C(), cmd_5F16(), cmd_5F43(), cmd_0F11(), cmd_5F3F(), cmd_0F14(),
    cmd_0F41(), cmd_5F2F(), cmd_5F15(), cmd_5F45(), cmd_5F48()]
