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

        self.model = QSqlQueryModel()
        
        self.setStyleSheet("QWidget[addplastererClass=True]{padding:100px;}")

        self.mainLayout = self.layout()
        
        self.setLayout(self.mainLayout)

        self.currentMemberId = None

        


    def layout(self):

        self.mainLayout = QVBoxLayout()

        #Search For Jobs Group Box
        self.searchJobsGroupBox = QGroupBox("Select a Job")

        #View Appointments Group Box
        self.viewAppointmentsGroupBox = QGroupBox("View Appoinments")
        
        #Create Jobs Widgets
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        self.searchJobsField = QLineEdit()
        self.searchJobsField.setPlaceholderText("Search for a job...")

        #Create View Appointment Widgets
        self.appointmentDateLabel = QLabel("Appointment Date")
        self.appointmentTimeLabel = QLabel("Appointment Time")
        
        self.jobStreetLabel = QLabel("Job Street")
        self.jobTownLabel = QLabel("Job Town")
        self.jobCountyLabel = QLabel("Job County")
        self.jobPostCodeLabel = QLabel("Job Post Code")


        self.appointmentDateEdit = QCalendarWidget()
        self.appointmentTimeEdit = QTimeEdit()


        self.grid = QGridLayout()
        self.grid.addWidget(self.appointmentDateLabel, 1, 0)
        self.grid.addWidget(self.appointmentDateEdit, 1, 1)

        self.grid.addWidget(self.appointmentTimeLabel, 2, 0)
        self.grid.addWidget(self.appointmentTimeEdit, 2, 1)


        #Search Jobs Layout
        self.searchJobsLayout = QVBoxLayout()
        self.searchJobsLayout.addWidget(self.table_view)
        self.searchJobsLayout.addWidget(self.searchJobsField)

        #Edit appointment Layout
        self.editAppointmentLayout = QHBoxLayout()
        #self.editAppointmentLayout.addWidget(self.grid)
        self.viewAppointmentsGroupBox.setLayout(self.grid)
        
    

        #Add Layout to Jobs Group Box
        self.searchJobsGroupBox.setLayout(self.searchJobsLayout)

        #Add To main Layout then return to constructor
        self.mainLayout.addWidget(self.searchJobsGroupBox)
        self.mainLayout.addWidget(self.viewAppointmentsGroupBox)
        
        return self.mainLayout

    def searchDatabase(self):

        queryText = self.searchField.text()

        query = self.connection.getSearchQuery(queryText)

        self.showResults(query)
        
    def showAllJobsInTable(self):

        query = self.connection.getAllJobs()

        self.showResults(query)

        
    def addConnection(self, connection):
        
        self.connection = connection

        self.connections()
        
        return True

    def connections(self):
        pass

    def showResults(self, query):
        
        self.model.setQuery(query)
        self.table_view.setModel(self.model)
        self.table_view.show()


