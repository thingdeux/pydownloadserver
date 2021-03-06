import sqlite3
import os
import logger

current_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_path, '.database.db')


def tableIntegrityCheck():
    def verifyColumnsExist(pragma_list, check_list):
        valid_table = True
        try:
            for checked_item in check_list:
                if (pragma_list[checked_item['column_location']][0] ==
                    checked_item['column_location'] and
                   pragma_list[checked_item['column_location']][1] ==
                   checked_item['column_name']):
                    pass
                else:
                    valid_table = False

            return valid_table
        except:
            return False

    db_connection = connectToDB()
    db = db_connection.cursor()
    db.execute('''PRAGMA table_info(config)''')
    config_cols = db.fetchall()
    db.execute('''PRAGMA table_info(jobs)''')
    job_cols = db.fetchall()
    db_connection.close()

    config_check = [
        {'column_location': 0, 'column_name': 'id'},
        {'column_location': 1, 'column_name': 'config_type'},
        {'column_location': 2, 'column_name': 'name'},
        {'column_location': 3, 'column_name': 'value'},
        {'column_location': 4, 'column_name': 'html_tag'},
        {'column_location': 5, 'column_name': 'html_display_name'}]

    job_check = [
        {'column_location': 0, 'column_name': 'id'},
        {'column_location': 1, 'column_name': 'url'},
        {'column_location': 2, 'column_name': 'status'},
        {'column_location': 3, 'column_name': 'time_queued'},
        {'column_location': 4, 'column_name': 'source'},
    ]

    if (verifyColumnsExist(config_cols, config_check) is True and
       (verifyColumnsExist(job_cols, job_check)) is True):
        return True
    else:
        return False


def verifyDatabaseExistence():
    # Check to see if DB exists
    if (os.path.isfile(db_path)):
        try:
            db_connection = connectToDB()
            db_connection.close()
            return(True)
        except Exception, err:
            for i in err:
                logger.log("Unable to verify DB Existence - " + i)
    else:
        return(False)


def createFreshTables():
    # If DB doesn't exist create its tables and keys
    db_connection = sqlite3.connect(db_path)
    db = db_connection.cursor()

    db.execute('''CREATE TABLE jobs
            (id INTEGER PRIMARY KEY, url TEXT, status TEXT,
                time_queued TEXT, source TEXT)''')
    db.execute('''CREATE TABLE config
            (id INTEGER PRIMARY KEY, config_type TEXT, name TEXT, value TEXT,
                html_tag TEXT, html_display_name)''')
    db.execute(''' CREATE INDEX sourceIndex ON jobs(source ASC) ''')
    db.execute(''' CREATE INDEX statusIndex ON jobs(status ASC) ''')

    db_connection.commit()
    db_connection.close()


def connectToDB():
    try:
        # If DB doesn't exist create its tables and keys
        db_connection = sqlite3.connect(db_path)
        return (db_connection)
    except Exception, err:
        for error in err:
            logger.log("Unable to connect to DB - " + error)
            return (False)


def debugCreateTestData():

    db_connection = connectToDB()
    db = db_connection.cursor()

    # Buid data string to insert
    jobsData = [
        (None, 'http://c758482.r82.cf2.rackcdn.com/Sublime\
            %20Text%202.0.2%20Setup.exe', "Queued", logger.getTime(), "email"),

        (None, 'http://i.imgur.com/lOOw9rq.gif',
            "Downloading", logger.getTime(), "web")
    ]

    configData = [
        (None, 'E-Mail', 'email_username',
            'pydownloadserver', 'text', 'GMail Username:'),
        (None, 'E-Mail', 'email_password',
            'TestTest', 'password', 'Gmail Password:'),
        (None, 'General', 'download_path', current_path,
            'text', "Download Location:"),
        (None, 'Server', 'server_host', '0.0.0.0', 'text', "Host:"),
        (None, 'Server', 'server_port', '12334', 'text', "Port")

    ]

    db.executemany('INSERT INTO jobs VALUES (?,?,?,?,?)', jobsData)
    db.executemany('INSERT INTO config VALUES (?,?,?,?,?,?)', configData)

    try:
        db_connection.commit()
        db_connection.close()
        logger.log(logger.getTime() + " Inserted test data into db")
    except Exception, err:
        for error in err:
            logger.log("Unable to insert test data" + error)
            db_connection.close()


def getJobs(resultRequested):
    try:
        db_connection = connectToDB()
        db = db_connection.cursor()

        if resultRequested is "all":
            db.execute('''SELECT * from jobs ''')
        elif resultRequested is "active":
            db.execute('''SELECT * from jobs WHERE status ="Queued"
                          OR status = "Downloading" ''')
        elif resultRequested is "historical":
            db.execute('''SELECT * from jobs WHERE status = "Successful"
                          OR status = "Failed"
                          ORDER BY "time_queued" ASC''')
        elif resultRequested is "failed":
            db.execute('''SELECT * from jobs WHERE status ="Failed" ''')
        elif resultRequested is "successful":
            db.execute('''SELECT * from jobs WHERE status = "Successful" ''')
        elif resultRequested is "queued":
            db.execute('''SELECT * from jobs WHERE status = "Queued" ''')
        elif resultRequested is "downloading":
            db.execute('''SELECT * from jobs WHERE status ="Downloading" ''')

        data = db.fetchall()
        db_connection.close()

        return (data)
    except Exception, err:
        for error in err:
            logger.log("Unable to query DB - " + error)
            db_connection.close()
        return(False)


