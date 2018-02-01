from DatabaseManagement import DatabaseManagement
from CSVReader import CSVReader
import argparse


def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--read',help='csv file to read')
    parser.add_argument('-s', '--store', help='database file to store')
    parser.add_argument('-pr', '--print_rows', type=int, help='print rows')
    parser.add_argument('-db', '--database', help='database to read from')
    parser.add_argument('-sm', '--material', help='search for material')
    parser.add_argument('-sc', '--color', help='search by color')
    parser.add_argument('-sb', '--band_gap', type=float, help='search by band gap')
    parser.add_argument('-t', '--tol', type=float, help='tolerance in percentage', default=5)
    parser.add_argument('--bg_min', type=float, help='minimum band gap')
    parser.add_argument('--bg_max', type=float, help='maximum band gap')

    return parser.parse_args()


def process_args():

    args = get_args()

    if args.read and args.store:

        csvr = CSVReader(args.read)

        properties = csvr.get_properties_from_csv()

        dbm = DatabaseManagement(db_name=args.store)

        dbm.create_db()
        dbm.create_table()

        dbm.append_multiple_rows(properties)

    elif args.database and (args.print_rows is not None):

        dbm = DatabaseManagement(db_name=args.database)

        dbm.print_info(num_rows=args.print_rows)

    elif args.database and args.material:

        dbm = DatabaseManagement(db_name=args.database)

        dbm.search_by_material(material_name=args.material)

    elif args.database and args.color:

        dbm = DatabaseManagement(db_name=args.database)

        dbm.search_by_color(color=args.color)

    elif args.database and args.band_gap:

        dbm = DatabaseManagement(db_name=args.database)

        dbm.search_by_band_gap(band_gap=args.band_gap, tol_perc=args.tol)

    elif (args.bg_min is not None) and (args.bg_max is not None):

        dbm = DatabaseManagement(db_name=args.database)

        dbm.search_by_band_gap_range(band_gap_min=args.bg_min, band_gap_max=args.bg_max)

    else:
        print('\n The arguemnts provided are not valid.')


def main():

    process_args()


if __name__ == "__main__":
    main()
