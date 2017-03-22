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


def attributes_insert(cur, conn, *attribute_obj):
    """
    This function inserted collected survey attributes into the attributes table.
    :param cur: Active and live cursor to the database.
    :param conn: Active and live connection to the database.
    :return: This function does return a tuple of common attribute variables
    to pass and insert the gps_shot variable to other collecting functions.
    """
    # Assigning the results of the collect_common_atts() function to this for
    # tuple unpacking on insert.
    #common = cf.collect_common_atts()
    # Assigning the above collected values to the Common Attributes class
    #ca_atts = sc.CommonAttributes(*common)
    # Inserting into the Common Attributes table. Note: setting the values of
    # the CommonAttributes class with those member variables.
    try:
        cur.execute(
            """INSERT INTO %s (%s, %s, %s, %s, %s, %s) VALUES ('%s','%s',
            '%s','%s','%s','%s');"""
            % (colu.attributes_table, colu.whole_station, colu.offset_station,
               colu.gps_point, colu.grade_point, colu.depth_cover, colu.jottings,
               attribute_obj[0], attribute_obj[1],
               attribute_obj[2], attribute_obj[3], attribute_obj[4],
               attribute_obj[5]))
        conn.commit()
        print("Attribute record inserted successfully.")
    except pg2.Error as e:
        print(e.pgerror)
        print("Attribute record not inserted.")


def bend_insert(cur, conn, *bnd_obj):
    """
    This function inserts the collected bend attributes into the database.
    :param cur: Active and current cursor object to the database.
    :param conn: Active and current connection object to the database.
    :return: This function does not return any object.
    """
    try:
        cur.execute(
            "INSERT INTO %s (%s, %s, %s, %s) VALUES ('%s','%s','%s','%s');"
            % (colu.bend_table, colu.deg, colu.bnd_dir, colu.bnd_type,
               colu.bnd_gps, bnd_obj[7], bnd_obj[8],
               bnd_obj[9], bnd_obj[2]))
        conn.commit()
        print("Bend record inserted successfully.")
    except pg2.Error as e:
        print(e.pgerror)
        print("Bend record not inserted.")


def comb_bend_insert(some_gps_point, cur, conn):
    """
    This function inserts the collected combo bend attributes into the database.
    :param some_gps_point: Passed in gps_shot from the attributes table.
    :param cur: Active and current cursor object to the database.
    :param conn: Active and current connection object to the database.
    :return: This function does not return any object.
    """
    try:
        cmbdy = cf.collect_combo_bend()
        cmbo = sc.ComboBend(*cmbdy)
        cur.execute(
            "INSERT INTO %s (%s, %s, %s) VALUES ('%s','%s','%s');" %
            (colu.cmb_bend_table, colu.deg2, colu.bnd_dir2, colu.c_bnd_gps,
            cmbo.degree_2, cmbo.direction_2, some_gps_point))
        conn.commit()
        print("Combo Bend record inserted successfully.")
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("Combo Bend record not inserted.")


def weld_insert(some_gps_point, cur, conn):
    """
    This function inserts the collected weld attributes into the database.
    :param some_gps_point: Passed in gps_shot from the attributes table.
    :param cur: Active and current cursor object to the database.
    :param conn: Active and current connection object to the database.
    :return: This function does not return any object.
    """
    try:
        weldy = cf.collect_weld()
        wld_atts = sc.Weld(*weldy)
        cur.execute(
            """INSERT INTO %s (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');""" %
            (colu.weld_table, colu.wld_type, colu.wld_x_id, colu.upstream_jt,
             colu.downstream_jt, colu.ah_length, colu.ht, colu.wll_chng,
             colu.ditch_loc, colu.welder_initials, colu.wld_gps,
             wld_atts.weld_type, wld_atts.weld_id, wld_atts.up_asset,
             wld_atts.down_asset, wld_atts.length_ah, wld_atts.heat,
             wld_atts.wall_change, wld_atts.ditch, wld_atts.welder_inits,
             some_gps_point))
        conn.commit()
        print("Weld record inserted successfully.")
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("Weld record not inserted.")
