
Data provider
==============

This code takes advantage of two classes: `CSVReader` and `DataManagement`. 
The `CSVReader` class can be used to extract data from a CSV file.
And the `DataManagement` class can be used for storing and retrieving data
to and from a SQLite database, respectively.
An example of a typical workflow can be:

* Retrieving data from a CSV file and store that to a SQLite database.

```bash
python data_provider.py -r <csv file> -s <db file>

```

* Viewing user specified number of rows from the database file.

```bash
python data_provider.py -db <db file> -pr <number of rows>
```

* Searching the database for a particular material.

```bash
python data_provider.py -db <db file> -sm <material name>
```

* Searching the database for a material with particular color.

```bash
python data_provider.py -db <db file> -sc <color>
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

* Searching the database for a material with given range of band gap in eV. 

```bash
python data_provider.py -db <db file> --bg_min <minimum band gap> --bg_max <maximum band gap>
```

## Requirements:

The code is tested with Python 3.
Other than the python standard libraries, it requires `tabulate` package to output the search results.
Tabulate can be installed using `pip`,
```bash
pip install tabulate`
```

Or `conda`

```bash
conda install tabulate`
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

**Caveat for tests:** 

Sometimes Windows is unable to remove the test db `unittest.db` which can result
in failed tests.


