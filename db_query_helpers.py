import psycopg2 as pg
import db_column_cons as cols


def find_weld(find_gps_shot, c_cursor, c_conn):
    """
    This function finds a certain weld in the database that is queried by the user.
    :param find_gps_shot: The gps_shot of the weld in question. supplied by user input
    :param c_cursor: current, active cursor to use
    :param c_conn: current active connection to use
    :return:
    """
    c_cursor.execute(
        """SELECT * FROM %s, %s WHERE %s = '%s';""" % (cols.attributes_table,
                                                       cols.weld_table,
                                                       cols.gps_point,
                                                       find_gps_shot))
    query_result = c_cursor.fetchone()
    final_station = (str(query_result[1]), str(query_result[2]))
    presented_result = {'Station: ': '+'.join(final_station),
                        'GPS Shot: ': query_result[3], 'Grade Shot: ': query_result[4],
                        'Cover: ': query_result[5], 'Notes: ': query_result[6],
                        'Type: ': query_result[8], 'Weld Id: ': query_result[9],
                        'Upstream Asset: ': query_result[10], 'Downstream Asset: ': query_result[11],
                        'Length Ahead: ': query_result[12], 'Heat: ': query_result[13],
                        'Wall Change: ': query_result[14], 'In Ditch: ': query_result[15],
                        'Welder Initials: ': query_result[16]}
    return presented_result
