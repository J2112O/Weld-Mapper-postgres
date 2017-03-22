# This module has db query functions in it.
import psycopg2 as pg2
import db_column_cons as cols


# These are tuples of labels for printing and displaying data to the user from the query functions below.
common_labels = ('Station:', 'GPS Point:', 'Grade GPS Point:', 'Cover:',
                 'Notes:')
bnd_labels = ('Degree:', 'Direction:', 'Type:')
c_bnd_labels = ('Degree 2:', 'Direction 2:')
weld_labels = ('Weld Type:', 'Weld Id(X-Ray):', 'Upstream Joint:',
               'Downstream Joint:', 'Length Ahead:', 'Heat:', 'Wall Change:',
               'Location:', 'Welder Initials:')


def attributes_query(find_gps_shot, c_cursor, c_conn, search_count):
    """
    This function finds a certain set of common attributes in the database that is queried by the user.
    :param find_gps_shot: The gps_shot of the attributes being queried. Supplied by user input.
    :param c_cursor: Current, active cursor to use that is connected to the PostgreSQL database.
    :param c_conn: Current active connection to use.
    :return A list of the common attributes of the find_gps_shot query.
    """
    if search_count == 'ONE':
        try:
            c_cursor.execute(
                """SELECT * FROM %s WHERE %s = '%s';""" % (cols.attributes_table,
                                                           cols.gps_point,
                                                           find_gps_shot))
            query_result = c_cursor.fetchone()  # Assigning the one returned record to this tuple.
            # Joining the string values of the whole_station and offset_station
            # for printing/viewing. Decided to code this here on the client side,
            # instead of server side with 'whole_station||'+'||offset_station'
            final_station = (str(query_result[1]), str(query_result[2]))
            # List of all the final results in a nice readable and printable format for display, in order.
            presented_result = ['+'.join(final_station), query_result[3],
                                query_result[4], query_result[5], query_result[6]]
            for a, b in zip(common_labels, presented_result):
                print(a, b)
        except pg2.DatabaseError as e:
            print(e.pgerror)
            print("No Record(s) Found.")
    elif search_count == 'ALL':
        try:
            c_cursor.execute(
                """SELECT * FROM %s;""" % (cols.attributes_table,))
            many_results = c_cursor.fetchall()  # Assigning all the returned records to this tuple.
            many_final_station = (str(many_results[1]), str(many_results[2]))
            many_presented_result = ['+'.join(many_final_station), many_results[3],
                                many_results[4], many_results[5], many_results[6]]
            for a, b in zip(common_labels, many_presented_result):
                print(a, b)
        except pg2.DatabaseError as e:
            print(e.pgerror)
            print("No Record(s) Found.")


def single_bend_query(findb_gps_shot, cb_cursor, cb_conn):
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
            """SELECT %s||'+'||%s,%s,%s,%s,%s,%s,%s,%s
            FROM %s
            INNER JOIN %s
            ON attributes.gps_shot = bend.gps_shot
            WHERE attributes.gps_shot = '%s';"""
            % (cols.whole_station, cols.offset_station, findb_gps_shot,
               cols.grade_point, cols.depth_cover, cols.jottings, cols.deg,
               cols.bnd_dir, cols.bnd_type, cols.attributes_table,
               cols.bend_table, findb_gps_shot))
        # Assigning the results of the cursor to this tuple and fetching one record.
        b_query_result = cb_cursor.fetchone()
        # Merging the common_labels and the bend_labels together for
        # printing with the query results.
        for a, b in zip(common_labels + bnd_labels, b_query_result):
            print(a, b)
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("No Record(s) Found.")


def all_bend_query(cb_cursor, cb_conn):
    """
    This function returns all records from the bend table.
    :param cb_cursor: Current and active cursor to use
    :param cb_conn: Current, active connection to use.
    :return: A list of all the bend records found in the database.
    """
    try:
        cb_cursor.execute(
            """SELECT %s||'+'||%s,attributes.gps_shot,%s,%s,%s,%s,%s,%s
            FROM %s
            INNER JOIN %s
            ON attributes.gps_shot = bend.gps_shot;"""
            % (cols.whole_station, cols.offset_station, cols.grade_point,
               cols.depth_cover, cols.jottings, cols.deg, cols.bnd_dir,
               cols.bnd_type, cols.attributes_table, cols.bend_table))
        # Assigning the results of the cursor to this tuple and fetching all the records.
        b_many_result = cb_cursor.fetchall()
        # Merging the common_labels and the bend_labels together for
        # printing with the query results.
        for record in b_many_result:
            for a, b in zip(common_labels + bnd_labels, record):
                print(a,b)
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("No Record(s) Found.")


