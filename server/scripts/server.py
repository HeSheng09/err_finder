import socket
import json
import time
import datetime
import random
from threading import Thread
from conn_db import ConnDb


class ConnClient(Thread):
    def __init__(self, *args):
        super().__init__()
        self.client = args[0]
        self.address = args[1]

    def run(self):
        self._tcp_link(self.client, self.address)

    # 分发服务至对应的接口
    def _tcp_link(self, s, addr):
        print(f'Accept new connection from {addr}')
        s.send(b'connection succeed!')
        while True:
            # 接收操作
            data = b''
            e = s.recv(1024).decode('utf-8')
            num = int(e)
            s.send(b'Confirm')
            e = s.recv(1024)
            while len(data) < num - 1024:
                data += e
                e = s.recv(1024)
            data += e
            # 根据操作分发到指定处理器
            if data.decode('utf-8') == 'exit':
                break
            else:
                data = json.loads(data.decode('utf-8'))
                if data['operation'] == 'login':
                    login(s, data)
                elif data['operation'] == 'login_out':
                    login_out(s, data)
                elif data['operation'] == 'is login':
                    is_login(s, data)
                elif data['operation'] == 'upload':
                    upload(s, data)
                elif data['operation'] == 'download headinfo' or data['operation'] == 'open project':
                    download_head(s, data)
                elif data['operation'] == 'download file' or data['operation'] == 'open project: download':
                    download(s, data)
                elif data['operation'] == 'save error':
                    save_error(s, data)
                elif data['operation'] == 'select error':
                    select_err(s, data)
                elif data['operation'] == 'delete error':
                    delete_err(s, data)
                elif data['operation'] == 'edit exist error':
                    edit_exist_err(s, data)
                else:
                    s.send(b'11')
                    print(s.recv(1024).decode('utf-8'))
                    s.send(b'bad request')
        s.close()
        print(f'Connection from {addr} closed.')


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
        self.host = socket.gethostname()  # 获取本地主机名
        self.port = 12345
        self.stop_flag = False
        self.login_users = []

    def start(self):
        t = Thread(target=self.clear_users)
        t.start()
        self.server.bind((self.host, self.port))
        self.server.listen(5)  # 等待客户端连接
        while not self.stop_flag:
            c, addr = self.server.accept()  # 建立客户端连接
            # print(c, addr)
            client = ConnClient(c, addr)
            client.start()

    def clear_users(self):  # 检查当前登录账号两小时内的最近操作记录
        db = ConnDb()
        while True:
            update_time = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime('%Y%m%d%H%M%S')
            for user in self.login_users:
                data = db.select('MAX(opr_time)', 'operation', f'opr_time > {update_time} AND user = {user}')
                if data[0][0] is None:  # 两小时内没有操作记录，视为登录超时，释放该账号
                    self.login_users.remove(user)
                    # print(datetime.datetime.now() - db.select('MAX(opr_time)', 'operation', f'user = {user}')[0][0])
            # print(self.login_users)
            time.sleep(7200)

    def stop(self):
        self.stop_flag = True


