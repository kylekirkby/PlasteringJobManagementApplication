from PyQt4.QtCore import  *
from PyQt4.QtGui import *
from SQLConnection import *

import re

class AddJobWidget(QWidget):

    """ This is the add job widget """

    def __init__(self, parent):

        super().__init__()
        
        self.setProperty("addJobClass","True")
        self.connection = None
        self.currentRow = None
        self.currentRow2 = None

        self.model = QSqlQueryModel()
        
        self.plastererModel = QSqlQueryModel()

        self.parent = parent
        
        self.mainLayout = self.layout()
        self.setLayout(self.mainLayout)
        self.setStyleSheet("QWidget[addJobClass=True]{padding:100px;}")

    def addConnection(self, connection):
        
        self.connection = connection

        allPlasterersQuery = self.connection.getAllPlasterers()
        self.showPlastererResults(allPlasterersQuery)

        allClientsQuery = self.connection.getAllClients()        
        self.showClientResults(allClientsQuery)
    
        return True

    def searchForPlasterer(self):
        
        queryText = self.searchPlasterersField.text()
        query = self.connection.getSearchQuery2(queryText)
        self.showPlastererResults(query)

        return True

    def searchForClient(self):

        queryText = self.searchClientsField.text()
        query = self.connection.getSearchQuery(queryText)
        self.showClientResults(query)
        return True


    def validateStreet(self):

        text = self.jobStreet.text()
        length = len(text)

        if length > 5:
            self.jobStreet.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.jobStreet.setStyleSheet("background-color:#f6989d;")
            return False


    def validateTown(self):
        
        text = self.jobTown.text()
        length = len(text)

        if length > 3:
            self.jobTown.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.jobTown.setStyleSheet("background-color:#f6989d;")
            return False


    def validatePostCode(self):
        
        text = self.jobPostCode.text()

        postCodeRegEx = re.compile("[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}")

        match = postCodeRegEx.match(text.upper())

        if match:
            self.jobPostCode.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.jobPostCode.setStyleSheet("background-color:#f6989d;")
            return False


    def validateDescription(self):
        text = self.jobDescription.toPlainText()

        textLength = len(text)

        if textLength >= 3:
            self.jobDescription.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.jobDescription.setStyleSheet("background-color:#f6989d;")
            return False
        
    def clearForm(self):

        self.jobPlastererTable.clearSelection()
        self.jobClientTable.clearSelection()

        self.clientIDContent.clear()
        self.plastererIDContent.clear()
        self.jobStreet.clear()
        self.jobTown.clear()
        self.jobCounty.setCurrentIndex(0)
        self.jobPostCode.clear()
        self.jobDescription.clear()

        self.searchPlasterersField.clear()
        self.searchClientsField.clear()
        
        self.jobStreet.setStyleSheet("background-color:#FFF;")
        self.jobTown.setStyleSheet("background-color:#FFF;")
        self.jobPostCode.setStyleSheet("background-color:#FFF;")
        self.jobDescription.setStyleSheet("background-color:#FFF;")
        

        self.errorTextContentLabel.setText("None")
        

    def addJobToDatabase(self):

        county = str(self.jobCounty.currentText())

        clientID = str(self.clientIDContent.text())
        plastererID = str(self.plastererIDContent.text())

        values = {"Street": self.jobStreet.text(),
                  "Town": self.jobTown.text(),
                  "County": county,
                  "PostCode": self.jobPostCode.text(),
                  "ClientID": clientID,
                  "PlastererID": plastererID,
                  "Description": self.jobDescription.toPlainText()}

        jobAdded = self.connection.addJob(values)

        if jobAdded:

            self.clearForm()
            self.parent.switchToJobsMenu()
            
            infoText = """ The New job has been added to the database!"""
            QMessageBox.information(self, "Job Added", infoText)
            
        else:
            infoText = """ The New job was not added to the database successfully! """

            QMessageBox.critical(self, "Job Not Added", infoText)
            
    
    def validateAddJobForm(self):

        self.checkStreet = self.validateStreet()
        self.checkTown = self.validateTown()
        self.checkPostCode = self.validatePostCode()
        self.checkDescription = self.validateDescription()

        self.plastererIDText = self.plastererIDContent.text()
        self.clientIDText = self.clientIDContent.text()

        


        self.errorMsg = ""

        if self.checkStreet == False:
            self.errorMsg += "Invalid Street, "
        if self.checkTown == False:
            self.errorMsg += "Invalid Town, "
        if self.checkPostCode == False:
            self.errorMsg += "Invalid Post Code Format, "
        if self.plastererIDText == "":
            self.errorMsg += "Must choose a plasterer for the job!, "
        if self.clientIDText == "":
            self.errorMsg += "Must choose a client that the job is for!, "

        if self.checkDescription == False:
            self.errorMsg += "Description must be more than 3 characters long!, "

        

        self.errorTextContentLabel.setText(self.errorMsg)
        

        if self.errorMsg == "":
            self.addJobToDatabase()
            return True
        else:
            return False

    def showClientResults(self, query):
        
        self.model.setQuery(query)
        self.jobClientTable.setModel(self.model)
        self.jobClientTable.setSortingEnabled(True)
        self.jobClientTable.show()

        #widget connections
        self.jobClientTable.selectionModel().selectionChanged.connect(self.getSelectedClient)

    def showPlastererResults(self,query):

        self.plastererModel.setQuery(query)
        self.jobPlastererTable.setModel(self.plastererModel)
        self.jobPlastererTable.setSortingEnabled(True)
        self.jobPlastererTable.show()

        #widget connections
        self.jobPlastererTable.selectionModel().selectionChanged.connect(self.getSelectedPlasterer)

    def getSelectedClient(self):

        selectedIndexes = self.jobClientTable.selectionModel().selection().indexes()

        rows = []

        for each in selectedIndexes:
            rowNum = each.row()
            if rowNum not in rows:
                rows.append(rowNum)

        numberOfRowsSelected = len(rows)
    
        if numberOfRowsSelected == 1:
            self.currentRow = rows[0]
            #cliID = int(self.currentRow) + 1
            cliID = self.model.record(self.currentRow).field(0).value()

            self.updateSelectedClient(cliID)


    def getSelectedPlasterer(self):

        selectedIndexes = self.jobPlastererTable.selectionModel().selection().indexes()

        rows = []

        for each in selectedIndexes:
            rowNum = each.row()
            if rowNum not in rows:
                rows.append(rowNum)

        numberOfRowsSelected = len(rows)
    
        if numberOfRowsSelected == 1:
            self.currentRow2 = rows[0]
            #cliID = int(self.currentRow) + 1
            plastererID = self.plastererModel.record(self.currentRow2).field(0).value()

            self.updateSelectedPlasterer(plastererID)

    def clientTableWidget(self):

        self.vBox = QVBoxLayout()

        self.jobClientTable = QTableView()
        self.jobClientTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.jobClientTable.setModel(self.plastererModel)    
        self.jobClientTable.setToolTip("This is the unique ID of the client the job is for.")

        self.searchClientsField = QLineEdit()
        self.searchClientsField.setPlaceholderText("Search for a client...")

        ##Show the selected client id

        self.clientID = QLabel("Client ID:")
        self.clientIDContent = QLabel()

        self.hBox = QHBoxLayout()
        self.hBox.addWidget(self.clientID)
        self.hBox.addWidget(self.clientIDContent)

        self.selectedClientWidget = QWidget()
        self.selectedClientWidget.setLayout(self.hBox)


        self.vBox.addWidget(self.jobClientTable)
        self.vBox.addWidget(self.searchClientsField)
        self.vBox.addWidget(self.selectedClientWidget)


        ##main entire widget
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.vBox)

        self.searchClientsField.textChanged.connect(self.searchForClient)



        return self.mainWidget

    

    def plastererTableWidget(self):

        self.vBox = QVBoxLayout()

        self.jobPlastererTable = QTableView()
        self.jobPlastererTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.jobPlastererTable.setModel(self.model)    
        self.jobPlastererTable.setToolTip("This is the unique ID of the plasterer that will complete the job.")

        self.searchPlasterersField = QLineEdit()
        self.searchPlasterersField.setPlaceholderText("Search for a plasterer...")

        ##Show the selected client id

        self.plastererID = QLabel("Plasterer ID:")
        self.plastererIDContent = QLabel()

        self.hBox = QHBoxLayout()
        self.hBox.addWidget(self.plastererID)
        self.hBox.addWidget(self.plastererIDContent)

        self.selectedPlastererWidget = QWidget()
        self.selectedPlastererWidget.setLayout(self.hBox)


        self.vBox.addWidget(self.jobPlastererTable)
        self.vBox.addWidget(self.searchPlasterersField)
        self.vBox.addWidget(self.selectedPlastererWidget)


        ##main entire widget
        self.mainWidget2 = QWidget()
        self.mainWidget2.setLayout(self.vBox)

        self.searchPlasterersField.textChanged.connect(self.searchForPlasterer)

        return self.mainWidget2

    
        

    def updateSelectedClient(self, clientID):

        self.clientIDContent.setText(str(clientID))

    def updateSelectedPlasterer(self, plastererID):

        self.plastererIDContent.setText(str(plastererID))


    def layout(self):

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

        self.jobStreetLabel = QLabel('Street')
        self.jobTownLabel = QLabel('Town/City')
        self.jobCountyLabel = QLabel('County')
        self.jobPostCodeLabel = QLabel('Post Code')
        self.jobClient = QLabel("Job Client")
        self.jobPlasterer = QLabel("Job Plasterer")
        self.jobDescriptionLabel = QLabel("Job Description")

        self.jobStreet= QLineEdit()
        self.jobTown = QLineEdit()
        self.jobCounty = QComboBox()
        self.jobCounty.addItems(self.counties)
        self.jobPostCode = QLineEdit()
        self.jobDescription = QPlainTextEdit()


        

        self.getPlastererWidget = self.plastererTableWidget()


        self.getClientWidget = self.clientTableWidget()
        
        
        #self.getPlastererWidget = QLabel("Test")
        
        self.cancelFormButton = QPushButton("Back")
        self.clearFormButton = QPushButton("Clear Form")
        self.addJobFormButton = QPushButton("Add Job")

        self.errorTextLabel = QLabel("Errors:")
        self.errorTextContentLabel = QLabel("None")
        self.errorTextContentLabel.setStyleSheet("color: red;")


        self.addJobTitleText = QLabel("Add a Job")
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.addJobTitleText.setGraphicsEffect(self.shadow)
        self.addJobTitleText.setStyleSheet("font-size:20px;")



        grid = QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(self.errorTextLabel,0,0)
        grid.addWidget(self.errorTextContentLabel,0,1)
        
        grid.addWidget(self.jobStreetLabel, 1, 0)
        grid.addWidget(self.jobStreet, 1, 1)

        grid.addWidget(self.jobTownLabel, 2, 0)
        grid.addWidget(self.jobTown, 2, 1)

        grid.addWidget(self.jobCountyLabel, 3, 0)
        grid.addWidget(self.jobCounty, 3, 1)

        grid.addWidget(self.jobPostCodeLabel, 4, 0)
        grid.addWidget(self.jobPostCode, 4, 1)

        grid.addWidget(self.jobClient, 5, 0)
        grid.addWidget(self.getClientWidget, 5, 1)

        grid.addWidget(self.jobPlasterer, 6, 0)
        grid.addWidget(self.getPlastererWidget, 6, 1)

        grid.addWidget(self.jobDescriptionLabel, 7 ,0)
        grid.addWidget(self.jobDescription, 7, 1)

        self.gridWidget = QWidget()
        self.gridWidget.setLayout(grid)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.addJobTitleText)
        self.verticalLayout.addStretch(1)
        self.verticalLayout.addWidget(self.gridWidget)

        self.hBoxL = QHBoxLayout()
        self.hBoxL.addWidget(self.cancelFormButton)
        self.hBoxL.addWidget(self.clearFormButton)
        self.hButtonL = QWidget()
        self.hButtonL.setLayout(self.hBoxL)
        
        self.verticalLayout.addWidget(self.hButtonL)
        self.verticalLayout.addWidget(self.addJobFormButton)
        self.verticalLayout.addStretch(1)

        #connections
        self.jobStreet.textChanged.connect(self.validateStreet)
        self.jobTown.textChanged.connect(self.validateTown)
        self.jobPostCode.textChanged.connect(self.validatePostCode)
        self.jobDescription.textChanged.connect(self.validateDescription)
        self.addJobFormButton.clicked.connect(self.validateAddJobForm)
        self.clearFormButton.clicked.connect(self.clearForm)



        return self.verticalLayout





