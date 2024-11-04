import sqlite3 as sql
import time


class gantryDB:
    def connect(self):
        self.con = sql.connect('gantry.db')
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS gantry (timeStart DATETIME, timeEnd DATETIME, xAbs REAL, yAbs REAL, xRel REAL, yRel REAL)")


    def insert(self, timeStart, timeEnd, xAbs, yAbs, xRel, yRel):
        self.cur.execute("INSERT INTO gantry (timeStart, timeEnd, xAbs, yAbs, xRel, yRel) VALUES (?,?,?,?,?,?)", (timeStart, timeEnd, xAbs/1000.0, yAbs/1000.0, xRel/1000.0, yRel/1000.0))
        self.con.commit()
        
    def select(self):
        self.cur.execute("SELECT * FROM gantry")
        return self.cur.fetchall()
        
    def close(self):
        self.con.close()


if __name__ == '__main__':
   print("rainDB class can  not be used on its own")