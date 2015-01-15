from PyQt4.QtGui import *
from PyQt4.QtCore import *

class InvoicesMenuWidget(QWidget):
    """ This class creates a widget that displays the menu for the invoice section
    of the application """


    def __init__(self):

        super().__init__()


        self.layout = self.createJobsMenuLayout()
        self.setLayout(self.layout)
##        self.setAutoFillBackground(True)
##        p = self.palette()
##        p.setColor(self.backgroundRole(), Qt.white)
##        self.setPalette(p)

        self.setStyleSheet("""QPushButton[buttonClass=home] {
                           font-size: 16px; background-color: rgba(188, 188, 188, 50);
                           border: 1px solid rgba(188, 188, 188, 250);
                           height:100px;
                           border-radius:5px;}""")

    def createJobsMenuLayout(self):

        

        self.addInvoicePushButton = QPushButton("New Invoice")
        self.addInvoicePushButton.setProperty("buttonClass","home")
        self.addInvoicePushButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.manageInvoicesPushButton = QPushButton("Manage Invoices")
        self.manageInvoicesPushButton.setProperty("buttonClass","home")
        self.manageInvoicesPushButton.setCursor(QCursor(Qt.PointingHandCursor))


        self.backButton = QPushButton("Back")


        self.jobsMenuLayout = QHBoxLayout()

        self.jobsMenuLayout.addWidget(self.addInvoicePushButton)
        self.jobsMenuLayout.addWidget(self.manageInvoicesPushButton)
        self.jobsMenuLayout.addWidget(self.backButton)

        self.tempWidget = QWidget()
        self.tempWidget.setLayout(self.jobsMenuLayout)

        
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.tempWidget)
        self.verticalLayout.addWidget(self.backButton)




        return self.verticalLayout
