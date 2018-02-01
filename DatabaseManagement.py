import sqlite3 as sql
from os import path
from tabulate import tabulate


class DatabaseManagement():
    '''
    This class is used to manage database with the properties
    given in the csv file.
    '''

    def __init__(self, db_name, data_dir='.', verbose=True):

        self.db_name = db_name
        self.data_dir = data_dir
        self.verbose = verbose

        self.set_db_path()

    def print_or_not(self, this_str):

        if self.verbose:
            print(this_str)

    def set_db_path(self):
        '''
        Returns the full path of the database. This is called during the
        initialization of the class. This path can be used to further manipulate
        the database.

        :return: the full path of the database.
        '''

        self.db_full_path = path.join(self.data_dir, self.db_name)

    def create_connection(self):
        '''Creates a connection to the database and returns the connection
        object.

        :return:  the connection object to the database.
        '''

        return sql.connect(self.db_full_path)

    def close_connection(self, conn):
        ''' Closes the connection object provided as the input parameter.

        :param conn: connection object to the database.
        :return: returns status of the close.
        '''

        return conn.close()

    def create_cursor(self, conn):
        ''' Returns a cursor object to the connection object provided.

        :param conn: connection object to the database.
        :return: returns cursor object.
        '''

        return conn.cursor()

    def close_cursor(self, cursor):
        ''' Closes the cursor object.

        :param cursor: cursor object to close.
        :return: returns status of the close.
        '''

        return cursor.close()


    def create_db(self):
        ''' Creates the database if not exist.
        '''

        if path.isfile(self.db_full_path):
            self.print_or_not(' Database already exists.')

        else:
            self.print_or_not(' Database does not exist. Creating..')

            conn = sql.connect(self.db_full_path)

            self.print_or_not(' Database created.')

            self.close_connection(conn)

    def create_table(self):
        ''' Creates table material_properties with three columns.

        '''

        conn = self.create_connection()

        c = self.create_cursor(conn)

        try:
            c.execute('''CREATE TABLE material_properties (material text, band_gap real, color text)''')

            self.print_or_not(' Table was created successfully.')

        except sql.Error as e:
            print(' An error has occurred while creating the table:', e.args[0])

        return self.close_connection(conn)

    def append_one_row(self, material_name, band_gap, color):
        ''' Inserts one row to the table material_properties.

        :param material_name: name of the material
        :param band_gap: band gap of the material
        :param color: color of the material
        '''

        conn = self.create_connection()

        c = self.create_cursor(conn)

        try:
            c.execute('''INSERT INTO material_properties VALUES (?,?,?)''',
                      (material_name, band_gap, color))
        except sql.Error as e:
            print(' An error has occurred while inserting:', e.args[0])

        conn.commit()

        return self.close_connection(conn)

    def append_multiple_rows(self, properties):
        ''' Inserts multiple rows to the table material_properties

        :param properties: a list containing tuples of values to be inserted.
        Example of such list:

        prop = [('Material1', 2.4, 'White'),
                ('Material2', 1.5 , 'Black')]
        '''

        conn = self.create_connection()

        c = self.create_cursor(conn)

        try:
            c.executemany('''INSERT INTO material_properties VALUES (?,?,?)''',
                      properties)
            self.print_or_not(' Insertion into database was successful.')
        except sql.Error as e:
            print(' An error has occurred while inserting:', e.args[0])

        conn.commit()

        return self.close_connection(conn)

    def print_info(self, num_rows=5):
        ''' Prints number of specified rows

        :param num_rows: number of rows to print
        '''

        conn = self.create_connection()

        c = self.create_cursor(conn)

        if num_rows < 1:
            raise ValueError(' Number of rows to print should be larger than 0.')

        try:
            c.execute('''SELECT * FROM material_properties LIMIT (?)''',(num_rows,))

            table = c.fetchall()

            print('\n')

            print(tabulate(table, headers=['Material', 'Band gap', 'Color']))

        except sql.Error as e:
            print(' An error has occurred while retrieving:', e.args[0])

        return self.close_connection(conn)


    def delete_by_material(self, material_name):
        ''' Deletes entry from the database by material name

        :param material_name: name of the material to delete
        '''

        conn = self.create_connection()

        c = self.create_cursor(conn)

        try:
            c.execute('''DELETE FROM material_properties WHERE material=(?)''',
                      material_name)
            print(' Delete successful.')
        except sql.Error as e:
            print(' An error has occurred while deleting: ', e.args[0])

        conn.commit()

        return self.close_connection(conn)

    def search_by_material(self, material_name):
        ''' Searches database by material_name

        :param material_name: name of the material to search for.
        '''

        conn = self.create_connection()

        c = self.create_cursor(conn)

        self.print_or_not('\n Searching for material "{}"..'.format(material_name))

        try:
            c.execute('''SELECT band_gap, color FROM material_properties WHERE material=(?)''',
                      (material_name,))

            table = c.fetchall()

            if len(table) > 0:

                self.print_or_not('\n Found {} matching material(s).\n'.format(len(table)))

                self.print_or_not(tabulate(table, headers=['Band gap', 'Color']))

            else:

                self.print_or_not('\n No matching material found.\n')

        except sql.Error as e:
            print(' An error has occurred while searching: ', e.args[0])

        self.close_connection(conn)

        return table

    def search_by_color(self, color):
        ''' Searches database by material color

        :param color: color of the material to search for
        '''

        conn = self.create_connection()

        c = self.create_cursor(conn)

        self.print_or_not('\n Searching for materials with color "{}"..'.format(color))

        try:
            c.execute('''SELECT material, band_gap FROM material_properties WHERE color=(?)''',
                      (color,))

            table = c.fetchall()

            if len(table) > 0:

                self.print_or_not('\n Found {} material(s).\n'.format(len(table), color))

                self.print_or_not(tabulate(table, headers=['Material', 'Band gap']))

            else:

                self.print_or_not('\n No material found.\n')

        except sql.Error as e:
            print(' An error has occurred while searching:', e.args[0])

        self.close_connection(conn)

        return table

    def search_by_band_gap(self, band_gap, tol_perc=5):
        ''' Searcher the database by band gap with tolerance provided in percentage

        :param band_gap: band gap to search for
        :param tol_perc: tolerance of the band gap search
        '''

        conn = self.create_connection()

        c = self.create_cursor(conn)

        tol_frac = tol_perc/100.0
        bg_dev = band_gap * tol_frac

        bg_max = band_gap + bg_dev
        bg_min = band_gap - bg_dev

        self.print_or_not('\n Searching for material(s) with band gap: {:.2f}eV (Tolerance {:.1f}%)..'.format(band_gap, tol_perc))

        try:
            c.execute('''SELECT * FROM material_properties WHERE band_gap <= (?) and band_gap >= (?)''',
                      (bg_max,bg_min))

            table = c.fetchall()

            if len(table) > 0:

                self.print_or_not('\n Found {} material(s) within range.\n'.format(len(table)))

                self.print_or_not(tabulate(table, headers=['Material', 'Band gap', 'Color']))

            else:

                self.print_or_not('\n No material found.\n')

        except sql.Error as e:
            print(' An error has occurred while searching:', e.args[0])

        self.close_connection(conn)

        return table

    def search_by_band_gap_range(self, band_gap_min, band_gap_max):
        ''' Searches the database by the band gap range provided.

        :param band_gap_min: minimum band gap
        :param band_gap_max: maximum band gap
        '''

        conn = self.create_connection()

        c = self.create_cursor(conn)

        if band_gap_min < 0.0 or band_gap_max < 0.0:
            raise ValueError(' Band gap cannot be less than 0eV.')

        if band_gap_min > band_gap_max:
            raise ValueError(' Minimum value of band gap should be smaller than the maximum value.')

        self.print_or_not('\n Searching for material(s) from {:.2f}eV to {:.2f}eV band gap..'.format(band_gap_min, band_gap_max))

        try:
            c.execute('''SELECT * FROM material_properties WHERE band_gap >= (?) and band_gap <= (?)''',
                      (band_gap_min, band_gap_max))

            table = c.fetchall()

            if len(table) > 0:

                self.print_or_not('\n Found {} material(s) within range.\n'.format(len(table)))

                self.print_or_not(tabulate(table, headers=['Material', 'Band gap', 'Color']))

            else:

                self.print_or_not('\n No material found.\n')

        except sql.Error as e:
            print(' An error has occurred while searching:', e.args[0])

        self.close_connection(conn)

        return table


