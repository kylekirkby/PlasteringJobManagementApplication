from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sys
import time

from SQLConnection import *


from ClientsMenu import *
from PlasterersMenu import *
from JobsMenu import *
from AddClient import *
from AddPlasterer import *
from ManageClients import *


class MainWindow(QMainWindow):
    """ This is the main window class for the plastering job management
program """
    def __init__(self):
    
        super().__init__()

        self.setWindowTitle("Plastering Job Management Application")
        self.resize(900,800)
        self.icon = QIcon(QPixmap("./icon.png"))
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

        #Disable database related actions
        self.dbNotOpen()

        #Setup the PyQt Signals and Connections
        self.connections()


    def addDbConnectionsToWidgets(self):

        self.addClientL.addConnection(self.connection)
        self.addPlastererL.addConnection(self.connection)
        self.manageClientsL.addConnection(self.connection)

       
    def dbNotOpen(self):
        
        self.addClient.setEnabled(False)
        self.editClients.setEnabled(False)
        self.searchClients.setEnabled(False)

        self.addPlasterer.setEnabled(False)
        self.editPlasterers.setEnabled(False)
        self.viewPlasterers.setEnabled(False)

        self.addJob.setEnabled(False)
        self.viewJobs.setEnabled(False)

        self.newDatabase.setEnabled(True)
        self.openDatabase.setEnabled(True)
        self.closeDatabase.setEnabled(False)


        self.stackedLayout.setCurrentIndex(0)
    
        
    def dbOpen(self):
        
        self.addClient.setEnabled(True)
        self.editClients.setEnabled(True)
        self.searchClients.setEnabled(True)
        
        self.addPlasterer.setEnabled(True)
        self.editPlasterers.setEnabled(True)
        self.viewPlasterers.setEnabled(True)

        self.addJob.setEnabled(True)
        self.viewJobs.setEnabled(True)

        self.newDatabase.setEnabled(False)
        self.openDatabase.setEnabled(False)
        self.closeDatabase.setEnabled(True)

        self.stackedLayout.setCurrentIndex(1)

        self.addDbConnectionsToWidgets()


        
    def mainSettings(self):
        
        #actions
        self.addClient = QAction("Add Client",self)
        self.editClients = QAction("Edit Clients", self)
        self.searchClients = QAction("Search Clients", self)

        self.addPlasterer = QAction("Add Plasterer", self)
        self.editPlasterers = QAction("Edit Plasterers", self)
        self.viewPlasterers = QAction("View Plasterers", self)

        self.addJob = QAction("New Job",self)
        self.viewJobs = QAction("Manage Jobs", self)

        self.help = QAction("Help",self)
        self.about = QAction("About", self)

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
        self.clientsMenu.addAction(self.editClients)
        self.clientsMenu.addAction(self.searchClients)

        #Jobs Menu
        self.jobsMenu = self.menu.addMenu("Jobs")
        self.jobsMenu.addAction(self.addJob)
        self.jobsMenu.addAction(self.viewJobs)

        
        #Plasterers Menu
        self.plasterersMenu = self.menu.addMenu("Plasterers")
        self.plasterersMenu.addAction(self.addPlasterer)
        self.plasterersMenu.addAction(self.editPlasterers)
        self.plasterersMenu.addAction(self.viewPlasterers)

        
        #Help Menu
        self.helpMenu = self.menu.addMenu("Help")
        self.helpMenu.addAction(self.help)
        self.helpMenu.addAction(self.about)

        #tool bar
        self.toolBar = QToolBar()
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.addClient)
        self.toolBar.addAction(self.editClients)
        self.toolBar.addAction(self.searchClients)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.addPlasterer)
        self.toolBar.addAction(self.editPlasterers)
        self.toolBar.addAction(self.viewPlasterers)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.addJob)
        self.toolBar.addAction(self.viewJobs)
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


        self.addClient.triggered.connect(self.switchToAddClient)
        self.addPlasterer.triggered.connect(self.switchToAddPlasterer)

        self.clientsPushButton.clicked.connect(self.switchToClientsMenu)
        self.plasterersPushButton.clicked.connect(self.switchToPlasterersMenu)


        self.clientsLayoutWidget.backButton.clicked.connect(self.switchToMainMenu)
        self.clientsLayoutWidget.addClientPushButton.clicked.connect(self.switchToAddClient)
        self.clientsLayoutWidget.manageClientsPushButton.clicked.connect(self.switchToManageClients)
        
        self.plasterersLayoutWidget.addPlastererPushButton.clicked.connect(self.switchToAddPlasterer)
        self.plasterersLayoutWidget.backButton.clicked.connect(self.switchToMainMenu)

        self.jobsPushButton.clicked.connect(self.switchToJobsMenu)

        self.jobsLayoutWidget.backButton.clicked.connect(self.switchToMainMenu)
        
        self.addClientL.cancelFormButton.clicked.connect(self.switchToClientsMenu)
        self.addPlastererL.cancelFormButton.clicked.connect(self.switchToPlasterersMenu)


        self.manageClientsL.cancelPushButton.clicked.connect(self.switchToClientsMenu)


        
    def createNewDatabase(self):

        path = QFileDialog.getSaveFileName()

        if self.connection:
            self.close_connection()

        print(path)
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

        path = QFileDialog.getOpenFileName()

        if path != "":

            self.connection = SQLConnection(path)        
            opened = self.connection.open_database()

            if opened:
                self.dbOpen()
                self.statusBar.showMessage("Database has been opened.")
  
        

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





        self.dbOpenLayout = QHBoxLayout()

        self.dbOpenLayout.addWidget(self.clientsPushButton)
        self.dbOpenLayout.addWidget(self.plasterersPushButton)
        self.dbOpenLayout.addWidget(self.jobsPushButton)

        
        
        self.dbOpenWidget = QWidget()

        self.dbOpenWidget.setLayout(self.dbOpenLayout)

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
    
    def clientsLayout(self):
        self.clientsLayoutWidget = ClientsMenuWidget()
        self.stackedLayout.addWidget(self.clientsLayoutWidget)

    def plasterersLayout(self):
        self.plasterersLayoutWidget = PlasterersMenuWidget()
        self.stackedLayout.addWidget(self.plasterersLayoutWidget)

    def jobsLayout(self):
        self.jobsLayoutWidget = JobsMenuWidget()
        self.stackedLayout.addWidget(self.jobsLayoutWidget)


    def manageClientsLayout(self):
        self.manageClientsL = ManageClientsWidget(self)
        self.stackedLayout.addWidget(self.manageClientsL)
        



        

    def addClientLayout(self):
        self.addClientL = AddClientWidget(self)
        self.stackedLayout.addWidget(self.addClientL)

    def addPlastererLayout(self):
        self.addPlastererL = AddPlastererWidget(self)
        self.stackedLayout.addWidget(self.addPlastererL)
        
    def showAboutMessageBox(self):

        aboutText = """This application allows plasterers to manage their jobs and clients. \n It was developed by Kyle Kirkby using PyQt4 and Python3."""

        QMessageBox.about(self, "About", aboutText)

def showSplash():
    
    splash_pix = QPixmap('splash.png')
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

