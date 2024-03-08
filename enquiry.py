import sys
import csv
import sqlite3
import pickle
from datetime import date
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QListView
from PyQt5.QtCore import QStringListModel

class EnquiryMainWindow(QMainWindow):
    def __init__(self,db_name="messdata.db"):
        super(EnquiryMainWindow,self).__init__()
        self.db_name = db_name
        self.initUI()
        self.connect_to_db()

    def connect_to_db(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def initUI(self):
        self.setObjectName("MainWindow")
        self.resize(492, 872)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 491, 811))
        font = QtGui.QFont()
        font.setFamily("FiraCode Nerd Font")
        font.setPointSize(14)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.RollNoLabel = QtWidgets.QLabel(self.frame)
        self.RollNoLabel.setGeometry(QtCore.QRect(40, 30, 111, 41))
        font = QtGui.QFont()
        font.setFamily("FiraCode Nerd Font")
        font.setPointSize(14)
        self.RollNoLabel.setFont(font)
        self.RollNoLabel.setObjectName("RollNoLabel")
        self.RollNoValue = QtWidgets.QLineEdit(self.frame)
        self.RollNoValue.setGeometry(QtCore.QRect(140, 30, 171, 41))
        self.RollNoValue.setObjectName("RollNoValue")
        self.RollNoSubmit = QtWidgets.QPushButton(self.frame)
        self.RollNoSubmit.setGeometry(QtCore.QRect(340, 30, 111, 41))
        self.RollNoSubmit.setObjectName("RollNoSubmit")
        self.RollNoSubmit.clicked.connect(self.handle_submit)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 90, 491, 721))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.DayWiseWindow = QtWidgets.QScrollArea(self.frame_2)
        self.DayWiseWindow.setGeometry(QtCore.QRect(0, 60, 491, 601))
        self.DayWiseWindow.setWidgetResizable(True)
        self.DayWiseWindow.setObjectName("DayWiseWindow")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 489, 599))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.DayWiseWindow.setWidget(self.scrollAreaWidgetContents)
        self.DateLabel = QtWidgets.QLabel(self.frame_2)
        self.DateLabel.setGeometry(QtCore.QRect(60, 10, 101, 41))
        font = QtGui.QFont()
        font.setFamily("FiraCode Nerd Font")
        font.setPointSize(14)
        self.DateLabel.setFont(font)
        self.DateLabel.setObjectName("DateLabel")
        self.AmountLabel = QtWidgets.QLabel(self.frame_2)
        self.AmountLabel.setGeometry(QtCore.QRect(290, 10, 101, 41))
        font = QtGui.QFont()
        font.setFamily("FiraCode Nerd Font")
        font.setPointSize(14)
        self.AmountLabel.setFont(font)
        self.AmountLabel.setObjectName("AmountLabel")
        self.TotalLabel = QtWidgets.QLabel(self.frame_2)
        self.TotalLabel.setGeometry(QtCore.QRect(280, 670, 81, 51))
        font = QtGui.QFont()
        font.setFamily("FiraCode Nerd Font")
        font.setPointSize(14)
        self.TotalLabel.setFont(font)
        self.TotalLabel.setObjectName("TotalLabel")
        self.TotalAmountValue = QtWidgets.QLabel(self.frame_2)
        self.TotalAmountValue.setGeometry(QtCore.QRect(360, 670, 111, 51))
        font = QtGui.QFont()
        font.setFamily("FiraCode Nerd Font")
        font.setPointSize(14)
        self.TotalAmountValue.setFont(font)
        self.TotalAmountValue.setText("")
        self.TotalAmountValue.setObjectName("TotalAmountValue")
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(0, 80, 491, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 492, 28))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.RollNoLabel.setText(_translate("MainWindow", "RollNo:"))
        self.RollNoSubmit.setText(_translate("MainWindow", "Submit"))
        self.DateLabel.setText(_translate("MainWindow", "Date"))
        self.AmountLabel.setText(_translate("MainWindow", "Amount"))
        self.TotalLabel.setText(_translate("MainWindow", "Total:"))

    def show_message(self,Message):
        pass
    def handle_submit(self):
        """
        Fetches day-wise payment and total payment for the entered Roll No.
        Updates the display with the retrieved data.
        """
        roll_no = self.RollNoValue.text()

        if not roll_no:
            # Show error message if no Roll No is entered
            self.show_message("Please enter a Roll Number to proceed.")
            return

        # Fetch data from database using fetched_data function (defined below)
        self.day_wise_data, total_amount  = self.fetch_data(roll_no)

        if not self.day_wise_data:
            # Show message if no data found
            self.show_message("No data found for Roll Number " + roll_no)
            return

         # Clear previous content (if applicable)
        central_widget = self.DayWiseWindow.widget()
        if central_widget is not None:
            central_widget.setParent(None)

        # Create a new central widget
        central_widget = QWidget(self.DayWiseWindow)
        self.DayWiseWindow.setWidget(central_widget)

        # Create a list model for the day-wise data
        day_wise_model = QStringListModel(central_widget)
        day_wise_data_strings = [
            f"{date}: \t\t{amount:.2f}" for date, amount in self.day_wise_data.items()
        ]  # Format data strings efficiently
        day_wise_model.setStringList(day_wise_data_strings)

        # Create a QListView to display the data
        day_wise_list_view = QListView(central_widget)
        day_wise_list_view.setModel(day_wise_model)  # Set model for the list view

        # Create a layout to hold the list view
        layout = QVBoxLayout(central_widget)  # Use QVBoxLayout for vertical display
        layout.addWidget(day_wise_list_view)

        # Update total amount display
        self.TotalAmountValue.setText(f"{total_amount:.2f}")  # Format to 2 decimal places

    def fetch_data(self, roll_no):
        """
        Fetches day-wise purchase data and total amount from the database for a Roll No.
        Args:
            roll_no (str): Student's Roll No.
        Returns:
            dict or None: Dictionary containing day-wise purchase amounts (date: amount)
                or None if no data found for the Roll No.
        """

        try:
            # Fetch daily purchases BLOB for the Roll No
            self.cursor.execute("SELECT DailyPurchases FROM students WHERE Rollno = ?", (roll_no,))
            serialized_data = self.cursor.fetchone()[0]  # Get the first element (BLOB)

            if not serialized_data:
                # No data found, return None
                return None

            # Deserialize the BLOB data
            daily_purchases = pickle.loads(serialized_data)

            # Calculate total amount
            total_amount = 0.0
            for amount in daily_purchases.values():
                total_amount += amount

            # Return dictionary with day-wise amounts and total amount
            return {date: daily_purchases[date] for date in daily_purchases.keys()}, total_amount

        except sqlite3.Error as e:
            # Handle database errors (optional)
            print("Error fetching data:", e)
            return None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = EnquiryMainWindow()
    ui.show()
    sys.exit(app.exec_())
