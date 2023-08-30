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

        print('5FC6 SegmentType %d SegmentCount %d (' % (segmentType, segmentCount), end='')
        for segment in segmentList:
            print('Hour %d Min %d PlanID %d, ' % (segment[0], segment[1], segment[2]), end='')
        print(') NumWeekDay %d (' % (numWeekDay), end = '')
        for weekDay in weekDaylist:
            print('weekDay %d, ' % (weekDay), end='')
        print(')')

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

rxcmds = [cmd_5FCC(), cmd_0FC2(), cmd_5FC6(), cmd_0F80(), cmd_5FE3()]
