import psycopg2 as pg2
import db_column_cons as colu
import survey_codes as sc
import collector_functions as cf


def create_attributes_table(cur, conn):
    """
    This function creates the common attributes table.
    :param cur: Active and connected cursor object to the database
    :param conn: Active connection object to the database
    :return: This function does not return any object.
    """
    try:
        # Creating the Common Attributes table.
        cur.execute(
            """CREATE TABLE IF NOT EXISTS %s (%s SERIAL PRIMARY KEY, %s INTEGER NOT NULL, %s
            REAL NOT NULL, %s INTEGER UNIQUE NOT NULL, %s INTEGER NOT NULL, %s REAL NOT
            NULL, %s VARCHAR(25));""" % (colu.attributes_table, colu.ca_uid,
                                        colu.whole_station, colu.offset_station,
                                        colu.gps_point, colu.grade_point,
                                        colu.depth_cover, colu.jottings))
        conn.commit()
        print("{} table created.".format(colu.attributes_table))
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("{} table not created.".format(colu.attributes_table))


def create_bend_table(cur, conn):
    """
    This function creates the bend table.
    :param cur: Active and connected cursor object to the database
    :param conn: Active connection object to the database
    :return: This function does not return any object.
    """
    try:
        # Creating the Bend Table.
        cur.execute(
            """CREATE TABLE IF NOT EXISTS %s (%s SERIAL PRIMARY KEY, %s REAL NOT
            NULL, %s VARCHAR(25) NOT NULL, %s VARCHAR(25), %s INTEGER UNIQUE NOT NULL,
            FOREIGN KEY(%s) REFERENCES %s(%s));""" % (colu.bend_table, colu.bnd_uid, colu.deg,
                                                    colu.bnd_dir, colu.bnd_type, colu.bnd_gps, colu.bnd_gps,
                                                    colu.attributes_table, colu.gps_point))
        conn.commit()
        print("{} table created.".format(colu.bend_table))
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("{} table not created.".format(colu.bend_table))


def create_cmbo_bnd_table(cur, conn):
    """
    This function creates the combo_bend table.
    :param cur: Active and connected cursor object to the database
    :param conn: Active connection object to the database
    :return: This function does not return any object.
    """
    try:
        # Creating the ComboBend Table.
        cur.execute(
            """CREATE TABLE IF NOT EXISTS %s (%s SERIAL PRIMARY KEY, %s REAL NOT
            NULL, %s VARCHAR(25), %s INTEGER UNIQUE NOT NULL, FOREIGN KEY(%s) REFERENCES %s(%s));""" %
            (colu.cmb_bend_table, colu.cmbo_uid, colu.deg2, colu.bnd_dir2,
            colu.c_bnd_gps, colu.c_bnd_gps, colu.attributes_table, colu.gps_point))
        conn.commit()
        print("{} table created.".format(colu.cmb_bend_table))
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("{} table not created.".format(colu.cmb_bend_table))


def create_weld_table(cur, conn):
    """
    This function creates the weld table.
    :param cur: Active and connected cursor object to the database
    :param conn: Active connection object to the database
    :return: This function does not return any object.
    """
    try:
        # Creating the Weld Table.
        cur.execute(
            """CREATE TABLE IF NOT EXISTS %s (%s SERIAL PRIMARY KEY, %s VARCHAR(25)
            NOT NULL, %s VARCHAR(25) NOT NULL, %s VARCHAR(25), %s VARCHAR(25), %s REAL
            NOT NULL, %s VARCHAR(25), %s VARCHAR(25) DEFAULT 'N/A', %s VARCHAR(25) NOT
            NULL, %s VARCHAR(25) DEFAULT 'N/A', %s INTEGER UNIQUE NOT NULL, FOREIGN KEY(%s) REFERENCES %s(%s));"""
            % (colu.weld_table, colu.weld_uid, colu.wld_type, colu.wld_x_id,
            colu.upstream_jt, colu.downstream_jt, colu.ah_length, colu.ht,
            colu.wll_chng, colu.ditch_loc, colu.welder_initials, colu.wld_gps, colu.wld_gps,
            colu.attributes_table, colu.gps_point))
        conn.commit()
        print("{} table created.".format(colu.weld_table))
    except pg2.Error as e:
        print(e.pgerror)
        print("{} table not created.".format(colu.weld_table))


def attributes_insert(cur, conn):
    """
    This function inserted collected survey attributes into the attributes table.
    :param cur: Active and live cursor to the database.
    :param conn: Active and live connection to the database.
    :return: This function does return a tuple of common attribute variables
    to pass and insert the gps_shot variable to other collecting functions.
    """
    # Assigning the results of the collect_common_atts() function to this for
    # tuple unpacking on insert.
    common = cf.collect_common_atts()
    # Assigning the above collected values to the Common Attributes class
    ca_atts = sc.CommonAttributes(*common)
    # Inserting into the Common Attributes table. Note: setting the values of
    # the CommonAttributes class with those member variables.
    try:
        cur.execute(
            """INSERT INTO %s (%s, %s, %s, %s, %s, %s) VALUES ('%s','%s',
            '%s','%s','%s','%s');"""
            % (colu.attributes_table, colu.whole_station, colu.offset_station,
               colu.gps_point, colu.grade_point, colu.depth_cover, colu.jottings,
               ca_atts.whole_station_number, ca_atts.dec_station_num,
               ca_atts.gps_shot, ca_atts.grade_shot, ca_atts.cover,
               ca_atts.notes))
        conn.commit()
        print("Attribute record inserted successfully.")
        return ca_atts
    except pg2.Error as e:
        print(e.pgerror)
        print("Attribute record not inserted.")


def bend_insert(some_gps_point, cur, conn):
    """
    This function inserts the collected bend attributes into the database.
    :param some_gps_point: Passed in gps_shot from the attributes table.
    :param cur: Active and current cursor object to the database.
    :param conn: Active and current connection object to the database.
    :return: This function does not return any object.
    """
    try:
        bendy = cf.collect_bend()
        bnd_atts = sc.Bend(*bendy)
        cur.execute(
            "INSERT INTO %s (%s, %s, %s, %s) VALUES ('%s','%s','%s','%s');"
            % (colu.bend_table, colu.deg, colu.bnd_dir, colu.bnd_type,
               colu.bnd_gps, bnd_atts.degree, bnd_atts.direction,
               bnd_atts.type, some_gps_point))
        conn.commit()
        print("Bend record inserted successfully.")
    except pg2.Error as e:
        print(e.pgerror)
        print("Bend record not inserted.")
