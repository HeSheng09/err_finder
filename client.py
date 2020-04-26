import json
import login
from main import *
import download
import project
import document
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QImage, QCursor
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QMessageBox, QFileDialog, QLabel
import sys
import os
import socket
import math


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.user = "000000"
        self.map_ID = ''
        self.map_title = ''
        self.map_type = 'image'
        self.file = []
        self.labels = []
        self.selected_error = QLabel(self.sawc_select)
        self.is_edit_select_err = False

        self.actionlogin_in.triggered.connect(self.login_in)
        self.actionlogin_out.triggered.connect(self.login_out)
        self.actionupload.triggered.connect(self.upload)
        self.actiondownload.triggered.connect(self.download)
        self.actionproject.triggered.connect(self.open_project)
        self.clear_edit.clicked.connect(self.cancel)
        self.save_edit.clicked.connect(self.save)
        self.select.clicked.connect(self.select_err)
        self.first.clicked.connect(self.first_select)
        self.next.clicked.connect(self.next_select)
        self.last.clicked.connect(self.last_select)
        self.end.clicked.connect(self.end_select)
        self.edit.clicked.connect(self.edit_err)
        self.pushButton.clicked.connect(self.delete_err)
        self.actiondocument.triggered.connect(self.document)
        self.action_about.triggered.connect(self.about)

    def login_in(self):
        self.dialog = LoginDialog()
        self.dialog.show()

    def login_out(self):
        if self.user != '000000':
            opr = {"operation": "login_out", "ID": self.user}
            result = send(opr)
            print(result)
            self.user = '000000'
            win.current_user.setText("当前用户：尚未登录，请登录！")

    def upload(self):
        if is_login():  # 已登录，可以上传文件
            # 选择要上传的文件
            file_name, file_type = QFileDialog.getOpenFileName(self, "选取文件",
                                                               f"C:/Users/{os.environ['USERNAME']}/Documents/",
                                                               "Image File(*.png *.jpg *.tif);; Text File(*.txt *.dat *.json *.xml)")
            if not file_name == '':
                if file_type == 'Image File(*.png *.jpg *.tif)':
                    opr = {"operation": "upload", "user": win.user, "title": file_name.split('/')[-1], "type": 'image'}
                else:
                    opr = {"operation": "upload", "user": win.user, "title": file_name.split('/')[-1], "type": 'text'}
                with open(file_name, 'rb') as f:
                    file = f.read()
                result = file_upload(opr, file)
                if result['result'] == 'file upload success':
                    msg_box = QMessageBox.information(self,'上传文件','文件上传成功！')
                else:
                    msg_box = QMessageBox.information(self, '上传文件', '文件上传失败，请稍后重试！')

    def download(self):
        if is_login():
            # 查询返回一个文件列表，选择要下载的文件
            opr = {"operation": "download headinfo", "user": win.user}
            self.file_list = send(opr)
            self.download_dialog = DownLoadDialog()
            self.download_dialog.show()

    def open_project(self):
        if is_login():
            # 查询返回一个文件列表，选择要打开的项目
            opr = {"operation": "open project", "user": win.user}
            self.file_list = send(opr)
            self.project_dialog = ProjectDialog()
            self.project_dialog.show()
            for label in self.labels:
                label.setVisible(False)
            self.labels.clear()
            self.selected_error.setVisible(False)
            self.label.setText("本次共搜索到0条结果！")
            self.is_edit_select_err = False

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        pos = self.relative_pos()
        cursor = QCursor()
        win_pos = self.geometry()
        centralwidget_pos = self.centralwidget.geometry()
        showspace_pos = self.showspace.geometry()
        scrollarea_pos = self.scrollArea.geometry()
        scrollarea_ab_pos = QPoint()
        scrollarea_ab_pos.setX(scrollarea_pos.x()+showspace_pos.x()+centralwidget_pos.x()+win_pos.x())
        scrollarea_ab_pos.setY(scrollarea_pos.y()+showspace_pos.y()+centralwidget_pos.y()+win_pos.y())
        if scrollarea_ab_pos.x()<cursor.pos().x()<(scrollarea_ab_pos.x()+scrollarea_pos.width()) and scrollarea_ab_pos.y()<cursor.pos().y()<(scrollarea_ab_pos.y()+scrollarea_pos.height()):
            if self.map_type == 'image':
                self.input_x.setText(str(pos.x()))
                self.input_y.setText(str(pos.y()))
            else:
                row = math.ceil(pos.y()/14)
                self.input_y.setText(str(row))

                def get_max_char():
                    len_x = [0 for _ in range(len(self.file))]
                    for i in range(len(self.file)):
                        len_x[i] = len(self.file[i])
                    len_x.sort()
                    return len_x[len(self.file) - 1]

                w_col = self.map.width() / (get_max_char())
                col = math.ceil(pos.x()/w_col)
                self.input_x.setText(str(col))

    def cancel(self):
        self.input_x.setText('')
        self.input_y.setText('')
        self.input_type.setText('')
        self.input_detail.setText('')

    def save(self):
        if is_login():
            if self.map_ID != '':
                x = self.input_x.text()
                y = self.input_y.text()
                e_type = self.input_type.text()
                detail = self.input_detail.toPlainText()
                if x == '' or y == '' or e_type == '' or detail =='':
                    msg_box = QMessageBox.information(self, "提示", "请完善质检信息！")
                else:
                    if not self.is_edit_select_err:
                        data = {"pos": str(x) + ' ' + str(y), "type": e_type, "detail": detail, "OID": self.map_ID}
                        opr = {"operation": "save error", "user": self.user, "data": data}
                        result = send(opr)
                    else:
                        data = {"ID": self.edit_select_err_ID,"pos": str(x) + ' ' + str(y), "type": e_type, "detail": detail, "OID": self.map_ID}
                        opr = {"operation": "edit exist error", "user": self.user, "data": data}
                        result = send(opr)
                    if result['result'] == 'save error success':
                        msg_box = QMessageBox.information(self, '提示', '保存成功')
                        self.cancel()
                    elif result['result'] == 'edit exist error success':
                        self.is_edit_select_err = False
                        msg_box = QMessageBox.information(self, '提示', '保存成功')
                        self.cancel()
                    else:
                        msg_box = QMessageBox.information(self, '提示', '保存失败')
            else:
                msg_box = QMessageBox.information(self, '提示', '未打开项目，请先打开项目！\n\t文件-->项目')

    def relative_pos(self):
        cursor = QCursor
        absolute_pos = cursor.pos()
        win_pos = self.geometry()
        centralwidget_pos = self.centralwidget.geometry()
        showspace_pos = self.showspace.geometry()
        scrollarea_pos = self.scrollArea.geometry()
        sawc_pos = self.scrollAreaWidgetContents.geometry()
        pos = QPoint()
        pos.setX(absolute_pos.x()-win_pos.x()-centralwidget_pos.x()-showspace_pos.x()-scrollarea_pos.x()-sawc_pos.x())
        pos.setY(absolute_pos.y()-win_pos.y()-centralwidget_pos.y()-showspace_pos.y()-scrollarea_pos.y()-sawc_pos.y())
        return pos

    def select_err(self):
        if is_login():
            if self.map_ID != '':
                key = self.input_select.text()
                opr = {"operation": "select error", "user": self.user, "key": key, "OID": self.map_ID}
                result = send(opr)
                self.err_list = result['error']
                for label in self.labels:
                    label.setVisible(False)
                self.labels.clear()
                self.selected_error.setVisible(False)
                self.labels = [QLabel(self.sawc_select) for _ in range(len(result['error'])+1)]
                self.labels[0].setGeometry(5, 3, 100, 18)
                self.labels[0].setText('序号  |  位置  |  类型  |  详情')
                self.labels[0].adjustSize()
                self.labels[0].setVisible(True)
                idx = 1
                for error in self.err_list:
                    self.labels[idx].setGeometry(5, 20 * idx + 2, 100, 18)
                    text = str(idx) + '  >>\t' + error['pos'] + '\t' + error['type'] + '\t'
                    for line in error['detail'].split('\n'):
                        text += line
                    self.labels[idx].setText(text)
                    self.labels[idx].adjustSize()
                    self.labels[idx].setVisible(True)
                    idx += 1
                self.label.setText(f'本次共搜索到{idx-1}条结果！')
                self.selected_error.setGeometry(3, 20, 1920, 18)
                self.selected_error.setStyleSheet(
                    'border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')
                if len(self.err_list) >= 1:
                    self.selected_error.setVisible(True)
                self.sawc_select.adjustSize()
            else:
                msg_box = QMessageBox.information(self, '提示', '未打开项目，请先打开项目！\n\t文件-->项目')

    def first_select(self):
        self.selected_error.setGeometry(3, 20, 1920, 18)
        self.selected_error.setStyleSheet(
            'border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')
        self.selected_error.setVisible(True)

    def last_select(self):
        y = self.selected_error.y()
        if y == 20:
            msg_box = QMessageBox.information(self, '提示', '当前已经是第一条！')
        else:
            self.selected_error.setGeometry(3, y - 20, 1920, 18)
            self.selected_error.setStyleSheet(
                'border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')
            self.selected_error.setVisible(True)

    def next_select(self):
        y = self.selected_error.y()
        if y / 20 == len(self.err_list):
            msg_box = QMessageBox.information(self, '提示', '当前已经是最后一条！')
        else:
            self.selected_error.setGeometry(3, y + 20, 1920, 18)
            self.selected_error.setStyleSheet(
                'border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')
            self.selected_error.setVisible(True)

    def end_select(self):
        self.selected_error.setGeometry(3, 20 * len(self.err_list), 1920, 18)
        self.selected_error.setStyleSheet(
            'border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')
        self.selected_error.setVisible(True)

    def edit_err(self):
        if is_login():
            if self.map_ID != '':
                idx = int(self.selected_error.y() / 20 - 1)
                if len(self.err_list) >= 1:
                    self.input_x.setText(self.err_list[idx]['pos'].split(' ')[0])
                    self.input_y.setText(self.err_list[idx]['pos'].split(' ')[1])
                    self.input_type.setText(self.err_list[idx]['type'])
                    self.input_detail.setText(self.err_list[idx]['detail'])
                    self.is_edit_select_err = True
                    self.edit_select_err_ID = self.err_list[idx]['ID']
            else:
                msg_box = QMessageBox.information(self, '提示', '未打开项目，请先打开项目！\n\t文件-->项目')

    def delete_err(self):
        if is_login():
            if self.map_ID != '':
                idx = int(self.selected_error.y() / 20 - 1)
                if len(self.err_list) >= 1:
                    ID = self.err_list[idx]['ID']
                    opr = {"operation": "delete error", "ID": ID, "user": self.user}
                    result = send(opr)
                    if result['result'] == "delete error success":
                        msg_box = QMessageBox.information(self, "提示", "删除成功！")
                        self.select_err()
                    else:
                        msg_box = QMessageBox.information(self, "提示", "删除失败")
            else:
                msg_box = QMessageBox.information(self, '提示', '未打开项目，请先打开项目！\n\t文件-->项目')

    def document(self):
        doc = DocDialog(self)
        doc.setWindowTitle('文档')
        with open("../res/doc.html", "r", encoding="utf-8") as f:
            doc.textBrowser.setText(f.read())
        doc.show()

    def about(self):
        ab = DocDialog(self)
        ab.setWindowTitle('关于')
        # ab.resize(400, 200)
        ab.setFixedSize(330, 160)
        ab.textBrowser.setStyleSheet("border-color:none")
        with open('../res/about.html', 'r', encoding="utf-8") as f:
            ab.textBrowser.setText(f.read())
        # ab.textBrowser.setFontPointSize(100)
        ab.show()


