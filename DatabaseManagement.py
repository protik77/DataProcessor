import sqlite3 as sql
from os import path

class DatabaseManagement():
    '''
    This class is used to manage database with the properties
    given in the csv file.
    '''

    def __init__(self, db_name, data_dir='data'):

        self.db_name = db_name
        self.data_dir = data_dir

        self.SetDBPath()

    def SetDBPath(self):
        '''
        Returns the full path of the database. This is called during the
        initialization of the class. This path can be used to further manipulate
        the database.

        :return: the full path of the database.
        '''

        self.db_full_path = path.join(self.data_dir, self.db_name)

    def CreateConnection(self):
        '''Creates a connection to the database and returns the connection
        object.

        :return:  the connection object to the database.
        '''

        return sql.connect(self.db_full_path)

    def CloseConnection(self, conn):
        ''' Closes the connection object provided as the input parameter.

        :param conn: connection object to the database.
        :return: returns status of the close.
        '''

        return conn.close()

    def CreateCursor(self, conn):
        ''' Returns a cursor object to the connection object provided.

        :param conn: connection object to the database.
        :return: returns cursor object.
        '''

        return conn.cursor()

    def CloseCursor(self, cursor):
        ''' Closes the cursor object.

        :param cursor: cursor object to close.
        :return: returns status of the close.
        '''

        return cursor.close()


    def CreateDB(self):
        ''' Creates the database if not exist.
        '''

        if path.isfile(self.db_full_path):
            print(' DB already exists.')

        else:
            print(' DB does not exist.')

            conn = sql.connect(self.db_full_path)

            print(' DB created.')

            conn.close()

    def CreateTable(self):
        ''' Creates table material_properties with three columns.

        '''

        conn = self.CreateConnection()

        c = self.CreateCursor(conn)

        try:
            c.execute('''CREATE TABLE material_properties 
                (material text, band_gap real, color text)''')

            print(' Table was created successfully.')

        except sql.Error as e:
            print(' An error has occurred while creating the table:', e.args[0])

        self.CloseConnection(conn)

    def InsertOneRow(self, material_name, band_gap, color):
        ''' Inserts one row to the table material_properties.

        :param material_name: name of the material
        :param band_gap: band gap of the material
        :param color: color of the material
        '''

        conn = self.CreateConnection()

        c = self.CreateCursor(conn)

        try:
            c.execute('INSERT INTO material_properties VALUES (?,?,?)',
                      (material_name, band_gap, color))
        except sql.Error as e:
            print(' An error has occurred while inserting:', e.args[0])

        self.CloseConnection(conn)

    def InsertMultipleRows(self, properties):
        ''' Inserts multiple rows to the table material_properties

        :param properties: a list containing tuples of values to be inserted.
        Example of such list:

        prop = [('Material1', 2.4, 'White'),
                ('Material2', 1.5 , 'Black')]
        '''

        conn = self.CreateConnection()

        c = self.CreateCursor(conn)

        try:
            c.executemany('INSERT INTO material_properties VALUES (?,?,?)',
                      properties)
        except sql.Error as e:
            print(' An error has occurred while inserting:', e.args[0])

        self.CloseConnection(conn)



