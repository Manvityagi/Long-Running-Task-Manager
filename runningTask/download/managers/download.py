import os

import pandas as pd
from django.db import connection

from download.managers.exception import InterruptException


class DownloadManager:
    """ An download manager class which interacts with the database"""

    def __init__(self, userId):
        """Constructor to intitalize some properties.

        Args:
            user_id : id of the user downloading file. 
        """
        self.userId = userId
        self.tableName = userId
        self.currentRow = 0
        self.isPaused = False
        self.isTerminated = False
        self.progress = 0
        self.headers = []
        self.c = connection.cursor()
        query = f"select column_name\
            from information_schema.columns\
            where table_schema = 'public' and table_name = '{self.tableName}';"
        data = self.c.execute(query)
        while True:
            data = self.c.fetchone()
        # what is this ? 
            if data == None:   
                self.headers = ",".join(self.headers)
                break
            self.headers.append(str(data[0]))
        query = f"SELECT MAX(Sid) FROM {self.tableName}"
        self.c.execute(query)
        self.total_entries = self.c.fetchone()[0]
        super().__init__()

    def start(self):
        """
        Method to start downloading rows of csv file into database

        Raises:
            InterruptException: When the download is paused or terminated. 
        """
        c = connection.cursor()
        f = None
        if self.currentRow == 0:
            f = open(f"./public/{self.tableName}.csv", "w+")
            f.write(self.headers)
        else:
            f = open(f"./public/{self.tableName}.csv", "a+")
        self.isPaused = False
        self.isTerminated = False
        while self.total_entries - self.currentRow > 0:
            try:
                if self.check_status():
                    raise InterruptException
                self.currentRow += 1
                self.progress = int(self.currentRow / self.total_entries * 100)
                query = f"SELECT * FROM {self.tableName} WHERE Sid={self.currentRow}"
                data = c.execute(query)
                data = c.fetchone()
                data = ",".join(str(e) for e in data)
                f.write("\n")
                f.write(data)
            except InterruptException:
                f.close()
                return

    def pause(self):
        """
        Method to pause download of rows from csv file into database. 
        """
        self.isPaused = True

    def resume(self):
        """
        Method to resume download of rows from csv file into database. 
        """
        if self.isTerminated:
            return
        self.isPaused = False
        self.start()

    def check_status(self):
        """
        Method to check pause/terminate status.  
        """
        return self.isPaused or self.isTerminated

    def terminate(self):
        """
            Method to Rollback all the entries till now in the database. 

            Raises: FileNotFoundError
        """
        self.isTerminated = True
        try:
            os.remove(f"./{self.tableName}.csv")
        except FileNotFoundError:
            return "Trying to delete non-existent file."

    def get_progress(self):
        """
            Method to get percentage completion of download.
        """
        return self.progress
