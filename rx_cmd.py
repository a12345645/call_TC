class rx_cmd:
    command = b''
    illustrate = ''
    def __init__(self):
        pass
    def content(self, info):
        pass
    def Iscmd(self, info):
        return self.command == info[0:2]

class cmd_5FC6(rx_cmd):
    command = b'\x5f\xc6'
    def content(self, info):
        segmentType = info[2]
        segmentCount = info[3]
        if len(info) < 4 + segmentCount * 3:
            print('5FC6 decode error')
            return
        segmentList = []
        for i in range(segmentCount):
            segmentList.append((info[4 + i * 3], info[5 + i * 3], info[6 + i * 3]))
        numWeekDay = info[4 + segmentCount * 3]
        if len(info) < 4 + segmentCount * 3 + numWeekDay:
            print('5FC6 decode error')
            return
        weekDaylist = []
        for i in range(numWeekDay):
            weekDaylist.append(info[4 + segmentCount * 3 + i])

        print('5FC6 SegmentType %d SegmentCount %d' % (segmentType, segmentCount), end='')
        for segment in segmentList:
            print('\nHour %d Min %d PlanID %d, ' % (segment[0], segment[1], segment[2]), end='')
        print('\nNumWeekDay %d' % (numWeekDay), end = '')
        for weekDay in weekDaylist:
            print('\nweekDay %d, ' % (weekDay), end='')
        print('')

class cmd_5FCC(rx_cmd):
    command = b'\x5f\xcc'
    def content(self, info):
        if len(info) != 7:
            return
        print('5FCC ControlStrategy %d SubPhaseID %d StepID %d Second %d' % (info[2], info[3], info[4], info[5] * 256 + info[6]))
        
class cmd_0FC2(rx_cmd):
    command = b'\x0f\xc2'
    def content(self, info):
        if len(info) != 9:
            return
        print('0FC2 Year: %d Month: %d Day: %d Week: %d Hour: %d Min: %d Sec: %d' % (info[2], info[3], info[4], info[5], info[6], info[7], info[8]))

class cmd_0F80(rx_cmd):
    command = b'\x0f\x80'
    def content(self, info):
        if len(info) != 4:
            return
        print('0F80 CommandID: %02x %02x' % (info[2], info[3]))

class cmd_5FE3(rx_cmd):
    command = b'\x5f\xe3'
    def content(self, info):
        if len(info) != 8:
            return
        print('5FE3 ChildNo: %d PlanID: %d StartOffset: %d %d EndOffset: %d %d' % (info[2], info[3], info[4], info[5], info[6], info[7])) 

class cmd_0FC3(rx_cmd):
    command = b'\x0f\xc3'
    def content(self, info):
        if len(info) != 8:
            return
        print('0FC3 Year: %d Month: %d Day: %d CompanyID %d Version %d CommandSet %d' % (info[2], info[3], info[4], info[5], info[6], info[7]))

class cmd_5FC4(rx_cmd):
    command = b'\x5f\xc4'
    def content(self, info):
        if len(info) < 4:
            return
        print('5FC4 PlanID: %d SubPhaseCount %d' % (info[2], info[3]))
        for i in range(info[3]):
            print('MinGreen: %d MaxGreen: %d Yellow: %d AllRed: %d PedGreenFlash: %d PedRed: %d' % 
            (info[4 + i * 7], info[5 + i * 7] * 256 + info[6 + i * 7], info[7 + i * 7], info[8 + i * 7], info[9 + i * 7], info[10 + i * 7]))

class cmd_5FC3(rx_cmd):
    command = b'\x5f\xc3'
    def content(self, info):
        if len(info) < 4:
            return
        print('5FC3 PhaseOrder: %d SignalMap: %d SignalCount: %d SubPhaseCount: %d' % (info[2], info[3], info[4], info[5]))
        for i in range(info[5]):
            print('subphase %d ' % (i + 1), end='')
            for j in range(info[4]):
                print('%02x ' % (info[6 + i * info[4] + j]), end='')
            print('')

class cmd_0F91(rx_cmd):
    command = b'\x0f\x91'
    def content(self, info):
        print('0F91 Reboot Communication.')

class cmd_0F04(rx_cmd):
    command = b'\x0f\x04'
    def content(self, info):
        print('0F04 %02x %02x' % (info[2], info[3]))

class cmd_0FC1(rx_cmd):
    command = b'\x0f\xC1'
    def content(self, info):
        print('0FC1 %02x %02x' % (info[2], info[3]))

rxcmds = [cmd_5FCC(), cmd_0FC2(), cmd_5FC6(), cmd_0F80(), cmd_5FE3(), cmd_0FC3(), cmd_5FC4(),
    cmd_5FC3(), cmd_0F04(), cmd_0FC1()]