def insertJob(url, source):
    try:
        db_connection = connectToDB()
        db = db_connection.cursor()
        # Build job list to be inserted into DB
        job = [(None, url, "Queued", logger.getTime(), source)]
        # iterate over list and create insert command for DB
        db.executemany('INSERT INTO jobs VALUES (?,?,?,?,?)', job)

        try:
            db_connection.commit()
            db_connection.close()
        except Exception, err:
            for error in err:
                logger.log(error)
                db_connection.close()
    except Exception, err:
        for error in err:
            db_connection.close()
            logger.log("Unable to insert record - " + error)


# Pull config info from the DB
def getConfig(config_name='all'):

    def confToDict(passed_tuple):
        built_dict = {}
        for item in passed_tuple:
            try:
                len(built_dict[item[1]])
                built_dict[item[1]].append(item)
            except:
                built_dict[item[1]] = []
                built_dict[item[1]].append(item)
        return (built_dict)

    if config_name == 'all' or config_name == '':
        try:
            db_connection = connectToDB()
            db = db_connection.cursor()
            db.execute('''SELECT * from config''')
            config_data = db.fetchall()
            db_connection.close()

            return (confToDict(config_data))

        except Exception, err:
                for error in err:
                    logger.log("Unable to get config info - " + error)
                    db_connection.close()
                return (False)
    else:
        try:
            db_connection = connectToDB()
            db = db_connection.cursor()
            db.execute('SELECT * FROM config WHERE name=? GROUP BY=?',
                       (config_name, config_name))

            config_item = db.fetchall()
            db_connection.close()

            return (confToDict(config_item))
        except Exception, err:
            for error in err:
                logger.log("Unable to get config info - " + error)
                db_connection.close()


def updateJobStatus(id, requestedStatus):

    try:
        db_connection = connectToDB()
        db = db_connection.cursor()

        if requestedStatus == "failed":
            db.execute('''UPDATE jobs SET status=? where id=?''',
                       ("Failed", id,))
        elif requestedStatus == "downloading":
            db.execute('''UPDATE jobs SET status=? where id=?''',
                       ("Downloading", id,))
        elif requestedStatus == "successful":
            db.execute('''UPDATE jobs SET status=? where id=?''',
                       ("Successful", id,))
        elif requestedStatus == "queued":
            db.execute('''UPDATE jobs SET status=? where id=?''',
                       ("Queued", id,))

        try:
            db_connection.commit()
            db_connection.close()
        except Exception, err:
            for error in err:
                logger.log(error)
                db_connection.close()
    except Exception, err:
        for error in err:
            db_connection.close()
            logger.log("Unable to update record - " + error)


def updateTimeRemainingByID(job_id, time_remaining):
    try:
        db_connection = connectToDB()
        db = db_connection.cursor()
        db.execute('UPDATE jobs SET time_left =:time_left WHERE id=:id',
                   {"time_left": time_remaining, "id": job_id})

        db_connection.commit()
        db.connection.close()

    except Exception, err:
        for error in err:
            logger.log("Unable to modify job - " + error)
            db_connection.close()


def cleanUpAfterCrash():
    try:
        db_connection = connectToDB()
        db = db_connection.cursor()
        db.execute('''UPDATE jobs SET status="Queued" WHERE
                   status="Downloading"''')

        db_connection.commit()
        db.connection.close()

    except Exception, err:
        for error in err:
            logger.log("Unable to cleanup Database after crash - " + error)
            db_connection.close()


def changeJobStatusByID(job_id, new_status):

    if new_status in ('Successful', 'Failed', 'Queued', 'Downloading'):

        try:
            db_connection = connectToDB()
            db = db_connection.cursor()
            db.execute('UPDATE jobs SET status =:status WHERE id=:id',
                       {"status": new_status, "id": job_id})

            db_connection.commit()
            db_connection.close()

        except Exception, err:
            for error in err:
                logger.log("Unable to modify job - " + error)
                db_connection.close()
    else:
        logger.log("Attempting to update job with an invalid status")


def modifyConfigurationItemByName(config_parameter_name, new_value):
    try:
        db_connection = connectToDB()
        db = db_connection.cursor()
        db.execute('UPDATE config SET value = :new_value WHERE name = :name ',
                   {"name": config_parameter_name, "new_value": new_value})
        db_connection.commit()
        db_connection.close()

    except Exception, err:
        for error in err:
            logger.log("Unable to get config info - " + error)
            db_connection.close()


def deleteHistory(kind="all"):
    db_connection = connectToDB()
    db = db_connection.cursor()

    if kind == "all":
        # Delete everything in the table
        db.execute('''DELETE FROM jobs WHERE status ="Successful"
                      OR status="Failed"''')
    elif kind == "failed":
        db.execute('''DELETE FROM jobs WHERE status="Failed"''')

    db_connection.commit()
    db.connection.close()


if __name__ == "__main__":
    print tableIntegrityCheck()
