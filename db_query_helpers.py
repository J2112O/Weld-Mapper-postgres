import psycopg2 as pg
import db_column_cons as cols


# These are tuples of labels for printing and displaying data to the user from the query functions below.
common_labels = ('Station:', 'GPS Point:', 'Grade GPS Point:', 'Cover:', 'Notes:')
bnd_labels = ('Degree:', 'Direction:', 'Type:')
c_bnd_labels = ('Degree 2:', 'Direction 2:')
weld_labels = ('Weld Type:', 'Weld Id(X-Ray):', 'Upstream Joint:',
               'Downsteam Joint:', 'Length Ahead:', 'Heat:', 'Wall Change:',
               'Location:', 'Welder Initials:')
combined_bnd_labels = bnd_labels + c_bnd_labels


def attributes_query(find_gps_shot, c_cursor, c_conn):
    """
    This function finds a certain set of common attributes in the database that is queried by the user.
    :param find_gps_shot: The gps_shot of the attributes in question. supplied by user input
    :param c_cursor: current, active cursor to use
    :param c_conn: current active connection to use
    :return A list of common attributes
    """
    # An empty list to hold the results from the returned cursor
    presented_result = []
    try:
        c_cursor.execute(
            """SELECT * FROM %s WHERE %s = '%s';""" % (cols.attributes_table,
                                                       cols.gps_point,
                                                       find_gps_shot))
        query_result = c_cursor.fetchone() # Temporary assignment to this tuple.
        # Joining the string values of the whole_station and offset_station for printing/viewing
        final_station = (str(query_result[1]), str(query_result[2]))
        # List of all the final results in a nice readable and printable format for display, in order.
        presented_result = ['+'.join(final_station), query_result[3],
                            query_result[4], query_result[5], query_result[6]]
        for a, b in zip(common_labels, presented_result):
            print(a, b)
        return presented_result
    except pg.DatabaseError as e:
        print(e.pgerror)


def bend_query(findb_gps_shot, cb_cursor, cb_conn):
    """
    This function finds the bend associated with the passed in gps_point.
    :param findb_gps_shot: Associated gps_shot of the bend in question.
    :param cb_cursor: current, active cursor to use
    :param cb_conn: current active connection to use
    :return: A list of the searched bend attributes with common attributes
    """
    # Inner Joining the attributes and bend table on the shared gps_shot
    try:
        cb_cursor.execute(
            """SELECT %s||'+'||%s,%s,%s,%s,%s,%s,%s,%s FROM %s INNER JOIN %s
            ON attributes.gps_shot = bend.gps_shot WHERE attributes.gps_shot =
            '%s';""" % (cols.whole_station, cols.offset_station, findb_gps_shot,
                        cols.grade_point, cols.depth_cover, cols.jottings,
                        cols.deg, cols.bnd_dir, cols.bnd_type,
                        cols.attributes_table, cols.bend_table, findb_gps_shot))
        b_query_result = cb_cursor.fetchone() # Assigning the results of the cursor to this tuple.
        # Adding the common_labels and the bend_labels together for printing with the query results.
        for a, b in zip(common_labels + bnd_labels, b_query_result):
            print(a,b)
            return b_query_result
    except pg.DatabaseError as e:
        print(e.pgerror)


def cmbo_bend_query(cb_gps_shot, cm_cursor, cm_conn):
    """
    This function finds and returns the combo bend associated with the passed in gps_point.
    :param cb_gps_shot: Associated gps_shot of the combo bend in question
    :param cm_cursor: Current, active cursor object
    :param cm_conn: Current active connection to use
    :return: A list of the searched combo bend attributes.
    """
    try:
        cm_cursor.execute(
            """SELECT %s||'+'||%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            FROM %s
            INNER JOIN %s
            ON attributes.gps_shot = bend.gps_shot
            INNER JOIN %s
            ON bend.gps_shot = combo_bend.gps_shot
            WHERE attributes.gps_shot = '%s';"""
            % (cols.whole_station, cols.offset_station, cb_gps_shot,
                cols.grade_point, cols.depth_cover, cols.jottings,
                        cols.deg, cols.bnd_dir, cols.bnd_type, cols.deg2, cols.bnd_dir2,
                        cols.attributes_table, cols.bend_table, cols.cmb_bend_table, cb_gps_shot))
        cb_query_result = cm_cursor.fetchone()
        print(cb_query_result)
        for a, b in zip(common_labels + combined_bnd_labels, cb_query_result):
            print(a,b)
            return cb_query_result
    except pg.DatabaseError as e:
        print(e.pgerror)
