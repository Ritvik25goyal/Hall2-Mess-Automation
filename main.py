import sys
import csv
import sqlite3
import pickle
from datetime import date
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout

class ExtraEntryMainWindow(QMainWindow):
    def __init__(self,extras_file,db_name="messdata.db"):
        super(ExtraEntryMainWindow,self).__init__()
        self.extras = self.load_extras(extras_file)
        self.db_name = db_name
        self.initUI()
        self.connect_to_db()

    def connect_to_db(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def load_extras(self, filename):
        extras = {}
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                extras[row[0]] = float(row[1])
        return extras

    def initUI(self):
        self.setObjectName("MainWindow")
        self.resize(1077, 856)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1071, 791))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 761, 791))
        font = QtGui.QFont()
        font.setFamily("FiraCode Nerd Font")
        font.setPointSize(14)
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.EntrySubmit = QtWidgets.QPushButton(self.frame_2)
        self.EntrySubmit.setGeometry(QtCore.QRect(620, 740, 97, 31))
        self.EntrySubmit.setObjectName("EntrySubmit")
        self.EntrySubmit.clicked.connect(self.Entry_Submit)
        self.RollNoFormValue = QtWidgets.QLineEdit(self.frame_2)
        self.RollNoFormValue.setGeometry(QtCore.QRect(120, 20, 121, 31))
        self.RollNoFormValue.setText("")
        self.RollNoFormValue.setObjectName("RollNoFormValue")
        self.RollNoFormLabel = QtWidgets.QLabel(self.frame_2)
        self.RollNoFormLabel.setGeometry(QtCore.QRect(10, 20, 101, 31))
        self.RollNoFormLabel.setObjectName("RollNoFormLabel")
        self.RollNoFormSubmit = QtWidgets.QPushButton(self.frame_2)
        self.RollNoFormSubmit.setGeometry(QtCore.QRect(610, 20, 97, 31))
        self.RollNoFormSubmit.setObjectName("RollNoFormSubmit")
        self.RollNoFormSubmit.clicked.connect(self.update_student_info)
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setGeometry(QtCore.QRect(0, 60, 761, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.ExtrasMenu = QtWidgets.QScrollArea(self.frame_2)
        self.ExtrasMenu.setGeometry(QtCore.QRect(20, 90, 721, 621))
        self.ExtrasMenu.setWidgetResizable(True)
        self.ExtrasMenu.setObjectName("ExtrasMenu")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 719, 619))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.ExtrasMenu.setWidget(self.scrollAreaWidgetContents)
        self.OthersAmount = QtWidgets.QLineEdit(self.frame_2)
        self.OthersAmount.setGeometry(QtCore.QRect(130, 730, 131, 41))
        self.OthersAmount.setText("")
        self.OthersAmount.setObjectName("OthersAmount")
        self.OthersAmount.setValidator(QtGui.QIntValidator())
        self.OthersAmount.textChanged.connect(self.calculate_total)
        self.OthersLabel = QtWidgets.QLabel(self.frame_2)
        self.OthersLabel.setGeometry(QtCore.QRect(20, 740, 71, 23))
        self.OthersLabel.setObjectName("OthersLabel")
        self.TotalLabel = QtWidgets.QLabel(self.frame_2)
        self.TotalLabel.setGeometry(QtCore.QRect(280, 740, 81, 31))
        self.TotalLabel.setObjectName("TotalLabel")
        self.TotalAmount = QtWidgets.QLabel(self.frame_2)
        self.TotalAmount.setGeometry(QtCore.QRect(360, 740, 111, 31))
        self.TotalAmount.setText("")
        self.TotalAmount.setObjectName("TotalAmount")
        self.ResetButton = QtWidgets.QPushButton(self.frame_2)
        self.ResetButton.setGeometry(QtCore.QRect(510, 740, 97, 31))
        self.ResetButton.setObjectName("ResetButton")
        self.ResetButton.clicked.connect(self.reset_data)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(760, 0, 311, 791))
        font = QtGui.QFont()
        font.setFamily("FiraCode Nerd Font")
        font.setPointSize(14)
        self.frame_3.setFont(font)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.line = QtWidgets.QFrame(self.frame_3)
        self.line.setGeometry(QtCore.QRect(-17, 0, 20, 791))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.StudentNameLabel = QtWidgets.QLabel(self.frame_3)
        self.StudentNameLabel.setGeometry(QtCore.QRect(30, 330, 71, 23))
        self.StudentNameLabel.setObjectName("StudentNameLabel")
        self.StudentRollNoLabel = QtWidgets.QLabel(self.frame_3)
        self.StudentRollNoLabel.setGeometry(QtCore.QRect(30, 430, 91, 23))
        self.StudentRollNoLabel.setObjectName("StudentRollNoLabel")
        self.StudentRoomNoLabel = QtWidgets.QLabel(self.frame_3)
        self.StudentRoomNoLabel.setGeometry(QtCore.QRect(30, 510, 91, 23))
        self.StudentRoomNoLabel.setObjectName("StudentRoomNoLabel")
        self.StudentImageFrame = QtWidgets.QLabel(self.frame_3)
        self.StudentImageFrame.setGeometry(QtCore.QRect(40, 30, 231, 261))
        self.StudentImageFrame.setText("")
        self.StudentImageFrame.setScaledContents(True)
        self.StudentImageFrame.setObjectName("StudentImageFrame")
        self.StudentName = QtWidgets.QLabel(self.frame_3)
        self.StudentName.setGeometry(QtCore.QRect(30, 360, 261, 61))
        self.StudentName.setText("")
        self.StudentName.setObjectName("StudentName")
        self.StudentRollNo = QtWidgets.QLabel(self.frame_3)
        self.StudentRollNo.setGeometry(QtCore.QRect(30, 462, 261, 31))
        self.StudentRollNo.setText("")
        self.StudentRollNo.setObjectName("StudentRollNo")
        self.StudentRoomNo = QtWidgets.QLabel(self.frame_3)
        self.StudentRoomNo.setGeometry(QtCore.QRect(30, 550, 261, 41))
        self.StudentRoomNo.setText("")
        self.StudentRoomNo.setObjectName("StudentRoomNo")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1077, 28))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        print(self.extras)
        self.quantity_boxes=[]
        self.ExtrasMenu.setWidget(self.scrollAreaWidgetContents)
        self.ExtrasMenuV = QVBoxLayout(self.scrollAreaWidgetContents) 
        for item,price in self.extras.items():
            hbox = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel(item)
            price_label = QtWidgets.QLabel(f"Price: ${price:.2f}")
            quantity_box = QtWidgets.QLineEdit()
            quantity_box.setText("0")
            quantity_box.setValidator(QtGui.QIntValidator())
            quantity_box.textChanged.connect(self.calculate_total)
            hbox.addWidget(label)
            hbox.addWidget(price_label)
            hbox.addWidget(quantity_box)
            self.quantity_boxes.append(quantity_box)
            self.ExtrasMenuV.addLayout(hbox)


        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.EntrySubmit.setText(_translate("MainWindow", "Submit"))
        self.RollNoFormLabel.setText(_translate("MainWindow", "Roll No:"))
        self.RollNoFormSubmit.setText(_translate("MainWindow", "Submit"))
        self.StudentNameLabel.setText(_translate("MainWindow", "Name"))
        self.StudentRollNoLabel.setText(_translate("MainWindow", "Roll No"))
        self.StudentRoomNoLabel.setText(_translate("MainWindow", "Room No"))
        self.OthersLabel.setText(_translate("MainWindow", "Other:"))
        self.OthersAmount.setText("0")
        self.TotalLabel.setText(_translate("MainWindow", "Total:"))
        self.TotalAmount.setText("0")
        self.ResetButton.setText(_translate("MainWindow", "Reset"))


    def calculate_total(self):
        total = 0
        for quantity_box, (item, price) in zip(self.quantity_boxes, self.extras.items()):
            try:
                quantity = int(quantity_box.text())
                total += quantity * price
            except ValueError:
                pass
        try:
            total += int(self.OthersAmount.text())
        except ValueError:
            pass
        self.TotalAmount.setText(f"{total:.2f}")

    def update_student_info(self):
        roll_no = self.RollNoFormValue.text()
        # Check if Roll No is entered
        if not roll_no:
            # Display error message if Roll No is empty
            self.show_message("Please enter a Roll Number!")
            return

        # Fetch student information based on Roll No
        query = f"SELECT Name, RoomNo FROM students WHERE Rollno = ?"
        self.cursor.execute(query, (roll_no,))
        student_data = self.cursor.fetchone()

        # Check if student data is found
        if not student_data:
            # Display error message if student not found
            self.show_message("Student not found!")
            return

        # Update student information labels (assuming labels exist)
        self.StudentName.setText(student_data[0])  # Update name label
        self.StudentName.adjustSize()
        self.StudentRollNo.setText(roll_no)  # Update Roll No label (already entered)
        self.StudentRoomNo.setText(student_data[1])  # Update room number label
        self.StudentImageFrame.setPixmap(QtGui.QPixmap(f"StudentImages/{int(roll_no)}_0.jpg"))  # Update Student Image

    def show_message(self, message):
        # Implement a method to display messages (e.g., popup dialog)2
        # This example uses a print statement for demonstration
        print(message)

    def reset_data(self):
        for i in self.quantity_boxes :
            i.setText("0")
        self.OthersAmount.setText("0")

    def Entry_Submit(self):
        # Check if student information is not updated (Roll No not entered)
        if not self.RollNoFormValue.text():
            self.show_message("Please update student information first!")
            return

        # Calculate total amount based on quantity boxes (assuming logic exists)
        self.calculate_total()

        # Get today's date in YYYY-MM-DD format
        # todays_date = date.today().strftime("%Y-%m-%d")
        todays_date = "2024-03-09"
        AddedAmmount = int(float(self.TotalAmount.text()))

        self.cursor.execute("SELECT DailyPurchases FROM students WHERE Rollno = ?", (self.RollNoFormValue.text(),))
        serialized_data = self.cursor.fetchone()[0]

        if serialized_data:
            # Deserialize existing purchase data
            daily_purchases = pickle.loads(serialized_data)

            # Check if today's date exists
            if todays_date in daily_purchases:
                # Add amount to existing entry
                daily_purchases[todays_date] += AddedAmmount
            else:
                # Create a new entry for today's date
                daily_purchases[todays_date] = AddedAmmount

        else:
            # Initialize daily purchases if no existing data
            daily_purchases = {todays_date: AddedAmmount}

        serialized_data = pickle.dumps(daily_purchases)

        # Update DailyPurchases BLOB and TotalAmount in the database    
        self.cursor.execute("""
            UPDATE students
            SET DailyPurchases = ?, TotalAmount = TotalAmount + ?
            WHERE Rollno = ?
        """, (serialized_data, AddedAmmount, self.RollNoFormValue.text()))
        # Commit changes to the database
        self.conn.commit()

        # Display success message
        self.show_message("Entry submitted successfully!")
        self.reset_data()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    extras_file = "Extras.csv"
    MainWindow = ExtraEntryMainWindow(extras_file)
    MainWindow.show()
    sys.exit(app.exec_())
