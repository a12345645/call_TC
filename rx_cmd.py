class rx_cmd:
    command = b''
    illustrate = ''
    def __init__(self):
        pass
    def content(self, info):
        pass
    def Iscmd(self, info):
        return self.command == info[0:2]
    
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

rxcmds = [cmd_5FCC(), cmd_0FC2()]