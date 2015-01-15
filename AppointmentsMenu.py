from PyQt4.QtGui import *
from PyQt4.QtCore import *

class AppointmentMenuWidget(QWidget):
    """ This class creates a widget that displays the menu for the appointments section
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

        

        self.addAppointmentPushButton = QPushButton("New Appointment")
        self.addAppointmentPushButton.setProperty("buttonClass","home")
        self.addAppointmentPushButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.manageAppointmentsPushButton = QPushButton("Manage Appointments")
        self.manageAppointmentsPushButton.setProperty("buttonClass","home")
        self.manageAppointmentsPushButton.setCursor(QCursor(Qt.PointingHandCursor))


        self.backButton = QPushButton("Back")


        self.jobsMenuLayout = QHBoxLayout()

        self.jobsMenuLayout.addWidget(self.addAppointmentPushButton)
        self.jobsMenuLayout.addWidget(self.manageAppointmentsPushButton)
        self.jobsMenuLayout.addWidget(self.backButton)

        self.tempWidget = QWidget()
        self.tempWidget.setLayout(self.jobsMenuLayout)

        
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.tempWidget)
        self.verticalLayout.addWidget(self.backButton)




        return self.verticalLayout
