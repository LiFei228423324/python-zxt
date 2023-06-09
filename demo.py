import sys
import serial
import socket
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from paho.mqtt import client as mqtt_client
class thing:
    def textChanged(self):
        print("文本发生了改变")
    def Changed(self):
        print("选中文本发生改变")
        
    def Pressed(self):
        print("Enter")
    
    def click(self):
        print("down")


        

class dialog:
    def showdialog(self):
        print("up")
        global dlg
        dlg = QDialog()
        dlg.setWindowTitle("Dialog")
        b = QPushButton("ok",dlg)
        b.move(50,20)
        b.clicked.connect(self.bb)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()

    def bb(self):
        print("dialog关闭")
        dlg.close()


class window(QWidget):

    def __init__(self,parent = None):
        super(window,self).__init__(parent) 
        self.resize(1000,1000)
        self.setWindowTitle("PyQt5")


        # ser = serial.Serial("COM1",9600)
        # ser.write("ABCFDE".encode('utf-8'))
        # ser.close()

        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_addr = ("121.37.241.174",8600)
        client.connect(server_addr)
        client.send("sss".encode("gbk"))

        my_thing = thing()

        label = QLabel(self)
        label.setText('Hello World!')
        label.move(20,30)
        
        pix = QPixmap('github.jpg')
        img = QLabel(self)
        img.setGeometry(20,60,100,100)
        img.setPixmap(pix)
        img.setScaledContents(True)

        edit = QLineEdit(self)
        edit.resize(100,30)
        edit.move(20,170)
        edit.setEchoMode(QLineEdit.EchoMode.Normal)
        edit.setMaxLength(6)
        edit.setReadOnly(False)
        edit.setValidator(QIntValidator())
        # my_thing.Changed()
        edit.returnPressed.connect(lambda:my_thing.Changed())
        edit.textChanged.connect(lambda:my_thing.textChanged())
        
        

        btn = QPushButton('打开dialog',self)
        btn.resize(100,30)
        btn.move(20,200)
        btn.setCheckable(True)


        
        # btn.setAutoRepeat(True)
        # btn.setAutoRepeatDelay(50)
        # btn.setAutoRepeatInterval(400)

        btn.pressed.connect(lambda:my_thing.click())
        btn.released.connect(lambda:dialog().showdialog())


        radiobtn1 = QRadioButton("Radio1",self)
        radiobtn1.move(20,230)
        radiobtn1.toggled.connect(lambda:self.radio(radiobtn1))

        radiobtn2 = QRadioButton("Radio2",self)
        radiobtn2.move(80,230)
        radiobtn2.toggled.connect(lambda:self.radio(radiobtn2))


        checkbox1 = QCheckBox("Checkbox1",self)
        checkbox1.move(20,250)
        # checkbox1.stateChanged.connect(lambda:self.check(checkbox1))

        checkbox2 = QCheckBox("Checkbox2",self)
        checkbox2.move(100,250)
        # checkbox2.toggled.connect(lambda:self.check(checkbox2))
        
        
        cg = QButtonGroup(self)
        cg.addButton(checkbox1,1)
        cg.addButton(checkbox2,2)

        cg.buttonClicked[QAbstractButton].connect(self.btngroup)


        self.combo = QComboBox(self)
        self.combo.resize(150,30)
        self.combo.move(20,280)
        self.combo.addItems(["Android","Java","Python","C#","JavaScript","C++"])
        self.combo.currentIndexChanged.connect(self.cur)


        list = QListWidget(self)
        list.resize(400,200)
        list.move(0,310)

        item = QListWidgetItem(QIcon('github.jpg'),'new project')
        list.setIconSize(QSize(50,50))
        list.addItem(QListWidgetItem(QIcon('github.jpg'),'new project'))
        list.addItem(QListWidgetItem(QIcon('github.jpg'),'new project'))
        list.addItem(QListWidgetItem(QIcon('github.jpg'),'new project'))
        list.addItem(QListWidgetItem(QIcon('github.jpg'),'new project'))
    

    def cur(self,i):
        # print("Item in the list are")
        # for count in range(self.combo.count()):
        #     print(self.combo.itemText(count))
        print("Current Index",i,"selection changed ",self.combo.currentText())

    def btngroup(self,btn):
        print(btn.text()+" is selected")
        
    def radio(self,r):
        if r.text() == "Radio1":
            if r.isChecked() == True:
                print(r.text()+" is_selected")
            else: print(r.text()+" is_deselected")
        if r.text() == "Radio2":
            if r.isChecked() == True:
                print(r.text()+" is_selected")
            else: print(r.text()+" is_deselected")

    def check(self,r):
        if r.text() == "Checkbox1":
            if r.isChecked() == True:
                print(r.text()+" is_selected")
            else: print(r.text()+" is_deselected")
        if r.text() == "Checkbox2":
            if r.isChecked() == True:
                print(r.text()+" is_selected")
            else: print(r.text()+" is_deselected")


        

       

def main():
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ex = window()
    ex.show()
    sys.exit(app.exec_())
    
    


if __name__ == '__main__':
    main()
    

    
