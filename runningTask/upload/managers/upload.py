import pandas as pd
from django.db import connection
from upload.managers.exception import InterruptException


class UploadManager:
    """ An upload manager class which interacts with the database"""

    def __init__(self, user_id, file_name="Records.csv"):
        """Constructor to intitalize some properties.

        Args:
            user_id : id of the user uploading file. 
            file_name: Name of file being uploaded.
        """
        self.user_id = user_id
        self.file_name = file_name
        self.table_name = user_id
        self.lines_read = 0
        self.is_paused = False
        self.is_terminated = False
        self.progress = 0
        self.headers = ""
        self.total_rows = 0
        super().__init__()

    # duplicate table name ko handle kar lena yaha
    def create_table(self):
        """Method to create a table and save to the database.

        Raises:
            Conflict: If a table with same name already exists.
        """
        try:
            c = connection.cursor()
            query = f'CREATE TABLE {self.table_name} (\
            Sid SERIAL PRIMARY KEY, \
            Region varchar(255), \
            Country varchar(255), \
            "Item Type" varchar(255), \
            "Sales Channel" varchar(255), \
            "Order Priority" varchar(255), \
            "Order ID" varchar(255), \
            "Units Sold" FLOAT,\
            "Unit Price" FLOAT,\
            "Unit Cost" FLOAT,\
            "Total Revenue" FLOAT,\
            "Total Cost" FLOAT,\
            "Total Profit" FLOAT\
            );'
            c.execute(query)
            df = pd.read_csv(self.file_name, skiprows=self.lines_read)
            self.headers = df.columns.to_list()
            tmp = ""
            for i in self.headers:
                if len(tmp) != 0:
                    tmp += ","
                if len(str(i).split(" ")) == 1:
                    tmp += str(i)
                else:
                    tmp += '"' + str(i) + '"'
            self.headers = tmp
        finally:
            c.close()

    def start(self):
        """
        Method to start uploading rows of csv file into database

        Raises:
            InterruptException: When the upload is paused or terminated. 
        """
        c = connection.cursor()

        self.is_paused = False
        self.is_terminated = False

        df = pd.read_csv(self.file_name, skiprows=self.lines_read)
        rows_list = [list(row) for row in df.values]

        if self.lines_read == 0:
            self.create_table()
            self.total_rows = len(df)

        for row in rows_list:
            try:
                tmp = ""
                for i in row:
                    if len(tmp) != 0:
                        tmp += ","
                    tmp += "'" + str(i) + "'"
                row = tmp
                query = f"INSERT INTO {self.table_name}({self.headers}) VALUES({row});"
                c.execute(query)
                self.lines_read += 1
                self.progress = self.lines_read / self.total_rows * 100
                status = self.check_status()
                if status:
                    raise InterruptException
            except InterruptException:
                break

    def pause(self):
        """
        Method to pause upload of rows from csv file into database. 
        """
        self.is_paused = True

    def resume(self):
        """
        Method to resume upload of rows from csv file into database. 
        """
        if self.is_terminated:
            return
        self.is_paused = False
        self.start()

    def check_status(self):
        """
        Method to check pause/terminate status.  
        """
        return self.is_paused or self.is_terminated

    def terminate(self):
        """
            Method to Rollback all the entries till now in the database. 
        """
        c = connection.cursor()
        self.is_terminated = True
        query = f"DROP TABLE IF EXISTS {self.table_name}"
        c.execute(query)

    def get_progress(self):
        """
            Method to get percentage completion of upload.
        """
        return self.progress

    def table_exists(self):
        c = connection.cursor()
        try:
            query = f"SELECT MAX(SId) from {self.table_name}"
            c.execute(query)
            return True
        except:
            return False
            
