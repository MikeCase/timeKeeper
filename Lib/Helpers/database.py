import sqlite3
from datetime import datetime
from pprint import pprint


class TKDB():

    def __init__(self):

        self.dbfile = 'tkdb.db'
        self.table = 'TimeClocks'
        self.fields = [
            'id',
            'clockDate',
            'clockInTime',
            'clockOutTime',
            'currentClock',
        ]
        self.create_table = f'''CREATE TABLE if not exists {self.table}(
            {self.fields[0]} INTEGER PRIMARY KEY AUTOINCREMENT, 
            {self.fields[1]} date,
            {self.fields[2]} string,
            {self.fields[3]} string NULLABLE,
            {self.fields[4]} BOOLEAN
            )'''

        self.conn = sqlite3.connect(self.dbfile)
        self.cur = self.conn.cursor()
        self.cur.execute(self.create_table)

    def clockIn(self, clocktime):
        clockInDate = clocktime.date()
        clockInTime = clocktime.time()
        currentClock = 1

        self.cur.execute(
            f"INSERT INTO {self.table} ({self.fields[1]}, {self.fields[2]}, {self.fields[4]}) VALUES (DATE('{clockInDate}'), TIME('{clockInTime}'), {currentClock})")

        self.conn.commit()

    def clockOut(self, id, clocktime):
        clockOutTime = clocktime.time()
        currentClock = 0

        self.cur.execute(
            f'''UPDATE {self.table} SET {self.fields[3]} = TIME('{clockOutTime}'),
            {self.fields[4]} = {currentClock}
            WHERE
                {self.fields[0]} = {id}
            '''
        )
        self.conn.commit()

    def getReports(self):
        """Get the report for the given time scale"""
        pass

    def getAllRecords(self):
        """Get a list of all times to show on the reports page"""
        self.cur.execute(f"SELECT * FROM {self.table}")
        records = self.cur.fetchall()

        return records
        # pprint(records)

    def getLastRecord(self):
        """ Get the last record in the db """
        self.cur.execute(
            f"SELECT * FROM {self.table} ORDER BY id DESC LIMIT 1")
        lastrecord = self.cur.fetchone()

        return lastrecord


    def getRange(self, date_range):
        
        self.cur.execute(
            f"SELECT * FROM {self.table} where clockDate BETWEEN DATE('{date_range[0]}') AND DATE('{date_range[-1]}') AND currentClock = 0"
        )
        records = self.cur.fetchall()
        
        return records