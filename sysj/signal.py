import socket, sys, threading, string, struct, math

TYPE_THL   = 0x84
TYPE_STATE = 0x30 # Turned on(1) or off(0)
TYPE_POWER = 0x31
MAGIC = 0xAABB

def printHex(num):
    print ":".join("{:02x}".format(ord(c)) for c in num)

class SysJInput:
    MAGIC_LENGTH = 3
    handler = None

    def worker(self, conn, addr):
        conn.settimeout(5)
        try:
            while True:
                try:
                    magic = conn.recv(self.MAGIC_LENGTH)
                    if int(magic[:2].encode('hex'), 16) == MAGIC:
                        length = int(magic[2].encode('hex'), 16)
                        packet = conn.recv(length)
                        self.handler(self.__getNodeID(packet), self.__getActuatorID(packet), self.__getValue(packet))
                except socket.timeout:
                    pass
        except:
            conn.close()


    def createServer(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen(1)
        while True:
            try:
                sock.settimeout(5)
                conn, addr = sock.accept()
                th = threading.Thread(target=self.worker, args=(conn,addr))
                th.start()
            except socket.timeout:
                pass

    def __getNodeGroup(self, packet):
        return int(packet[:1].encode('hex'), 16)

    def __getNodeID(self, packet):
        return int(packet[1:2].encode('hex'), 16)

    def __getPacketType(self, packet):
        return int(packet[2:3].encode('hex'), 16)

    def __getActuatorID(self, packet):
        return int(packet[3:4].encode('hex'), 16)

    def __getValue(self, packet):
        return int(packet[4:].encode('hex'), 16)

    def __init__(self, ip, port, handler):
        self.handler = handler
        t1 = threading.Thread(target=self.createServer, args=(ip,port))
        t1.start()
        pass

class SysJOutput:
    connList = []
    lock = threading.Lock()

    def worker(self, conn, addr):
        conn.settimeout(5)
        try:
            magic = conn.recv(self.MAGIC)
            if int(magic[:2].encode('hex'), 16) == 0xAABB:
                length = int(magic[2].encode('hex'), 16)
                packet = conn.recv(length)
                self.handler(self.__getNodeID(packet), self.__getValue(packet))
        finally:
            conn.close()

    def createServer(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen(1)
        while True:
            try:
                sock.settimeout(5)
                conn, addr = sock.accept()
                with self.lock:
                    self.connList.append(conn)
            except socket.timeout:
                pass

    def __init__(self, ip, port):
        th = threading.Thread(target=self.createServer, args=(ip,port))
        th.start()

    def send(self, nodeid, ptype, value):
        value = [x for x in value]
        packet = [0xAA, 0xBB, 0x00, 0x0B, nodeid, ptype] + value
        packet[2] = len(packet[3:])
        for conn in self.connList:
            try:
                conn.send(bytearray(packet))
            except socket.error:
                self.connList.remove(conn)
                pass


