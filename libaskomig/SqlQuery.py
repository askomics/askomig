import os
import sqlite3

class SqlQuery():

    def __init__(self, database_path, old_dir, new_dir):

        self.database_path = database_path
        self.old_dir = old_dir
        self.new_dir = new_dir

    def sql_query(self, query, variables=None, get_id=False, specific_database=None):

        database = self.database_path if not specific_database else specific_database

        connection = sqlite3.connect("file:" + database, uri=True)
        cursor = connection.cursor()

        if variables:
            cursor.execute(query, variables)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        connection.commit()
        connection.close()

        if get_id:
            return cursor.lastrowid

        return rows

    def add_user(self, user):

        query = '''
        INSERT INTO users VALUES(
            NULL,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?   
        )
        '''

        user_id = self.sql_query(query, (user['username'], user['email'], user['password'], user['salt'], user['apikey'], user['admin'], user['blocked']), True)

        if 'Gurl' in user :
            query = '''
            INSERT INTO galaxy_accounts VALUES(
                NULL,
                ?,
                ?,
                ?
            )
            '''

            self.sql_query(query, (user_id, user['Gurl'], user['Gkey']), True)

        return user_id

    def create_user_table(self):

        query = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username text,
            email text,
            password text,
            salt text,
            apikey text,
            admin boolean,
            blocked boolean
        )
        '''
        self.sql_query(query)

    def create_galaxy_table(self):

        query = '''
        CREATE TABLE IF NOT EXISTS galaxy_accounts (
            galaxy_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            url text,
            apikey text,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        '''
        self.sql_query(query)

    def create_integration_table(self):

        query = '''
        CREATE TABLE IF NOT EXISTS integration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename text,
            state text,
            start int,
            end int,
            error text,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        '''
        self.sql_query(query)

    def create_query_table(self):

        query = '''
        CREATE TABLE IF NOT EXISTS query (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            state text,
            start int,
            end int,
            data text,
            file text,
            preview text,
            graph text,
            variates text,
            nrows int,
            error text,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        '''
        self.sql_query(query)

    def create_endpoints_table(self):

        query = '''
        CREATE TABLE IF NOT EXISTS endpoints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text,
            url text,
            auth text,
            enable boolean,
            message text
        )
        '''
        self.sql_query(query)

    def create_all_tables(self):

        self.create_user_table()
        self.create_galaxy_table()
        self.create_integration_table()
        self.create_query_table()
        self.create_endpoints_table()

    def move_job_database(self, username, user_id):

        db_path = self.old_dir + '/db/' + username + '/jobs.db'
        if os.path.exists(db_path):
            jobs = self.get_old_jobs(db_path)
            for job in jobs:
                # Insert in new database
                if job[1] == 'SPARQL Request':
                    tuple_to_insert = (
                        user_id,
                        'done' if job[2] == 'Ok ' else 'error',
                        job[3],
                        job[4],
                        job[5],
                        job[6],
                        None if job[7] == '' else job[7],
                        job[8],
                        job[9],
                        job[10],
                        None if job[2] == 'Ok ' else 'ERROR'
                    )
                    self.save_query_job(tuple_to_insert)
                else:
                    tuple_to_insert = (
                        user_id,
                        job[1],
                        'done' if job[2] == 'Done' else 'error',
                        job[3],
                        job[4],
                        None if job[2] == '' else 'ERROR'
                    )
                    self.save_integration_job(tuple_to_insert)


    def move_endpoint_manager(self, username):

        db_path = self.old_dir + '/common/' + username + '/endpoints.db'
        if os.path.exists(db_path):
            endpoints = self.get_old_endpoints(db_path)
            for endpoint in endpoints:
                # Insert in new database
                tuple_to_insert = (
                    endpoint[1],
                    endpoint[2],
                    endpoint[3].upper(),
                    endpoint[4],
                    None if endpoint[5] == '' else endpoint[5]
                )
                self.save_endpoints_job(tuple_to_insert)


    def get_old_jobs(self, db_path):

        query = '''
        SELECT *
        FROM jobs
        ORDER BY jobID
        '''
        jobs = self.sql_query(query, specific_database=db_path)

        return jobs

    def get_old_endpoints(self, db_path):

        query = '''
        SELECT *
        FROM endpoints
        ORDER BY id
        '''
        jobs = self.sql_query(query, specific_database=db_path)

        return jobs

    def save_query_job(self, tpl):

        query = '''
        INSERT INTO query VALUES(
        NULL,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        '''
        self.sql_query(query, tpl)

    def save_integration_job(self, tpl):

        query = '''
        INSERT INTO integration VALUES(
            NULL,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        '''
        self.sql_query(query, tpl)

    def save_endpoints_job(self, tpl):

        query = '''
        INSERT INTO endpoints VALUES(
            NULL,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        '''

        self.sql_query(query, tpl)
