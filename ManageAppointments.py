from PyQt4.QtCore import  *
from PyQt4.QtGui import *
from PyQt4.QtSql import *


from SQLConnection import *

import re

class ManageAppointmentsWidget(QWidget):

    """ This is the manage appointments widget """

    def __init__(self, parent):

        super().__init__()
        
        self.connection = None

        self.parent = parent

        self.results_table = None

        self.display = False

        self.currentRow = None
        self.currentRowAppointment = None
        
        self.model = QSqlQueryModel()
        
        self.selectAppointmentModel = QSqlQueryModel()
        
        self.setStyleSheet("QWidget[addplastererClass=True]{padding:100px;}")

        self.mainLayout = self.layout()
        
        self.setLayout(self.mainLayout)

        self.currentMemberId = None

    def showAppointmentData(self, data):

        appointmentId = data[0]
        jobId = data[1]
        dateString = data[2]
        timeString = data[3]

        newDate = QDate.fromString(dateString,"ddd d MMMM yyyy")
        newTime = QTime.fromString(timeString,"HH:mm ap")
        

        self.appointmentDateEdit.setSelectedDate(newDate)
        self.appointmentTimeEdit.setTime(newTime)
        
    def updateAppointment(self):
        pass

    def cancelEditAppointment(self):
        self.appointmentTimeEdit.clear()
        self.select_appointment.clearSelection()
        
        self.viewAppointmentsGroupBox.setEnabled(False)
        self.selectAppointmentGroupBox.setEnabled(True)

    def cancelSelectAppointment(self):
        self.table_view.clearSelection()
        self.select_appointment.clearSelection()


        self.searchJobsGroupBox.setEnabled(True)
        
        self.viewAppointmentsGroupBox.setEnabled(False)
        self.selectAppointmentGroupBox.setEnabled(False)
        
        


    def showAppointments(self):

        selectedIndexes = self.table_view.selectionModel().selection().indexes()
        rows = []
        for each in selectedIndexes:
            rowNum = each.row()
            if rowNum not in rows:
                rows.append(rowNum)

        numberOfRowsSelected = len(rows)
    
        if numberOfRowsSelected == 1:
            if self.currentRow != rows[0]:
                self.currentRow = rows[0]
                #cliID = int(self.currentRow) + 1
                jobId = self.model.record(self.currentRow).field(0).value()
                query = self.connection.getAppointments(jobId)

                self.showAppointmentResults(query)
            
                #Enable the select appointment widget
                self.selectAppointmentGroupBox.setEnabled(True)
                self.searchJobsGroupBox.setEnabled(False)
                self.viewAppointmentsGroupBox.setEnabled(False)
        

    def showData(self):

        selectedIndexes = self.select_appointment.selectionModel().selection().indexes()
        rows = []
        for each in selectedIndexes:
            rowNum = each.row()
            if rowNum not in rows:
                rows.append(rowNum)

        numberOfRowsSelected = len(rows)
    
        if numberOfRowsSelected == 1:
            self.currentRowAppointment = rows[0]

            appointmentId = self.selectAppointmentModel.record(self.currentRowAppointment).field(0).value()
            data = self.connection.getAppointmentData(appointmentId)

            self.showAppointmentData(data)
        
            #Enable the select appointment widget
            self.selectAppointmentGroupBox.setEnabled(False)
            self.searchJobsGroupBox.setEnabled(False)
            self.viewAppointmentsGroupBox.setEnabled(True)        


    def layout(self):

        self.mainLayout = QVBoxLayout()

        #Search For Jobs Group Box
        self.searchJobsGroupBox = QGroupBox("Select a Job")
    

        #View Appointments Group Box
        self.viewAppointmentsGroupBox = QGroupBox("View Appoinments")
        self.viewAppointmentsGroupBox.setEnabled(False)

        #Select Appointment Group Box
        self.selectAppointmentGroupBox = QGroupBox("Select Appointment")
        self.selectAppointmentGroupBox.setEnabled(False)
        
        #Create Jobs Widgets
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setModel(self.model)
        self.table_view.selectionModel().selectionChanged.connect(self.showAppointments)

        self.showAllJobsPushButton = QPushButton("Show All Jobs")

        self.searchJobsField = QLineEdit()
        self.searchJobsField.setPlaceholderText("Search for a job...")


        #Create Select appointment widgets
        self.select_appointment = QTableView()
        self.select_appointment.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.select_appointment.setModel(self.selectAppointmentModel)
        self.select_appointment.selectionModel().selectionChanged.connect(self.showData)


        self.cancelSelectAppointmentPushButton = QPushButton("Cancel")


        

        #Create View Appointment Widgets
        self.appointmentDateLabel = QLabel("Appointment Date")
        self.appointmentTimeLabel = QLabel("Appointment Time")
        
        self.jobStreetLabel = QLabel("Job Street")
        self.jobTownLabel = QLabel("Job Town")
        self.jobCountyLabel = QLabel("Job County")
        self.jobPostCodeLabel = QLabel("Job Post Code")


        self.appointmentDateEdit = QCalendarWidget()
        self.appointmentTimeEdit = QTimeEdit()
        self.appointmentTimeEdit.setDisplayFormat("hh:mm")

        self.saveAppointmentChanges = QPushButton("Save Changes")
        self.cancelAppointmentChanges = QPushButton("Cancel Changes")
        self.deleteAppointmentPushButton = QPushButton("Delete Appointment")
        



        self.grid = QGridLayout()
        self.grid.addWidget(self.appointmentDateLabel, 1, 0)
        self.grid.addWidget(self.appointmentDateEdit, 1, 1)

        self.grid.addWidget(self.appointmentTimeLabel, 2, 0)
        self.grid.addWidget(self.appointmentTimeEdit, 2, 1)

        self.grid.addWidget(self.deleteAppointmentPushButton, 3, 0)
        self.grid.addWidget(self.saveAppointmentChanges, 3, 1)
        self.grid.addWidget(self.cancelAppointmentChanges, 3, 2)


        #Search Jobs Layout
        self.searchJobsLayout = QVBoxLayout()
        self.searchJobsLayout.addWidget(self.table_view)
        self.searchJobsLayout.addWidget(self.showAllJobsPushButton)
        self.searchJobsLayout.addWidget(self.searchJobsField)
 
        #select appointment layout
        self.selectAppointmentLayout = QVBoxLayout()
        self.selectAppointmentLayout.addWidget(self.select_appointment)
        self.selectAppointmentLayout.addWidget(self.cancelSelectAppointmentPushButton)
        
        

        #Edit appointment Layout
        self.editAppointmentLayout = QHBoxLayout()
        #self.editAppointmentLayout.addWidget(self.grid)
        self.viewAppointmentsGroupBox.setLayout(self.grid)
        
        #Add Select Appointments layout to the group box
        self.selectAppointmentGroupBox.setLayout(self.selectAppointmentLayout)

        #Add Layout to Jobs Group Box
        self.searchJobsGroupBox.setLayout(self.searchJobsLayout)

        #Add To main Layout then return to constructor
        self.mainLayout.addWidget(self.searchJobsGroupBox)
        self.mainLayout.addWidget(self.selectAppointmentGroupBox)
        self.mainLayout.addWidget(self.viewAppointmentsGroupBox)
        
        return self.mainLayout

    def searchDatabase(self):

        queryText = self.searchJobsField.text()
        query = self.connection.getSearchQueryJobs(queryText)
        self.showResults(query)
        
    def showAllJobsInTable(self):

        query = self.connection.getAllJobs()
        self.showResults(query)
        
    def addConnection(self, connection):
        
        self.connection = connection
        self.connections()
        
        return True

    def connections(self):
        self.searchJobsField.textChanged.connect(self.searchDatabase)
        self.showAllJobsPushButton.clicked.connect(self.showAllJobsInTable)
        self.saveAppointmentChanges.clicked.connect(self.updateAppointment)
        self.cancelAppointmentChanges.clicked.connect(self.cancelEditAppointment)
        self.cancelSelectAppointmentPushButton.clicked.connect(self.cancelSelectAppointment)

    def showResults(self, query):
        
        self.model.setQuery(query)
        self.table_view.setModel(self.model)
        self.table_view.show()

    def showAppointmentResults(self, query):
        
        self.selectAppointmentModel.setQuery(query)
        self.select_appointment.setModel(self.selectAppointmentModel)
        self.select_appointment.show()