def login(sock, data):
    db = ConnDb()
    result = db.select('name,password', 'user', "ID='"+str(data['ID'])+"'")
    if len(result) == 0:
        sock.send(b'4')
        print(sock.recv(1024).decode('utf-8'))
        sock.send(b'fail')
        db.insert('operation', ('opr_time', 'user', 'operation', 'result'),
                  f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{data['ID']}','login_in','fail')")
    elif result[0][1] == data['password']:
        server.login_users.append(data['ID'])
        print(server.login_users)
        d = json.dumps({"result": "login in success", "name": result[0][0]}).encode('utf-8')
        sock.send(str(len(d)).encode('utf-8'))
        print(sock.recv(1024).decode('utf-8'))
        sock.send(d)
        db.insert('operation', ('opr_time', 'user', 'operation', 'result'),
                  f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{data['ID']}','login_in','success')")
    else:
        d = json.dumps({"result": "fail"}).encode('utf-8')
        sock.send(str(len(d)).encode('utf-8'))
        print(sock.recv(1024).decode('utf-8'))
        sock.send(d)
        db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                  values=f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{data['ID']}','login_in','fail','none')")


def login_out(sock, data):
    if data['ID'] in server.login_users:
        server.login_users.remove(data['ID'])
        print(server.login_users)
    d = json.dumps({"result": "login out succeed"}).encode('utf-8')
    sock.send(str(len(d)).encode('utf-8'))
    print(sock.recv(1024).decode('utf-8'))
    sock.send(d)
    db = ConnDb()
    db.insert('operation', ('opr_time', 'user', 'operation', 'result'),
              f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{data['ID']}','login_out','success')")


def is_login(sock, data):
    if data['ID'] in server.login_users:
        d = json.dumps({"result": "login on"}).encode('utf-8')
    else:
        d = json.dumps({"result": "login off"}).encode('utf-8')
    sock.send(str(len(d)).encode('utf-8'))
    print(sock.recv(1024).decode('utf-8'))
    sock.send(d)


def upload(sock, opr):
    # 接收文件
    file = b''
    e = sock.recv(1024).decode('utf-8')
    num = int(e)
    sock.send(b'Confirm')
    e = sock.recv(1024)
    while len(file) < num - 1024:
        file += e
        e = sock.recv(1024)
    file += e
    print(opr)
    db = ConnDb()
    OID = generate_ID()
    # 插入实际文件
    if opr['type'] == 'text':
        result = db.insert_file('txt', ('ID', 'data'), (f"'{OID}'", f"'{file.decode('utf-8')}'"))
    else:
        result = db.insert_file('image', ('ID', 'data'), (f"'{OID}'", file))
    if result == 'success':
        # 插入索引文件
        ID = generate_ID()
        table = 'map'
        cols = ('ID', 'title', 'type', 'OID')
        values = f"('{ID}','{opr['title']}','{opr['type']}','{OID}')"
        result = db.insert(table, cols, values)
        if result == 'success':
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','upload','success','{ID}')")
            d = json.dumps({"result": "file upload success"}).encode('utf-8')
        else:
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','upload','fail')")
            d = json.dumps({"result": "file upload failed"}).encode('utf-8')
    else:
        # 插入操作记录
        db.insert('operation', ('opr_time', 'user', 'operation', 'result'),
                  f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','upload','fail')")
        d = json.dumps({"result": "file upload failed"}).encode('utf-8')
    sock.send(str(len(d)).encode('utf-8'))
    print(sock.recv(1024).decode('utf-8'))
    sock.send(d)


def download_head(sock, opr):
    db = ConnDb()
    file_list = db.select('*', 'map', 'None')
    d = {"result": "success", "file": []}
    for file in file_list:
        d['file'].append({'ID': file[0], 'title': file[1], 'type': file[2]})
    # print(d)
    d = json.dumps(d).encode('utf-8')
    sock.send(str(len(d)).encode('utf-8'))
    print(sock.recv(1024).decode('utf-8'))
    sock.send(d)


def download(sock, opr):
    db = ConnDb()
    try:
        OID = db.select('OID', 'map', f"ID = '{opr['ID']}'")[0][0]
        if opr['type'] == 'image':
            file = db.select('data', 'image', f"ID = '{OID}'")[0][0]
        else:
            file = db.select('data', 'txt', f"ID = '{OID}'")[0][0].encode('utf-8')
        sock.send(str(len(file)).encode('utf-8'))
        print(sock.recv(1024).decode('utf-8'))
        sock.sendall(file)
        if opr['operation'] == 'download file':
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','download file','success','{opr['ID']}')")
        elif opr['operation'] == 'open project: download':
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','open project','success','{opr['ID']}')")
    except:
        if opr['operation'] == 'download file':
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','download file','failed','{opr['ID']}')")
        elif opr['operation'] == 'open project: download':
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','open project','failed','{opr['ID']}')")


def save_error(sock, opr):
    db = ConnDb()
    try:
        data = opr['data']
        ID = generate_ID()
        table = 'error'
        cols = ('ID', 'pos', 'type', 'detail', 'OID')
        values = f"('{ID}','{data['pos']}','{data['type']}','{data['detail']}','{data['OID']}')"
        result = db.insert(table, cols, values)
        if result == 'success':
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','save error','success','{ID}')")
            d = json.dumps({"result": "save error success"}).encode('utf-8')
        else:
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','save error','fail')")
            d = json.dumps({"result": "save error failed"}).encode('utf-8')
    except:
        # 插入操作记录
        db.insert('operation', ('opr_time', 'user', 'operation', 'result'),
                  f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','save error','fail')")
        d = json.dumps({"result": "save error failed"}).encode('utf-8')
    sock.send(str(len(d)).encode('utf-8'))
    print(sock.recv(1024).decode('utf-8'))
    sock.send(d)


def edit_exist_err(sock, opr):
    db = ConnDb()
    try:
        data = opr['data']
        values = (f"'{data['pos']}'", f"'{data['type']}'", f"'{data['detail']}'")
        result = db.update('error', ('pos', 'type', 'detail'), values, f"ID = '{data['ID']}'")
        if result == 'success':
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','edit exist error','success','{opr['data']['ID']}')")
            d = json.dumps({"result": "edit exist error success"}).encode('utf-8')
        else:
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','edit exist error','fail','{opr['data']['ID']}')")
            d = json.dumps({"result": "edit exist error fail"}).encode('utf-8')
    except:
        # 插入操作记录
        db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                  f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','edit exist error','fail','{opr['data']['ID']}')")
        d = json.dumps({"result": "edit exist error fail"}).encode('utf-8')
    sock.send(str(len(d)).encode('utf-8'))
    print(sock.recv(1024).decode('utf-8'))
    sock.send(d)


def select_err(sock, opr):
    db = ConnDb()
    error_list = db.select('ID,pos,type,detail', 'error', f"OID = '{opr['OID']}' AND (type LIKE '%{opr['key']}%' OR detail LIKE '%{opr['key']}%')")
    d = {"result": "success", "error": []}
    for err in error_list:
        d['error'].append({'ID': err[0], 'pos': err[1], 'type': err[2], 'detail': err[3]})
    d = json.dumps(d).encode('utf-8')
    sock.send(str(len(d)).encode('utf-8'))
    print(sock.recv(1024).decode('utf-8'))
    sock.send(d)


def delete_err(sock, opr):
    db = ConnDb()
    try:
        result = db.delete('error', f"ID = '{opr['ID']}'")
        if result == 'success':
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','delete error','success','{opr['ID']}')")
            d = json.dumps({"result": "delete error success"}).encode('utf-8')
        else:
            # 插入操作记录
            db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                      f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','delete error','fail','{opr['ID']}')")
            d = json.dumps({"result": "delete error fail"}).encode('utf-8')
    except:
        # 插入操作记录
        db.insert('operation', ('opr_time', 'user', 'operation', 'result', 'object'),
                  f"('{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}','{opr['user']}','delete error','fail','{opr['ID']}')")
        d = json.dumps({"result": "delete error fail"}).encode('utf-8')
    sock.send(str(len(d)).encode('utf-8'))
    print(sock.recv(1024).decode('utf-8'))
    sock.send(d)


def generate_ID():
    length = random.randint(8, 32)
    code = 'qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAQWERTYUIOP0987654321'
    ID = ''
    for i in range(length):
        ID += code[random.randint(0, 61)]
    return ID


if __name__ == '__main__':
    server = Server()
    server.start()
