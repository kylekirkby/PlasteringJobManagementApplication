from PyQt4.QtCore import  *
from PyQt4.QtGui import *
from SQLConnection import *

import re

class AddMaterialWidget(QWidget):

    """ This is the add material widget """

    def __init__(self, parent):

        super().__init__()
        
        self.setProperty("addMaterialClass","True")

        self.connection = None

        self.parent = parent
        
        self.mainLayout = self.layout()
        
        self.setLayout(self.mainLayout)

        self.setStyleSheet("QWidget[addMaterialClass=True]{padding:100px;}")

    def addConnection(self, connection):
        
        self.connection = connection

        return True

    def validateMaterialName(self):

        text = self.materialNameEdit.text()
        length = len(text)

        if length > 2:
            self.materialNameEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.materialNameEdit.setStyleSheet("background-color:#f6989d;")
            return False

    def validateMaterialPrice(self):
        

        text = self.materialPriceEdit.text()

        priceRegex = re.compile("[0-9]+\.[0-9]+")

        match = priceRegex.match(text.upper())

        if match:
            self.materialPriceEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.materialPriceEdit.setStyleSheet("background-color:#f6989d;")
            return False

   
    def clearForm(self):
        
        self.materialNameEdit.clear()
        self.materialPriceEdit.clear()
     
        self.materialNameEdit.setStyleSheet("background-color:#FFF;")
        self.materialPriceEdit.setStyleSheet("background-color:#FFF;")

        self.errorTextContentLabel.setText("None")
        

    def addMaterialToDatabase(self):

        values = { "MaterialName": self.materialNameEdit.text(),
                   "MaterialPrice": self.materialPriceEdit.text()}

        materialAdded = self.connection.addMaterial(values)

        if materialAdded:

            self.clearForm()
            self.parent.switchToMaterialsMenu()
            
            infoText = """ The New material has been added to the database!"""
            QMessageBox.information(self, "Material Added", infoText)
            
        else:
            infoText = """ The New material was not added to the database successfully! """

            QMessageBox.critical(self, "Material Not Added", infoText)
            
    
    def validateForm(self):

        self.checkName = self.validateMaterialName()
        self.checkPrice = self.validateMaterialPrice()


        self.errorMsg = ""

        if self.checkName == False:
            self.errorMsg += "Invalid Material Name, "
        if self.checkPrice == False:
            self.errorMsg += "Invalid Material Price (must be 00.00 format), "

        self.errorTextContentLabel.setText(self.errorMsg)
        

        if self.errorMsg == "":
            self.addMaterialToDatabase()
            return True
        else:
            return False
    

    def layout(self):

        self.addMaterialTitleText = QLabel("Add a Material")
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.addMaterialTitleText.setGraphicsEffect(self.shadow)
        self.addMaterialTitleText.setStyleSheet("font-size:20px;")

        self.materialNameLabel = QLabel("Material Name")
        self.materialPriceLabel = QLabel("Material Price")

        self.materialNameEdit = QLineEdit()
        self.materialPriceEdit = QLineEdit()

        self.cancelFormButton = QPushButton("Cancel")
        self.addMaterialFormButton = QPushButton("Add Material")

        self.errorTextLabel = QLabel("Errors: ")
        self.errorTextContentLabel = QLabel()
        self.errorTextContentLabel.setStyleSheet("color: red;")

        self.grid = QGridLayout()

        self.grid.addWidget(self.errorTextLabel, 0 ,0)
        self.grid.addWidget(self.errorTextContentLabel, 0, 1)

        self.grid.addWidget(self.materialNameLabel, 1, 0)
        self.grid.addWidget(self.materialNameEdit, 1, 1)

        self.grid.addWidget(self.materialPriceLabel, 2, 0)
        self.grid.addWidget(self.materialPriceEdit, 2, 1)

        self.grid.addWidget(self.cancelFormButton, 3, 0)
        self.grid.addWidget(self.addMaterialFormButton, 3, 1)

        
        self.gridWidget = QWidget()
        self.gridWidget.setLayout(self.grid)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.addMaterialTitleText)
        self.verticalLayout.addStretch(1)
        self.verticalLayout.addWidget(self.gridWidget)

        self.hBoxL = QHBoxLayout()
        self.hBoxL.addWidget(self.cancelFormButton)
        self.hBoxL.addWidget(self.addMaterialFormButton)
        self.hButtonL = QWidget()
        self.hButtonL.setLayout(self.hBoxL)
        
        self.verticalLayout.addWidget(self.hButtonL)
        self.verticalLayout.addStretch(1)


        self.materialPriceEdit.textChanged.connect(self.validateMaterialPrice)
        self.materialNameEdit.textChanged.connect(self.validateMaterialName)
        self.addMaterialFormButton.clicked.connect(self.validateForm)

        return self.verticalLayout





