from PyQt4.QtCore import  *
from PyQt4.QtGui import *
from PyQt4.QtSql import *


from SQLConnection import *

import re

class ManageClientsWidget(QWidget):

    """ This is the add plasterer widget """

    def __init__(self, parent):

        super().__init__()
        
        self.connection = None

        self.parent = parent

        self.results_table = None

        self.display = False

        self.currentRow = None

        self.model = QSqlQueryModel()
        
        self.setStyleSheet("QWidget[addplastererClass=True]{padding:100px;}")

        self.mainLayout = self.layout()
        
        self.setLayout(self.mainLayout)

        


    def layout(self):

        self.searchClientsGroup = QGroupBox("Search Clients")

        self.showAllClientsPushButton = QPushButton("Show All Clients")

        self.showAllClientsPushButton.setMaximumWidth(100)

        self.searchClientsLayout = QHBoxLayout()

        self.searchField = QLineEdit()
        self.searchPushButton = QPushButton("Search")

        self.searchClientsLayout.addWidget(self.searchField)
        self.searchClientsLayout.addWidget(self.searchPushButton)

        self.searchClientsGroup.setLayout(self.searchClientsLayout)

        self.searchL = QVBoxLayout()
        self.searchL.addWidget(self.searchClientsGroup)

        self.searchWidget = QWidget()
        self.searchWidget.setLayout(self.searchL)

        
        self.tableGroup = QGroupBox("Clients")
        
        self.results_table = QTableView()


        #set selection behaviour to select entire row at a time
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        

        self.newL = QVBoxLayout()
        self.newL.addWidget(self.results_table)
        self.newL.addWidget(self.showAllClientsPushButton)

        self.tableGroup.setLayout(self.newL)

        self.groupL = QVBoxLayout()
        self.groupL.addWidget(self.tableGroup)

        self.groupWidget = QWidget()
        self.groupWidget.setLayout(self.groupL)

        self.editClientWidget = self.editClient()

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.searchWidget)
        self.vBoxLayout.addWidget(self.groupWidget)
        self.vBoxLayout.addWidget(self.editClientWidget)

        return self.vBoxLayout

    def editClient(self):

        self.editClientGroupBox = QGroupBox("Edit Client Info")
        self.editClientGroupBox.setEnabled(False)
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.firstNameEditLabel = QLabel("First Name")
        self.surnameEditLabel = QLabel("Surname")
        self.streetEditLabel = QLabel("Street")
        self.townEditLabel = QLabel("Town/City")
        self.countyEditLabel = QLabel("County")
        self.postCodeEditLabel = QLabel("Post Code")
        self.emailEditLabel = QLabel("Email")
        self.phoneNumberEditLabel = QLabel("Phone Number")

        self.firstNameEdit = QLineEdit()
        self.surnameEdit = QLineEdit()
        self.streetEdit = QLineEdit()
        self.townEdit = QLineEdit()
        self.countyEdit = QLineEdit()
        self.postCodeEdit = QLineEdit()
        self.emailEdit = QLineEdit()
        self.phoneNumberEdit = QLineEdit()

        self.savePushButton = QPushButton("Save Info")
        self.cancelPushButton = QPushButton("Back To Menu")

        self.grid.addWidget(self.firstNameEditLabel, 1, 0)
        self.grid.addWidget(self.firstNameEdit, 1, 1)

        self.grid.addWidget(self.surnameEditLabel, 2, 0)
        self.grid.addWidget(self.surnameEdit, 2, 1)

        self.grid.addWidget(self.streetEditLabel, 3, 0)
        self.grid.addWidget(self.streetEdit, 3, 1)

        self.grid.addWidget(self.townEditLabel, 4, 0)
        self.grid.addWidget(self.townEdit, 4, 1)

        self.grid.addWidget(self.countyEditLabel, 5, 0)
        self.grid.addWidget(self.countyEdit, 5, 1)

        self.grid.addWidget(self.postCodeEditLabel, 6, 0)
        self.grid.addWidget(self.postCodeEdit, 6, 1)

        self.grid.addWidget(self.emailEditLabel, 7, 0)
        self.grid.addWidget(self.emailEdit, 7, 1)

        self.grid.addWidget(self.phoneNumberEditLabel, 8, 0)
        self.grid.addWidget(self.phoneNumberEdit, 8, 1)
        
        self.grid.addWidget(self.cancelPushButton, 9, 0)
        self.grid.addWidget(self.savePushButton, 9, 1)

        self.editClientGroupBox.setLayout(self.grid)

        self.newL = QVBoxLayout()

        self.newL.addWidget(self.editClientGroupBox)

        self.userInfoEdit = QWidget()
        self.userInfoEdit.setLayout(self.newL)

        

        return self.userInfoEdit

    def searchDatabase(self):

        queryText = self.searchField.text()

        query = self.connection.getSearchQuery(queryText)

        #print(queryText)

        self.showResults(query)
        
    def showAllClientsInTable(self):

        query = self.connection.getAllClients()

        self.showResults(query)

        
    def addConnection(self, connection):
        
        self.connection = connection

        self.connections()
        
        return True

    def changeFormFields(self):

        selectedIndexes = self.results_table.selectionModel().selection().indexes()

        rows = []

        for each in selectedIndexes:

            rowNum = each.row()

            if rowNum not in rows:
                rows.append(rowNum)

        numberOfRowsSelected = len(rows)
    
        if numberOfRowsSelected == 1:
            if self.currentRow != rows[0]:
                self.currentRow = rows[0]
                cliID = int(self.currentRow) + 1
                data = self.connection.getClientData(cliID)

                self.editClientPopulate(data)

                            
    def editClientPopulate(self, data):

        clientId = data[0]
        clientFirstName = data[1]
        clientSurname = data[2]
        street = data[3]
        town = data[4]
        county = data[5]
        postCode = data[6]
        email = data[7]
        phoneNumber = data[8]

        self.editClientGroupBox.setEnabled(True)

        self.firstNameEdit.setText(clientFirstName)
        self.surnameEdit.setText(clientSurname)
        self.streetEdit.setText(street)
        self.townEdit.setText(town)
        self.countyEdit.setText(county)
        self.postCodeEdit.setText(postCode)
        self.emailEdit.setText(email)
        self.phoneNumberEdit.setText(phoneNumber)

        

    def showResults(self, query):
        
        self.model.setQuery(query)
        self.results_table.setModel(self.model)
        self.results_table.setSortingEnabled(True)
        self.results_table.show()

        self.results_table.selectionModel().selectionChanged.connect(self.changeFormFields)
        
    def connections(self):
        self.searchField.textChanged.connect(self.searchDatabase)
        self.showAllClientsPushButton.clicked.connect(self.showAllClientsInTable)
        #self.results_table.selectionModel().selectionChanged.connect(self.changeFormFields)

        





