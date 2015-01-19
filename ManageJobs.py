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
        
        self.setStyleSheet("QWidget[addjobClass=True]{padding:100px;}")

        self.mainLayout = self.layout()
        
        self.setLayout(self.mainLayout)

        self.currentMemberId = None

        


    def layout(self):

        self.searchJobsGroup = QGroupBox("Search Jobs")

        self.showAllJobsPushButton = QPushButton("Show All Jobs")

        self.showAllJobsPushButton.setMaximumWidth(100)

        self.searchJobsLayout = QHBoxLayout()

        self.searchField = QLineEdit()
        self.searchPushButton = QPushButton("Search")

        self.searchJobsLayout.addWidget(self.searchField)
        self.searchJobsLayout.addWidget(self.searchPushButton)

        self.searchJobsGroup.setLayout(self.searchJobsLayout)

        self.searchL = QVBoxLayout()
        self.searchL.addWidget(self.searchJobsGroup)

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
        self.newL.addWidget(self.showAllJobsPushButton)

        self.tableGroup.setLayout(self.newL)

        self.groupL = QVBoxLayout()
        self.groupL.addWidget(self.tableGroup)

        self.groupWidget = QWidget()
        self.groupWidget.setLayout(self.groupL)

        self.editJobWidget = self.editJob()

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.searchWidget)
        self.vBoxLayout.addWidget(self.groupWidget)
        self.vBoxLayout.addWidget(self.editJobWidget)

        return self.vBoxLayout

    def editJob(self):

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

        self.errorTextLabel = QLabel("Errors: ")        
        self.errorTextContentLabel = QLabel()
        
        self.jobStreetEditLabel = QLabel("Job Street")
        self.jobTownEditLabel = QLabel("Job Town")
        self.jobCountyEditLabel = QLabel("Job County")
        self.jobPostCodeEditLabel = QLabel("Job Post Code")
        
        self.jobDaysWorkedLabel = QLabel("Days worked")
        self.jobStatusLabel = QLabel("Status")

        self.savePushButton = QPushButton("Save Job")
        self.cancelPushButton = QPushButton("Cancel")
        
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
        
        self.jobGrid.addWidget(self.errorTextLabel, 0, 0)
        self.jobGrid.addWidget(self.errorTextContentLabel,0 ,1)
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

        
        self.jobGrid.addWidget(self.cancelPushButton, 7, 0)
        self.jobGrid.addWidget(self.savePushButton, 7, 1)
        
        
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
        
    def showAllJobsInTable(self):
        
        query = self.connection.getAllJobs()

        self.showResults(query)

        
    def addConnection(self, connection):
        
        self.connection = connection

        self.connections()
        
        return True

    def editingJob(self):
        
        self.searchJobsGroup.setEnabled(False)
        self.tableGroup.setEnabled(False)

        self.editJobGroupBox.setEnabled(True)


    def searchingJobs(self):
        #clear edit form
        self.jobStreetEdit.clear()
        self.jobTownEdit.clear()
        self.jobPostCodeEdit.clear()
        self.jobCountyEdit.setCurrentIndex(0)



        self.jobStreetEdit.setStyleSheet("")
        self.jobTownEdit.setStyleSheet("")
        self.jobCountyEdit.setStyleSheet("")
        self.jobPostCodeEdit.setStyleSheet("")



        self.results_table.selectionModel().clearSelection()
        
        self.searchJobsGroup.setEnabled(True)
        self.tableGroup.setEnabled(True)
        
        self.jobDetailsGroupBox.setEnabled(False)

        
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
                data = self.connection.getJobData(cliID)


                self.searchJobsGroup.setEnabled(False)
                self.tableGroup.setEnabled(False)
                self.jobDetailsGroupBox.setEnabled(True)

                self.editJobPopulate(data)




                            
    def editJobPopulate(self, data):

        jobCurrentIdData = data[0][0]
        jobClientIdData = data[0][1]
        jobPlastererIdData = data[0][2]
        jobInvoiceIdData = data[0][3]
        jobDescriptionData = data[0][4]
        jobStreetData = data[0][5]
        jobTownData = data[0][6]
        jobCountyData = data[0][7]
        jobPostCodeData = data[0][8]
        jobDaysWorkedData = data[0][9]
        jobCompleteData = data[0][10]

        clientFirstName = data[1][2]
        clientSurname = data[1][3]
        clientStreet = data[1][4]
        clientTown = data[1][5]
        clientCounty = data[1][6]
        clientPostCode = data[1][7]
        clientEmail = data[1][8]
        clientPhoneNumber = data[1][9]

        self.firstNameLabel.setText(clientFirstName)
        self.surnameLabel.setText(clientSurname)
        self.streetLabel.setText(clientStreet)
        self.townLabel.setText(clientTown)
        self.countyLabel.setText(clientCounty)
        self.postCodeLabel.setText(clientPostCode)
        self.emailLabel.setText(clientEmail)
        self.phoneNumberLabel.setText(clientPhoneNumber)

        self.currentMemberId = jobCurrentIdData

        self.jobStreetEdit.setText(jobStreetData)
        self.jobTownEdit.setText(jobTownData)

        self.countyIndex = self.jobCountyEdit.findText(jobCountyData)
        self.jobCountyEdit.setCurrentIndex(self.countyIndex)

        self.jobPostCodeEdit.setText(jobPostCodeData)
        self.jobStatusLabelContent.setText(jobCompleteData)
        self.jobDaysWorkedLabelContent.setText(jobDaysWorkedData)
        

        

    def showResults(self, query):
        
        self.model.setQuery(query)
        self.results_table.setModel(self.model)
        self.results_table.setSortingEnabled(True)
        self.results_table.show()

        self.results_table.selectionModel().selectionChanged.connect(self.changeFormFields)
        
    def connections(self):
        self.searchField.textChanged.connect(self.searchDatabase)
        self.showAllJobsPushButton.clicked.connect(self.showAllJobsInTable)
        #self.results_table.selectionModel().selectionChanged.connect(self.changeFormFields)


        

        self.jobStreetEdit.textChanged.connect(self.validateStreet)
        self.jobTownEdit.textChanged.connect(self.validateTown)
        self.jobPostCodeEdit.textChanged.connect(self.validatePostCode)
        self.savePushButton.clicked.connect(self.validateForm)
        self.cancelPushButton.clicked.connect(self.searchingJobs)


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

        jobAdded = self.connection.updateJob(values)

        if jobAdded:

            self.searchingJobs()

            #clear the table
            query = self.connection.initialTableP()
            self.showResults(query)
             
            infoText = """ The jobs information has been updated!"""
            QMessageBox.information(self, "Job Info Updated!", infoText)
            
        else:
            infoText = """ The job was not updated successfully! """

            QMessageBox.critical(self, "Job Not Updated!", infoText)
        

    def validateForm(self):

        self.checkStreet = self.validateStreet()
        self.checkTown = self.validateTown()
        self.checkPostCode = self.validatePostCode()


        self.errorMsg = ""

        if self.checkStreet == False:
            self.errorMsg += "Invalid Street, "
        if self.checkTown == False:
            self.errorMsg += "Invalid Town, "
        if self.checkPostCode == False:
            self.errorMsg += "Invalid Post Code Format, "

        self.errorTextContentLabel.setText(self.errorMsg)
        

        if self.errorMsg == "":
            self.addUpdatedDataToDb()
            return True
        else:
            return False

    


    def validateStreet(self):

        text = self.jobStreetEdit.text()
        length = len(text)

        if length > 5:
            self.jobStreetEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.jobStreetEdit.setStyleSheet("background-color:#f6989d;")
            return False


    def validateTown(self):
        
        text = self.jobTownEdit.text()
        length = len(text)

        if length > 3:
            self.jobTownEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.jobTownEdit.setStyleSheet("background-color:#f6989d;")
            return False


    def validatePostCode(self):
        
        text = self.jobPostCodeEdit.text()

        postCodeRegEx = re.compile("[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}")

        match = postCodeRegEx.match(text.upper())

        if match:
            self.jobPostCodeEdit.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.jobPostCodeEdit.setStyleSheet("background-color:#f6989d;")
            return False






