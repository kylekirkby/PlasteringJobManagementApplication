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

        self.parent = parent
        
        self.mainLayout = self.layout()
        
        self.setLayout(self.mainLayout)

        self.setStyleSheet("QWidget[addJobClass=True]{padding:100px;}")

    def addConnection(self, connection):
        
        self.connection = connection

        return True

    def validateFirstName(self):

        text = self.jobFirstName.text()
        length = len(text)

        if length > 2:
            self.jobFirstName.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.jobFirstName.setStyleSheet("background-color:#f6989d;")
            return False

    def validateSurname(self):

        text = self.jobSurname.text()
        length = len(text)

        if length > 2:
            self.jobSurname.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.jobSurname.setStyleSheet("background-color:#f6989d;")
            return False

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


    def validatePhoneNumber(self):
        text = self.jobPhoneNumber.text()
        length = len(text)

        if length >= 11:
            self.jobPhoneNumber.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.jobPhoneNumber.setStyleSheet("background-color:#f6989d;")
            return False

    def validateEmail(self):
        text = self.jobEmail.text()

        emailRegEx = re.compile("^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$")

        match = emailRegEx.match(text)

        if match:
            self.jobEmail.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.jobEmail.setStyleSheet("background-color:#f6989d;")
            return False

    def clearForm(self):
        
        self.jobTitle.setCurrentIndex(0)
        self.jobFirstName.clear()
        self.jobSurname.clear()
        self.jobStreet.clear()
        self.jobTown.clear()
        self.jobCounty.setCurrentIndex(0)
        self.jobPostCode.clear()
        self.jobPhoneNumber.clear()
        self.jobEmail.clear()

        self.jobFirstName.setStyleSheet("background-color:#FFF;")
        self.jobSurname.setStyleSheet("background-color:#FFF;")
        self.jobStreet.setStyleSheet("background-color:#FFF;")
        self.jobTown.setStyleSheet("background-color:#FFF;")
        self.jobPostCode.setStyleSheet("background-color:#FFF;")
        self.jobPhoneNumber.setStyleSheet("background-color:#FFF;")
        self.jobEmail.setStyleSheet("background-color:#FFF;")

        self.errorTextContentLabel.setText("None")
        

    def addJobToDatabase(self):

        county = str(self.jobCounty.currentText())
        title = str(self.jobTitle.currentText())

        values = { "Title": title,
                   "FirstName": self.jobFirstName.text(),
                  "Surname": self.jobSurname.text(),
                  "Street": self.jobStreet.text(),
                  "Town": self.jobTown.text(),
                  "County": county,
                  "PostCode": self.jobPostCode.text(),
                  "Email": self.jobEmail.text(),
                   "PhoneNumber": self.jobPhoneNumber.text()}

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

        self.checkFirstName = self.validateFirstName()
        self.checkSurname = self.validateSurname()
        self.checkStreet = self.validateStreet()
        self.checkTown = self.validateTown()
        self.checkPostCode = self.validatePostCode()
        self.checkPhoneNumber = self.validatePhoneNumber()
        self.checkEmail = self.validateEmail()

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
        

        self.errorTextContentLabel.setText(self.errorMsg)
        

        if self.errorMsg == "":
            self.addJobToDatabase()
            return True
        else:
            return False
    

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

        self.jobStreet= QLineEdit()
        self.jobTown = QLineEdit()
        self.jobCounty = QComboBox()
        self.jobCounty.addItems(self.counties)
        self.jobPostCode = QLineEdit()
        
        self.jobClientEdit = QTableView()

        self.clientQueryModel = QSqlQueryModel()


        
        self.jobClientEdit.setToolTip("This is the unique ID of the client the job is for.")
        self.jobPlastererEdit = QLineEdit()

        
        self.cancelFormButton = QPushButton("Cancel")
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
        grid.addWidget(self.jobClientEdit, 5, 1)

        grid.addWidget(self.jobPlasterer, 6, 0)
        grid.addWidget(self.jobPlastererEdit, 6, 1)

        self.gridWidget = QWidget()
        self.gridWidget.setLayout(grid)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.addJobTitleText)
        self.verticalLayout.addStretch(1)
        self.verticalLayout.addWidget(self.gridWidget)

        self.hBoxL = QHBoxLayout()
        self.hBoxL.addWidget(self.cancelFormButton)
        self.hBoxL.addWidget(self.addJobFormButton)
        self.hButtonL = QWidget()
        self.hButtonL.setLayout(self.hBoxL)
        
        self.verticalLayout.addWidget(self.hButtonL)
        self.verticalLayout.addStretch(1)

        #connections
        self.jobStreet.textChanged.connect(self.validateStreet)
        self.jobTown.textChanged.connect(self.validateTown)
        self.jobPostCode.textChanged.connect(self.validatePostCode)
        self.addJobFormButton.clicked.connect(self.validateAddJobForm)



        return self.verticalLayout