class LoginDialog(QDialog, login.Ui_Dialog):
    def __init__(self,parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.login.clicked.connect(self.login_in)

    def login_in(self):
        opr = {"operation": "login", "ID": self.login_id.text(), "password": self.login_password.text()}
        result = send(opr)
        print(result)
        if result['result'] == 'login in success':
            msg_box = QMessageBox.information(self, '登录', '登陆成功！')
            self.close()
            win.user = self.login_id.text()
            win.current_user.setText("当前用户："+result['name'])
        else:
            self.login_defeated_info.setText('账户名或密码错误！')
            win.current_user.setText("当前用户：尚未登录，请登录！")


class DownLoadDialog(QDialog, download.Ui_Dialog):
    def __init__(self, parent=None):
        super(DownLoadDialog, self).__init__(parent)
        self.setupUi(self)
        self.file_list = win.file_list['file']
        self.load()
        self.open_file_browser.clicked.connect(self.open_file)
        self.first.clicked.connect(self.first_file)
        self.next.clicked.connect(self.next_file)
        self.last.clicked.connect(self.last_file)
        self.end.clicked.connect(self.end_file)
        self.save_file.clicked.connect(self.save)
        self.cancel.clicked.connect(self.give_up)

    def load(self):
        idx = 0
        label = QLabel(self.scrollAreaWidgetContents)
        label.setGeometry(5, 3, 100, 18)
        label.setText('序号  |  文件名  |  文件类型')
        label.adjustSize()
        for file in self.file_list:
            label = QLabel(self.scrollAreaWidgetContents)
            label.setGeometry(5, 20*idx+22, 100, 18)
            label.setText(str(idx+1)+'  >>\t'+file['title']+'\t'+file['type'])
            label.adjustSize()
            idx += 1
        self.selected_label = QLabel(self.scrollAreaWidgetContents)
        self.selected_label.setGeometry(3, 20, 1920, 18)
        self.selected_label.setStyleSheet('border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')

    def open_file(self):
        file_name, file_type = QFileDialog.getSaveFileName(self, "选择文件下载位置",
                                                           f"C:/Users/{os.environ['USERNAME']}/Documents/",
                                                           "Image File(*.png *.jpg *.tif);; Text File(*.txt *.dat *.json *.xml)")
        if file_name != '':
            self.file_path.setText(file_name)

    def first_file(self):
        self.selected_label.setGeometry(3, 20, 1920, 18)
        self.selected_label.setStyleSheet('border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')

    def next_file(self):
        y = self.selected_label.y()
        if y / 20 == len(self.file_list):
            msg_box = QMessageBox.information(self,'提示', '当前已经是最后一条！')
        else:
            self.selected_label.setGeometry(3, y+20, 1920, 18)
            self.selected_label.setStyleSheet('border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')

    def last_file(self):
        y = self.selected_label.y()
        if y == 20:
            msg_box = QMessageBox.information(self, '提示', '当前已经是第一条！')
        else:
            self.selected_label.setGeometry(3, y - 20, 1920, 18)
            self.selected_label.setStyleSheet('border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')

    def end_file(self):
        self.selected_label.setGeometry(3, 20*len(self.file_list), 1920, 18)
        self.selected_label.setStyleSheet('border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')

    def save(self):
        try:
            idx = int(self.selected_label.y()/20-1)
            ID = self.file_list[idx]['ID']
            f_type = self.file_list[idx]['type']
            opr = {'operation': "download file", 'user': win.user, 'ID': ID, 'type': f_type}
            file_path = self.file_path.text()
            file = file_download(opr)
            with open(file_path, 'wb') as f:
                f.write(file)
            msg_box = QMessageBox.information(self, '提示', '下载成功！')
            self.close()
        except:
            msg_box = QMessageBox.information(self, '提示', '下载失败！')
            self.close()

    def give_up(self):
        self.close()


class ProjectDialog(QDialog, project.Ui_Dialog):
    def __init__(self, parent=None):
        super(ProjectDialog, self).__init__(parent)
        self.setupUi(self)
        self.file_list = win.file_list['file']
        self.load()
        self.first.clicked.connect(self.first_file)
        self.next.clicked.connect(self.next_file)
        self.last.clicked.connect(self.last_file)
        self.end.clicked.connect(self.end_file)
        self.save_file.clicked.connect(self.save)
        self.cancel.clicked.connect(self.give_up)

    def load(self):
        idx = 0
        label = QLabel(self.scrollAreaWidgetContents)
        label.setGeometry(5, 3, 100, 18)
        label.setText('序号  |  文件名  |  文件类型')
        label.adjustSize()
        for file in self.file_list:
            label = QLabel(self.scrollAreaWidgetContents)
            label.setGeometry(5, 20*idx+22, 100, 18)
            label.setText(str(idx+1)+'  >>\t'+file['title']+'\t'+file['type'])
            label.adjustSize()
            idx += 1
        self.selected_label = QLabel(self.scrollAreaWidgetContents)
        self.selected_label.setGeometry(3, 20, 1920, 18)
        self.selected_label.setStyleSheet('border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')

    def first_file(self):
        w = self.scrollAreaWidgetContents.width()
        self.selected_label.setGeometry(3, 20, 1920, 18)
        self.selected_label.setStyleSheet('border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')

    def next_file(self):
        y = self.selected_label.y()
        if y / 20 == len(self.file_list):
            msg_box = QMessageBox.information(self,'提示', '当前已经是最后一条！')
        else:
            w = self.scrollAreaWidgetContents.width()
            self.selected_label.setGeometry(3, y+20, 1920, 18)
            self.selected_label.setStyleSheet('border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')

    def last_file(self):
        y = self.selected_label.y()
        if y == 20:
            msg_box = QMessageBox.information(self, '提示', '当前已经是第一条！')
        else:
            w = self.scrollAreaWidgetContents.width()
            self.selected_label.setGeometry(3, y - 20, 1920, 18)
            self.selected_label.setStyleSheet('border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')

    def end_file(self):
        w = self.scrollAreaWidgetContents.width()
        self.selected_label.setGeometry(3, 20*len(self.file_list), 1920, 18)
        self.selected_label.setStyleSheet('border: 1px solid red;background: none;border-top:none;border-left:none;border-right:none;')

    def save(self):
        try:
            idx = int(self.selected_label.y() / 20 - 1)
            win.map_ID = self.file_list[idx]['ID']
            win.map_title = self.file_list[idx]['title']
            win.map_type = self.file_list[idx]['type']
            opr = {'operation': "open project: download", 'user': win.user, 'ID': win.map_ID, 'type': win.map_type}
            file = file_download(opr)
            if win.map_type == 'text':
                win.file = file.decode('utf-8').split('\r\n')
                win.map.setText(file.decode('utf-8'))
                win.label_data.setStyleSheet('background: white')
                win.label_image.setStyleSheet('background: lightgrey')
            else:
                img = QImage.fromData(file, win.map_title.split('.')[-1])
                win.map.setPixmap(QPixmap.fromImage(img))
                win.label_data.setStyleSheet('background: lightgrey')
                win.label_image.setStyleSheet('background: white')
            win.map.adjustSize()
            win.scrollAreaWidgetContents.adjustSize()
            self.close()
        except:
            msg_box = QMessageBox.information(self, '提示', '文件打开失败！')
            self.close()

    def give_up(self):
        self.close()


class DocDialog(QDialog, document.Ui_Dialog):
    def __init__(self, parent=None):
        super(DocDialog, self).__init__(parent)
        self.setupUi(self)


def send(opr: dict):
    s = socket.socket()
    s.connect(('47.98.164.4', 12345))
    print(s.recv(1024).decode('utf-8'))  # connection succeed
    opr = json.dumps(opr).encode('utf-8')
    l_opr = len(opr)
    # 发送一个操作
    s.send(str(l_opr).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))
    s.send(opr)
    data = b''
    # 接收操作结果
    e = s.recv(1024).decode('utf-8')
    num = int(e)
    s.send(b'Confirm')
    e = s.recv(1024)
    while len(data) < num - 1024:
        data += e
        e = s.recv(1024)
    data += e
    data = json.loads(data.decode('utf-8'))
    # 通知服务器关闭连接
    s.send(b'4')
    print(s.recv(1024).decode('utf-8'))
    s.send(b'exit')
    # 关闭连接
    s.close()
    return data


