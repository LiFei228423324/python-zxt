import random
import sys
import typing
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtChart import *
import requests
import json
import time
from threading import Thread
token = ""
tt = ""
temp_value = 0
hum_value = 0

# class window(QWidget,QChart):

#     def __init__(self, parent = None):
#         super(window,self).__init__(parent)
#         self.resize(1000,1000)
#         self.setWindowTitle("Chart")


        #定义LineSerise，将类QLineSeries实例化
        # series_1 = QLineSeries() 
        
        # #定义折线坐标点
        # _1_point_0 = QPointF(0.00,0.00)
        # _1_point_1 = QPointF(1.00,6.00)
        # _1_point_2 = QPointF(2.00,2.00)
        # _1_point_3 = QPointF(3.00,3.00)
        # _1_point_4 = QPointF(4.00,1.00)
        # _1_point_5 = QPointF(5.00,5.00)

        # #定义折线清单
        # _1_point_list = [_1_point_0,_1_point_1,_1_point_2,_1_point_3,_1_point_4,_1_point_5] 
        # #折线添加坐标清单
        # series_1.append(_1_point_list)
        # #折线命名
        # series_1.setName("折线一")


        # #定义x轴，实例化
        # x_Aix= QValueAxis()
        # #设置量程
        # x_Aix.setRange(0.00,5.00)
        # #设置坐标轴坐标显示方式，精确到小数点后两位
        # x_Aix.setLabelFormat("%0.2f")
        # #设置x轴有几个量程
        # x_Aix.setTickCount(6)
        # #设置每个单元格有几个小的分级
        # x_Aix.setMinorTickCount(0)

        # #定义y轴，实例化
        # y_Aix= QValueAxis()
        # #设置量程
        # y_Aix.setRange(0.00,6.00)
        # #设置坐标轴坐标显示方式，精确到小数点后两位
        # y_Aix.setLabelFormat("%0.2f")
        # #设置x轴有几个量程
        # y_Aix.setTickCount(7)
        # #设置每个单元格有几个小的分级
        # y_Aix.setMinorTickCount(0)


        # charview = QChartView(self)
        # charview.setGeometry(0,0,self.width(),self.height())

        # #添加折线
        # charview.chart().addSeries(series_1)
        # #设置x轴属性
        # charview.chart().setAxisX(x_Aix)
        # charview.chart().setAxisY(y_Aix)
        # #使用默认坐标系
        # charview.chart().createDefaultAxes()
        # #设置标题笔刷
        # charview.chart().setTitleBrush(QBrush(Qt.cyan))
        # #设置标题
        # charview.chart().setTitle("Demo")
        
        # charview.show()

        # self.chart_init()
        # self.timer_init()
        
    
class window(QWidget,QChart):

    def __init__(self, parent = None):
        super(window,self).__init__(parent)
        self.resize(1920,1080)
        self.setWindowTitle("CCCCCCCC")
        temp = chartview_temp()
        hum = chartview_hum()
        self.setShortcutAutoRepeat(True)
        layout = QHBoxLayout(self)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        left = QVBoxLayout(self)
        right = QVBoxLayout(self)

        layout.addLayout(left,Qt.AlignCenter)
        layout.addLayout(right,Qt.AlignCenter)

        temp.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        hum.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)

        left.addWidget(temp,1,Qt.AlignTop | Qt.AlignCenter)
        left.addWidget(hum,1,Qt.AlignBottom | Qt.AlignCenter)

        self.setLayout(layout)

        right.addStretch(1)
        
        self.temp = QLabel(self)
        self.temp.setText("温度")
        self.temp.resize(200,100)
        self.temp.move(1200,300)
        self.temp.setAlignment(Qt.AlignCenter)
        self.temp.setFont(QFont("微软雅黑",28))
        right.addWidget(self.temp,1 ,Qt.AlignTop | Qt.AlignCenter)
        
        self.hum = QLabel(self)
        self.hum.setText("湿度")
        # self.hum.resize(200,100)
        self.hum.move(1200,800)   
        self.hum.setAlignment(Qt.AlignCenter)
        self.hum.setFont(QFont("微软雅黑",28))
        right.addWidget(self.hum,1,Qt.AlignBottom | Qt.AlignCenter)
        

        right.addStretch(1)

        self.timer_init()
        

    def up_data(self):
        self.temp.setText("温度\n"+str(temp_value))
        self.hum.setText("湿度\n"+str(hum_value))

    def timer_init(self):
        #使用QTimer，2秒触发一次，更新数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.up_data)
        self.timer.start(1000)

