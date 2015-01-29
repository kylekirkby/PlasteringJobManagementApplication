from PyQt4.QtCore import  *
from PyQt4.QtGui import *
from SQLConnection import *

import re

class AddAppointmentWidget(QWidget):

    """ This is the add appointment widget """

    def __init__(self, parent):

        super().__init__()
        
        self.setProperty("addAppointmentClass","True")

        self.connection = None

        self.currentRow = None

        self.parent = parent

        self.jobTableView = QTableView()

        self.mainLayout = self.layout()
        
        self.setLayout(self.mainLayout)


        self.model = QSqlQueryModel()

        self.setStyleSheet("QWidget[addAppointmentClass=True]{padding:100px;}")

    def addConnection(self, connection):
        
        self.connection = connection
        query = self.connection.getAllJobs()
        self.showResults(query)
        
        return True

    def showAllJobs(self):
        query = self.connection.getAllJobs()
        self.showResults(query)
        return True

    def showResults(self, query):

        self.model.setQuery(query)
        self.jobTableView.setModel(self.model)
        self.jobTableView.show()

        self.jobTableView.selectionModel().selectionChanged.connect(self.getSelectedJobId)

    def searchJobsTable(self):
        queryText = self.searchJobField.text()
        query = self.connection.getSearchQueryJobs(queryText)
        self.showResults(query)
        return True


    def clearForm(self):

        self.jobTableView.clearSelection()
        #self.appointmentDateEdit.setStyleSheet("selection-background-color: rgba(0, 0, 0, 0);")
        self.appointmentDateDisplayLabel.clear()
        self.jobIDLabel.clear()
        
        self.errorTextContentLabel.setText("None")
        

    def addAppointmentToDatabase(self):

        appointmentTime = self.appointmentTimeEdit.time()

        appointmentTimeFormatted = appointmentTime.toString("HH:mm ap")

        values = { "JobId": self.jobIDLabel.text(),
                   "AppointmentDate": self.appointmentDateDisplayLabel.text(),
                  "AppointmentTime": appointmentTimeFormatted}

        appointmentAdded = self.connection.addAppointment(values)

        if appointmentAdded:

            self.clearForm()
            self.parent.switchToAppointmentsMenu()
            
            infoText = """ The New appointment has been added to the database!"""
            QMessageBox.information(self, "Appointment Added", infoText)
            
        else:
            infoText = """ The New appointment was not added to the database successfully! """

            QMessageBox.critical(self, "Appointment Not Added", infoText)
            
    

    def validateForm(self):

        self.jobIdCheck = self.jobIDLabel.text()
        self.appointmentDateCheck = self.appointmentDateDisplayLabel.text()
        

        self.errorMsg = ""

        if self.jobIdCheck == "":
            self.errorMsg += "A Job Id is needed, "
        if self.appointmentDateCheck == "":
            self.errorMsg += "Appointment Date is needed, "

        self.errorTextContentLabel.setText(self.errorMsg)
        
        if self.errorMsg == "":
            self.addAppointmentToDatabase()
            return True
        else:
            return False

    
        
    def findJobWidget(self):

        self.vBox = QVBoxLayout()

        self.jobTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.jobTableView.setToolTip("This is the unique ID of the job the appointment is for.")

        self.searchJobField = QLineEdit()
        self.searchJobField.setPlaceholderText("Search for a job...")

        self.showAllJobsPushButton = QPushButton("Show All Jobs")

        ##Show the selected job id

        self.jobID = QLabel("Job ID:")
        self.jobIDLabel = QLabel()

        self.hBox = QHBoxLayout()
        self.hBox.addWidget(self.jobID)
        self.hBox.addWidget(self.jobIDLabel)

        

        self.selectedJobWidget = QWidget()
        self.selectedJobWidget.setLayout(self.hBox)


        self.vBox.addWidget(self.jobTableView)
        self.vBox.addWidget(self.showAllJobsPushButton)
        self.vBox.addWidget(self.searchJobField)
        self.vBox.addWidget(self.selectedJobWidget)


        ##main entire widget
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.vBox)
        

        self.searchJobField.textChanged.connect(self.searchJobsTable)
        self.showAllJobsPushButton.clicked.connect(self.showAllJobs)
        
        return self.mainWidget


    def getSelectedJobId(self):

        selectedIndexes = self.jobTableView.selectionModel().selection().indexes()

        rows = []

        for each in selectedIndexes:

            rowNum = each.row()

            if rowNum not in rows:
                rows.append(rowNum)

        numberOfRowsSelected = len(rows)
    
        if numberOfRowsSelected == 1:
            if self.currentRow != rows[0]:
                self.currentRow = rows[0]
                
                jobId = self.model.record(self.currentRow).field(0).value()

                self.jobIDLabel.setText(str(jobId))

                
                
        return True

    def showAppointmentDate(self):
        dateText = self.appointmentDateEdit.selectedDate()
        dateTextFormatted = dateText.toString("ddd d MMMM yyyy")
        self.appointmentDateDisplayLabel.setText(dateTextFormatted)
        return True



    def layout(self):

        self.addAppointmentTitleText = QLabel("Add an Appointment")
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.addAppointmentTitleText.setGraphicsEffect(self.shadow)
        self.addAppointmentTitleText.setStyleSheet("font-size:20px;")

        self.appointmentJobLabel = QLabel("Job")
        self.appointmentDateLabel = QLabel("Appointment Date")
        self.appointmentTimeLabel = QLabel("Appointment Time")
        self.appointmentDateDisplayLabel = QLabel()


        self.appointmentJobEdit = self.findJobWidget()
        self.appointmentDateEdit = QCalendarWidget()
        self.appointmentTimeEdit = QTimeEdit()
        self.appointmentTimeEdit.setDisplayFormat("hh:mm")

        self.cancelFormButton = QPushButton("Cancel")
        self.addAppointmentFormButton = QPushButton("Add Appointment")

        self.errorTextLabel = QLabel("Errors: ")
        self.errorTextContentLabel = QLabel("None")
        self.errorTextContentLabel.setStyleSheet("color: red;")

        self.grid = QGridLayout()

        self.grid.addWidget(self.errorTextLabel, 0 ,0)
        self.grid.addWidget(self.errorTextContentLabel, 0, 1)

        self.grid.addWidget(self.appointmentJobLabel, 1, 0)
        self.grid.addWidget(self.appointmentJobEdit, 1, 1)

        self.grid.addWidget(self.appointmentDateLabel, 2, 0)
        self.grid.addWidget(self.appointmentDateEdit, 2, 1)

        self.grid.addWidget(self.appointmentDateDisplayLabel, 3, 1)

        self.grid.addWidget(self.appointmentTimeLabel, 4, 0)
        self.grid.addWidget(self.appointmentTimeEdit, 4, 1)

        self.grid.addWidget(self.cancelFormButton, 5, 0)
        self.grid.addWidget(self.addAppointmentFormButton, 5, 1)

        
        self.gridWidget = QWidget()
        self.gridWidget.setLayout(self.grid)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.addAppointmentTitleText)
        self.verticalLayout.addStretch(1)
        self.verticalLayout.addWidget(self.gridWidget)

        self.hBoxL = QHBoxLayout()
        self.hBoxL.addWidget(self.cancelFormButton)
        self.hBoxL.addWidget(self.addAppointmentFormButton)
        self.hButtonL = QWidget()
        self.hButtonL.setLayout(self.hBoxL)
        
        self.verticalLayout.addWidget(self.hButtonL)
        self.verticalLayout.addStretch(1)

        self.addAppointmentFormButton.clicked.connect(self.validateForm)
        self.appointmentDateEdit.selectionChanged.connect(self.showAppointmentDate)

        self.cancelFormButton.clicked.connect(self.parent.switchToAppointmentsMenu)

        return self.verticalLayout