def file_upload(opr: dict, file: bytes):
    s = socket.socket()
    s.connect(('47.98.164.4', 12345))
    print(s.recv(1024).decode('utf-8'))  # connection succeed
    opr = json.dumps(opr).encode('utf-8')
    l_opr = len(opr)
    # 发送一个操作
    s.send(str(l_opr).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))
    s.send(opr)
    # 发送文件内容
    s.send(str(len(file)).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))
    s.send(file)
    # 接收操作结果
    data = b''
    e = s.recv(1024).decode('utf-8')
    num = int(e)
    s.send(b'Confirm')
    e = s.recv(1024)
    while len(data) < num - 1024:
        data += e
        e = s.recv(1024)
    data += e
    data = json.loads(data.decode('utf-8'))
    # 通知服务器关闭连接
    s.send(b'4')
    print(s.recv(1024).decode('utf-8'))
    s.send(b'exit')
    # 关闭连接
    s.close()
    return data


def file_download(opr):
    s = socket.socket()
    s.connect(('47.98.164.4', 12345))
    print(s.recv(1024).decode('utf-8'))  # connection succeed
    opr = json.dumps(opr).encode('utf-8')
    l_opr = len(opr)
    # 发送一个操作
    s.send(str(l_opr).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))
    s.send(opr)
    data = b''
    # 接收操作结果
    e = s.recv(1024).decode('utf-8')
    num = int(e)
    s.send(b'Confirm')
    e = s.recv(1024)
    while len(data) < num - 1024:
        data += e
        e = s.recv(1024)
    data += e
    # data = json.loads(data.decode('utf-8'))
    # 通知服务器关闭连接
    s.send(b'4')
    print(s.recv(1024).decode('utf-8'))
    s.send(b'exit')
    # 关闭连接
    s.close()
    return data


def is_login():
    if win.user == '000000':
        return False
    else:
        opr = {"operation": "is login", "ID": win.user}
        result = send(opr)
        if result['result'] == 'login on':
            return True
        else:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())