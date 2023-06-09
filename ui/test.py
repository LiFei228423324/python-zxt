import sys
import random
from Ui_untitled import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *
from PyQt5.QtMultimediaWidgets import *
import openpyxl

temp = 0
hum = 0
 
temp_i = 0
hum_i = 0
temp_data = [[],[]]
hum_data = [[],[]]

def savetoexcel(data,wbname):   
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for i in range(len(data)):
        for j in range(len(data[i])):
            sheet.cell(i+1,j+1).value = data[i][j]

    workbook.save(wbname)

class window(QMainWindow,Ui_MainWindow):
    def __init__(self,app):
        super(QMainWindow,self).__init__()
        self.app = app
        self.setup_ui()


        # btn = QPushButton(self)
        # btn.setGeometry(0,0,120,120)
        # btn.setStyleSheet("QPushButton{background-color:#00DD00}")
        # btn.setStyleSheet("QPushButton:pressed{background-color:#00FFDD}")
        # btn.pressed.connect(self.down)
        # btn.released.connect(self.up)

        self.temp_btn.clicked.connect(self.temp_excel)
        self.hum_btn.clicked.connect(self.hum_excel)


    def temp_excel(self):
        savetoexcel(temp_data,'温度历史数据.xlsx')
    def hum_excel(self):
        savetoexcel(hum_data,'湿度历史数据.xlsx')

    def setup_ui(self):
        self.setupUi(self)

        self.plot_temp = QChartView_Temp()
        self.temp_view.setChart(self.plot_temp)
        self.temp_view.setRenderHint(QPainter.Antialiasing)

        self.plot_hum = QChartView_Hum()
        self.hum_view.setChart(self.plot_hum)
        self.hum_view.setRenderHint(QPainter.Antialiasing)


        QVideoWidget()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_data)
        self.timer.start(2000)

    def get_data(self):
        global temp,hum
        
        temp = random.randint(-40,60)
        self.temp.setText(str(temp)+"℃")

        hum = random.randint(0,100)
        self.hum.setText(str(hum)+"%") 


class QChartView_Temp(QChart):
    def __init__(self,parent=None):
        super(QChartView_Temp,self).__init__()
        self. window = parent
        
        self.legend().hide()
        self.setTheme(QChart.ChartTheme.ChartThemeHighContrast)

        self.axisX = QDateTimeAxis()
        self.axisX.setRange(QDateTime.currentDateTime().addSecs(-10*1),QDateTime.currentDateTime().addSecs(0))
        self.axisX.setFormat("hh:mm:ss")
        self.axisX.setTickCount(6)
        self.addAxis(self.axisX,Qt.AlignBottom)
        
        
        self.axisY = QValueAxis()
        self.axisY.setRange(-40,60)
        self.axisY.setGridLineVisible(False)
        self.addAxis(self.axisY,Qt.AlignLeft)

        self.series = QSplineSeries()        # QLineSeries 折线  #QSplineSeries 曲线
        # self.series.setUseOpenGL(True)     #抗锯齿
        self.addSeries(self.series)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)

        self.set_font(10)
        
        self.timer_init()
    
    def set_font(self,font):
        self.labelsFont = QFont()
        self.labelsFont.setPixelSize(font)
        self.axisX.setLabelsFont(self.labelsFont)
        self.axisY.setLabelsFont(self.labelsFont)
        
        

    def timer_init(self):
        #使用QTimer，2秒触发一次，更新数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handle_update)
        self.timer.start(2000)

    def handle_update(self):
        global temp_i
        bjtime = QDateTime.currentDateTime()

        self.axisX.setMin(bjtime.addSecs(-10*1))
        self.axisX.setMax(bjtime.currentDateTime().addSecs(0))

        if(self.series.count()>5):
            self.series.removePoints(0,self.series.count()-5)
        self.series.append(bjtime.toMSecsSinceEpoch(),temp)
        if temp_i==0:
            temp_i+=1
            temp_data.insert(0,['时间','Value'])
        else:
            temp_data.insert(temp_i,[bjtime.toString("hh:mm:ss"),temp])
            temp_i+=1

class QChartView_Hum(QChart):
    def __init__(self,parent=None):
        super(QChartView_Hum,self).__init__()
        self. window = parent
        
        self.legend().hide()
        self.setTheme(QChart.ChartTheme.ChartThemeHighContrast)

        self.axisX = QDateTimeAxis() 
        self.axisX.setRange(QDateTime.currentDateTime().addSecs(-10*1),QDateTime.currentDateTime().addSecs(0))
        self.axisX.setFormat("hh:mm:ss")
        self.axisX.setTickCount(6)
        self.addAxis(self.axisX,Qt.AlignBottom)
        
        
        self.axisY = QValueAxis()
        self.axisY.setRange(0,100)
        self.axisY.setGridLineVisible(False)
        self.addAxis(self.axisY,Qt.AlignLeft)

        self.series = QSplineSeries()
        # self.series.setName("Temperature")
        self.series.setUseOpenGL(True)
        self.addSeries(self.series)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)

        self.set_font(10)
        
        self.timer_init()
    
    def set_font(self,font):
        self.labelsFont = QFont()
        self.labelsFont.setPixelSize(font)
        self.axisX.setLabelsFont(self.labelsFont)
        self.axisY.setLabelsFont(self.labelsFont)
        
        

    def timer_init(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handle_update)
        self.timer.start(2000)

    def handle_update(self):
        global hum_i
        bjtime = QDateTime.currentDateTime()
            
        self.axisX.setMin(bjtime.addSecs(-10*1))
        self.axisX.setMax(bjtime.addSecs(0))

        if(self.series.count()>5):
            self.series.removePoints(0,self.series.count()-5)
        self.series.append(bjtime.toMSecsSinceEpoch(),hum)

        if hum_i==0:
            hum_i+=1
            hum_data.insert(0,['时间','Value'])
        else:
            
            hum_data.insert(hum_i,[bjtime.toString("hh:mm:ssdwfsdaduo"),hum])

            hum_i+=1

def main():
    app = QApplication(sys.argv)
    view = window(app)
    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
