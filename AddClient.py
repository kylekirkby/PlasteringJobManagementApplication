from PyQt4.QtCore import  *
from PyQt4.QtGui import *
from SQLConnection import *

import re

class AddClientWidget(QWidget):

    """ This is the add client widget """

    def __init__(self):

        super().__init__()
        
        self.setProperty("addClientClass","True")
        
        self.mainLayout = self.layout()
        
        self.setLayout(self.mainLayout)

        self.setStyleSheet("QWidget[addClientClass=True]{padding:100px;}")

    def validateFirstName(self):

        text = self.clientFirstName.text()
        length = len(text)

        if length > 2:
            self.clientFirstName.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.clientFirstName.setStyleSheet("background-color:#f6989d;")
            return False

    def validateSurname(self):

        text = self.clientSurname.text()
        length = len(text)

        if length > 2:
            self.clientSurname.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.clientSurname.setStyleSheet("background-color:#f6989d;")
            return False

    def validateStreet(self):

        text = self.clientStreet.text()
        length = len(text)

        if length > 5:
            self.clientStreet.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.clientStreet.setStyleSheet("background-color:#f6989d;")
            return False


    def validateTown(self):
        
        text = self.clientTown.text()
        length = len(text)

        if length > 3:
            self.clientTown.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.clientTown.setStyleSheet("background-color:#f6989d;")
            return False


    def validatePostCode(self):
        
        text = self.clientPostCode.text()

        postCodeRegEx = re.compile("[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}")

        match = postCodeRegEx.match(text.upper())

        if match:
            self.clientPostCode.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.clientPostCode.setStyleSheet("background-color:#f6989d;")
            return False


    def validatePhoneNumber(self):
        text = self.clientPhoneNumber.text()
        length = len(text)

        if length >= 11:
            self.clientPhoneNumber.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.clientPhoneNumber.setStyleSheet("background-color:#f6989d;")
            return False

    def validateEmail(self):
        text = self.clientEmail.text()

        emailRegEx = re.compile("^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$")

        match = emailRegEx.match(text)

        if match:
            self.clientEmail.setStyleSheet("background-color:#c4df9b;")
            return True
        else:
            self.clientEmail.setStyleSheet("background-color:#f6989d;")
            return False


    def validateAddClientForm(self):

        self.checkFirstName = self.validateFirstName()
        self.checkSurname = self.validateSurname()
        self.checkStreet = self.validateStreet()
        self.checkTown = self.validateTown()
        self.checkPostCode = self.validatePostCode()
        self.checkPhoneNumber = self.validatePhoneNumber()
        self.checkEmail = self.validateEmail()

        self.errorMsg = ""
        
        if self.checkFirstName == True:
            if self.checkSurname == True:
                if self.checkStreet == True:
                    if self.checkTown == True:
                        if self.checkPostCode == True:
                            if self.checkPhoneNumber == True:
                                if self.checkEmail == True:
                                    self.errorTextContentLabel.setText("No Errors Found")
                                else:
                                    #email failed
                                    self.errorTextContentLabel.setText("Email is not valid")
                            else:
                                #phone number failed
                                self.errorTextContentLabel.setText("Phone Number is not valid")
                        else:
                            #post code failed
                            self.errorTextContentLabel.setText("Post Code is not valid")
                    else:
                        #town failed
                        self.errorTextContentLabel.setText("Town is not valid")
                else:
                    #street failed
                    self.errorTextContentLabel.setText("Street is not valid")
            else:
                #surname failed
                self.errorTextContentLabel.setText("Surname is not valid")
        else:
            #first name failed
            self.errorTextContentLabel.setText("First Name is not valid")
        


    

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

        self.clientTitleLabel = QLabel('Title')
        self.clientFirstNameLabel = QLabel('First Name')
        self.clientSurnameLabel = QLabel('Surname')
        self.clientStreetLabel = QLabel('Street')
        self.clientTownLabel = QLabel('Town/City')
        self.clientCountyLabel = QLabel('County')
        self.clientPostCodeLabel = QLabel('Post Code')
        self.clientPhoneNumberLabel = QLabel('Phone Number')
        self.clientEmailLabel = QLabel('Email')

        self.clientTitle = QComboBox()
        self.titles = ["Mr","Mrs","Ms","Sir"]
        self.clientTitle.addItems(self.titles)

        self.clientFirstName = QLineEdit()
        self.clientSurname = QLineEdit()
        self.clientStreet = QLineEdit()
        self.clientTown = QLineEdit()
        self.clientCounty = QComboBox()
        self.clientCounty.addItems(self.counties)
        self.clientPostCode = QLineEdit()
        self.clientPhoneNumber = QLineEdit()
        self.clientEmail = QLineEdit()

        self.cancelFormButton = QPushButton("Cancel")
        self.addClientFormButton = QPushButton("Add Client")

        self.errorTextLabel = QLabel("Errors:")
        self.errorTextContentLabel = QLabel("None")

        self.addClientTitleText = QLabel("Add a Client")
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.addClientTitleText.setGraphicsEffect(self.shadow)
        self.addClientTitleText.setStyleSheet("font-size:20px;")



        grid = QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(self.errorTextLabel,0,0)
        grid.addWidget(self.errorTextContentLabel,0,1)
        
        grid.addWidget(self.clientTitleLabel, 1, 0)
        grid.addWidget(self.clientTitle, 1, 1)

        grid.addWidget(self.clientFirstNameLabel, 2, 0)
        grid.addWidget(self.clientFirstName, 2, 1)

        grid.addWidget(self.clientSurnameLabel, 3, 0)
        grid.addWidget(self.clientSurname, 3, 1)

        grid.addWidget(self.clientStreetLabel, 4, 0)
        grid.addWidget(self.clientStreet, 4, 1)

        grid.addWidget(self.clientTownLabel, 5, 0)
        grid.addWidget(self.clientTown, 5, 1)

        grid.addWidget(self.clientCountyLabel, 6, 0)
        grid.addWidget(self.clientCounty, 6, 1)

        grid.addWidget(self.clientPostCodeLabel, 7, 0)
        grid.addWidget(self.clientPostCode, 7, 1)

        grid.addWidget(self.clientPhoneNumberLabel, 8, 0)
        grid.addWidget(self.clientPhoneNumber, 8, 1)

        grid.addWidget(self.clientEmailLabel, 9, 0)
        grid.addWidget(self.clientEmail, 9, 1)

        self.gridWidget = QWidget()
        self.gridWidget.setLayout(grid)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.addClientTitleText)
        self.verticalLayout.addStretch(1)
        self.verticalLayout.addWidget(self.gridWidget)

        self.hBoxL = QHBoxLayout()
        self.hBoxL.addWidget(self.cancelFormButton)
        self.hBoxL.addWidget(self.addClientFormButton)
        self.hButtonL = QWidget()
        self.hButtonL.setLayout(self.hBoxL)
        
        self.verticalLayout.addWidget(self.hButtonL)
        self.verticalLayout.addStretch(1)

        #connections
        self.clientFirstName.textChanged.connect(self.validateFirstName)
        self.clientSurname.textChanged.connect(self.validateSurname)
        self.clientStreet.textChanged.connect(self.validateStreet)
        self.clientTown.textChanged.connect(self.validateTown)
        self.clientPostCode.textChanged.connect(self.validatePostCode)
        self.clientEmail.textChanged.connect(self.validateEmail)
        self.clientPhoneNumber.textChanged.connect(self.validatePhoneNumber)
        self.addClientFormButton.clicked.connect(self.validateAddClientForm)



        return self.verticalLayout





