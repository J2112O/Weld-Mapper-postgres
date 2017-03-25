import psycopg2 as pg2
import db_column_cons as colu


def create_attributes_table(cur, conn):
    """This function creates the attributes table in the database.
    :param
        cur: Active and connected cursor object to the database
    :param
        conn: Active connection object to the database
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
    """This function creates the bend table in the database.
    :param
        cur: Active and connected cursor object to the database
    :param
        conn: Active connection object to the database
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
    """This function creates the combo_bend table in the database.
    :param
         cur: Active and connected cursor object to the database
    :param
        conn: Active connection object to the database
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
    """This function creates the weld table in the database.
    :param
        cur: Active cursor object connection to the database.
    :param
        conn: Active connection object to the database
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


def remove_record(cur, con, gps_shot):
    """Completely remove (delete) a record from the database.
    :param
        cur: The current, active cursor object to the database.
    :param
        con: The current, active connection to the database.
    :param
        gps_shot: The user-supplied gps_shot of the record to delete.
    :return:
        Does not return any object(s).
    """
    remove_sql = "DELETE FROM attributes WHERE gps_shot = %s;"
    point_to_delete = (gps_shot,)
    print("!!!WARNING!!!\nTHIS OPERATION WILL COMPLETELY REMOVE THE RECORD"
          " FROM THE DATABASE!!!!!")
    proceed = str(input("Do you wish to proceed with deleting this record?"
                        " (YES or NO)")).upper()
    if proceed == "YES":
        try:
            cur.execute(remove_sql, point_to_delete)
            con.commit()
            print("Record deleted from database.")
        except pg2.DatabaseError as e:
            print(e.pgerror)
    else:
        print("Record not deleted.")


def attributes_insert(cur, conn, whole_stat, off_stat, gps, grade, cvr, some_notes):
    """This function inserts collected survey attributes into the attributes table.
    :param
        cur: Active and live cursor to the database
    :param
        conn: Active and live connection to the database.
    :param
        whole_stat: Whole station number. ie: (The 89893 in 89893+33.3)
    :param
        off_stat: Offset station number. ie: (The 33.3 in 89893+33.3)
    :param
        gps: gps shot
    :param
        grade: grade shot
    :param
        cvr: cover
    :param
        some_notes: notes
    """
    attrib_sql = "INSERT INTO attributes (whole_station,offset_station,gps_shot" \
                 ",grade_shot,cover,notes) VALUES (%s,%s,%s,%s,%s,%s);"
    values = (whole_stat, off_stat, gps, grade, cvr, some_notes)
    try:
        '''
        cur.execute(
            """INSERT INTO %s (%s, %s, %s, %s, %s, %s) VALUES ('%s','%s',
            '%s','%s','%s','%s');"""
            % (colu.attributes_table, colu.whole_station, colu.offset_station,
               colu.gps_point, colu.grade_point, colu.depth_cover, colu.jottings,
               whole_stat, off_stat, gps, grade, cvr, some_notes))
               '''
        cur.execute(attrib_sql, values)
        conn.commit()
        print("Attribute record inserted successfully.")
    except pg2.Error as e:
        print(e.pgerror)
        print("Attribute record not inserted.")


def bend_insert(cur, conn, some_deg, some_dir, some_type, some_gps):
    """This function inserts the collected bend attributes into the database.
    :param
        cur: Active and current cursor object to the database.
    :param
        conn: Active and current connection object to the database.
    :param
        some_deg: degree
    :param
        some_dir: direction
    :param
        some_type: type of bend.
    :param
        some_gps: gps shot of bend.
    """
    bend_sql = "INSERT INTO bend (degree,direction,type,gps_shot) VALUES (%s,%s,%s,%s);"
    bnd_vals = (some_deg, some_dir, some_type, some_gps)
    try:
        '''
        cur.execute(
            "INSERT INTO %s (%s, %s, %s, %s) VALUES ('%s','%s','%s','%s');"
            % (colu.bend_table, colu.deg, colu.bnd_dir, colu.bnd_type,
               colu.bnd_gps, some_deg, some_dir, some_type, some_gps))
               '''
        cur.execute(bend_sql, bnd_vals)
        conn.commit()
        print("Bend record inserted successfully.")
    except pg2.Error as e:
        print(e.pgerror)
        print("Bend record not inserted.")


def comb_bend_insert(cur, conn, some_deg2, some_dir2, some_gps):
    """This function inserts the collected combo bend attributes into the database.
    :param
        some_gps_point: Passed in gps_shot from the attributes table.
    :param
        cur: Active and current cursor object to the database.
    :param
        conn: Active and current connection object to the database.
    :param
        some_deg2: degree2 of the combo bend
    :param
        some_dir: direction2 of the combo bend.
    :param
        some_gps: gps shot of combo bend.
    """
    try:
        cur.execute(
            "INSERT INTO %s (%s, %s, %s) VALUES ('%s','%s','%s');" %
            (colu.cmb_bend_table, colu.deg2, colu.bnd_dir2, colu.c_bnd_gps,
             some_deg2, some_dir2, some_gps))
        conn.commit()
        print("Combo Bend record inserted successfully.")
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("Combo Bend record not inserted.")


def weld_insert(cur, conn, some_wld_type, some_wld_x_id, some_up_jt, some_dw_jt,
                some_ln, some_ht, some_wall_chg, some_ditch, some_inits,
                some_gps):
    """This function inserts the collected weld attributes into the database.
    :param
        some_gps_point: Passed in gps_shot from the attributes table.
    :param
        cur: Active and current cursor object to the database.
    :param
        conn: Active and current connection object to the database.
    :param
        some_wld_type: type of weld.
    :param
        some_wld_x_id: the weld id or xray
    :param
        some_up_jt: upstream joint asset of the weld
    :param
        some_dw_jt: downstream joint asset of the weld
    :param
        some_ln: length ahead of the weld.
    :param
        some_ht: heat number.
    :param
        some_wall_chg: wall change confirmation of the weld. (yes or no)
    :param
        some_ditch: ditch location of the weld (In ditch? yes or no)
    :param
        some_inits: welder initials. database automatically inserts 'N/A'
        should these values not be required dependent on client requirements.
    :param
        some_: gps_shot associated with this weld.
    """
    try:
        cur.execute(
            """INSERT INTO %s (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');""" %
            (colu.weld_table, colu.wld_type, colu.wld_x_id, colu.upstream_jt,
             colu.downstream_jt, colu.ah_length, colu.ht, colu.wll_chng,
             colu.ditch_loc, colu.welder_initials, colu.wld_gps,
             some_wld_type, some_wld_x_id, some_up_jt, some_dw_jt, some_ln,
             some_ht, some_wall_chg, some_ditch, some_inits, some_gps))
        conn.commit()
        print("Weld record inserted successfully.")
    except pg2.DatabaseError as e:
        print(e.pgerror)
        print("Weld record not inserted.")
