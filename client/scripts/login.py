# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(342, 192)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(342, 192))
        Dialog.setMaximumSize(QtCore.QSize(342, 192))
        Dialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Dialog.setModal(False)
        self.login_password = QtWidgets.QLineEdit(Dialog)
        self.login_password.setGeometry(QtCore.QRect(120, 80, 180, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.login_password.setFont(font)
        self.login_password.setText("")
        self.login_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_password.setObjectName("login_password")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 88, 54, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 38, 54, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.login_id = QtWidgets.QLineEdit(Dialog)
        self.login_id.setGeometry(QtCore.QRect(120, 30, 180, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.login_id.setFont(font)
        self.login_id.setText("")
        self.login_id.setObjectName("login_id")
        self.login = QtWidgets.QPushButton(Dialog)
        self.login.setGeometry(QtCore.QRect(130, 134, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.login.setFont(font)
        self.login.setObjectName("login")
        self.login_defeated_info = QtWidgets.QLabel(Dialog)
        self.login_defeated_info.setGeometry(QtCore.QRect(120, 110, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.login_defeated_info.setFont(font)
        self.login_defeated_info.setStyleSheet("#login_defeated_info{color:rgb(255, 0, 0)}")
        self.login_defeated_info.setText("")
        self.login_defeated_info.setObjectName("login_defeated_info")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "登录"))
        self.label.setText(_translate("Dialog", "密码："))
        self.label_2.setText(_translate("Dialog", "账号："))
        self.login.setText(_translate("Dialog", "登录"))
