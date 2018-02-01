
Data provider
==============

This code takes advantage of two classes: `CSVReader` and `DataManagement`. 
The `CSVReader` class can be used to extract data from a CSV file.
And the `DataManagement` class can be used for storing and retrieving data
to and from a SQLite database, respectively.
An example of a typical workflow can be:

* Retrieving data from a CSV file and store that to a SQLite database:

```bash
python data_provider.py -r <csv file> -s <db file>

```

**Example:**
```bash
>python data_provider.py -r data.csv -s data.db
 Database does not exist. Creating..
 Database created.
 Table was created successfully.
 Insertion into database was successful.
```

* Viewing user specified number of rows from the database file.

```bash
python data_provider.py -db <db file> -pr <number of rows>
```

**Example:**
```bash
>python data_provider.py -db data.db -pr 5


Material      Band gap  Color
----------  ----------  ----------
Cd1I2            3.19   White
Zr1S2            1.68   Violet
Ga1Sb1           0.812  Light Gray
P                1.6    Red
Ca1Te1           4.07   White
```

* Searching the database for a particular material.

```bash
python data_provider.py -db <db file> -sm <material name>
```

**Example:**
```bash
>python data_provider.py -db data.db -sm P

 Searching for material "P"..

 Found 3 matching materials.

  Band gap  Color
----------  -------
      1.6   Red
      0.33  Black
      1.4   Red
```

* Searching the database for a material with particular color.

```bash
python data_provider.py -db <db file> -sc <color>
```

**Example:**
```bash
>python data_provider.py -db data.db -sc Black

 Searching for materials with color "Black"..

 Found 5 material(s).

Material      Band gap
----------  ----------
In2Te3            1
P                 0.33
Ga2Te3            1.5
In1N1             2.4
Sn1O2             2.7
```

* Searching the database for a material with given band gap in eV. 
For this optionally a tolerance in percentage can be given. 
The default tolerance is 5%.

```bash
python data_provider.py -db <db file> -sb <band gap> -t <tolerance>
```
Or,
```bash
python data_provider.py -db data.db -sb 2.0 -t 5
```

**Example:**
```bash
>python data_provider.py -db data.db -sb 2 -t 2

 Searching for material(s) with band gap: 2.00eV (Tolerance 2.0%)..

 Found 5 material(s) within range.

Material      Band gap  Color
----------  ----------  --------
In2S3             2.03  Red
Hf1S2             1.96  Dark Red
B1P1              2     Red
Cd1P2             2.02  Dark Red
Si2Te3            2     Red
```

* Searching the database for a material with given range of band gap in eV. 

```bash
python data_provider.py -db <db file> --bg_min <minimum band gap> --bg_max <maximum band gap>
```

**Example:**
```bash
>python data_provider.py -db data.db --bg_min 1.5 --bg_max 2

 Searching for material(s) from 1.50eV to 2.00eV band gap..

 Found 10 material(s) within range.

Material      Band gap  Color
----------  ----------  -----------
Zr1S2             1.68  Violet
P                 1.6   Red
Al1Sb1            1.6   Dark Gray
Ga2Se3            1.86  Red
Ga2Te3            1.5   Black
Hf1S2             1.96  Dark Red
Mn1Se1            1.8   Brown-Black
B1P1              2     Red
Al1Sb1            1.62  Dark Gray
Si2Te3            2     Red
```

## Requirements and dependencies:

The code is tested with Python 3.
Other than the python standard libraries, it requires `tabulate` package to output the search results.
Tabulate can be installed using `pip`,
```bash
pip install tabulate
```

Or using `conda`,

```bash
conda install tabulate
```


## Available arguments:

```bash
  -r READ, --read READ  csv file to read
  -s STORE, --store STORE
                        database file to store
  -pr PRINT_ROWS, --print_rows PRINT_ROWS
                        print rows
  -db DATABASE, --database DATABASE
                        database to read from
  -sm MATERIAL, --material MATERIAL
                        search for material
  -sc COLOR, --color COLOR
                        search by color
  -sb BAND_GAP, --band_gap BAND_GAP
                        search by band gap
  -t TOL, --tol TOL     tolerance in percentage
  --bg_min BG_MIN       minimum band gap
  --bg_max BG_MAX       maximum band gap
```

## Test for the classes

The code also includes tests for the classes. The tests can be run using,

```bash
python -m unittest test_data_provider.py -v
```

**Example test output:**

```bash
>python -m unittest test_data_provider.py -v
test_number_of_materials (test_data_provider.TestCSVReader)
Tests if the number of material is correct ... ok
test_property_tuple (test_data_provider.TestCSVReader)
Tests is the tuple returned correctly ... ok
test_band_gap_range_search (test_data_provider.TestDatabaseManager)
Tests if band gap range search is successful or not ... ok
test_band_gap_search (test_data_provider.TestDatabaseManager)
Tests if band gap search is successful or not ... ok
test_color_search (test_data_provider.TestDatabaseManager)
Tests if color search is successful or not ... ok
test_db_creation (test_data_provider.TestDatabaseManager)
Tests if the db file created or not ... ok
test_material_search (test_data_provider.TestDatabaseManager)
Tests if the material search is successful or not ... ok
test_multiple_append (test_data_provider.TestDatabaseManager)
Tests if the multiple append is successful or not ... ok
test_table_creation (test_data_provider.TestDatabaseManager)
Tests if the table was created successfully in the database ... ok

----------------------------------------------------------------------
Ran 9 tests in 1.672s

OK
```

**Caveat for tests:** 

Sometimes Windows is unable to remove the test db `unittest.db` which can result
in failed tests.


