from PyQt4.QtCore import  *
from PyQt4.QtGui import *
from SQLConnection import *

import re

class AddInvoiceWidget(QWidget):

    """ This is the add invoice widget """

    def __init__(self, parent):

        super().__init__()
        
        self.setProperty("addInvoiceClass","True")

        self.connection = None

        self.model = QSqlQueryModel()
        self.materialsModel = QSqlQueryModel()

        self.currentRow = None
    

        self.parent = parent
        
        self.mainLayout = self.layout()

        self.connections()
        
        self.setLayout(self.mainLayout)

        self.setStyleSheet("QWidget[addInvoiceClass=True]{padding:100px;}")

    

    def addConnection(self, connection):
        
        self.connection = connection

        return True

    def clearForm(self):
        
        self.invoiceTitle.setCurrentIndex(0)
        self.invoiceFirstName.clear()
        self.invoiceSurname.clear()
        self.invoiceStreet.clear()
        self.invoiceTown.clear()
        self.invoiceCounty.setCurrentIndex(0)
        self.invoicePostCode.clear()
        self.invoicePhoneNumber.clear()
        self.invoiceEmail.clear()

        self.invoiceFirstName.setStyleSheet("background-color:#FFF;")
        self.invoiceSurname.setStyleSheet("background-color:#FFF;")
        self.invoiceStreet.setStyleSheet("background-color:#FFF;")
        self.invoiceTown.setStyleSheet("background-color:#FFF;")
        self.invoicePostCode.setStyleSheet("background-color:#FFF;")
        self.invoicePhoneNumber.setStyleSheet("background-color:#FFF;")
        self.invoiceEmail.setStyleSheet("background-color:#FFF;")

        self.errorTextContentLabel.setText("None")

    def showAllJobsInTable(self):
        
        query = self.connection.getAllJobs()

        self.showResults(query)

    def addInvoiceArea(self):

        pass

    def showResults(self, query):
        
        self.model.setQuery(query)
        
        self.jobSelectTable.setModel(self.model)
        self.jobSelectTable.setSortingEnabled(True)
        self.jobSelectTable.show()

        self.jobSelectTable.selectionModel().selectionChanged.connect(self.addInvoiceArea)

    def showMaterialResults(self, query):
        
        self.materialsModel.setQuery(query)
        
        self.jobMaterialsTable.setModel(self.materialsModel)
        self.jobMaterialsTable.setSortingEnabled(True)
        self.jobMaterialsTable.show()

    def connections(self):
        self.showAllJobsPushButton.clicked.connect(self.showAllJobsInTable)
        

    def addInvoiceToDatabase(self):

        county = str(self.invoiceCounty.currentText())
        title = str(self.invoiceTitle.currentText())

        values = { "Title": title,
                   "FirstName": self.invoiceFirstName.text(),
                  "Surname": self.invoiceSurname.text(),
                  "Street": self.invoiceStreet.text(),
                  "Town": self.invoiceTown.text(),
                  "County": county,
                  "PostCode": self.invoicePostCode.text(),
                  "Email": self.invoiceEmail.text(),
                   "PhoneNumber": self.invoicePhoneNumber.text()}

        invoiceAdded = self.connection.addInvoice(values)

        if invoiceAdded:

            self.clearForm()
            self.parent.switchToInvoicesMenu()
            
            infoText = """ The New invoice has been added to the database!"""
            QMessageBox.information(self, "Invoice Added", infoText)
            
        else:
            infoText = """ The New invoice was not added to the database successfully! """

            QMessageBox.critical(self, "Invoice Not Added", infoText)
            
    
    def validateAddInvoiceForm(self):
        pass


