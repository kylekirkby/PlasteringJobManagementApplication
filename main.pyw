from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sys
import time

from SQLConnection import *


from ClientsMenu import *
from PlasterersMenu import *
from JobsMenu import *
from AppointmentsMenu import *
from InvoicesMenu import *
from MaterialsMenu import *

from AddClient import *
from AddPlasterer import *
from AddJob import *

from ManageClients import *
from ManagePlasterers import *
from ManageJobs import *

class MainWindow(QMainWindow):
    """ This is the main window class for the plastering job management
program """
    def __init__(self):
    
        super().__init__()

        self.setWindowTitle("Plastering Job Management Application")
        self.resize(900,800)
        self.icon = QIcon(QPixmap("./Images/icon.png"))
        self.setWindowIcon(self.icon)

        

        #Connection Attribute stores the database connection
        self.connection = None

        
        #stacked layout
        self.stackedLayout = QStackedLayout()

        self.widget = QWidget()

        self.widget.setLayout(self.stackedLayout)

        #Set the central widget to the stacked layout

        self.setCentralWidget(self.widget)
        


        #Add the Menu Bar and Main Settings Etc...
        self.mainSettings()

        #Create the Widgets
        self.initialCentralWidget()
        self.dbOpenLayout()
        self.clientsLayout()
        self.plasterersLayout()
        self.addClientLayout()
        self.addPlastererLayout()
        self.jobsLayout()
        self.manageClientsLayout()
        self.managePlasterersLayout()
        self.manageJobsLayout()
        self.addJobLayout()
        self.appointmentsLayout()
        self.invoicesLayout()
        self.materialsLayout()

        #Disable database related actions
        self.dbNotOpen()

        #Setup the PyQt Signals and Connections
        self.connections()


    def addDbConnectionsToWidgets(self):

        self.addClientL.addConnection(self.connection)
        self.addPlastererL.addConnection(self.connection)
        self.manageClientsL.addConnection(self.connection)
        self.managePlasterersL.addConnection(self.connection)
        self.addJobL.addConnection(self.connection)
        self.manageJobsL.addConnection(self.connection)

       
    def dbNotOpen(self):
        
        self.addClient.setEnabled(False)
        self.manageClients.setEnabled(False)

        self.addPlasterer.setEnabled(False)
        self.managePlasterers.setEnabled(False)

        self.addJob.setEnabled(False)
        self.viewJobs.setEnabled(False)

        self.addAppointment.setEnabled(False)
        self.manageAppointments.setEnabled(False)

        self.addInvoice.setEnabled(False)
        self.manageInvoices.setEnabled(False)

        self.newDatabase.setEnabled(True)
        self.openDatabase.setEnabled(True)
        self.closeDatabase.setEnabled(False)

        self.addMaterial.setEnabled(False)
        self.manageMaterials.setEnabled(False)

        self.stackedLayout.setCurrentIndex(0)
    
        
    def dbOpen(self):
        
        self.addClient.setEnabled(True)
        self.manageClients.setEnabled(True)

        
        self.addPlasterer.setEnabled(True)
        self.managePlasterers.setEnabled(True)

        self.addJob.setEnabled(True)
        self.viewJobs.setEnabled(True)

        self.addMaterial.setEnabled(True)
        self.manageMaterials.setEnabled(True)

        self.addAppointment.setEnabled(True)
        self.manageAppointments.setEnabled(True)

        self.addInvoice.setEnabled(True)
        self.manageInvoices.setEnabled(True)
        

        self.newDatabase.setEnabled(False)
        self.openDatabase.setEnabled(False)
        self.closeDatabase.setEnabled(True)

        self.stackedLayout.setCurrentIndex(1)

        self.addDbConnectionsToWidgets()


        
    def mainSettings(self):
        
        #actions
        self.addClient = QAction("Add Client",self)
        self.manageClients = QAction("Manage Clients",self)

        self.addPlasterer = QAction("Add Plasterer", self)
        self.managePlasterers = QAction("Manage Plasterers",self)

        self.addJob = QAction("New Job",self)
        self.viewJobs = QAction("Manage Jobs", self)

        self.help = QAction("Help",self)
        self.about = QAction("About", self)

        self.addMaterial = QAction("New Material", self)
        self.manageMaterials = QAction("Manage Materials", self)

        self.addAppointment = QAction("Add Appointment", self)
        self.manageAppointments = QAction("Manage Appointments", self)

        self.addInvoice = QAction("New Invoice", self)
        self.manageInvoices = QAction("Manage Invoices", self)
        

        self.openDatabase = QAction("Open Database", self)
        self.newDatabase = QAction("New Database", self)
        self.closeDatabase = QAction("Close Database", self)
        
        #menu bar
        self.menu = QMenuBar()

        #Database Menu
        self.databaseMenu = self.menu.addMenu("Database")
        self.databaseMenu.addAction(self.newDatabase)
        self.databaseMenu.addAction(self.openDatabase)
        self.databaseMenu.addAction(self.closeDatabase)

        #Clients Menu
        self.clientsMenu = self.menu.addMenu("Clients")
        self.clientsMenu.addAction(self.addClient)
        self.clientsMenu.addAction(self.manageClients)

        #Plasterers Menu
        self.plasterersMenu = self.menu.addMenu("Plasterers")
        self.plasterersMenu.addAction(self.addPlasterer)
        self.plasterersMenu.addAction(self.managePlasterers)

        #Materials Menu
        self.materialsMenu = self.menu.addMenu("Materials")
        self.materialsMenu.addAction(self.addMaterial)
        self.materialsMenu.addAction(self.manageMaterials)

        #Jobs Menu
        self.jobsMenu = self.menu.addMenu("Jobs")
        self.jobsMenu.addAction(self.addJob)
        self.jobsMenu.addAction(self.viewJobs)

        #Appointments Menu
        self.appointmentsMenu = self.menu.addMenu("Appointments")
        self.appointmentsMenu.addAction(self.addAppointment)
        self.appointmentsMenu.addAction(self.manageAppointments)

        #Invoices Menu
        self.invoicesMenu = self.menu.addMenu("Invoices")
        self.invoicesMenu.addAction(self.addInvoice)
        self.invoicesMenu.addAction(self.manageInvoices)





        #Help Menu
        self.helpMenu = self.menu.addMenu("Help")
        self.helpMenu.addAction(self.help)
        self.helpMenu.addAction(self.about)

        #tool bar
        self.toolBar = QToolBar()
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.addClient)
        self.toolBar.addAction(self.manageClients)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.addPlasterer)
        self.toolBar.addAction(self.managePlasterers)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.addMaterial)
        self.toolBar.addAction(self.manageMaterials)
        self.toolBar.addSeparator()
        

        self.toolBar.addAction(self.addJob)
        self.toolBar.addAction(self.viewJobs)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.addAppointment)
        self.toolBar.addAction(self.manageAppointments)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.addInvoice)
        self.toolBar.addAction(self.manageInvoices)
        self.toolBar.addSeparator()

        



        self.toolBar.setMovable(False)
        
        self.addToolBar(self.toolBar)

        self.setMenuBar(self.menu)

        self.statusBar = QStatusBar()

        self.setStatusBar(self.statusBar)
        
    def connections(self):
    
        self.about.triggered.connect(self.showAboutMessageBox)
        self.newDatabase.triggered.connect(self.createNewDatabase)
        self.openDatabase.triggered.connect(self.openDatabaseConn)
        self.closeDatabase.triggered.connect(self.closeDatabaseConn)
        self.newDbPushButton.clicked.connect(self.createNewDatabase)
        self.openDbPushButton.clicked.connect(self.openDatabaseConn)
        self.viewJobs.triggered.connect(self.switchToManageJobs)
        self.addJob.triggered.connect(self.switchToAddJob)


        self.addClient.triggered.connect(self.switchToAddClient)
        self.manageClients.triggered.connect(self.switchToManageClients)

        self.managePlasterers.triggered.connect(self.switchToManagePlasterers)
        
        self.addPlasterer.triggered.connect(self.switchToAddPlasterer)
    

        self.clientsPushButton.clicked.connect(self.switchToClientsMenu)
        self.plasterersPushButton.clicked.connect(self.switchToPlasterersMenu)


        self.clientsLayoutWidget.backButton.clicked.connect(self.switchToMainMenu)
        self.clientsLayoutWidget.addClientPushButton.clicked.connect(self.switchToAddClient)
        self.clientsLayoutWidget.manageClientsPushButton.clicked.connect(self.switchToManageClients)
        
        self.plasterersLayoutWidget.addPlastererPushButton.clicked.connect(self.switchToAddPlasterer)
        self.plasterersLayoutWidget.managePlasterersPushButton.clicked.connect(self.switchToManagePlasterers)
        self.plasterersLayoutWidget.backButton.clicked.connect(self.switchToMainMenu)

        self.jobsPushButton.clicked.connect(self.switchToJobsMenu)

        self.jobsLayoutWidget.backButton.clicked.connect(self.switchToMainMenu)
        
        self.addClientL.cancelFormButton.clicked.connect(self.switchToClientsMenu)
        self.addPlastererL.cancelFormButton.clicked.connect(self.switchToPlasterersMenu)
        self.addJobL.cancelFormButton.clicked.connect(self.switchToJobsMenu)

        self.jobsLayoutWidget.manageJobsPushButton.clicked.connect(self.switchToManageJobs)

        self.jobsLayoutWidget.addJobPushButton.clicked.connect(self.switchToAddJob)

        self.materialsPushButton.clicked.connect(self.switchToMaterialsMenu)
        self.invoicesPushButton.clicked.connect(self.switchToInvoicesMenu)
        self.appointmentsPushButton.clicked.connect(self.switchToAppointmentsMenu)

        self.appointmentsLayoutWidget.backButton.clicked.connect(self.switchToMainMenu)
        self.invoicesLayoutWidget.backButton.clicked.connect(self.switchToMainMenu)
        self.materialsLayoutWidget.backButton.clicked.connect(self.switchToMainMenu)


        
    def createNewDatabase(self):

        dialog = QFileDialog()
        dialog.setDirectory("./Data/")

        path = dialog.getSaveFileName()

        # Append extension if not there yet
        if not path.endswith(".db"):
            path += ".db"

        if self.connection:
            self.close_connection()

        if path != "":
            self.connection  = SQLConnection(path)
            self.connection.create_database()
            self.statusBar.showMessage("A new Database has been created!")
            self.dbOpen()

    def closeDatabaseConn(self):
        
        if self.connection:
            self.close_connection()
            self.statusBar.showMessage("Database has been closed.")
        else:
            self.statusBar.showMessage("No Database to close!")

    def openDatabaseConn(self):
        
        if self.connection:
            self.close_connection()

        dialog = QFileDialog()
        dialog.setDirectory("./Data/")

        path = dialog.getOpenFileName()

        # Append extension if not there yet
        if path.endswith(".db"):
            if path != "":
                self.connection = SQLConnection(path)        
                opened = self.connection.open_database()

                if opened:
                    self.dbOpen()
                    self.statusBar.showMessage("Database has been opened.")
        else:
            infoText = """This is not a correct '.db' database file!"""
            QMessageBox.warning(self, "Incorrect Database!", infoText)
        

    def close_connection(self):
        if self.connection:
            closed = self.connection.close_database()

            if closed:
                self.statusBar.showMessage("Database has been closed.")
                self.dbNotOpen()
                self.connection = None
            else:
                self.statusBar.showMessage("An error occured!")
        else:
            self.statusBar.showMessage("No Database to close.")

    def dbOpenLayout(self):

        self.setStyleSheet("""QPushButton[buttonClass=home] {
                           font-size: 16px; background-color: rgba(188, 188, 188, 50);
                           border: 1px solid rgba(188, 188, 188, 250);
                           height:100px;
                           border-radius:5px;}""")

        self.clientsPushButton = QPushButton("Clients")
        self.clientsPushButton.setProperty("buttonClass","home")
        self.clientsPushButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.plasterersPushButton = QPushButton("Plasterers")
        self.plasterersPushButton.setProperty("buttonClass","home")
        self.plasterersPushButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.jobsPushButton = QPushButton("Jobs")
        self.jobsPushButton.setProperty("buttonClass","home")
        self.jobsPushButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.materialsPushButton = QPushButton("Materials")
        self.materialsPushButton.setProperty("buttonClass","home")
        self.materialsPushButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.invoicesPushButton = QPushButton("Invoices")
        self.invoicesPushButton.setProperty("buttonClass","home")
        self.invoicesPushButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.appointmentsPushButton = QPushButton("Appointments")
        self.appointmentsPushButton.setProperty("buttonClass","home")
        self.appointmentsPushButton.setCursor(QCursor(Qt.PointingHandCursor))




        self.horizontalLayout = QHBoxLayout()

        self.horizontalLayout.addWidget(self.clientsPushButton)
        self.horizontalLayout.addWidget(self.plasterersPushButton)
        self.horizontalLayout.addWidget(self.jobsPushButton)
        

        self.hWidget1 = QWidget()
        self.hWidget1.setLayout(self.horizontalLayout)

        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.addWidget(self.materialsPushButton)
        self.horizontalLayout2.addWidget(self.invoicesPushButton)
        self.horizontalLayout2.addWidget(self.appointmentsPushButton)

        self.hWidget2 = QWidget()
        self.hWidget2.setLayout(self.horizontalLayout2)

        self.mainMenuLayout = QVBoxLayout()
        self.mainMenuLayout.addWidget(self.hWidget1)
        self.mainMenuLayout.addWidget(self.hWidget2)

        

        self.dbOpenWidget = QWidget()

        self.dbOpenWidget.setLayout(self.mainMenuLayout)

        self.stackedLayout.addWidget(self.dbOpenWidget)

        
        
    def initialCentralWidget(self):

        self.setStyleSheet("""QPushButton[buttonClass=home] {
                           font-size: 16px; background-color: rgba(188, 188, 188, 50);
                           border: 1px solid rgba(188, 188, 188, 250);
                           height:100px;
                           border-radius:5px;}""")



        self.newDbPushButton = QPushButton("New Database")
        self.newDbPushButton.setProperty("buttonClass","home")
        self.newDbPushButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.openDbPushButton = QPushButton("Open Database")
        self.openDbPushButton.setProperty("buttonClass","home")
        self.openDbPushButton.setCursor(QCursor(Qt.PointingHandCursor))





        self.mainLayout = QHBoxLayout()

        self.mainLayout.addWidget(self.newDbPushButton)
        self.mainLayout.addWidget(self.openDbPushButton)
        
        
        self.mainWidget = QWidget()

        self.mainWidget.setLayout(self.mainLayout)

        self.stackedLayout.addWidget(self.mainWidget)

    def switchToClientsMenu(self):
        self.stackedLayout.setCurrentIndex(2)

    def switchToPlasterersMenu(self):
        self.stackedLayout.setCurrentIndex(3)

    def switchToMainMenu(self):
        self.stackedLayout.setCurrentIndex(1)

    def switchToAddClient(self):
        self.stackedLayout.setCurrentIndex(4)


    def switchToAddPlasterer(self):
        self.stackedLayout.setCurrentIndex(5)

    def switchToJobsMenu(self):
        self.stackedLayout.setCurrentIndex(6)

    def switchToManageClients(self):
        self.stackedLayout.setCurrentIndex(7)
        query = self.connection.initialTable()
        
        self.manageClientsL.showResults(query)


    def switchToManagePlasterers(self):
        self.stackedLayout.setCurrentIndex(8)
        
        query = self.connection.initialTableP()

        self.managePlasterersL.showResults(query)

    def switchToManageJobs(self):
        self.stackedLayout.setCurrentIndex(9)

        query = self.connection.initialTableJ()
        self.manageJobsL.showResults(query)



    def switchToAddJob(self):
        self.stackedLayout.setCurrentIndex(10)

    def switchToAppointmentsMenu(self):
        self.stackedLayout.setCurrentIndex(11)
    def switchToInvoicesMenu(self):
        self.stackedLayout.setCurrentIndex(12)
    def switchToMaterialsMenu(self):
        self.stackedLayout.setCurrentIndex(13)
    
    
    def clientsLayout(self):
        self.clientsLayoutWidget = ClientsMenuWidget()
        self.stackedLayout.addWidget(self.clientsLayoutWidget)

    def plasterersLayout(self):
        self.plasterersLayoutWidget = PlasterersMenuWidget()
        self.stackedLayout.addWidget(self.plasterersLayoutWidget)

    def jobsLayout(self):
        self.jobsLayoutWidget = JobsMenuWidget()
        self.stackedLayout.addWidget(self.jobsLayoutWidget)




    def appointmentsLayout(self):
        self.appointmentsLayoutWidget = AppointmentMenuWidget()
        self.stackedLayout.addWidget(self.appointmentsLayoutWidget)
        
    def invoicesLayout(self):
        self.invoicesLayoutWidget = InvoicesMenuWidget()
        self.stackedLayout.addWidget(self.invoicesLayoutWidget)

    def materialsLayout(self):
        self.materialsLayoutWidget = MaterialsMenuWidget()
        self.stackedLayout.addWidget(self.materialsLayoutWidget)
        


    def manageClientsLayout(self):
        self.manageClientsL = ManageClientsWidget(self)
        self.stackedLayout.addWidget(self.manageClientsL)

    def managePlasterersLayout(self):

        self.managePlasterersL = ManagePlasterersWidget(self)
        self.stackedLayout.addWidget(self.managePlasterersL)

    def manageJobsLayout(self):
        self.manageJobsL = ManageJobsWidget(self)
        self.stackedLayout.addWidget(self.manageJobsL)
        

    def addClientLayout(self):
        self.addClientL = AddClientWidget(self)
        self.stackedLayout.addWidget(self.addClientL)

    def addPlastererLayout(self):
        self.addPlastererL = AddPlastererWidget(self)
        self.stackedLayout.addWidget(self.addPlastererL)

    def addJobLayout(self):
        self.addJobL = AddJobWidget(self)
        self.stackedLayout.addWidget(self.addJobL)
        
    def showAboutMessageBox(self):

        aboutText = """This application allows plasterers to manage their jobs and clients. \n It was developed by Kyle Kirkby using PyQt4 and Python3."""

        QMessageBox.about(self, "About", aboutText)

def showSplash():
    
    splash_pix = QPixmap('./Images/splash.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    time.sleep(2)
    splash.finish(splash)
    

if __name__ == "__main__":

    app = QApplication(sys.argv)
    showSplash()
    window = MainWindow()
    window.show()
    window.raise_()
    app.exec_()

