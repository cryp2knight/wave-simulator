# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from PyQt5 import QtGui

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random

import sys
from PyQt5.QtCore import QTimer





class Wave:
  def __init__(self, amplitude, wavelength, frequency, phase):
    self.wavelength = wavelength
    self.amplitude = amplitude
    self.frequency = frequency
    self.phase = phase


class AddWave(QDialog):
    def __init__(self, *args, **kwargs):
        QDialog.__init__(self)
        loadUi("newWave.ui",self)
        self.label = self.labelName.text()
        self.labelName.textChanged.connect(self.lbln)
        self.amplitude.valueChanged.connect(self.ampl)
        self.wavelength.valueChanged.connect(self.wavl)
        self.frequency.valueChanged.connect(self.freq)
        self.phase.valueChanged.connect(self.phas)
        amp = self.amplitude.value()
        wav = self.wavelength.value()
        fre = self.frequency.value()
        pha = self.phase.value()
        self.wave = Wave(amp, wav, fre, pha)

    def ampl(self):
        self.wave.amplitude = self.amplitude.value()
    def wavl(self):
        self.wave.wavelength = self.wavelength.value()
    def freq(self):
        self.wave.frequency = self.frequency.value()
    def phas(self):
        self.wave.phase = self.phase.value()
    def lbln(self):
        self.label = self.labelName.text()


class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("waves.ui",self)

        self.setWindowTitle("Waves Simulator")
        self.lines = []
        self.waves_index = None
        #self.pushButton_generate_random_signal.clicked.connect(self.update_graph)
        self.newwave.clicked.connect(self.insertWave)
        self.removewave.clicked.connect(self.remove)
        #self.listWidget.clicked.connect(self.setSelectedItems)
        self.dsAmplitude.valueChanged.connect(self.dsAmplitude_valueChanged)
        self.dsWavelength.valueChanged.connect(self.dsWavelength_valueChanged)
        self.dsFrequency.valueChanged.connect(self.dsFrequency_valueChanged)
        self.dsPhase.valueChanged.connect(self.dsPhase_valueChanged)
        self.dsLabel.textChanged.connect(self.dsLabel_textChanged)
        self.playButton.clicked.connect(self.play)
        self.playAll.clicked.connect(self.playall)
        self.timer = QTimer()
        self.timer1 = QTimer()

        self.listWidget.itemPressed.connect(self.itemSelected)
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    def play(self):
        if self.playButton.text() == "Play":
            self.timer.timeout.connect(self.tick)
            self.timer.start(100)
            self.playButton.setText("Stop")
            self.playAll.setEnabled(False)
        else:
            self.timer.stop()
            self.playButton.setText("Play")
            self.playAll.setEnabled(True)

    def playall(self):
        if self.playAll.text() == "Play All":
            self.timer1.timeout.connect(self.all)
            self.timer1.start(100)
            self.playAll.setText("Stop All")
            self.playButton.setEnabled(False)
        else:
            self.timer1.stop()
            self.playAll.setText("Play All")
            self.playButton.setEnabled(True)

    def all(self):
        for i in self.lines:
            i["phase"] += .5
        self.update_graph()



    def tick(self):
        self.lines[self.waves_index]["phase"] += .5
        self.update_graph()


    def remove(self):
        self.listWidget.takeItem(self.listWidget.currentRow())
        self.lines.pop(self.waves_index)
        self.update_graph()
        self.update_graph()

    def dsAmplitude_valueChanged(self):
        self.lines[self.waves_index]["amplitude"] = self.dsAmplitude.value()
        self.update_graph()

    def dsWavelength_valueChanged(self):
        self.lines[self.waves_index]["wavelength"] = self.dsWavelength.value()
        self.update_graph()

    def dsFrequency_valueChanged(self):
        self.lines[self.waves_index]["frequency"] = self.dsFrequency.value()
        self.update_graph()

    def dsPhase_valueChanged(self):
        self.lines[self.waves_index]["phase"] = self.dsPhase.value()
        self.update_graph()

    def dsLabel_textChanged(self):

        self.lines[self.waves_index]["label"] = self.dsLabel.text()
        self.update_graph()


    def itemSelected(self):
        self.waves_index = self.listWidget.currentRow()
        temp = self.lines[self.waves_index]
        self.dsAmplitude.setValue(temp["amplitude"])
        self.dsWavelength.setValue(temp["wavelength"])
        self.dsFrequency.setValue(temp["frequency"])
        self.dsPhase.setValue(temp["phase"])
        self.dsLabel.setText(temp["label"])

        self.dsAmplitude.setEnabled(True)
        self.dsLabel.setEnabled(True)
        self.dsPhase.setEnabled(True)
        self.dsFrequency.setEnabled(True)
        self.dsWavelength.setEnabled(True)
        self.playAll.setEnabled(True)
        self.playButton.setEnabled(True)
        self.removewave.setEnabled(True)

    def insertWave(self):
        dlg = AddWave(self)
        dlg.setWindowTitle("Add New Wave")
        if dlg.exec_():
            if dlg.label == "":
                dlg.label = "wave"
            vals = {
                "amplitude":dlg.wave.amplitude,
                "wavelength":dlg.wave.wavelength,
                "frequency":dlg.wave.frequency,
                "phase":dlg.wave.phase,
                "label": dlg.label
            }
            self.lines.append(vals)
            print(self.lines)
            item = QListWidgetItem(dlg.label)
            self.listWidget.addItem(item)
            self.update_graph()
        else:
            print("Cancel")

    def update_graph(self):
        labels = []
        for line in self.lines:
            x = np.linspace(0, 100, 1000)
            i = 1
            y = line["amplitude"]*np.cos(2 * np.pi * (x/line["wavelength"] - line["frequency"] * i)+line["phase"])
            self.MplWidget.canvas.axes.plot(x, y)
            labels.append(line["label"])
            self.MplWidget.canvas.axes.legend(tuple(labels),loc='upper right')
            self.MplWidget.canvas.draw()

        self.MplWidget.canvas.axes.clear()
        if len(labels) == 0:
            self.removewave.setEnabled(False)
            self.dsAmplitude.setEnabled(False)
            self.dsLabel.setEnabled(False)
            self.dsPhase.setEnabled(False)
            self.dsFrequency.setEnabled(False)
            self.dsWavelength.setEnabled(False)
            self.playAll.setEnabled(False)
            self.playButton.setEnabled(False)
            self.MplWidget.canvas.draw()
        labels.clear()


        

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()






