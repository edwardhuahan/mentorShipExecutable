import kivy 
from kivy.config import Config
#  0 being off 1 being on as in true/false
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
import sqlite3
from kivy.uix.textinput import TextInput
import tkinter
root = tkinter.Tk()
root.withdraw()
from tkinter.filedialog import askopenfilename
import csv

LabelBase.register(name="Ostrich",
    fn_regular="ostrich-regular.ttf",
    fn_bold="OstrichSans-Bold.otf"
    )   
# https://www.youtube.com/watch?v=Y5piQF0Rh-M
# font imported to be used in the program
  
class containerLayout(GridLayout):
    def makeBaseTables(self,curs,csv1,csv2):
        # creates the base mentor and mentee table based off the CSV files
        # https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
        curs.execute("CREATE TABLE mentor (id INTEGER PRIMARY KEY,time,email,fname TEXT, lname TEXT,gend TEXT,\
                                           music TEXT,hobby TEXT,sport TEXT,eventpref TEXT,subS TEXT,subW TEXT,mentnum,session);")
        with open(csv1, 'rt') as fin:
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['Timestamp'], i['Email address'], i['First Name'], i['Last Name'], i['Please identify your gender'], i['What is your favourite genre of music? '],
                      i['What are your favourite hobbies?'], i['What are your favourite sports?'], i['If you had the choice, which of the following events and activities would you attend?'], 
                      i['What subjects are you most confident about?'], i['Thinking back to the year you came to OSA, what subject were you most concerned about? '],
                      i['Would you be willing to mentor two mentees?'], i['Please select which mentor training session you will attend. Please keep in mind that all three of these sessions are going to be after school from 3:40-5:30 in the library. ']) for i in dr]
        curs.executemany(
            "INSERT INTO mentor (time,email,fname,lname,gend,music,hobby,sport,eventPref,subS,subW,mentnum,session)\
             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db)
        
        curs.execute(
            "CREATE TABLE mentee (id INTEGER PRIMARY KEY,time,fname TEXT,lname TEXT,email,session,school,gend TEXT,gendpref TEXT,\
                                  music TEXT,hobby TEXT,sport TEXT,eventPref TEXT,subS TEXT,subW TEXT,sp);")
        with open(csv2, 'rt') as fin:
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['Timestamp'], i['Student First Name'], i['Student Last Name'], i['Email address'], i['Please select a session'], 
                      i['What school do you currently attend?'],i['Please identify your gender'],i['Please select the gender of mentor that you would be comfortable being matched with.'], 
                      i['What is your favourite genre of music? '], i['What are your favourite hobbies?'], i['What are your favourite sports?'], 
                      i['If you had the choice, which of the following events and activities would you attend?'], i['What subjects are you most confident about?'],
                      i['What subject worries you the most for next year?'],i['Student Planners are available at a cost of $10 (cash). If you wish to order one, please indicate below:']) for i in dr]
        curs.executemany(
            "INSERT INTO mentee (time,fname,lname,email,session,school,gend,gendpref,music,hobby,sport,eventpref,subS,subW,sp)\
             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db)
        
    def OkButton(self, widget1,widget2,widget3):
        #takes the the CSV filepaths and throws it to makeBaseTables
        self.text=widget2.text+'.db'
        for i in [widget1,widget2]:
            i.disabled=True
        widget3.disabled=False
        conn=sqlite3.connect(self.text)
        c = conn.cursor()
        root = tkinter.Tk()
        root.withdraw()
        csv1_filepath = askopenfilename(title="Choose the mentors' CSV file",filetypes = [("CSV files", "*.csv")])
        root = tkinter.Tk()
        root.withdraw()
        csv2_filepath = askopenfilename(title="Choose the mentees' CSV file",filetypes = [("CSV files", "*.csv")])
        self.makeBaseTables(c,csv1_filepath,csv2_filepath)

        conn.commit()
        conn.close()

    def create(self,widget1,widget2,widget3):
        #opens up the text input and Ok button
        widget1.disabled=True
        for i in [widget2,widget3]:
            i.disabled=False

    def creatinTablesForTheButtons(self,c,stringa,weighting):
        #weighting adds a different number to countMatched depending on sorting aspect 
        # https://stackoverflow.com/questions/973541/how-to-set-sqlite3-to-be-case-insensitive-when-string-comparing
        # http://www.sqlitetutorial.net/sqlite-left-join/ 
        c.execute("CREATE VIEW vw_%s1b AS SELECT mentor_id,b.genderpref_id,b.%s1, CASE WHEN b.%s1 ='' THEN 0 WHEN b.%s1 = 'Other' THEN 0 WHEN b.%s1 IS NOT null THEN %d ELSE 0 END AS countMatched FROM mentor_boy AS a LEFT OUTER JOIN gendpref_boy AS b ON b.%s1 = a.%s1 COLLATE NOCASE OR b.%s1 = a.%s2 COLLATE NOCASE OR b.%s1 = a.%s3 COLLATE NOCASE"%(stringa,stringa,stringa,stringa,stringa,weighting,stringa,stringa,stringa,stringa,stringa,stringa))
        c.execute("CREATE VIEW vw_%s2b AS SELECT mentor_id,b.genderpref_id,b.%s2, CASE WHEN b.%s2 ='' THEN 0 WHEN b.%s2 = 'Other' THEN 0 WHEN b.%s2 IS NOT null THEN %d ELSE 0 END AS countMatched FROM mentor_boy AS a LEFT OUTER JOIN gendpref_boy AS b ON b.%s2 = a.%s1 COLLATE NOCASE OR b.%s2 = a.%s2 COLLATE NOCASE OR b.%s2 = a.%s3 COLLATE NOCASE"%(stringa,stringa,stringa,stringa,stringa,weighting,stringa,stringa,stringa,stringa,stringa,stringa))
        c.execute("CREATE VIEW vw_%s3b AS SELECT mentor_id,b.genderpref_id,b.%s3, CASE WHEN b.%s3 ='' THEN 0 WHEN b.%s3 = 'Other' THEN 0 WHEN b.%s3 IS NOT null THEN %d ELSE 0 END AS countMatched FROM mentor_boy AS a LEFT OUTER JOIN gendpref_boy AS b ON b.%s3 = a.%s1 COLLATE NOCASE OR b.%s3 = a.%s2 COLLATE NOCASE OR b.%s3 = a.%s3 COLLATE NOCASE"%(stringa,stringa,stringa,stringa,stringa,weighting,stringa,stringa,stringa,stringa,stringa,stringa))
        
        c.execute("CREATE VIEW vw_%s1g AS SELECT mentor_id,b.genderpref_id,b.%s1, CASE WHEN b.%s1 ='' THEN 0 WHEN b.%s1 = 'Other' THEN 0 WHEN b.%s1 IS NOT null THEN %d ELSE 0 END AS countMatched FROM mentor_girl AS a LEFT OUTER JOIN gendpref_girl AS b ON b.%s1 = a.%s1 COLLATE NOCASE OR b.%s1 = a.%s2 COLLATE NOCASE OR b.%s1 = a.%s3 COLLATE NOCASE"%(stringa,stringa,stringa,stringa,stringa,weighting,stringa,stringa,stringa,stringa,stringa,stringa))
        c.execute("CREATE VIEW vw_%s2g AS SELECT mentor_id,b.genderpref_id,b.%s2, CASE WHEN b.%s2 ='' THEN 0 WHEN b.%s2 = 'Other' THEN 0 WHEN b.%s2 IS NOT null THEN %d ELSE 0 END AS countMatched FROM mentor_girl AS a LEFT OUTER JOIN gendpref_girl AS b ON b.%s2 = a.%s1 COLLATE NOCASE OR b.%s2 = a.%s2 COLLATE NOCASE OR b.%s2 = a.%s3 COLLATE NOCASE"%(stringa,stringa,stringa,stringa,stringa,weighting,stringa,stringa,stringa,stringa,stringa,stringa))
        c.execute("CREATE VIEW vw_%s3g AS SELECT mentor_id,b.genderpref_id,b.%s3, CASE WHEN b.%s3 ='' THEN 0 WHEN b.%s3 = 'Other' THEN 0 WHEN b.%s3 IS NOT null THEN %d ELSE 0 END AS countMatched FROM mentor_girl AS a LEFT OUTER JOIN gendpref_girl AS b ON b.%s3 = a.%s1 COLLATE NOCASE OR b.%s3 = a.%s2 COLLATE NOCASE OR b.%s3 = a.%s3 COLLATE NOCASE"%(stringa,stringa,stringa,stringa,stringa,weighting,stringa,stringa,stringa,stringa,stringa,stringa))

        c.execute("CREATE VIEW vw_%s1n AS SELECT mentor_id,b.genderpref_id,b.%s1, CASE WHEN b.%s1 ='' THEN 0 WHEN b.%s1 = 'Other' THEN 0 WHEN b.%s1 IS NOT null THEN %d ELSE 0 END AS countMatched FROM mentor_n AS a LEFT OUTER JOIN gendpref_n AS b ON b.%s1 = a.%s1 COLLATE NOCASE OR b.%s1 = a.%s2 COLLATE NOCASE OR b.%s1 = a.%s3 COLLATE NOCASE"%(stringa,stringa,stringa,stringa,stringa,weighting,stringa,stringa,stringa,stringa,stringa,stringa))
        c.execute("CREATE VIEW vw_%s2n AS SELECT mentor_id,b.genderpref_id,b.%s2, CASE WHEN b.%s2 ='' THEN 0 WHEN b.%s2 = 'Other' THEN 0 WHEN b.%s2 IS NOT null THEN %d ELSE 0 END AS countMatched FROM mentor_n AS a LEFT OUTER JOIN gendpref_n AS b ON b.%s2 = a.%s1 COLLATE NOCASE OR b.%s2 = a.%s2 COLLATE NOCASE OR b.%s2 = a.%s3 COLLATE NOCASE"%(stringa,stringa,stringa,stringa,stringa,weighting,stringa,stringa,stringa,stringa,stringa,stringa))
        c.execute("CREATE VIEW vw_%s3n AS SELECT mentor_id,b.genderpref_id,b.%s3, CASE WHEN b.%s3 ='' THEN 0 WHEN b.%s3 = 'Other' THEN 0 WHEN b.%s3 IS NOT null THEN %d ELSE 0 END AS countMatched FROM mentor_n AS a LEFT OUTER JOIN gendpref_n AS b ON b.%s3 = a.%s1 COLLATE NOCASE OR b.%s3 = a.%s2 COLLATE NOCASE OR b.%s3 = a.%s3 COLLATE NOCASE"%(stringa,stringa,stringa,stringa,stringa,weighting,stringa,stringa,stringa,stringa,stringa,stringa))

    def generateReport(self,widget):
        # https://www.w3resource.com/sqlite/sqlite-select-query-statement.php
        conn=sqlite3.connect(self.text)
        c = conn.cursor()
        c.execute("CREATE TABLE reportb AS SELECT G.mentor_id,G.genderpref_id, SUM(countMatched) AS CountMatched FROM \
                    (SELECT mentor_id,genderpref_id,hobby1,countMatched FROM vw_hobby1b UNION \
                        SELECT mentor_id, genderpref_id, hobby2, countMatched FROM vw_hobby2b UNION \
                        SELECT mentor_id, genderpref_id, hobby3, countMatched FROM vw_hobby3b UNION \
                        SELECT mentor_id, genderpref_id, sport1, countMatched FROM vw_sport1b UNION \
                        SELECT mentor_id, genderpref_id, sport2, countMatched FROM vw_sport2b UNION \
                        SELECT mentor_id, genderpref_id, sport3, countMatched FROM vw_sport3b UNION \
                        SELECT mentor_id, genderpref_id, music1, countMatched FROM vw_music1b UNION \
                        SELECT mentor_id, genderpref_id, music2, countMatched FROM vw_music2b UNION \
                        SELECT mentor_id, genderpref_id, music3, countMatched FROM vw_music3b UNION \
                        SELECT mentor_id, genderpref_id, eventpref1, countMatched FROM vw_eventpref1b UNION \
                        SELECT mentor_id, genderpref_id, eventpref2, countMatched FROM vw_eventpref2b UNION \
                        SELECT mentor_id, genderpref_id, eventpref3, countMatched FROM vw_eventpref3b UNION \
                        SELECT mentor_id, genderpref_id, subS1, countMatched FROM vw_subS1b UNION \
                        SELECT mentor_id, genderpref_id, subS2, countMatched FROM vw_subS2b UNION \
                        SELECT mentor_id, genderpref_id, subW, countMatched FROM vw_subWb \
                        ) AS G GROUP BY G.mentor_id, G.genderpref_id ORDER BY G.mentor_id, G.genderpref_id")
        
        c.execute("CREATE TABLE reportg AS SELECT G.mentor_id,G.genderpref_id, SUM(countMatched) AS CountMatched FROM \
                    (SELECT mentor_id, genderpref_id, hobby1, countMatched FROM vw_hobby1g UNION \
                        SELECT mentor_id, genderpref_id, hobby2, countMatched FROM vw_hobby2g UNION \
                        SELECT mentor_id, genderpref_id, hobby3, countMatched FROM vw_hobby3g UNION \
                        SELECT mentor_id, genderpref_id, sport1, countMatched FROM vw_sport1g UNION \
                        SELECT mentor_id, genderpref_id, sport2, countMatched FROM vw_sport2g UNION \
                        SELECT mentor_id, genderpref_id, sport3, countMatched FROM vw_sport3g UNION \
                        SELECT mentor_id, genderpref_id, music1, countMatched FROM vw_music1g UNION \
                        SELECT mentor_id, genderpref_id, music2, countMatched FROM vw_music2g UNION \
                        SELECT mentor_id, genderpref_id, music3, countMatched FROM vw_music3g UNION \
                        SELECT mentor_id, genderpref_id, eventpref1, countMatched FROM vw_eventpref1g UNION \
                        SELECT mentor_id, genderpref_id, eventpref2, countMatched FROM vw_eventpref2g UNION \
                        SELECT mentor_id, genderpref_id, eventpref3, countMatched FROM vw_eventpref3g UNION \
                        SELECT mentor_id, genderpref_id, subS1, countMatched FROM vw_subS1g UNION \
                        SELECT mentor_id, genderpref_id, subS2, countMatched FROM vw_subS2g UNION \
                        SELECT mentor_id, genderpref_id, subW, countMatched FROM vw_subWg \
                        ) AS G GROUP BY G.mentor_id, G.genderpref_id ORDER BY G.mentor_id, G.genderpref_id")

        c.execute("CREATE TABLE reportn AS SELECT G.mentor_id,G.genderpref_id, SUM(countMatched) AS CountMatched FROM \
                    (SELECT mentor_id, genderpref_id, hobby1, countMatched FROM vw_hobby1n UNION \
                        SELECT mentor_id, genderpref_id, hobby2, countMatched FROM vw_hobby2n UNION \
                        SELECT mentor_id, genderpref_id, hobby3, countMatched FROM vw_hobby3n UNION \
                        SELECT mentor_id, genderpref_id, sport1, countMatched FROM vw_sport1n UNION \
                        SELECT mentor_id, genderpref_id, sport2, countMatched FROM vw_sport2n UNION \
                        SELECT mentor_id, genderpref_id, sport3, countMatched FROM vw_sport3n UNION \
                        SELECT mentor_id, genderpref_id, music1, countMatched FROM vw_music1n UNION \
                        SELECT mentor_id, genderpref_id, music2, countMatched FROM vw_music2n UNION \
                        SELECT mentor_id, genderpref_id, music3, countMatched FROM vw_music3n UNION \
                        SELECT mentor_id, genderpref_id, eventpref1, countMatched FROM vw_eventpref1n UNION \
                        SELECT mentor_id, genderpref_id, eventpref2, countMatched FROM vw_eventpref2n UNION \
                        SELECT mentor_id, genderpref_id, eventpref3, countMatched FROM vw_eventpref3n UNION \
                        SELECT mentor_id, genderpref_id, subS1, countMatched FROM vw_subS1n UNION \
                        SELECT mentor_id, genderpref_id, subS2, countMatched FROM vw_subS2n UNION \
                        SELECT mentor_id, genderpref_id, subW, countMatched FROM vw_subWn  \
                        ) AS G GROUP BY G.mentor_id, G.genderpref_id ORDER BY G.mentor_id, G.genderpref_id")

        c.execute("CREATE TABLE results (mentor_id, genderpref_id,count_matched);")
        
        c.execute("SELECT COUNT(*) FROM gendpref_boy")
        x = int(c.fetchall()[0][0])
        c.execute("SELECT COUNT(*) FROM mentor_boy")
        y = int(c.fetchall()[0][0])

        while x > 0 and y > 0:
            c.execute("INSERT INTO results(mentor_id, genderpref_id,count_matched) SELECT mentor_id,genderpref_id,countMatched FROM reportb WHERE CountMatched= (SELECT MAX(CountMatched) FROM reportb LIMIT 1) LIMIT 1")
            # http://www.sqlitetutorial.net/sqlite-max/
            c.execute("SELECT mentor_id FROM reportb WHERE CountMatched = (SELECT MAX(CountMatched) FROM reportb LIMIT 1) LIMIT 1")
            mentor = c.fetchall()[0][0]
            c.execute("SELECT genderpref_id FROM reportb WHERE CountMatched = (SELECT MAX(CountMatched) FROM reportb LIMIT 1) LIMIT 1")
            mentee = c.fetchall()[0][0]
            # https://www.techonthenet.com/sqlite/delete.php
            c.execute("DELETE FROM reportn WHERE mentor_id = %s"%mentor)
            c.execute("DELETE from reportb WHERE mentor_id = %s"%mentor)
            c.execute("DELETE FROM reportb WHERE genderpref_id = %s"%mentee)
            x = x-1
            y = y-1


        c.execute("SELECT COUNT(*) FROM gendpref_girl")
        x= int(c.fetchall()[0][0])
        c.execute("SELECT COUNT(*) FROM mentor_girl")
        y = int(c.fetchall()[0][0])

        while x > 0 and y > 0:
            c.execute("INSERT INTO results(mentor_id,genderpref_id,count_matched) SELECT mentor_id,genderpref_id,countMatched FROM reportg WHERE CountMatched = (SELECT MAX(CountMatched) FROM reportg LIMIT 1) LIMIT 1")
            c.execute("SELECT mentor_id FROM reportg WHERE CountMatched = (SELECT MAX(CountMatched) FROM reportg LIMIT 1) LIMIT 1")
            mentor = c.fetchall()[0][0]
            c.execute("SELECT genderpref_id FROM reportg WHERE CountMatched = (SELECT MAX(CountMatched) FROM reportg LIMIT 1) LIMIT 1")
            mentee = c.fetchall()[0][0]
            c.execute("DELETE FROM reportn WHERE mentor_id = %s"%mentor)
            c.execute("DELETE FROM reportg WHERE mentor_id = %s"%mentor)
            c.execute("DELETE FROM reportg WHERE genderpref_id = %s"%mentee)
            
            x = x-1
            y = y-1
        
        c.execute("SELECT COUNT(DISTINCT genderpref_id) FROM reportn")
        x = int(c.fetchall()[0][0])
        c.execute("SELECT COUNT(DISTINCT mentor_id) FROM reportn")
        y = int(c.fetchall()[0][0])

        while y > 0 and x >0:
            c.execute("INSERT INTO results(mentor_id,genderpref_id,count_matched) SELECT mentor_id,genderpref_id,countMatched FROM reportn WHERE CountMatched = (SELECT MAX(CountMatched) FROM reportn LIMIT 1) LIMIT 1")
            c.execute("SELECT mentor_id FROM reportn WHERE CountMatched = (SELECT MAX(CountMatched) FROM reportn LIMIT 1) LIMIT 1")
            mentorMatch = c.fetchall()[0][0]
            c.execute("SELECT genderpref_id FROM reportn WHERE CountMatched = (SELECT MAX(CountMatched) FROM reportn LIMIT 1) LIMIT 1")
            menteeMatch = c.fetchall()[0][0]
            c.execute("DELETE FROM reportn WHERE genderpref_id = %s"%menteeMatch)
            c.execute("DELETE FROM reportn WHERE mentor_id = %s"%mentorMatch)
            y = y-1
            x= x-1
        
        c.execute("CREATE VIEW vw_finished AS SELECT DISTINCT a.mentor_id,a.genderpref_id,b.fname, b.lname, c.fname,c.lname,c.session,b.mentnum FROM results as a JOIN mentor AS b ON a.mentor_id = b.id JOIN mentee AS c ON a.genderpref_id = c.id")
        # https://stackoverflow.com/questions/10522830/how-to-export-sqlite-to-csv-in-python-without-being-formatted-as-a-list#10522863
        data = c.execute("SELECT * FROM vw_finished")
        with open('pairings.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Mentor ID', 'Mentee ID','Mentor First Name','Mentor Last Name','Mentee First Name','Mentee Last Name','Session','Number of Mentees Possible'])
            writer.writerows(data)

        conn.commit()
        conn.close()
        widget.disabled=True

    def exit(self):
        quit()
        
    def allSort(self, widget, generateWidget):
        print("ok hello like please are you running")
        """sorts by gender preference"""

        # https://stackoverflow.com/questions/52767758/create-new-sqlite-table-combining-column-from-other-tables-with-sqlite3-and-pyth
        # https://www.w3schools.com/sql/func_mysql_substr.asp
        conn=sqlite3.connect(self.text)
        c = conn.cursor()
        c.execute("CREATE TABLE gend_pref_boy_info (mentor_id INTEGER, genderpref_id TEXT);")
        c.execute("INSERT INTO gend_pref_boy_info(mentor_id) SELECT mentor.id FROM mentor WHERE mentor.gend='Male'")
        c.execute("INSERT INTO gend_pref_boy_info(genderpref_id) SELECT mentee.id FROM mentee WHERE mentee.gendpref='Male'")

        c.execute("CREATE TABLE gend_pref_girl_info (mentor_id INTEGER, genderpref_id TEXT);")
        c.execute("INSERT INTO gend_pref_girl_info(mentor_id) SELECT mentor.id FROM mentor WHERE mentor.gend='Female'")
        c.execute("INSERT INTO gend_pref_girl_info(genderpref_id) SELECT mentee.id FROM mentee WHERE mentee.gendpref='Female'")

        c.execute("CREATE TABLE gend_pref_n_info (mentor_id INTEGER, genderpref_id TEXT);")
        c.execute("INSERT INTO gend_pref_n_info(mentor_id) SELECT mentor.id FROM mentor")
        c.execute("INSERT INTO gend_pref_n_info(genderpref_id) SELECT mentee.id FROM mentee WHERE mentee.gendpref='No Preference'") 

        c.execute("CREATE VIEW vw_mentor_all AS SELECT id,fname,lname,gend,subW,hobby1,TRIM(SUBSTR(hobby2,pos1 + 1)) AS hobby2,TRIM(SUBSTR(hobby2,1,pos1 - 1)) AS hobby3,sport1,TRIM(SUBSTR(sport2,pos+1)) AS sport2,TRIM(SUBSTR(sport2,1,pos-1)) AS sport3,music1,TRIM(SUBSTR(music2,pos2+1)) AS music2,TRIM(SUBSTR(music2,1,pos2-1)) AS music3 ,eventpref1,TRIM(SUBSTR(eventpref2,pos3+1)) AS eventpref2,TRIM(SUBSTR(eventpref2,1,pos3-1)) AS eventpref3,subS1,TRIM(SUBSTR(subS2,pos4+1)) AS subS2 FROM (SELECT id,fname,lname,gend,subW,hobby1, hobby2, INSTR(hobby2, ', ') AS pos1, sport1, sport2, INSTR(sport2, ', ') AS pos, music1, music2, INSTR(music2, ', ') AS pos2, eventpref1, eventpref2, INSTR(eventpref2, ', ') AS pos3, subS1, subS2, INSTR(subS2, ', ') AS pos4 FROM (SELECT id,fname,lname,gend,subW,SUBSTR(hobby,1,pos1 - 1) AS hobby1, SUBSTR(hobby, pos1 + 1) AS hobby2,SUBSTR(sport,1,pos - 1) AS sport1, SUBSTR(sport,pos + 1) AS sport2, SUBSTR(music,1,pos2 - 1) AS music1, SUBSTR(music,pos2 + 1) AS music2, SUBSTR(eventpref,1,pos3 -1) AS eventpref1, SUBSTR(eventpref,pos3 + 1) AS eventpref2, SUBSTR(subS,1, pos4 - 1) AS subS1, SUBSTR(subS, pos4 + 1) AS subS2 FROM (SELECT *, id, fname,lname,gend,subW, INSTR(hobby, ', ') AS pos1, INSTR(sport, ', ') AS pos, INSTR(music, ', ') AS pos2, INSTR(eventpref, ', ') AS pos3, INSTR(subS, ', ') AS pos4 FROM mentor)))")
        c.execute("CREATE VIEW vw_mentee_all AS SELECT id,fname,lname,subW,hobby1,TRIM(SUBSTR(hobby2,pos1 + 1)) AS hobby2,TRIM(SUBSTR(hobby2,1,pos1 - 1)) AS hobby3,sport1,TRIM(SUBSTR(sport2,pos+1)) AS sport2,TRIM(SUBSTR(sport2,1,pos-1)) AS sport3,music1,TRIM(SUBSTR(music2,pos2+1)) AS music2,TRIM(SUBSTR(music2,1,pos2-1)) AS music3 ,eventpref1,TRIM(SUBSTR(eventpref2,pos3+1)) AS eventpref2,TRIM(SUBSTR(eventpref2,1,pos3-1)) AS eventpref3,subS1,TRIM(SUBSTR(subS2,pos4+1)) AS subS2 FROM (SELECT id,fname,lname,subW,hobby1, hobby2, INSTR(hobby2, ', ') AS pos1, sport1, sport2, INSTR(sport2, ', ') AS pos, music1, music2, INSTR(music2, ', ') AS pos2, eventpref1, eventpref2, INSTR(eventpref2, ', ') AS pos3, subS1, subS2, INSTR(subS2, ', ') AS pos4 FROM (SELECT id,fname,lname,subW,SUBSTR(hobby,1,pos1 - 1) AS hobby1, SUBSTR(hobby, pos1 + 1) AS hobby2,SUBSTR(sport,1,pos - 1) AS sport1, SUBSTR(sport,pos + 1) AS sport2, SUBSTR(music,1,pos2 - 1) AS music1, SUBSTR(music,pos2 + 1) AS music2, SUBSTR(eventpref,1,pos3 -1) AS eventpref1, SUBSTR(eventpref,pos3 + 1) AS eventpref2, SUBSTR(subS,1, pos4 - 1) AS subS1, SUBSTR(subS, pos4 + 1) AS subS2 FROM (SELECT *, id, fname,lname,subW, INSTR(hobby, ', ') AS pos1, INSTR(sport, ', ') AS pos, INSTR(music, ', ') AS pos2, INSTR(eventpref, ', ') AS pos3, INSTR(subS, ', ') AS pos4 FROM mentee)))")

        c.execute("CREATE VIEW gendpref_boy AS SELECT genderpref_id,t2.hobby1,t2.hobby2,t2.hobby3,t2.sport1,t2.sport2,t2.sport3,t2.music1,t2.music2,t2.music3,t2.eventpref1,t2.eventpref2,t2.eventpref3,t2.subS1,t2.subS2,t2.subW FROM gend_pref_boy_info AS t1 JOIN vw_mentee_all AS t2 ON t1.genderpref_id=t2.id")
        c.execute("CREATE VIEW mentor_boy AS SELECT mentor_id,t2.hobby1,t2.hobby2,t2.hobby3,t2.sport1,t2.sport2,t2.sport3,t2.music1,t2.music2,t2.music3,t2.eventpref1,t2.eventpref2,t2.eventpref3,t2.subS1,t2.subS2,t2.subW FROM gend_pref_boy_info AS t1 JOIN vw_mentor_all AS t2 ON t1.mentor_id=t2.id")
        
        c.execute("CREATE VIEW gendpref_girl AS SELECT genderpref_id,t2.hobby1,t2.hobby2,t2.hobby3,t2.sport1,t2.sport2,t2.sport3,t2.music1,t2.music2,t2.music3,t2.eventpref1,t2.eventpref2,t2.eventpref3,t2.subS1,t2.subS2,t2.subW FROM gend_pref_girl_info AS t1 JOIN vw_mentee_all AS t2 ON t1.genderpref_id=t2.id")
        c.execute("CREATE VIEW mentor_girl AS SELECT mentor_id,t2.hobby1,t2.hobby2,t2.hobby3,t2.sport1,t2.sport2,t2.sport3,t2.music1,t2.music2,t2.music3,t2.eventpref1,t2.eventpref2,t2.eventpref3,t2.subS1,t2.subS2,t2.subW FROM gend_pref_girl_info AS t1 JOIN vw_mentor_all AS t2 ON t1.mentor_id=t2.id")
        
        c.execute("CREATE VIEW gendpref_n AS SELECT genderpref_id,t2.hobby1,t2.hobby2,t2.hobby3,t2.sport1,t2.sport2,t2.sport3,t2.music1,t2.music2,t2.music3,t2.eventpref1,t2.eventpref2,t2.eventpref3,t2.subS1,t2.subS2,t2.subW FROM gend_pref_n_info AS t1 JOIN vw_mentee_all AS t2 ON t1.genderpref_id=t2.id")
        c.execute("CREATE VIEW mentor_n AS SELECT mentor_id,t2.hobby1,t2.hobby2,t2.hobby3,t2.sport1,t2.sport2,t2.sport3,t2.music1,t2.music2,t2.music3,t2.eventpref1,t2.eventpref2,t2.eventpref3,t2.subS1,t2.subS2,t2.subW FROM gend_pref_n_info AS t1 JOIN vw_mentor_all AS t2 ON t1.mentor_id=t2.id")

        #sorts by hobbies

        self.creatinTablesForTheButtons(c,"hobby",11)

        #sorts by sports

        self.creatinTablesForTheButtons(c,"sport",9)

        #sorts by event preference

        self.creatinTablesForTheButtons(c,"eventpref",3)

        #sorts by music pref

        self.creatinTablesForTheButtons(c,"music",7)

        #sorts by subject strength

        c.execute("CREATE VIEW vw_subS1b AS SELECT mentor_id,b.genderpref_id,b.subS1, CASE WHEN b.subS1 ='' THEN 0 WHEN b.subS1 = 'Other' THEN 0 WHEN b.subS1 IS NOT null THEN 3 ELSE 0 END AS countMatched FROM mentor_boy AS a LEFT OUTER JOIN gendpref_boy AS b ON b.subS1 = a.subS1 OR b.subS1 = a.subS2")
        c.execute("CREATE VIEW vw_subS2b AS SELECT mentor_id,b.genderpref_id,b.subS2, CASE WHEN b.subS1 ='' THEN 0 WHEN b.subS1 = 'Other' THEN 0 WHEN b.subS1 IS NOT null THEN 3 ELSE 0 END AS countMatched FROM mentor_boy AS a LEFT OUTER JOIN gendpref_boy AS b ON b.subS2 = a.subS1 OR b.subS2 = a.subS2")
        
        c.execute("CREATE VIEW vw_subS1g AS SELECT mentor_id,b.genderpref_id,b.subS1, CASE WHEN b.subS1 ='' THEN 0 WHEN b.subS1 = 'Other' THEN 0 WHEN b.subS1 IS NOT null THEN 3 ELSE 0 END AS countMatched FROM mentor_girl AS a LEFT OUTER JOIN gendpref_girl AS b ON b.subS1 = a.subS1 OR b.subS1 = a.subS2")
        c.execute("CREATE VIEW vw_subS2g AS SELECT mentor_id,b.genderpref_id,b.subS2, CASE WHEN b.subS1 ='' THEN 0 WHEN b.subS1 = 'Other' THEN 0 WHEN b.subS1 IS NOT null THEN 3 ELSE 0 END AS countMatched FROM mentor_girl AS a LEFT OUTER JOIN gendpref_girl AS b ON b.subS2 = a.subS1 OR b.subS2 = a.subS2")

        c.execute("CREATE VIEW vw_subS1n AS SELECT mentor_id,b.genderpref_id,b.subS1, CASE WHEN b.subS1 ='' THEN 0 WHEN b.subS1 = 'Other' THEN 0 WHEN b.subS1 IS NOT null THEN 3 ELSE 0 END AS countMatched FROM mentor_n AS a LEFT OUTER JOIN gendpref_n AS b ON b.subS1 = a.subS1 OR b.subS1 = a.subS2")
        c.execute("CREATE VIEW vw_subS2n AS SELECT mentor_id,b.genderpref_id,b.subS2, CASE WHEN b.subS1 ='' THEN 0 WHEN b.subS1 = 'Other' THEN 0 WHEN b.subS1 IS NOT null THEN 3 ELSE 0 END AS countMatched FROM mentor_n AS a LEFT OUTER JOIN gendpref_n AS b ON b.subS2 = a.subS1 OR b.subS2 = a.subS2")
        
        #sorts by subject weakness

        c.execute("CREATE VIEW vw_subWb AS SELECT mentor_id,b.genderpref_id,b.subW, CASE WHEN b.subW ='' THEN 0 WHEN b.subW = 'Other' THEN 0 WHEN b.subW IS NOT null THEN 4 ELSE 0 END AS countMatched FROM mentor_boy AS a LEFT OUTER JOIN gendpref_boy AS b ON b.subW = a.subW")
        c.execute("CREATE VIEW vw_subWg AS SELECT mentor_id,b.genderpref_id,b.subW, CASE WHEN b.subW ='' THEN 0 WHEN b.subW = 'Other' THEN 0 WHEN b.subW IS NOT null THEN 4 ELSE 0 END AS countMatched FROM mentor_girl AS a LEFT OUTER JOIN gendpref_girl AS b ON b.subW = a.subW")
        c.execute("CREATE VIEW vw_subWn AS SELECT mentor_id,b.genderpref_id,b.subW, CASE WHEN b.subW ='' THEN 0 WHEN b.subW = 'Other' THEN 0 WHEN b.subW IS NOT null THEN 4 ELSE 0 END AS countMatched FROM mentor_n AS a LEFT OUTER JOIN gendpref_n AS b ON b.subW = a.subW")
        conn.commit()
        conn.close()
        widget.disabled=True
        generateWidget.disabled=False


class mentorshipApp(App):
    def build(self):
        return containerLayout()

calc = mentorshipApp()
calc.run()
