
from PyQt4.QtSql import *

import sqlite3

from NewDatabase import *

class SQLConnection:
    
    """Handles the conncetion to the SQL database"""
    
    def __init__(self,path):

        self.path = path

        self.db = None
        
    def create_database(self):
        
        db = create_db(self.path)

        if db == True:
        
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            self.db.setDatabaseName(self.path)

            opened_ok = self.db.open()

            return opened_ok
        
        else:
            
            return False

    
    def create_table(self,table_name,sql):
        
        with sqlite3.connect(self.path) as db:
            cursor = db.cursor()
            cursor.execute("select name from sqlite_master where name=?",(table_name,))
            result = cursor.fetchall()
            if len(result) == 1:
                pass
            else:
                cursor.execute(sql)
                db.commit()

    def open_database(self):
        
        if self.db:
            self.close_database()

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.path)

        opened_ok = self.db.open()

        return opened_ok
    
    def close_database(self):

        if self.db:
            if self.db.isOpen() == True:
                self.db.close()
                #remove the database from the QSqlDatabase object - "conn" is the default
                #database name
                QSqlDatabase.removeDatabase("conn")
                closed = self.db.open()
                self.db = None
                return True
            else:
                return False
        else:
            return False
            
    def addClient(self, values):

        query = QSqlQuery(self.db)
        
        query.prepare(""" INSERT INTO Client(ClientTitle,ClientFirstName,ClientSurname,ClientAddrLine1,
ClientAddrLine2,ClientAddrLine3,ClientAddrLine4,ClientEmail,ClientPhoneNumber) VALUES(:clientTitle,
:clientFirstName,:clientSurname,:clientStreet,:clientTown,:clientCounty,:clientPostCode,:clientEmail,
:clientPhoneNumber)""")

        query.bindValue(":clientTitle",values["Title"])
        query.bindValue(":clientFirstName",values["FirstName"])
        query.bindValue(":clientSurname",values["Surname"])
        query.bindValue(":clientStreet",values["Street"])
        query.bindValue(":clientTown",values["Town"])
        query.bindValue(":clientCounty",values["County"])
        query.bindValue(":clientPostCode",values["PostCode"])
        query.bindValue(":clientEmail",values["Email"])
        query.bindValue(":clientPhoneNumber",values["PhoneNumber"])

        success = query.exec_()

        if success:
            return True
        else:
            return False
        
##            print("Failure!")
##            error = query.lastError()
##        
##            print(error.text())


    def addPlasterer(self, values):

        query = QSqlQuery(self.db)
        
        query.prepare(""" INSERT INTO Plasterer(PlastererTitle,PlastererFirstName,PlastererSurname,PlastererAddrLine1,
PlastererAddrLine2,PlastererAddrLine3,PlastererAddrLine4,PlastererEmail,PlastererPhoneNumber,PlastererDailyRate) VALUES(:plastererTitle,
:plastererFirstName,:plastererSurname,:plastererStreet,:plastererTown,:plastererCounty,:plastererPostCode,:plastererEmail,
:plastererPhoneNumber,:plastererDailyRate)""")

        query.bindValue(":plastererTitle",values["Title"])
        query.bindValue(":plastererFirstName",values["FirstName"])
        query.bindValue(":plastererSurname",values["Surname"])
        query.bindValue(":plastererStreet",values["Street"])
        query.bindValue(":plastererTown",values["Town"])
        query.bindValue(":plastererCounty",values["County"])
        query.bindValue(":plastererPostCode",values["PostCode"])
        query.bindValue(":plastererEmail",values["Email"])
        query.bindValue(":plastererPhoneNumber",values["PhoneNumber"])
        query.bindValue(":plastererDailyRate",values["DailyRate"])

        success = query.exec_()

        if success:
            return True
        else:
            return False

    def getAllClients(self):

        query = QSqlQuery(self.db)

        query.prepare("SELECT * FROM Client")

        query.exec_()

        return query
    def initialTable(self):

        query = QSqlQuery(self.db)
        query.prepare("SELECT * FROM Client WHERE 1=0")
        query.exec_()

        return query
    
    def getClientData(self, clientID):
##
##        query = QSqlQuery(self.db)
##        query.prepare("SELECT * FROM Client WHERE ClientID = :clientId")
##        query.bindValue(":clientId", clientID)
##        query.exec_()

        with sqlite3.connect(self.path) as db:

            cursor = db.cursor()
            sql = "SELECT * FROM Client WHERE ClientID = ?"
            values = (clientID,)
            cursor.execute(sql, values)
            data = cursor.fetchone()
            db.commit()

            return data
            

        
        
    

    def getSearchQuery(self, queryText):

        searchText = queryText

        if searchText == "":
            query = self.initialTable()

            return query
        else:

            query = QSqlQuery(self.db)

            query.prepare("""SELECT * FROM Client WHERE
        ClientFirstName LIKE '%'||:searchString||'%' OR
        ClientSurname LIKE '%'||:searchString||'%' OR
        ClientAddrLine1 LIKE '%'||:searchString||'%' OR
        ClientAddrLine2 LIKE '%'||:searchString||'%' OR
        ClientAddrLine3 LIKE '%'||:searchString||'%' OR
        ClientAddrLine4 LIKE '%'||:searchString||'%' OR
        ClientPhoneNumber LIKE '%'||:searchString||'%' OR
        ClientEmail LIKE '%'||:searchString||'%'
        """)
        

            query.bindValue(":searchString", searchText)

            success = query.exec_()

            if success:
                return query
            else:
                
                error =  query.lastError()
                print(error.text())

                return query

                
    def closeEvent(self,event):
        
        self.close_database()
