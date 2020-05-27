"""A simple PyQt5 POS system with an SQlite3 database
    Yolisa Pingilili
 """

import sqlite3
import sys
from PyQt5.QtWidgets import*
from PyQt5.QtWidgets import QMessageBox
from datetime import*



class TuckShop(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(250, 250, 200, 100)
        self.setWindowTitle('Tuck Shop')
        self.show()

        # create a connection to the database
        self.conn = sqlite3.connect('My Database.db')
        # create a cursor() object that allows writing to and modifying database values
        self.Cursor = self.conn.cursor()
        self.label = QLabel('')

        # create the comboBox and populate it with the goods of the shop
        self.combo = QComboBox()
        self.combo.addItems(['Chips', 'Chocolate', 'Cold Drink', 'Pies', 'Gum', 'Cigarettes', 'Tissue', 'Pens', 'Pencils', 'Noodles'])

        # create the buttons and connect them to
        # their appropriate methods
        enter = QPushButton('Enter')
        enter.clicked.connect(self.Enter)
        self.textBox = QLineEdit()
        close = QPushButton('Close')
        close.clicked.connect(self.closer)
        report = QPushButton('Sales report')
        report.clicked.connect(self.popup)

        # set the layout of the buttons
        hbox = QHBoxLayout()
        hbox.addWidget(enter)
        hbox.addWidget(close)
        hbox.addWidget(report)
        hbox2 = QWidget()
        hbox2.setLayout(hbox)

        # bring everything together in a grid layout
        grid = QGridLayout()
        grid.addWidget(self.combo, 0,1)
        grid.addWidget(self.textBox, 0, 2)
        grid.addWidget(self.label, 1,1)
        grid.addWidget(hbox2, 2,1)
        self.setLayout(grid)


    # takes user input(desired quantity of items) and compares it to the available items
    # if there are less available, prints a statement
    # else, subtracts the desired from the available and updates the available
    # the transaction is then recorded into the sales table
    # along with the date&time at which it took place
    def Enter(self):
        with self.conn:
            # get the current time(time of transaction from the system)
            today = datetime.now()
            today1 = today.strftime("%d/%m/%Y--%H:%M:%S")
            item = self.combo.currentText()
            text = self.textBox.displayText()
            int(text)
            # get the current number of the selected item in the db
            originalQuantity = self.conn.execute('SELECT Quantity, Stock_code FROM Stock WHERE Item_name=?', (item,)).fetchone()
            # 'select' returns a tuple, get the values out of the tuple(like an array)
            originalQuantity1 = originalQuantity[0]
            stockCode = originalQuantity[1]

            if originalQuantity1 < int(text):
                low = 'The required quantity is too high, we currently have '+ str(originalQuantity1)
                low1 = ' of the required item.'
                low2 = low+low1
                self.label.setText(low2)
                self.textBox.clear()
            else:
                newQuantity = originalQuantity1 - int(text)
                self.Cursor.execute("UPDATE Stock SET Quantity=? WHERE Item_name =?", (newQuantity, item))
                self.label.setText('')
                self.textBox.clear()
                # populate the Sales table with every sale that goes through
                self.Cursor.execute("INSERT INTO Sales VALUES(?, ?, ?)", (stockCode, int(text), today1))

    # the popup window returns/shows the sales
    # that have occurred in the shop
    # also shows cost price, sales price and profit
    def popup(self):
        with self.conn:
            window = QMessageBox()
            window.setGeometry(250,250, 500, 500)
            window.setWindowTitle('Sales Report')
            fields = self.conn.execute('SELECT Quantity FROM Sales').fetchall();
            fields2 = self.conn.execute('SELECT Stock_Code FROM Sales').fetchall();
            fields3 = self.conn.execute('SELECT Quantity FROM Sales').fetchall();
            # print(fields3)
            total = 0
            total2 = 0
            total3 = 0
            z = 0
            # loop through fields2 and fields3 to get the total cost price
            for eachTuple in fields2:
                for i in eachTuple:
                    costPrice = self.conn.execute('SELECT Cost_Price FROM Stock WHERE Stock_Code = ?', (i,)).fetchall();
                    salesPrice = self.conn.execute('SELECT Sales_Price FROM Stock WHERE Stock_Code = ?', (i,)).fetchall();
                    # print(salesPrice)
                    total2 += costPrice[0][0]*fields3[z][0]
                    total3 += salesPrice[0][0] * fields3[z][0]
                    z += 1
            # print(total3)
            # sum up the quantity field
            for eachItem in fields:
                for j in eachItem:
                   total += j
            profit = total3 - total2
            mystring = 'total quantity sold is {} and the total cost price is R{}, sale price is R{}, with a Profit of R{}'.format(total, total2, total3, profit)
            window.setText(mystring)
            show = window.exec()


    # method connected to the 'close' button
    # closes the application
    def closer(self):
        sys.exit()


# main method
def main():
    App = QApplication(sys.argv)
    shop = TuckShop()
    sys.exit(App.exec())
main()
