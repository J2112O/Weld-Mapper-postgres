import psycopg2 as pg2
import db_column_cons as col

cur = None
conn = None


try:
    conn = pg2.connect("host=127.0.0.1 dbname=postgres user=postgres password={} port=5433".format(col.password))
    cur = conn.cursor()
    print("Connected to {} database.".format("cut_log"))
    print()
except pg2.DatabaseError as e:
    print(e.pgerror)


def get_records():
    try:
        cur.execute("SELECT * FROM cut_log;")
        results = cur.fetchall()  # Assigning all results to this tuple.
        for record in results:
            print(record)
    except pg2.DatabaseError as e:
        print(e.pgerror)


def main():
    get_records()

if __name__ == '__main__':
    main()
