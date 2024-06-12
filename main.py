import threading
import time
import serial
import math

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
        r = b'\xaa\xdd' + self.command[2].to_bytes(1, 'big') + b'\xff\xff\x00\x08'
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
                        info = self.get_info().replace(b'\xaa\xaa', b'\xaa')
                        print('recv %02x %02x' % (info[0], info[1]), int(self.command[2]))
                        for i in self.cmds:
                            if i.Iscmd(info):
                                i.content(info)

                        com.write(self.response_ack())
                    else:
                        print('check_CKS wrong.')
                        continue
                elif data == b'\xdd':
                    if not self.recv_header():
                        continue
                    print('ack, seq', int(self.command[2]), '-', int(self.command[3]), int(self.command[4]))
                elif data == b'\xee':
                    if not self.recv_header():
                        continue
                    print('nak', int(self.command[2]), '-', int(self.command[3]), int(self.command[4]))
rx = RxCommand()

class TxCommand(object):
    cmds = txcmds
    seq_num = 0
    def request(self, line):
        info, msg = self.generate_info(line)
        if info == b'':
            print('Command nofind.')
            return
        
        cmd = self.generate_cmd(info)

        com.write(cmd)
        print(msg + ' complete, seq %d.' % self.seq_num)

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

    def repeat_aa(self, arr):
        result = b''
        for num in arr:
            result += num.to_bytes(1, 'big')
            if num == 0xAA:
                 result += num.to_bytes(1, 'big')
        return result

    def generate_cmd(self, info):
        if self.seq_num > 0xFF:
            self.seq_num = 0
        command = b'\xaa\xbb' + self.seq_num.to_bytes(1, 'big') + b'\xff\xff'
        self.seq_num += 1

        info = self.repeat_aa(info)
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
            time.sleep(1)

    def send_row_data(self, data):
        l = data.split(' ')
        packet = b''
        for i in l:
            packet += int(i, 16).to_bytes(1, 'big')
        com.write(packet)

    def check_CKS(self, data):
        cks = 0
        for d in data:
            cks ^= d
        return cks.to_bytes(1, 'big')

tx = TxCommand()


# tx.add_polling_request('5F4C')


# tx.request('5F48')
# tx.request('5F15 40 0 40 4 ' +
#             '55 10 39 11 ' + 
#             '140 70')
# tx.request('5F13 40 55 4 4 ' +
#             '74 81 74 81 ' +
#             '89 a1 89 a1 ' +
#             '81 74 81 74 ' +
#             'a1 89 a1 89')
# tx.request('5F43 40')
# tx.request('5F48')


# tx.request('5F13 40 D5 4 2 ' +
#             '44 81 44 81 ' +
#             '81 44 81 44')

# tx.request('5F13 40 D5 4 4 ' +
#             '74 81 74 81 ' +
#             '89 a1 89 a1 ' +
#             '81 74 81 74 ' +
#             'a1 89 a1 89')

# tx.request('5F13 40 D5 4 3 ' +
#             '44 a1 44 81 ' +
#             '81 44 81 61 ' +
#             'a1 41 a1 44')

# tx.request('5F13 40 D5 5 5 ' +
#             '81 44 81 41 81 ' +
#             '81 44 81 44 81 ' +
#             '41 81 44 81 81 ' +
#             '44 81 44 81 81 ' +
#             '81 81 81 81 44')

# tx.add_polling_request('5F2F 40 D5 5 5 ' +
#           '1 81 44 81 41 81 ' +
#           '5 81 44 81 44 81 ' +
#             '81 C4 81 C4 81 ' +
#             '81 84 81 84 81 ' +
#             '81 82 81 82 81 ' +
#             '81 81 81 81 81 ' +
#           '1 41 81 44 81 81 ' +
#           '5 44 81 44 81 81 ' +
#             'C4 81 C4 81 81 ' +
#             '84 81 84 81 81 ' +
#             '82 81 82 81 81 ' +
#             '81 81 81 81 81 ' +
#           '5 81 81 81 81 44 ' +
#             '81 81 81 81 C4 ' +
#             '81 81 81 81 84 ' +
#             '81 81 81 81 82 ' +
#             '81 81 81 81 81 ')

# tx.request('5F13 40 D5 5 5 ' +
#             '81 44 81 41 81 ' +
#             '81 44 81 44 81 ' +
#             '41 81 44 81 81 ' +
#             '44 81 44 81 81 ' +
#             '81 81 81 81 44')

# 5F16 example

# tx.request('5F16 1 1 0 0 40 7 7 1 2 3 4 5 6')

# tx.request('5F46 1 5')

# tx.request('5F4C')
