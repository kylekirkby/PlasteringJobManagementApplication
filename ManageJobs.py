from PyQt4.QtCore import  *
from PyQt4.QtGui import *
from PyQt4.QtSql import *


from SQLConnection import *

import re

class ManageJobsWidget(QWidget):

    """ This is the manage jobs widget """

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

        self.currentMemberId = None

        


    def layout(self):

        self.searchPlasterersGroup = QGroupBox("Search Jobs")

        self.showAllPlasterersPushButton = QPushButton("Show All Jobs")

        self.showAllPlasterersPushButton.setMaximumWidth(100)

        self.searchPlasterersLayout = QHBoxLayout()

        self.searchField = QLineEdit()
        self.searchPushButton = QPushButton("Search")

        self.searchPlasterersLayout.addWidget(self.searchField)
        self.searchPlasterersLayout.addWidget(self.searchPushButton)

        self.searchPlasterersGroup.setLayout(self.searchPlasterersLayout)

        self.searchL = QVBoxLayout()
        self.searchL.addWidget(self.searchPlasterersGroup)

        self.searchWidget = QWidget()
        self.searchWidget.setLayout(self.searchL)

        
        self.tableGroup = QGroupBox("Jobs")
        
        self.results_table = QTableView()

        self.results_table.resizeRowToContents(0)
        self.results_table.verticalHeader().setVisible(False)

        header = QHeaderView(Qt.Horizontal, self.results_table)
        header.setStretchLastSection(True)




        #self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        #set selection behaviour to select entire row at a time
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        

        self.newL = QVBoxLayout()
        self.newL.addWidget(self.results_table)
        self.newL.addWidget(self.showAllPlasterersPushButton)

        self.tableGroup.setLayout(self.newL)

        self.groupL = QVBoxLayout()
        self.groupL.addWidget(self.tableGroup)

        self.groupWidget = QWidget()
        self.groupWidget.setLayout(self.groupL)

        self.editPlastererWidget = self.editPlasterer()

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.searchWidget)
        self.vBoxLayout.addWidget(self.groupWidget)
        self.vBoxLayout.addWidget(self.editPlastererWidget)

        return self.vBoxLayout

    def editPlasterer(self):

        self.jobDetailsGroupBox = QGroupBox("Job")
        self.jobDetailsGroupBox.setEnabled(False)

        self.clientJobDetailsGroupBox = QGroupBox("Client")
        
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        
        self.errorTextLabel = QLabel("Errors: ")
        self.errorTextContentLabel = QLabel()

        self.firstNameEditLabel = QLabel("First Name")
        self.surnameEditLabel = QLabel("Surname")
        self.streetEditLabel = QLabel("Street")
        self.townEditLabel = QLabel("Town/City")
        self.countyEditLabel = QLabel("County")
        self.postCodeEditLabel = QLabel("Post Code")
        self.emailEditLabel = QLabel("Email")
        self.phoneNumberEditLabel = QLabel("Phone Number")
        
        self.firstNameLabel = QLabel()
        self.surnameLabel = QLabel()
        self.streetLabel = QLabel()
        self.townLabel = QLabel()
        self.countyLabel = QLabel()
        self.postCodeLabel = QLabel()
        self.emailLabel  = QLabel()
        self.phoneNumberLabel = QLabel()

        self.grid.addWidget(self.firstNameEditLabel, 1, 0)
        self.grid.addWidget(self.firstNameLabel, 1, 1)

        self.grid.addWidget(self.surnameEditLabel, 2, 0)
        self.grid.addWidget(self.surnameLabel, 2, 1)

        self.grid.addWidget(self.streetEditLabel, 3, 0)
        self.grid.addWidget(self.streetLabel, 3, 1)

        self.grid.addWidget(self.townEditLabel, 4, 0)
        self.grid.addWidget(self.townLabel, 4, 1)

        self.grid.addWidget(self.countyEditLabel, 5, 0)
        self.grid.addWidget(self.countyLabel, 5, 1)

        self.grid.addWidget(self.postCodeEditLabel, 6, 0)
        self.grid.addWidget(self.postCodeLabel, 6, 1)

        self.grid.addWidget(self.emailEditLabel, 7, 0)
        self.grid.addWidget(self.emailLabel, 7, 1)

        self.grid.addWidget(self.phoneNumberEditLabel, 8, 0)
        self.grid.addWidget(self.phoneNumberLabel, 8, 1)


        self.clientJobDetailsGroupBox.setLayout(self.grid)





         #job group box widgets

        self.jobInfoGroupBox = QGroupBox("Job Details")
        
        self.jobGrid = QGridLayout()
        self.jobGrid.setSpacing(10)

        

        self.jobStreetEditLabel = QLabel("Job Street")
        self.jobTownEditLabel = QLabel("Job Town")
        self.jobCountyEditLabel = QLabel("Job County")
        self.jobPostCodeEditLabel = QLabel("Job Post Code")
        
        self.jobDaysWorkedLabel = QLabel("Days worked")
        self.jobStatusLabel = QLabel("Status")

        
        self.jobStreetEdit = QLineEdit()
        self.jobTownEdit = QLineEdit()
        self.jobPostCodeEdit = QLineEdit()
        self.counties = ['Aberdeenshire', 'Angus', 'Argyll and Bute', 'Ayrshire', 'Ayrshire and Arran',
                 'Banffshire', 'Bedfordshire', 'Berkshire','Berwickshire', 'Buckinghamshire',
                 'Caithness', 'Cambridgeshire', 'Ceredigion', 'Cheshire', 'City of Bristol', 'City of Edinburgh',
                 'City of Glasgow', 'Clwyd', 'Cornwall', 'Cumbria', 'Denbighshire', 'Derbyshire', 'Devon', 'Dorset',
                 'Dumbartonshire', 'Dumfries','Durham', 'Dyfed', 'East Lothian', 'East Sussex', 'East Yorkshire', 'Essex',
                 'Ettrick and Lauderdale', 'Fife', 'Gloucestershire','Greater London', 'Greater Manchester', 'Gwent', 'Gwynedd',
                 'Hampshire', 'Herefordshire', 'Hertfordshire', 'Highlands', 'Inverness','Isle of Skye', 'Isle of Wight', 'Kent',
                 'Lanarkshire', 'Lancashire', 'Leicestershire', 'Lincolnshire', 'Merseyside', 'Mid Glamorgan','Morayshire', 'Norfolk',
                 'North Yorkshire', 'Northamptonshire', 'Northumberland', 'Nottinghamshire', 'Orkney', 'Oxfordshire', 'Perth and Kinross',
                 'Powys', 'Renfrewshire', 'Roxburgh', 'Shetland', 'Shropshire', 'Somerset', 'South Glamorgan', 'South Yorkshire', 'Staffordshire',
                 'Stirling and Falkirk', 'Suffolk', 'Surrey', 'Sutherland', 'Tweeddale', 'Tyne and Wear', 'Warwickshire', 'West Glamorgan',
                 'West Lothian', 'West Midlands', 'West Sussex', 'West Yorkshire', 'Western Isles', 'Wiltshire', 'Worcestershire']



        
        self.jobCountyEdit = QComboBox()
        self.jobCountyEdit.addItems(self.counties)

        self.jobStatusLabelContent = QLabel()
        self.jobDaysWorkedLabelContent = QLabel()
        

        self.jobGrid.addWidget(self.jobStreetEditLabel, 1, 0)
        self.jobGrid.addWidget(self.jobStreetEdit, 1, 1)

        self.jobGrid.addWidget(self.jobTownEditLabel, 2, 0)
        self.jobGrid.addWidget(self.jobTownEdit, 2, 1)

        self.jobGrid.addWidget(self.jobCountyEditLabel, 3, 0)
        self.jobGrid.addWidget(self.jobCountyEdit, 3 ,1)

        self.jobGrid.addWidget(self.jobPostCodeEditLabel, 4, 0)
        self.jobGrid.addWidget(self.jobPostCodeEdit, 4, 1)

        self.jobGrid.addWidget(self.jobStatusLabel, 5, 0)
        self.jobGrid.addWidget(self.jobStatusLabelContent, 5, 1)

        self.jobGrid.addWidget(self.jobDaysWorkedLabel, 6, 0)
        self.jobGrid.addWidget(self.jobDaysWorkedLabelContent, 6, 1)
        
        
        self.jobInfoGroupBox.setLayout(self.jobGrid)
        

        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.clientJobDetailsGroupBox)
        self.hLayout.addWidget(self.jobInfoGroupBox)
        
        self.hWidget = QWidget()
        self.hWidget.setLayout(self.hLayout)

        self.jobFunctionsGroupBox = QGroupBox("Job Actions")

        ##invoice section
        self.generateInvoicePushButton = QPushButton("Generate Invoice")
        self.viewInvoicePushButton = QPushButton("View Invoice")
        self.printInvoicePushButton = QPushButton("Print Invoice")
        self.emailInvoicePushButton = QPushButton("Email Invoice")

        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.generateInvoicePushButton)
        self.hLayout.addWidget(self.viewInvoicePushButton)
        self.hLayout.addWidget(self.printInvoicePushButton)
        self.hLayout.addWidget(self.emailInvoicePushButton)

        self.jobFunctionsGroupBox.setLayout(self.hLayout)

        
        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.jobFunctionsGroupBox)
        self.vLayout.addWidget(self.hWidget)
        

        self.jobDetailsGroupBox.setLayout(self.vLayout)




        self.newL = QVBoxLayout()

        self.newL.addWidget(self.jobDetailsGroupBox)
        

        self.userInfoEdit = QWidget()
        self.userInfoEdit.setLayout(self.newL)

        

        return self.userInfoEdit

    def searchDatabase(self):

        queryText = self.searchField.text()

        query = self.connection.getSearchQuery2(queryText)

        #print(queryText)

        self.showResults(query)
        
    def showAllPlasterersInTable(self):
        
        query = self.connection.getAllPlasterers()

        self.showResults(query)

        
    def addConnection(self, connection):
        
        self.connection = connection

        self.connections()
        
        return True

    def editingPlasterer(self):
        
        self.searchPlasterersGroup.setEnabled(False)
        self.tableGroup.setEnabled(False)

        self.editPlastererGroupBox.setEnabled(True)


    def searchingPlasterers(self):
        #clear edit form
        self.firstNameEdit.clear()
        self.surnameEdit.clear()
        self.streetEdit.clear()
        self.townEdit.clear()
        self.postCodeEdit.clear()
        self.emailEdit.clear()
        self.phoneNumberEdit.clear()
        self.dailyRateEdit.clear()

        self.firstNameEdit.setStyleSheet("")
        self.surnameEdit.setStyleSheet("")
        self.streetEdit.setStyleSheet("")
        self.townEdit.setStyleSheet("")
        self.countyEdit.setStyleSheet("")
        self.postCodeEdit.setStyleSheet("")
        self.emailEdit.setStyleSheet("")
        self.phoneNumberEdit.setStyleSheet("")
        self.dailyRateEdit.setStyleSheet("")


        self.results_table.selectionModel().clearSelection()
        
        self.searchPlasterersGroup.setEnabled(True)
        self.tableGroup.setEnabled(True)
        
        self.editPlastererGroupBox.setEnabled(False)

        
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
                data = self.connection.getPlastererData(cliID)


                self.searchPlasterersGroup.setEnabled(False)
                self.tableGroup.setEnabled(False)
                self.editPlastererGroupBox.setEnabled(True)

                self.editPlastererPopulate(data)




                            
    def editPlastererPopulate(self, data):

        currentId = data[0]
        title = data[1]
        firstName = data[2]
        surname = data[3]
        street = data[4]
        town = data[5]
        county = data[6]
        postCode = data[7]
        email = data[8]
        phoneNumber = data[9]
        dailyRate = data[10]

        self.currentMemberId = currentId

        self.titleIndex = self.titleEdit.findText(title)
        self.titleEdit.setCurrentIndex(self.titleIndex)

        self.firstNameEdit.setText(firstName)
        self.surnameEdit.setText(surname)
        self.streetEdit.setText(street)
        self.townEdit.setText(town)

        self.countyIndex = self.countyEdit.findText(county)
        self.countyEdit.setCurrentIndex(self.countyIndex)

        self.postCodeEdit.setText(postCode)
        self.emailEdit.setText(email)
        self.phoneNumberEdit.setText(phoneNumber)
        self.dailyRateEdit.setText(str(dailyRate))

        

    def showResults(self, query):
        
        self.model.setQuery(query)
        self.results_table.setModel(self.model)
        self.results_table.setSortingEnabled(True)
        self.results_table.show()

        self.results_table.selectionModel().selectionChanged.connect(self.changeFormFields)
        
    def connections(self):
        self.searchField.textChanged.connect(self.searchDatabase)
        self.showAllPlasterersPushButton.clicked.connect(self.showAllPlasterersInTable)
        #self.results_table.selectionModel().selectionChanged.connect(self.changeFormFields)


        
        self.firstNameEdit.textChanged.connect(self.validateFirstName)
        self.surnameEdit.textChanged.connect(self.validateSurname)
        self.streetEdit.textChanged.connect(self.validateStreet)
        self.townEdit.textChanged.connect(self.validateTown)
        self.postCodeEdit.textChanged.connect(self.validatePostCode)
        self.emailEdit.textChanged.connect(self.validateEmail)
        self.phoneNumberEdit.textChanged.connect(self.validatePhoneNumber)
        self.dailyRateEdit.textChanged.connect(self.validateDailyRate)
        self.savePushButton.clicked.connect(self.validateForm)
        self.cancelPushButton.clicked.connect(self.searchingPlasterers)


    def addUpdatedDataToDb(self):
        county = str(self.countyEdit.currentText())
        title = str(self.titleEdit.currentText())

        values = {"ID" : self.currentMemberId,
                    "Title": title,
                   "FirstName": self.firstNameEdit.text(),
                  "Surname": self.surnameEdit.text(),
                  "Street": self.streetEdit.text(),
                  "Town": self.townEdit.text(),
                  "County": county,
                  "PostCode": self.postCodeEdit.text(),
                  "Email": self.emailEdit.text(),
                   "PhoneNumber": self.phoneNumberEdit.text(),
                  "DailyRate" : self.dailyRateEdit.text()}

        plastererAdded = self.connection.updatePlasterer(values)

        if plastererAdded:

            self.searchingPlasterers()

            #clear the table
            query = self.connection.initialTableP()
            self.showResults(query)
             
            infoText = """ The plasterers information has been updated!"""
            QMessageBox.information(self, "Plasterer Info Updated!", infoText)
            
        else:
            infoText = """ The plasterer was not updated successfully! """

            QMessageBox.critical(self, "Plasterer Not Updated!", infoText)
        

    def validateForm(self):

        self.checkFirstName = self.validateFirstName()
        self.checkSurname = self.validateSurname()
        self.checkStreet = self.validateStreet()
        self.checkTown = self.validateTown()
        self.checkPostCode = self.validatePostCode()
        self.checkPhoneNumber = self.validatePhoneNumber()
        self.checkEmail = self.validateEmail()
        self.checkDailyRate = self.validateDailyRate()

        self.errorMsg = ""

        if self.checkFirstName == False:
            self.errorMsg += "Invalid First Name, "
        if self.checkSurname == False:
            self.errorMsg += "Invalid Surname, "
        if self.checkStreet == False:
            self.errorMsg += "Invalid Street, "
        if self.checkTown == False:
            self.errorMsg += "Invalid Town, "
        if self.checkPostCode == False:
            self.errorMsg += "Invalid Post Code Format, "
        if self.checkPhoneNumber == False:
            self.errorMsg += "Invalid Phone Number Format, "
        if self.checkEmail == False:
            self.errorMsg += "Invalid Email Format, "
        if self.checkDailyRate == False:
            self.errorMsg += "Invalid Daily Rate Format"
        

        self.errorTextContentLabel.setText(self.errorMsg)
        

        if self.errorMsg == "":
            self.addUpdatedDataToDb()
            return True
        else:
            return False

    

    def validateFirstName(self):

        text = self.firstNameEdit.text()
        length = len(text)

        if length > 2:
            self.firstNameEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.firstNameEdit.setStyleSheet("background-color:#f6989d;")
            return False

    def validateSurname(self):

        text = self.surnameEdit.text()
        length = len(text)

        if length > 2:
            self.surnameEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.surnameEdit.setStyleSheet("background-color:#f6989d;")
            return False

    def validateStreet(self):

        text = self.streetEdit.text()
        length = len(text)

        if length > 5:
            self.streetEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.streetEdit.setStyleSheet("background-color:#f6989d;")
            return False


    def validateTown(self):
        
        text = self.townEdit.text()
        length = len(text)

        if length > 3:
            self.townEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.townEdit.setStyleSheet("background-color:#f6989d;")
            return False


    def validatePostCode(self):
        
        text = self.postCodeEdit.text()

        postCodeRegEx = re.compile("[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}")

        match = postCodeRegEx.match(text.upper())

        if match:
            self.postCodeEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.postCodeEdit.setStyleSheet("background-color:#f6989d;")
            return False


    def validatePhoneNumber(self):
        text = self.phoneNumberEdit.text()
        length = len(text)

        if length == 11:
            self.phoneNumberEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.phoneNumberEdit.setStyleSheet("background-color:#f6989d;")
            return False

    def validateEmail(self):
        text = self.emailEdit.text()

        emailRegEx = re.compile("^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$")

        match = emailRegEx.match(text)

        if match:
            self.emailEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.emailEdit.setStyleSheet("background-color:#f6989d;")
            return False

    def validateDailyRate(self):
        
        text = self.dailyRateEdit.text()

        dailyRateRegEx = re.compile("[0-9]+\.[0-9]+")

        match = dailyRateRegEx.match(text.upper())

        if match:
            self.dailyRateEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.dailyRateEdit.setStyleSheet("background-color:#f6989d;")
            return False





