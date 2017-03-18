import psycopg2 as pg
import db_column_cons as cols


def attributes_query(find_gps_shot, choice, c_cursor, c_conn):
    """
    This function finds a certain weld in the database that is queried by the user.
    :param find_gps_shot: The gps_shot of the weld in question. supplied by user input
    :param c_cursor: current, active cursor to use
    :param c_conn: current active connection to use
    :return a list of common attributes
    """
    presented_result = []
    try:
        c_cursor.execute(
            """SELECT * FROM %s WHERE %s = '%s';""" % (cols.attributes_table,
                                                       cols.gps_point, find_gps_shot))
        query_result = c_cursor.fetchone()
        final_station = (str(query_result[1]), str(query_result[2]))
        presented_result = ['+'.join(final_station), query_result[3], query_result[4], query_result[5], query_result[6]]
        #return presented_result
    except pg.DatabaseError as e:
        print(e.pgerror)