##        self.errorMsg = ""
##        
##
##        self.errorTextContentLabel.setText(self.errorMsg)
##        
##
##        if self.errorMsg == "":
##            self.addInvoiceToDatabase()
##            return True
##        else:
##            return False
    

    def layout(self):

        #Job Select Group Box

        self.jobSelectGroupBox = QGroupBox("Select a Job")

        self.jobSelectTable = QTableView()
        self.jobSelectTable.setModel(self.model)
        self.jobSelectTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.searchJobField = QLineEdit()
        self.searchJobField.setPlaceholderText("Search for a job...")

        self.showAllJobsPushButton = QPushButton("Show All Jobs")

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.jobSelectTable)
        self.vBoxLayout.addWidget(self.searchJobField)
        self.vBoxLayout.addWidget(self.showAllJobsPushButton)

        self.jobSelectGroupBox.setLayout(self.vBoxLayout)

        #Add Invoice Group Box

        self.addInvoiceGroupBox = QGroupBox("New Invoice")


        self.invoiceDetailsGroupBox = QGroupBox("Invoice Details")

        self.invoiceJobId = QLabel("Job ID: ")
        self.invoiceJobIdEdit = QLabel()
        

        self.invoiceDescription = QLabel("Description: ")
        self.invoiceDescriptionEdit = QLineEdit()

        self.invoiceDate = QLabel("Date of Invoice: ")
        self.invoiceDateEdit = QLabel()

        self.invoiceAmountPreTax = QLabel("Sub Total (Pre Tax): ")
        self.invoiceAmountPreTaxEdit = QLineEdit()

        self.invoiceAmountAfterTax = QLabel("Total: ")
        self.invoiceAmountAfterTaxEdit = QLineEdit()


        self.addInvoiceGrid = QGridLayout()

        self.addInvoiceGrid.addWidget(self.invoiceJobId, 1, 0)
        self.addInvoiceGrid.addWidget(self.invoiceJobIdEdit, 1, 1)

        self.addInvoiceGrid.addWidget(self.invoiceDescription, 2, 0)
        self.addInvoiceGrid.addWidget(self.invoiceDescriptionEdit, 2, 1)

        self.addInvoiceGrid.addWidget(self.invoiceDate, 3, 0)
        self.addInvoiceGrid.addWidget(self.invoiceDateEdit, 3, 1)

        self.addInvoiceGrid.addWidget(self.invoiceAmountPreTax , 4 ,0)
        self.addInvoiceGrid.addWidget(self.invoiceAmountPreTaxEdit, 4, 1)

        self.addInvoiceGrid.addWidget(self.invoiceAmountAfterTax , 5, 0)
        self.addInvoiceGrid.addWidget(self.invoiceAmountAfterTaxEdit, 5, 1)

    


        self.invoiceDetailsGroupBox.setLayout(self.addInvoiceGrid)
        


        #Job Details GroupBox

        self.invoiceJobDetails = QGroupBox("Job Details")

        self.invoiceJobDescription = QLabel("Job Description")
        self.invoiceJobStreet = QLabel("Job Street")
        self.invoiceJobTown = QLabel("Job Town")
        self.invoiceJobCounty = QLabel("Job County")
        self.invoiceJobPostCode = QLabel("Job Post Code")
        self.invoiceJobDaysWorked = QLabel("Job Days Worked")
        self.invoiceJobComplete = QLabel("Job Complete")

        self.invoiceJobDescriptionEdit = QLabel()
        self.invoiceJobStreetEdit = QLabel()
        self.invoiceJobTownEdit = QLabel()
        self.invoiceJobCountyEdit = QLabel()
        self.invoiceJobPostCodeEdit = QLabel()
        self.invoiceJobDaysWorkedEdit = QLabel()
        self.invoiceJobCompleteEdit = QLabel()


        self.jobDetailsGrid = QGridLayout()

        self.jobDetailsGrid.addWidget(self.invoiceJobDescription, 1, 0)
        self.jobDetailsGrid.addWidget(self.invoiceJobDescriptionEdit, 1, 1)

        self.jobDetailsGrid.addWidget(self.invoiceJobStreet, 2, 0)
        self.jobDetailsGrid.addWidget(self.invoiceJobStreetEdit, 2, 1)

        self.jobDetailsGrid.addWidget(self.invoiceJobTown, 3, 0)
        self.jobDetailsGrid.addWidget(self.invoiceJobTownEdit, 3, 1)

        self.jobDetailsGrid.addWidget(self.invoiceJobCounty, 4, 0)
        self.jobDetailsGrid.addWidget(self.invoiceJobCountyEdit, 4, 1)

        self.jobDetailsGrid.addWidget(self.invoiceJobPostCode, 5, 0)
        self.jobDetailsGrid.addWidget(self.invoiceJobPostCodeEdit, 5, 1)

        self.jobDetailsGrid.addWidget(self.invoiceJobDaysWorked, 6, 0)
        self.jobDetailsGrid.addWidget(self.invoiceJobDaysWorkedEdit, 6, 1)

        self.jobDetailsGrid.addWidget(self.invoiceJobComplete, 7, 0)
        self.jobDetailsGrid.addWidget(self.invoiceJobCompleteEdit, 7, 1)

        self.invoiceJobDetails.setLayout(self.jobDetailsGrid)

        #Client Details GroupBox
        
        self.invoiceClientDetails = QGroupBox("Client Details")

        self.invoiceClientFirstName = QLabel("First Name")
        self.invoiceClientSurname = QLabel("Surname")
        self.invoiceClientStreet  = QLabel("Street")
        self.invoiceClientTown = QLabel("Town")
        self.invoiceClientCounty = QLabel("County")
        self.invoiceClientPostCode = QLabel("Post Code")
        self.invoiceClientPhoneNumber = QLabel("Phone Number")
        self.invoiceClientEmail = QLabel("Email")
        
        self.invoiceClientFirstNameEdit = QLabel()
        self.invoiceClientSurnameEdit = QLabel()
        self.invoiceClientStreetEdit = QLabel()
        self.invoiceClientTownEdit = QLabel()
        self.invoiceClientCountyEdit = QLabel()
        self.invoiceClientPostCodeEdit = QLabel()
        self.invoiceClientPhoneNumberEdit = QLabel()
        self.invoiceClientEmailEdit = QLabel()


        #Client Grid Layout
        self.clientGrid = QGridLayout()

        self.clientGrid.addWidget(self.invoiceClientFirstName, 1, 0)
        self.clientGrid.addWidget(self.invoiceClientFirstNameEdit, 1, 1)

        self.clientGrid.addWidget(self.invoiceClientSurname, 2, 0)
        self.clientGrid.addWidget(self.invoiceClientSurnameEdit, 2, 1)

        self.clientGrid.addWidget(self.invoiceClientStreet, 3, 0)
        self.clientGrid.addWidget(self.invoiceClientStreetEdit, 3, 1)

        self.clientGrid.addWidget(self.invoiceClientTown, 4, 0)
        self.clientGrid.addWidget(self.invoiceClientTownEdit, 4, 1)

        self.clientGrid.addWidget(self.invoiceClientCounty, 5, 0)
        self.clientGrid.addWidget(self.invoiceClientCountyEdit, 5, 1)

        self.clientGrid.addWidget(self.invoiceClientPostCode, 6, 0)
        self.clientGrid.addWidget(self.invoiceClientPostCodeEdit, 6, 1)

        self.clientGrid.addWidget(self.invoiceClientPhoneNumber, 7, 0)
        self.clientGrid.addWidget(self.invoiceClientPhoneNumberEdit, 7, 1)

        self.clientGrid.addWidget(self.invoiceClientEmail, 8, 0)
        self.clientGrid.addWidget(self.invoiceClientEmailEdit, 8, 1)

        self.invoiceClientDetails.setLayout(self.clientGrid)



        #Job Materials Group Box
        self.jobMaterialsGroupBox = QGroupBox("Job Materials")

        self.jobMaterialsTable = QTableView()
        self.jobMaterialsTable.setModel(self.materialsModel)
        self.jobMaterialsTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.materialsLayout = QVBoxLayout()
        self.materialsLayout.addWidget(self.jobMaterialsTable)

        self.jobMaterialsGroupBox.setLayout(self.materialsLayout)

        #Save Buttons etc

        self.buttonLayout = QHBoxLayout()
        self.saveInvoicePushButton = QPushButton("Create Invoice")
        self.cancelInvoicePushButton = QPushButton("Cancel Invoice")
        self.buttonLayout.addWidget(self.cancelInvoicePushButton)
        self.buttonLayout.addWidget(self.saveInvoicePushButton)

        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)

        

        
        
        #Invoice Layout
        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.invoiceClientDetails)
        self.hLayout.addWidget(self.invoiceJobDetails)
        self.hWidget = QWidget()
        self.hWidget.setLayout(self.hLayout)

        

        self.invoiceEditLayout = QVBoxLayout()

        self.invoiceEditLayout.addWidget(self.invoiceDetailsGroupBox)
        self.invoiceEditLayout.addWidget(self.hWidget)
        self.invoiceEditLayout.addWidget(self.jobMaterialsGroupBox)
        self.invoiceEditLayout.addWidget(self.buttonWidget)

        self.addInvoiceGroupBox.setLayout(self.invoiceEditLayout)
        
        

        
        
        

        #Main Vertical Widget
        
        self.verticalLayout = QVBoxLayout()

        #Add Widgets to vertical layout
        self.verticalLayout.addWidget(self.jobSelectGroupBox)
        self.verticalLayout.addWidget(self.addInvoiceGroupBox)

        return self.verticalLayout





