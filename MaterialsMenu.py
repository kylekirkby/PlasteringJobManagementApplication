from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MaterialsMenuWidget(QWidget):
    """ This class creates a widget that displays the menu for the materials section
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

        

        self.addMaterialPushButton = QPushButton("New Material")
        self.addMaterialPushButton.setProperty("buttonClass","home")
        self.addMaterialPushButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.manageMaterialsPushButton = QPushButton("Manage Materials")
        self.manageMaterialsPushButton.setProperty("buttonClass","home")
        self.manageMaterialsPushButton.setCursor(QCursor(Qt.PointingHandCursor))


        self.backButton = QPushButton("Back")


        self.jobsMenuLayout = QHBoxLayout()

        self.jobsMenuLayout.addWidget(self.addMaterialPushButton)
        self.jobsMenuLayout.addWidget(self.manageMaterialsPushButton)
        self.jobsMenuLayout.addWidget(self.backButton)

        self.tempWidget = QWidget()
        self.tempWidget.setLayout(self.jobsMenuLayout)

        
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.tempWidget)
        self.verticalLayout.addWidget(self.backButton)




        return self.verticalLayout
