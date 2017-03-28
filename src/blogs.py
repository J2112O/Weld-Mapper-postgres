import psycopg2 as pg2
import db_column_cons as col

cur = None
conn = None


try:
    conn = pg2.connect("host=127.0.0.1 dbname=postgres user=postgres password={} port=5433".format(col.password))
    cur = conn.cursor()
    print("Connected to {} database.".format("cut_log"))  # Just let's us know we are connected to the database.
    print()
except pg2.DatabaseError as e:
    print(e.pgerror)


def get_records():
    try:
        cur.execute("SELECT * FROM cut_log;")
        results = cur.fetchall()  # Assigning all results to this tuple.
        for record in results:  # Basically for each row in the table, print them out for me.
            print(record)
    except pg2.DatabaseError as e:
        print(e.pgerror)


def collect_info():
    print()  # Only used here to create space
    weld_id = str(input("Enter the Weld Id to update: "))
    cut_length = float(input("Enter the length of the cut: "))
    return [weld_id, cut_length]


def update_cuts(pipe_id_name, cut_length):
    sql_statement = """UPDATE cut_log
                    SET cuts = %s,
                    new_lt = length - %s
                    WHERE pipe_id = %s;"""
    values_to_insert = ( cut_length, cut_length, pipe_id_name)
    try:
        cur.execute(sql_statement, values_to_insert)
        conn.commit()
        print("Record updated successfully.")  # Will print this message if our update was successful.
    except pg2.DatabaseError as e:
        print(e.pgerror)


def main():
    get_records()
    values_to_pass = collect_info()
    update_cuts(values_to_pass[0], values_to_pass[1])

if __name__ == '__main__':
    main()
