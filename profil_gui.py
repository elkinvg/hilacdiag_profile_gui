from PyQt4 import QtGui, QtCore
import PyTango

from datetime import datetime

from taurus.qt.qtgui.plot import TaurusPlot
from taurus.qt.qtgui.input import TaurusValueComboBox

tango_test = PyTango.DeviceProxy("tango://nuclotango.jinr.ru:10000/training/hilacdiag/1")

def test():
    status = tango_test.status()
    state = tango_test.state()
    readTangoDataTest()
    print status
    print state

class Ui_MainWindow(QtGui.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.resize(879, 563)
        self.centralwidget = QtGui.QWidget(MainWindow)

        self.widgets(MainWindow)

        MainWindow.setCentralWidget(self.centralwidget)
        self.layouts(MainWindow)
        self.readTangoData()
        self.signals()

    def widgets(self,MainWindow):
        #3
        self.xPlot = TaurusPlot(self.centralwidget)
        # self.xPlot.setGeometry(QtCore.QRect(30, 100, 300, 200))

        #4
        self.yPlot = TaurusPlot(self.centralwidget)
        # self.yPlot.setGeometry(QtCore.QRect(520, 100, 300, 200))

        #1
        self.xLabel = QtGui.QLabel()
        self.xLabel.setText("X")
        #2
        self.yLabel = QtGui.QLabel()
        self.yLabel.setText("Y")
        #5
        self.baseXLabel = QtGui.QLabel()
        self.baseXLabel.setText("Baseline X")
        #6
        self.baseYLabel = QtGui.QLabel()
        self.baseYLabel.setText("Baseline Y")
        #7
        self.baseXLineEdit = QtGui.QLineEdit()
        self.baseXLineEdit.setReadOnly(True)
        #8
        self.baseYLineEdit = QtGui.QLineEdit()
        self.baseYLineEdit.setReadOnly(True)
        #9
        self.timeStampLabel = QtGui.QLabel()
        self.timeStampLabel.setText("time")
        #10
        self.timeStampLineEdit = QtGui.QLineEdit()
        self.timeStampLineEdit.setReadOnly(True)
        #11
        self.rangeAILabel = QtGui.QLabel()
        self.rangeAILabel.setText("range:")
        #12
        # self.rangeAICommand = QtGui.QLineEdit()
        # self.rangeAICommand = TaurusValueComboBox()
        self.rangeAICommand = QtGui.QComboBox()
        namesItems = ['Range 0.1','Range 0.2','Range 0.5','Range 1','Range 2','Range 5','Range 10']
        self.rangeAICommand.addItems(namesItems)
        # self.rangeAICommand.addValueNames(names)
        #13
        self.valueEdit = QtGui.QTextEdit()
        self.valueEdit.setReadOnly(True)

    def layouts(self, MainWindow):
        mainLayout = QtGui.QGridLayout()
        mainLayout.setSpacing(30)

        layout1 = QtGui.QHBoxLayout()
        layout1.addWidget(self.baseXLabel)
        layout1.addWidget(self.baseXLineEdit)

        layout2 = QtGui.QHBoxLayout()
        layout2.addWidget(self.baseYLabel)
        layout2.addWidget(self.baseYLineEdit)

        layout3 = QtGui.QHBoxLayout()
        layout3.addWidget(self.timeStampLabel)
        layout3.addWidget(self.timeStampLineEdit)

        layout4 = QtGui.QHBoxLayout()
        layout4.addWidget(self.rangeAILabel)
        layout4.addWidget(self.rangeAICommand)

        # mainLayout.addWidget(self.xPlot,1,0,1,2)
        # mainLayout.addWidget(self.yPlot,1,2,1,2)
        mainLayout.addWidget(self.xLabel,0,0)
        mainLayout.addWidget(self.yLabel,0,2)
        mainLayout.addWidget(self.xPlot,1,0)
        mainLayout.addWidget(self.yPlot,1,2)
        mainLayout.addLayout(layout1,2,0)
        mainLayout.addLayout(layout2,2,2)
        mainLayout.addLayout(layout3,3,0)
        mainLayout.addLayout(layout4,3,2)
        mainLayout.addWidget(self.valueEdit,1,1)

        centralWidget = MainWindow.centralWidget()
        centralWidget.setLayout(mainLayout)

    def commandRange(self,it):
        commands = ['SetAIRange0_1','SetAIRange0_2','SetAIRange0_5',
                    'SetAIRange1','SetAIRange2','SetAIRange5','SetAIRange10']
        command = commands[it]
        self.chTangoData()
        print(command)


    def signals(self):
        self.connect(self.rangeAICommand,QtCore.SIGNAL("activated(int)"),self.commandRange)

    def readTangoData(self):
        self.chTangoData()
        self.setBeginAIRange()

    def chTangoData(self):
        baselineX = tango_test.read_attribute("baselineX")
        baselineY = tango_test.read_attribute("baselineY")
        timestamp = tango_test.read_attribute("PR_Timestamp")
        dt = datetime.fromtimestamp(timestamp.value).strftime('%d-%m-%Y %H:%M:%S')
        self.baseXLineEdit.setText(str(baselineX.value))
        self.baseYLineEdit.setText(str(baselineY.value))
        self.timeStampLineEdit.setText(dt)

        prX0 = tango_test.read_attribute("prX0")
        prX0val = prX0.value
        prY0 = tango_test.read_attribute("prY0")
        prY0val = prY0.value
        prWX = tango_test.read_attribute("prWX")
        prWXval = prWX.value
        prWY = tango_test.read_attribute("prWY")
        prWYval = prWY.value

        self.valueEdit.clear()
        self.valueEdit.append("X0 = " + str(prX0val[0]))
        self.valueEdit.append("")
        self.valueEdit.append("Y0 = " + str(prY0val[0]))
        self.valueEdit.append("")
        self.valueEdit.append("Wx = " + str(prWXval[0]))
        self.valueEdit.append("")
        self.valueEdit.append("Wy = " + str(prWYval[0]))
        self.valueEdit.append("")

    def setBeginAIRange(self):
        airange = tango_test.read_attribute("AI_Range")
        if airange.value == 10.0:
            self.rangeAICommand.setCurrentIndex(6)
        if airange.value == 5.0:
            self.rangeAICommand.setCurrentIndex(5)
        if airange.value == 2.0:
            self.rangeAICommand.setCurrentIndex(4)
        if airange.value == 1.0:
            self.rangeAICommand.setCurrentIndex(3)
        if airange.value == 0.5:
            self.rangeAICommand.setCurrentIndex(2)
        if airange.value == 0.2:
            self.rangeAICommand.setCurrentIndex(1)
        if airange.value == 0.1:
            self.rangeAICommand.setCurrentIndex(0)

def testing(test):
    print str(test)
    print("sdsd")


def readTangoDataTest():
    baselineX = tango_test.read_attribute("baselineX")
    baselineY = tango_test.read_attribute("baselineY")
    timestamp = tango_test.read_attribute("PR_Timestamp")
    print("basX = " + str(baselineX.value))
    print("basY = " + str(baselineY.value))
    # print(timestamp.value)
    dt = datetime.fromtimestamp(timestamp.value).strftime('%d-%m-%Y %H:%M:%S')
    print(dt)

    airange = tango_test.read_attribute("AI_Range")
    # print(airange.value)
    if airange.value == 10.0:
        print('10.0')
    if airange.value == 5.0:
        print('5.0')
    if airange.value == 2.0:
        print('2.0')
    if airange.value == 1.0:
        print('1.0')
    if airange.value == 0.5:
        print('0.5')
    if airange.value == 0.2:
        print('0.2')
    if airange.value == 0.1:
        print('0.1')

    prX0 = tango_test.read_attribute("prX0")
    prX0val = prX0.value
    print("prX0 = " + str(prX0val[0]))

if __name__ == "__main__":
    import sys
    try:
        test()
    except PyTango.DevFailed as exc:
        print exc
        print "except"
        # print exc
        exit()
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    # app = QtGui.QApplication(sys.argv)
    # MainWindow = QtGui.QMainWindow()
    # MainWindow.show()
    # sys.exit(app.exec_())