def single_cmbo_bend_query(cb_gps_shot, cm_cursor, cm_conn):
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
            AND attributes.gps_shot = bend.gps_shot
            WHERE attributes.gps_shot = '%s';"""
            % (cols.whole_station, cols.offset_station, cb_gps_shot,
               cols.grade_point, cols.depth_cover, cols.jottings, cols.deg,
               cols.bnd_dir, cols.bnd_type, cols.deg2, cols.bnd_dir2,
               cols.attributes_table, cols.bend_table, cols.cmb_bend_table,
               cb_gps_shot))
        # Assigning the results of the cursor to this tuple and fetching one record.
        cb_query_result = cm_cursor.fetchone()
        # Merging the common, bend and combo bend labels together with the query result for printing and displaying
        # to the user.
        for a, b in zip(common_labels + bnd_labels + c_bnd_labels, cb_query_result):
            print(a, b)
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("No Record(s) Found.")


def all_cmbo_bend_query(cm_cursor, cm_conn):
    """
    This function returns all combo_bend records from the database.
    :param cm_cursor: The current active cursor to use.
    :param cm_conn: The current, active connection to the database.
    :return:
    """
    try:
        cm_cursor.execute(
            """SELECT %s||'+'||%s,attributes.gps_shot,%s,%s,%s,%s,%s,%s,%s,%s
            FROM %s
            INNER JOIN %s
            ON attributes.gps_shot = bend.gps_shot
            INNER JOIN %s
            ON bend.gps_shot = combo_bend.gps_shot
            AND attributes.gps_shot = bend.gps_shot;"""
            % (cols.whole_station, cols.offset_station,
               cols.grade_point, cols.depth_cover, cols.jottings, cols.deg,
               cols.bnd_dir, cols.bnd_type, cols.deg2, cols.bnd_dir2,
               cols.attributes_table, cols.bend_table, cols.cmb_bend_table))
        # Assigning the results of the cursor to this tuple and fetching one record.
        # Assigning the results of the cursor to this tuple and fetching all the records.
        many_query_result = cm_cursor.fetchall()
        # Merging the common, bend and combo bend labels together with the query result for printing and displaying
        # to the user.
        for record in many_query_result:
            for a, b in zip(common_labels + bnd_labels + c_bnd_labels, record):
                print(a, b)
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("No Record(s) Found.")


def single_weld_query(w_gps_shot, w_cursor, w_conn):
    """
    This function returns all attributes for a Weld Survey code by INNER JOIN
    on the attributes and weld table
    :param w_gps_shot: The gps_shot of the Weld being queried.
    :param w_cursor: Current active cursor object to use.
    :param w_conn: Current active connection object
    :return: Returns a list of all the attributes for the Weld that is searched.
    """
    try:
        w_cursor.execute(
            """SELECT %s||'+'||%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            FROM %s
            INNER JOIN %s
            ON attributes.gps_shot = weld.gps_shot
            WHERE attributes.gps_shot = '%s';"""
            % (cols.whole_station, cols.offset_station, w_gps_shot,
               cols.grade_point, cols.depth_cover, cols.jottings,
               cols.wld_type, cols.wld_x_id, cols.upstream_jt,
               cols.downstream_jt, cols.ah_length, cols.ht, cols.wll_chng,
               cols.ditch_loc, cols.welder_initials, cols.attributes_table,
               cols.weld_table, w_gps_shot))
        # Assigning the results of the cursor to this tuple and fetching one record.
        wld_query_result = w_cursor.fetchone()
        for a, b in zip(common_labels + weld_labels, wld_query_result):
            print(a, b)
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("No Record(s) Found.")


def all_weld_query(w_cursor, w_conn):
    """
    This function returns all records for welds found in the database.
    :param w_cursor: The current active cursor used for db activity.
    :param w_conn: The current active connection to the database.
    :return: A list of all records for all welds in the database.
    """
    try:
        w_cursor.execute(
            """SELECT %s||'+'||%s,attributes.gps_shot,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            FROM %s
            INNER JOIN %s
            ON attributes.gps_shot = weld.gps_shot;"""
            % (cols.whole_station, cols.offset_station,
               cols.grade_point, cols.depth_cover, cols.jottings,
               cols.wld_type, cols.wld_x_id, cols.upstream_jt,
               cols.downstream_jt, cols.ah_length, cols.ht, cols.wll_chng,
               cols.ditch_loc, cols.welder_initials, cols.attributes_table,
               cols.weld_table))
        # Assigning the results of the cursor to this tuple and fetching all the records.
        wld_many_result = w_cursor.fetchall()
        for record in wld_many_result:
            for a, b in zip(common_labels + weld_labels, record):
                print(a, b)
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("No Record(s) Found.")
