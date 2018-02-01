import unittest
from DatabaseManagement import DatabaseManagement
from CSVReader import CSVReader
import os
from os import path
import sqlite3 as sql



class test_csv_reader(unittest.TestCase):


    def test_number_of_materials(self):
        ''' Tests if the number of material is correct

        '''

        csvr = CSVReader('data.csv')

        properties = csvr.get_properties_from_csv()

        self.assertEqual(len(properties), 100)

    def test_property_tuple(self):
        ''' Tests is the tuple returned correctly

        '''

        assert_tuple = ('Cd1I2', 3.19, 'White')

        csvr = CSVReader('data.csv')

        properties = csvr.get_properties_from_csv()

        self.assertEqual(properties[0], assert_tuple)

class test_database_manager(unittest.TestCase):

    # def setUp(self):
    #
    #     self.dbm = DatabaseManagement('unittest.db')

    def tearDown(self):

        os.remove('unittest.db')

    def test_db_creation(self):
        ''' Tests if the db file created or not

        :return:
        '''

        dbm = DatabaseManagement('unittest.db', verbose=False)

        dbm.create_db()

        self.assertTrue(path.isfile('unittest.db'))

    def test_table_creation(self):
        ''' Tests if the table was created successfully in the database

        :return:
        '''
        dbm = DatabaseManagement('unittest.db', verbose=False)

        dbm.create_table()

        conn = dbm.create_connection()

        c = dbm.create_cursor(conn)

        c.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='material_properties' ''')

        self.assertTrue(c)

        dbm.close_connection(conn)

    def test_multiple_append(self):
        ''' Tests if the multiple append is successful or not

        :return:
        '''

        csvr = CSVReader('test_data.csv')

        properties = csvr.get_properties_from_csv()

        dbm = DatabaseManagement('unittest.db', verbose=False)

        dbm.create_db()
        dbm.create_table()

        dbm.append_multiple_rows(properties)

        conn = dbm.create_connection()

        c = dbm.create_cursor(conn)

        c.execute('''SELECT * FROM material_properties''')

        table = c.fetchall()

        dbm.close_connection(conn)

        self.assertEqual(len(table), 100)

    def test_material_search(self):
        ''' Tests if the material search is successful or not

        :return:
        '''

        csvr = CSVReader('test_data.csv')

        properties = csvr.get_properties_from_csv()

        dbm = DatabaseManagement('unittest.db', verbose=False)

        dbm.create_db()
        dbm.create_table()

        dbm.append_multiple_rows(properties)

        table = dbm.search_by_material('P')

        self.assertEqual(len(table), 3)

    def test_color_search(self):
        ''' Tests if color search is successful or not

        :return:
        '''

        csvr = CSVReader('test_data.csv')

        properties = csvr.get_properties_from_csv()

        dbm = DatabaseManagement('unittest.db', verbose=False)

        dbm.create_db()
        dbm.create_table()

        dbm.append_multiple_rows(properties)

        table = dbm.search_by_color('Black')

        self.assertEqual(len(table), 5)

    def test_band_gap_search(self):
        ''' Tests if band gap search is successful or not

        :return:
        '''

        csvr = CSVReader('test_data.csv')

        properties = csvr.get_properties_from_csv()

        dbm = DatabaseManagement('unittest.db', verbose=False)

        dbm.create_db()
        dbm.create_table()

        dbm.append_multiple_rows(properties)

        table = dbm.search_by_band_gap(band_gap=2)

        self.assertEqual(len(table), 8)

    def test_band_gap_range_search(self):
        ''' Tests if band gap range search is successful or not

        :return:
        '''

        csvr = CSVReader('test_data.csv')

        properties = csvr.get_properties_from_csv()

        dbm = DatabaseManagement('unittest.db', verbose=False)

        dbm.create_db()
        dbm.create_table()

        dbm.append_multiple_rows(properties)

        table = dbm.search_by_band_gap_range(band_gap_min=1.5, band_gap_max=2.0)

        self.assertEqual(len(table), 10)



if __name__ == '__main__':
    unittest.main()
