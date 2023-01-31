import sys
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QButtonGroup
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

def convert_to_bytes(size, units):
    units = units.lower()
    if units == "gb":
        return size * (1024 ** 3)
    elif units == "mb":
        return size * (1024 ** 2)
    elif units == "kb":
        return size * 1024
    elif units == "b":
        return size

def convert_speed_to_bytes_per_second(speed, units):
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

def download_time(size, size_units, speed, speed_units):
    size_in_bytes = convert_to_bytes(size, size_units)
    speed_in_bytes_per_second = convert_speed_to_bytes_per_second(speed, speed_units)
    return size_in_bytes / speed_in_bytes_per_second / 3600 

class DownloadTimeCalculator(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Download Time Calculator")
        self.setWindowIcon(QtGui.QIcon(r"M:\Mohamed\Programming\Download Time Calculator\ico.png"))
        self.setGeometry(100, 100, 400, 100)
        self.size_label = QLabel("File Size:")
        self.size_edit = QLineEdit()

        #create checkbox for size units
        self.size_gb = QRadioButton("GB")
        self.size_mb = QRadioButton("MB")
        self.size_kb = QRadioButton("KB")
        self.size_b = QRadioButton("B")
        self.size_unit_group = QButtonGroup(self)
        self.size_unit_group.addButton(self.size_gb)
        self.size_unit_group.addButton(self.size_mb)
        self.size_unit_group.addButton(self.size_kb)
        self.size_unit_group.addButton(self.size_b)
        self.size_unit_group.setExclusive(True)

        self.speed_label = QLabel("Download Speed:")
        self.speed_edit = QLineEdit()
#make separate radio buttons for speed units
        self.speed_mb = QRadioButton("MB/s")
        self.speed_kb = QRadioButton("KB/s")
        self.speed_b = QRadioButton("B/s")
        self.speed_mbit = QRadioButton("MBit/s")
        self.speed_kbit = QRadioButton("KBit/s")
        self.speed_bit = QRadioButton("Bit/s")
        self.speed_unit_group = QButtonGroup(self)
        self.speed_unit_group.addButton(self.speed_mb)
        self.speed_unit_group.addButton(self.speed_kb)
        self.speed_unit_group.addButton(self.speed_b)
        self.speed_unit_group.addButton(self.speed_mbit)
        self.speed_unit_group.addButton(self.speed_kbit)
        self.speed_unit_group.addButton(self.speed_bit)
        self.speed_unit_group.setExclusive(True)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)

        self.result_label = QLabel()

        size_layout = QHBoxLayout()
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_edit)
        size_units_layout = QHBoxLayout()
        size_units_layout.addWidget(self.size_gb)
        size_units_layout.addWidget(self.size_mb)
        size_units_layout.addWidget(self.size_kb)
        size_units_layout.addWidget(self.size_b)

        speed_layout = QHBoxLayout()
        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_edit)

        speed_units_layout = QHBoxLayout()
        speed_units_layout.addWidget(self.speed_mb)
        speed_units_layout.addWidget(self.speed_kb)
        speed_units_layout.addWidget(self.speed_b)
        speed_units_layout.addWidget(self.speed_mbit)
        speed_units_layout.addWidget(self.speed_kbit)
        speed_units_layout.addWidget(self.speed_bit)

        author = QLabel('Created by: Mohamed Darwesh (<a href="https://github.com/medovanx">@medovanx</a>)', self)
        author.move(10, 240)
        author.setOpenExternalLinks(True)
        author.setStyleSheet("""font-weight: bold; font-size: 12px;""")


        main_layout = QVBoxLayout()
        main_layout.addLayout(size_layout)
        main_layout.addLayout(size_units_layout)
        main_layout.addLayout(speed_layout)
        main_layout.addLayout(speed_units_layout)
        main_layout.addWidget(self.calculate_button)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(author)


        self.setLayout(main_layout)

    def calculate(self):
        try:
            size = float(self.size_edit.text())
            size_units = self.size_gb.text() if self.size_gb.isChecked() else self.size_mb.text() if self.size_mb.isChecked() else self.size_kb.text() if self.size_kb.isChecked() else self.size_b.text()
            speed = float(self.speed_edit.text())
            speed_units = self.speed_mb.text() if self.speed_mb.isChecked() else self.speed_kb.text() if self.speed_kb.isChecked() else self.speed_b.text() if self.speed_b.isChecked() else self.speed_mbit.text() if self.speed_mbit.isChecked() else self.speed_kbit.text() if self.speed_kbit.isChecked() else self.speed_bit.text()
        except ValueError:
            self.result_label.setText("<font color='red'>Please enter a valid number.</font>")
            self.result_label.setAlignment(Qt.AlignCenter)
            return
        time = download_time(size, size_units, speed, speed_units)
        #write time in days, hours, minutes, and seconds
        days = int(time // 24)
        hours = int(time % 24)
        minutes = int((time * 60) % 60)
        seconds = int((time * 3600) % 60)
        milliseconds = int((time * 3600000) % 1000)
        self.result_label.setText(f"Download Time: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds and {milliseconds} milliseconds")
        self.result_label.setAlignment(Qt.AlignCenter)

app = QApplication(sys.argv)
calculator = DownloadTimeCalculator()
calculator.show()
sys.exit(app.exec_())