class chartview_temp(QChartView,QChart):
    def __init__(self, *args, **kwargs):
        super(chartview_temp, self).__init__(*args, **kwargs)
        self.resize(800, 700)
        self.move(0,0)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.chart_init()
        self.timer_init()


    def timer_init(self):
        #使用QTimer，2秒触发一次，更新数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.drawLine)
        self.timer.start(2000)
    def chart_init(self):

        # QSplineSeries 曲线   QLineSeries 直线

        self.chart = QChart()
        self.series = QLineSeries()
        #设置曲线名称
        self.series.setName("温度")
        #把曲线添加到QChart的实例中
        self.chart.addSeries(self.series)
        #声明并初始化X轴，Y轴
        self.dtaxisX = QDateTimeAxis()
        self.vlaxisY = QValueAxis()
        #设置坐标轴显示范围
        self.dtaxisX.setMin(QDateTime.currentDateTime().addSecs(-10*1))
        self.dtaxisX.setMax(QDateTime.currentDateTime().addSecs(0))
        self.vlaxisY.setMin(-40)
        self.vlaxisY.setMax(60)
        #设置X轴时间样式
        self.dtaxisX.setFormat("hh:mm:ss")
        #设置坐标轴上的格点
        self.dtaxisX.setTickCount(6)
        self.vlaxisY.setTickCount(8)
        #设置坐标轴名称
        # self.dtaxisX.setTitleText("time")
        # self.vlaxisY.setTitleText("value")
        #设置网格不显示
        self.vlaxisY.setGridLineVisible(False)
        #把坐标轴添加到chart中
        self.chart.addAxis(self.dtaxisX,Qt.AlignBottom)
        self.chart.addAxis(self.vlaxisY,Qt.AlignLeft)
        #把曲线关联到坐标轴
        self.series.attachAxis(self.dtaxisX)
        self.series.attachAxis(self.vlaxisY)

        self.setChart(self.chart) 

    def drawLine(self):
        #获取当前时间
        bjtime = QDateTime.currentDateTime()
        #更新X轴坐标
        self.dtaxisX.setMin(QDateTime.currentDateTime().addSecs(-10*1))
        self.dtaxisX.setMax(QDateTime.currentDateTime().addSecs(0))
        #当曲线上的点超出X轴的范围时，移除最早的点
        if(self.series.count()>5):
            self.series.removePoints(0,self.series.count()-5)
        #产生随即数
        #添加数据到曲线末端
        self.series.append(bjtime.toMSecsSinceEpoch(),temp_value)


class chartview_hum(QChartView,QChart):
    def __init__(self, *args, **kwargs):
        super(chartview_hum, self).__init__(*args, **kwargs)
        self.resize(800, 700)
        self.move(0,0)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.chart_init()
        self.timer_init()


    def timer_init(self):
        #使用QTimer，2秒触发一次，更新数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.drawLine)
        self.timer.start(2000)
    def chart_init(self):

        # QSplineSeries 曲线   QLineSeries 直线

        self.chart = QChart()
        self.series = QLineSeries()
        #设置曲线名称
        self.series.setName("湿度")
        #把曲线添加到QChart的实例中
        self.chart.addSeries(self.series)
        #声明并初始化X轴，Y轴
        self.dtaxisX = QDateTimeAxis()
        self.vlaxisY = QValueAxis()
        #设置坐标轴显示范围
        self.dtaxisX.setMin(QDateTime.currentDateTime().addSecs(-10*1))
        self.dtaxisX.setMax(QDateTime.currentDateTime().addSecs(0))
        self.vlaxisY.setMin(0)
        self.vlaxisY.setMax(100)
        #设置X轴时间样式
        self.dtaxisX.setFormat("hh:mm:ss")
        #设置坐标轴上的格点
        self.dtaxisX.setTickCount(6)
        self.vlaxisY.setTickCount(8)
        #设置坐标轴名称
        # self.dtaxisX.setTitleText("time")
        # self.vlaxisY.setTitleText("value")
        #设置网格不显示
        self.vlaxisY.setGridLineVisible(False)
        #把坐标轴添加到chart中
        self.chart.addAxis(self.dtaxisX,Qt.AlignBottom)
        self.chart.addAxis(self.vlaxisY,Qt.AlignLeft)
        #把曲线关联到坐标轴
        self.series.attachAxis(self.dtaxisX)
        self.series.attachAxis(self.vlaxisY)

        self.setChart(self.chart)

    def drawLine(self):
        #获取当前时间
        bjtime = QDateTime.currentDateTime()
        #更新X轴坐标
        self.dtaxisX.setMin(QDateTime.currentDateTime().addSecs(-10*1))
        self.dtaxisX.setMax(QDateTime.currentDateTime().addSecs(0))
        #当曲线上的点超出X轴的范围时，移除最早的点
        if(self.series.count()>5):
            self.series.removePoints(0,self.series.count()-5)
        #产生随即数
        #添加数 据到曲线末端
        self.series.append(bjtime.toMSecsSinceEpoch(),hum_value)
        

def login(name,password):                   
    params = {"Account":name,
             "Password":password,
             "IsRememberMe":True}
    response = requests.post(url='http://api.nlecloud.com/Users/Login',data=params)
    if response.status_code==200: 
        # print(response.json())
        data = json.loads(response.text)
        return data['ResultObj']['AccessToken']
    else: return ""

def get_sensor():
    while True:
        global temp_value,hum_value,tt
        data = {"AccessToken":token}
        header = {"Content-Type":"Application/json"}
        response = requests.get( url='http://api.nlecloud.com/Devices/Datas?devIds=716756'
                           ,params=data ,headers=header)
        
        if response.status_code == 200:
            d = json.loads(response.text)
            a = ["0","0","0"]
            for i in range(4): 
                if d['ResultObj'][0]['Datas'][i]['ApiTag'] == 'temp':
                    a[0] = d['ResultObj'][0]['Datas'][i]['Value']
                    temp_value = a[0]
                elif d['ResultObj'][0]['Datas'][i]['ApiTag'] == 'hum':
                    a[1] = d['ResultObj'][0]['Datas'][i]['Value']
                    hum_value = a[1]
                elif d['ResultObj'][0]['Datas'][i]['ApiTag'] == 'light':
                    a[2] = d['ResultObj'][0]['Datas'][i]['Value']
                tt = d['ResultObj'][0]['Datas'][0]['RecordTime']
            print(a)
            print(tt)
        time.sleep(3)
 


def main():
    global token
    token = login("17691115647","hf200080")
    
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    view = window()
    view.show()
    
    Thread(target=get_sensor).start()
    sys.exit(app.exec_())
                                                                             



if __name__ == '__main__':
    main() 

    input("please input any key to exit!")