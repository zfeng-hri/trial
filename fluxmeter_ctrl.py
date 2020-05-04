'''
Hyperfine Research 2020
Module to control the fluxmeter

Author: Zhiyao Feng
Date: 22 March 2020
'''
import serial

import sys

class FluxmeterController:

    def __init__(self,portNum,baudRate):
        self._port = portNum
        self._baud = baudRate
        self.ser = serial.Serial()

    def openSerialPort(self):
        self.ser.baudrate = self._baud
        self.ser.port = self._port
        self.ser.open()

    def writeMeasure(self):
        print("writing")
        self.ser.write(b'*00:R00#[CR][LF]')

    def setRange(self, fluxRange):
        print("RangeSetting")
        stringRange = "*00:W01={}#[CR][LF]".format(fluxRange)
        self.ser.write(stringRange.encode())

    def readRange(self):
        #print("RangeReading")
        #self.ser.write(b'*00:R01#[CR][LF]')
        #self.readSerialPort()
        data = self.ser.readline()
        RangeInUse = int(data[8:11])
        print(RangeInUse)
        return RangeInUse


    def readSerialPort(self):
        print("reading")
        data = self.ser.readline()
        print(data)
        ReceivedDigit = data[1:6]

        return ReceivedDigit

    # measure 10 times and average the measurements
    def MultiMesurement(self):
        # read from serial port and average time
        dataSum = 0
        averageNum = 1
        for i in range(1, averageNum+1):
            #self.writeMeasure()
            tmp = self.readSerialPort()
            # print(tmp)
            dataSum = int(tmp) + dataSum
            print(int(tmp))
        dataAverage = dataSum / averageNum
        return dataAverage

    def closeSerialPort(self):
       self.ser.close()


def MagnetMomentCalc(dataAverage, MagnetVolume):
    KConstant = 0.00285
    #MagnetVolume = int(input("Enter your magnet volume value: "))
    MagnetMoment = dataAverage * 0.000001 * KConstant / MagnetVolume
    print(MagnetMoment)
    return format(MagnetMoment, '.6g')

'''                                                
x = FluxmeterController('COM5', 9600)
x.openSerialPort()
AverageMeasured = x.MultiMesurement()
print('Average Measurement is', AverageMeasured)
MagnetMomentCalc(AverageMeasured)
x.closeSerialPort()
'''