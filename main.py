import threading
import time
import serial

from tx_cmd import *
from rx_cmd import *

com = serial.Serial('/dev/ttyS0',9600)
 
class RxCommand(object):
    command = b''
    cmds = rxcmds
    def __init__(self):
        t = threading.Thread(target = self.recieve)
        t.start()
    
    def get_len(self):
        if len(self.command) < 7:
            return -1
        return (self.command[5] << 8) | self.command[6]

    def check_CKS(self, data, cks):
        c = 0
        for d in data:
            c ^= d
        return cks == c
    
    def get_CKS(self, data):
        cks = 0
        for d in data:
            cks ^= d
        return cks.to_bytes(1, 'big')
    
    def recv_header(self):
        self.command += com.read(5)
        l = self.get_len()
        if l < 7:
            return False
        self.command += com.read(self.get_len() - 7)
        return True
    
    def get_info(self):
        l = self.get_len()
        return self.command[7:l - 3]
    
    def response_ack(self):
        r = b'\xaa\xdd' + self.command[2].to_bytes(1, 'big') + b'\xff\xff\x08'
        return r + self.get_CKS(r)
    
    def recieve(self):
        while True:
            data = com.read(1)
            if data == b'\xaa':
                self.command = data
                data = com.read(1)
                self.command += data
                if data == b'\xbb':
                    if not self.recv_header():
                        continue
                    if (self.check_CKS(self.command[0:len(self.command) - 1], self.command[len(self.command) - 1])):
                        info = self.get_info()
                        print('%02x %02x' % (info[0], info[1]), int(self.command[2]))
                        for i in self.cmds:
                            if i.Iscmd(info):
                                i.content(info)
                                
                        com.write(self.response_ack())
                        
                    else:
                        print('check_CKS wrong.')
                elif data == b'\xdd':
                    if not self.recv_header():
                        continue
                    print('ack, seq', int(self.command[2]))
                elif data == b'\xee':
                    if not self.recv_header():
                        continue
                    print('nak')

rx = RxCommand()

class TxCommand(object):
    seq_num = 0
    cmds = txcmds
    
    def request(self, line):
        info, msg = self.generate_info(line)
        if info == b'':
            print('Command nofind.')
            return
        
        cmd = self.generate_cmd(info)

        com.write(cmd)
        print(msg + ' complete, seq %d.' % self.seq_num)
        self.seq_num += 1
    
    def generate_info(self, line):
        l = line.split(' ')
        info = b''
        msg = ''
        if len(l) == 0:
            return info, msg
        for i in self.cmds:
            if i.Iscmd(l[0]):
                info = i.info(l[1:])
                msg = i.command
                break  
        return info, msg
        
    def generate_cmd(self, info):
        if self.seq_num > 0xFF:
            self.seq_num = 0
        command = b'\xaa\xbb' + self.seq_num.to_bytes(1, 'big') + b'\xff\xff'

        cmd_len = 10 + len(info)
        
        command += cmd_len.to_bytes(2, 'big') + info + b'\xaa\xcc'
        command += self.check_CKS(command)
        return command


    class loop_cmd():
        enable = False
        cmd = b''
        
        def __init__(self, p, line, loop=0):
            self.parent = p
            self.line = line
            self.enable = True
            self.loop = loop

        def cmd(self):
            info, _ = self.parent.generate_info(self.line)
            if info == b'':
                self.enable = False
                return info
            return self.parent.generate_cmd(info)
    
    request_cmds = []
    polling_thread = ''
    def add_polling_request(self, line):
        l = self.loop_cmd(self, line)
        self.request_cmds.append(l)
        if self.polling_thread == '':
            self.polling_thread = threading.Thread(target = self.polling_request)
            self.polling_thread.start()
    
    def polling_request(self):
        while True:
            for i in self.request_cmds:
                if i.enable:
                    com.write(i.cmd())
                    self.seq_num += 1
            time.sleep(0.5)
        
    
    def check_CKS(self, data):
        cks = 0
        for d in data:
            cks ^= d
        return cks.to_bytes(1, 'big')

tx = TxCommand()

tx.add_polling_request('5f46 1 1')
# tx.request('5f18 5')
# tx.request('5f10 1')