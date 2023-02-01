import sys
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QButtonGroup, QTabWidget 
from PyQt5 import QtGui
from PyQt5.QtCore import Qt


def sizeToBytes(size, units):
    units = units.lower()
    if units == "tb":
        return size * (1024 ** 4)
    elif units == "gb":
        return size * (1024 ** 3)
    elif units == "mb":
        return size * (1024 ** 2)
    elif units == "kb":
        return size * 1024
    elif units == "b":
        return size


def speedToBytes(speed, units):
    units = units.lower()
    if units == "mbit/s":
        return speed * (1024 ** 2) / 8
    elif units == "kbit/s":
        return speed * 1024 / 8
    elif units == "bit/s":
        return speed / 8
    elif units == "mb/s":
        return speed * (1024 ** 2)
    elif units == "kb/s":
        return speed * 1024
    elif units == "b/s":
        return speed


def DownloadTime(size, sizeUnit, speed, speedUnit):
    sizeInBytes = sizeToBytes(size, sizeUnit)
    speedInBytes = speedToBytes(speed, speedUnit)
    return sizeInBytes / speedInBytes / 3600


class DownloadTimeCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Download Time Calculator")
        self.setWindowIcon(QtGui.QIcon(
            r"M:\Mohamed\Programming\Download Time Calculator\ico.png"))
        self.setFixedHeight(300)
        # create label for file size
        self.sizeLabel = QLabel("File Size")
        self.sizeLabel.setStyleSheet("QLabel {font-weight: bold; font-size: 15px; font-family: Tahoma;}")
        self.sizeLabelInput = QLineEdit()
        self.sizeLabelInput.setValidator(QtGui.QDoubleValidator())
        # placeholder text
        self.sizeLabelInput.setPlaceholderText("Enter file size")
        self.sizeLabelInput.setStyleSheet("QLineEdit {padding: 6px;font-size: 11px;border-width: 1px;border-color: #CCCCCC;background-color: #FFFFFF;border-style: solid;border-radius: 4px;}"
                                          "QLineEdit:focus {border-color: #1BC466;}")

        # create Radio buttons for file size units
        self.sizeTB = QRadioButton("TB")
        self.sizeGB = QRadioButton("GB")
        self.sizeMB = QRadioButton("MB")
        self.sizeKB = QRadioButton("KB")
        self.sizeB = QRadioButton("B")

        self.sizeGroup = QButtonGroup(self)
        self.sizeGroup.addButton(self.sizeTB)
        self.sizeGroup.addButton(self.sizeGB)
        self.sizeGroup.addButton(self.sizeMB)
        self.sizeGroup.addButton(self.sizeKB)
        self.sizeGroup.addButton(self.sizeB)
        self.sizeGroup.setExclusive(True)

        # create label for download speed
        self.speedLabel = QLabel("Download Speed")
        self.speedLabelHint = QLabel("Click the speed test button to automatically set the value")
        self.speedLabel.setStyleSheet("QLabel {font-weight: bold; font-size: 15px; font-family: Tahoma;}")
        self.speedLabelInput = QLineEdit()
        self.speedLabelInput.setValidator(QtGui.QDoubleValidator())
        self.speedLabelInput.setPlaceholderText("Enter download speed")

        self.speedLabelInput.setStyleSheet(
            "QLineEdit {padding: 6px;font-size: 11px;border-width: 1px;border-color: #CCCCCC;background-color: #FFFFFF;border-style: solid;border-radius: 4px;}"
            "QLineEdit:focus {border-color: #1BC466;}")

        # create Radio buttons for download speed units
        self.speedMB = QRadioButton("MB/s")
        self.speedKB = QRadioButton("KB/s")
        self.speedB = QRadioButton("B/s")
        self.speedMbit = QRadioButton("MBit/s")
        self.speedKbit = QRadioButton("KBit/s")
        self.speedBit = QRadioButton("Bit/s")

        self.speedGroup = QButtonGroup(self)
        self.speedGroup.addButton(self.speedMB)
        self.speedGroup.addButton(self.speedKB)
        self.speedGroup.addButton(self.speedB)
        self.speedGroup.addButton(self.speedMbit)
        self.speedGroup.addButton(self.speedKbit)
        self.speedGroup.addButton(self.speedBit)
        self.speedGroup.setExclusive(True)

        # create button to calculate download time
        self.CalculateButton = QPushButton("Calculate")
        self.CalculateButton.setStyleSheet("""
        QPushButton {
            color: #FFFFFF;
            font-family: Verdana;
            font-size: 13px;
            font-weight: bold;
            padding: 6px;
            background-color: #1BC466;
            border-radius: 10px;
            }
        QPushButton:hover {
            background:#0B5724;
            }
         """)
        self.CalculateButton.clicked.connect(self.calculate)

        # create button to test download speed
        self.testSpeedButton = QPushButton("Speed Test (Wait 10s)")
        self.testSpeedButton.clicked.connect(self.SpeedTest)
        self.testSpeedButton.setStyleSheet("""
        QPushButton {
            color: #FFFFFF;
            font-family: Verdana;
            font-size: 13px;
            font-weight: bold;
            padding: 6px;
            background-color: #3D94F6;
            border-radius: 10px;
            }
        QPushButton:hover {
            border: solid #337FED 1px;
            background: #1E62D0;
            }
         """)


        sizeUnitLayout = QHBoxLayout()
        sizeUnitLayout.addStretch(1)
        sizeUnitLayout.addWidget(self.sizeTB)
        sizeUnitLayout.addWidget(self.sizeGB)
        sizeUnitLayout.addWidget(self.sizeMB)
        sizeUnitLayout.addWidget(self.sizeKB)
        sizeUnitLayout.addWidget(self.sizeB)
        sizeUnitLayout.addStretch(1)

        speedUnitLayout = QHBoxLayout()
        speedUnitLayout.addStretch(1)
        speedUnitLayout.addWidget(self.speedMB)
        speedUnitLayout.addWidget(self.speedKB)
        speedUnitLayout.addWidget(self.speedB)
        speedUnitLayout.addWidget(self.speedMbit)
        speedUnitLayout.addWidget(self.speedKbit)
        speedUnitLayout.addWidget(self.speedBit)
        speedUnitLayout.addStretch(1)

        self.Result = QLabel()
        self.Result.setAlignment(Qt.AlignCenter)
        self.Result.setStyleSheet("QLabel {font-weight: bold; font-size: 13px; font-family: Tahoma;}")

        self.Developer = QLabel(
            '© Mohamed Darwesh (<a href="https://github.com/medovanx">@medovanx</a>)')
        self.Developer.setOpenExternalLinks(True)
        self.Developer.setStyleSheet("""font-weight: bold; font-size: 10px;""")
        self.Developer.setAlignment(Qt.AlignLeft)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.sizeLabel)
        mainLayout.addWidget(self.sizeLabelInput)
        mainLayout.addLayout(sizeUnitLayout)
        mainLayout.addWidget(self.speedLabel)
        mainLayout.addWidget(self.speedLabelHint)
        mainLayout.addWidget(self.speedLabelInput)
        mainLayout.addLayout(speedUnitLayout)
        mainLayout.addWidget(self.CalculateButton)
        mainLayout.addWidget(self.testSpeedButton)
        mainLayout.addWidget(self.Result)
        mainLayout.addWidget(self.Developer)

        self.setLayout(mainLayout)

    def SpeedTest(self):
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        try:
            self.speedLabelInput.setText(str(st.download() / 10**6))
            self.speedMbit.setChecked(True)
        except:
            self.Result.setText(f"Error occured while testing speed")
            return

    def calculate(self):
        try:
            size = float(self.sizeLabelInput.text())
            sizeUnit = self.sizeTB.text() if self.sizeTB.isChecked() else self.sizeGB.text() if self.sizeGB.isChecked() else self.sizeMB.text(
            ) if self.sizeMB.isChecked() else self.sizeKB.text() if self.sizeKB.isChecked() else self.sizeB.text()
            speed = float(self.speedLabelInput.text())
            speedUnit = self.speedMB.text() if self.speedMB.isChecked() else self.speedKB.text() if self.speedKB.isChecked() else self.speedB.text() if self.speedB.isChecked(
            ) else self.speedMbit.text() if self.speedMbit.isChecked() else self.speedKbit.text() if self.speedKbit.isChecked() else self.speedBit.text()
        except ValueError:
            self.Result.setText(
                "<font color='red'>Please enter a valid value.</font>")
            return

        time = DownloadTime(size, sizeUnit, speed, speedUnit)
        months = int(time // 30)
        days = int(time % 30)
        hours = int(time * 24 % 24)
        minutes = int(time * 24 * 60 % 60)
        seconds = int(time * 24 * 60 * 60 % 60)
        if months == 0 and days == 0 and hours == 0 and minutes == 0 and seconds == 0:
            self.Result.setText(f"Download Time: less than a second")
        elif months == 0:
            self.Result.setText(
                f"Download Time: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
        elif months == 0 and days == 0:
            self.Result.setText(
                f"Download Time: {hours} hours, {minutes} minutes, {seconds} seconds")
        elif months == 0 and days == 0 and hours == 0:
            self.Result.setText(
                f"Download Time: {minutes} minutes, {seconds} seconds")
        elif months == 0 and days == 0 and hours == 0 and minutes == 0:
            self.Result.setText(f"Download Time: {seconds} seconds")
        else:
            self.Result.setText(
                f"Download Time: {months} months, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")


app = QApplication(sys.argv)
window = DownloadTimeCalculator()
window.show()
sys.exit(app.exec_())
