# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 320)
        Dialog.setMinimumSize(QtCore.QSize(600, 320))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 150))
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 600, 200))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(600, 200))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.widget_3 = QtWidgets.QWidget(Dialog)
        self.widget_3.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.first = QtWidgets.QPushButton(self.widget_3)
        self.first.setMaximumSize(QtCore.QSize(41, 16777215))
        self.first.setObjectName("first")
        self.gridLayout_4.addWidget(self.first, 0, 0, 1, 1)
        self.last = QtWidgets.QPushButton(self.widget_3)
        self.last.setMaximumSize(QtCore.QSize(51, 16777215))
        self.last.setObjectName("last")
        self.gridLayout_4.addWidget(self.last, 0, 1, 1, 1)
        self.next = QtWidgets.QPushButton(self.widget_3)
        self.next.setMaximumSize(QtCore.QSize(51, 16777215))
        self.next.setObjectName("next")
        self.gridLayout_4.addWidget(self.next, 0, 2, 1, 1)
        self.end = QtWidgets.QPushButton(self.widget_3)
        self.end.setMaximumSize(QtCore.QSize(41, 16777215))
        self.end.setObjectName("end")
        self.gridLayout_4.addWidget(self.end, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.widget_3, 1, 0, 1, 1)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setMinimumSize(QtCore.QSize(0, 40))
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setVerticalSpacing(3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.file_path = QtWidgets.QLineEdit(self.widget)
        self.file_path.setMinimumSize(QtCore.QSize(0, 30))
        self.file_path.setObjectName("file_path")
        self.gridLayout_3.addWidget(self.file_path, 0, 1, 1, 1)
        self.open_file_browser = QtWidgets.QPushButton(self.widget)
        self.open_file_browser.setMinimumSize(QtCore.QSize(0, 30))
        self.open_file_browser.setMaximumSize(QtCore.QSize(60, 16777215))
        self.open_file_browser.setObjectName("open_file_browser")
        self.gridLayout_3.addWidget(self.open_file_browser, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.widget, 2, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(Dialog)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.save_file = QtWidgets.QPushButton(self.widget_2)
        self.save_file.setMaximumSize(QtCore.QSize(60, 16777215))
        self.save_file.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.save_file.setObjectName("save_file")
        self.gridLayout_2.addWidget(self.save_file, 0, 1, 1, 1)
        self.cancel = QtWidgets.QPushButton(self.widget_2)
        self.cancel.setMaximumSize(QtCore.QSize(60, 16777215))
        self.cancel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cancel.setObjectName("cancel")
        self.gridLayout_2.addWidget(self.cancel, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.widget_2, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "下载文件"))
        self.first.setText(_translate("Dialog", "首条"))
        self.last.setText(_translate("Dialog", "上一条"))
        self.next.setText(_translate("Dialog", "下一条"))
        self.end.setText(_translate("Dialog", "尾条"))
        self.label.setText(_translate("Dialog", "保存文件至："))
        self.open_file_browser.setText(_translate("Dialog", "浏览"))
        self.save_file.setText(_translate("Dialog", "确认"))
        self.cancel.setText(_translate("Dialog", "取消"))