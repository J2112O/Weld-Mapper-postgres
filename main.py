import psycopg2 as pg2
import survey_codes as sc
import helper_functions as hf
import db_column_cons as colu
import db_query_helpers as db_helper

code_choices = ("BEND", "WELD", "COMBO BEND")
cur = None
conn = None

try:
    conn = pg2.connect("host=127.0.0.1 dbname=as_built2 user=postgres password=Narmar123 port=5433")
    cur = conn.cursor()
    print("Connected to database. ")
except pg2.DatabaseError as e:
    print(e)


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

    # Creating the Bend Table.
    cur.execute(
        """CREATE TABLE IF NOT EXISTS %s (%s SERIAL PRIMARY KEY, %s REAL NOT
        NULL, %s VARCHAR(25) NOT NULL, %s VARCHAR(25), %s INTEGER UNIQUE NOT NULL,
        FOREIGN KEY(%s) REFERENCES %s(%s));""" % (colu.bend_table, colu.bnd_uid, colu.deg,
                                  colu.bnd_dir, colu.bnd_type, colu.bnd_gps, colu.bnd_gps,
                                  colu.attributes_table, colu.gps_point))
    conn.commit()
    print("{} table created.".format(colu.bend_table))

    # Creating the ComboBend Table.
    cur.execute(
        """CREATE TABLE IF NOT EXISTS %s (%s SERIAL PRIMARY KEY, %s REAL NOT
        NULL, %s VARCHAR(25), %s INTEGER UNIQUE NOT NULL, FOREIGN KEY(%s) REFERENCES %s(%s));""" %
        (colu.cmb_bend_table, colu.cmbo_uid, colu.deg2, colu.bnd_dir2,
         colu.c_bnd_gps, colu.c_bnd_gps, colu.attributes_table, colu.gps_point))
    conn.commit()
    print("{} table created.".format(colu.cmb_bend_table))

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


go_or_stop = str(input("Enter Collect to collect Data, Search to search the"
                       "Database or Exit to leave the program. ")).upper()
while go_or_stop != "EXIT":
    if go_or_stop == "COLLECT":
        for code in code_choices:
            print(code)
        print()
        choice = str(input("Enter the Survey Code to input data for: ")).upper()
        if choice == code_choices[0]:
            # Bend was chosen so calling the needed methods and assigning to variables for tuple unpacking on insert
            common = hf.collect_common_atts()
            # Assigning the above collect values to the Common Attributes class
            ca_atts = sc.CommonAttributes(*common)
            # Inserting into the Common Attributes table
            try:
                cur.execute(
                    """INSERT INTO %s (%s, %s, %s, %s, %s, %s) VALUES ('%s','%s',
                    '%s','%s','%s','%s');""" % (colu.attributes_table,
                                            colu.whole_station,
                                            colu.offset_station, colu.gps_point,
                                            colu.grade_point, colu.depth_cover,
                                            colu.jottings, ca_atts.whole_station_number,
                                            ca_atts.dec_station_num, ca_atts.gps_shot,
                                            ca_atts.grade_shot, ca_atts.cover,
                                            ca_atts.notes))
                conn.commit()
            except pg2.Error as e:
                print(e.pgerror)
            try:
                bendy = hf.collect_bend()
                bnd_atts = sc.Bend(*bendy)
                cur.execute(
                    "INSERT INTO %s (%s, %s, %s, %s) VALUES ('%s','%s','%s','%s');"
                    % (colu.bend_table, colu.deg, colu.bnd_dir, colu.bnd_type,
                       colu.bnd_gps, bnd_atts.degree, bnd_atts.direction,
                       bnd_atts.type, ca_atts.gps_shot))
                conn.commit()
            except pg2.Error as e:
                print(e.pgerror)
        elif choice == code_choices[1]:
            # Weld was chosen so calling the needed methods and assigning to variables for tuple unpacking on insert
            common = hf.collect_common_atts()
            ca_atts = sc.CommonAttributes(*common)
            # Inserting into the Common Attributes table
            try:
                cur.execute(
                    """INSERT INTO %s (%s, %s, %s, %s, %s, %s) VALUES ('%s','%s',
                    '%s','%s','%s','%s');""" % (colu.attributes_table,
                                            colu.whole_station,
                                            colu.offset_station, colu.gps_point,
                                            colu.grade_point, colu.depth_cover,
                                            colu.jottings,
                                            ca_atts.whole_station_number,
                                            ca_atts.dec_station_num,
                                            ca_atts.gps_shot, ca_atts.grade_shot,
                                            ca_atts.cover, ca_atts.notes))
                weldy = hf.collect_weld()
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
                     ca_atts.gps_shot))
                conn.commit()
            except pg2.Error as e:
                print(e.pgerror)
        elif choice == code_choices[2]:
            # ComboBend was chosen so calling the needed methods and assigning to variables for tuple unpacking on
            # insert
            common = hf.collect_common_atts()
            ca_atts = sc.CommonAttributes(*common)
            # Inserting into the Common Attributes table
            try:
                cur.execute(
                    """INSERT INTO %s (%s, %s, %s, %s, %s, %s) VALUES ('%s','%s',
                    '%s','%s','%s','%s');""" % (colu.attributes_table,
                                            colu.whole_station, colu.offset_station,
                                            colu.gps_point, colu.grade_point,
                                            colu.depth_cover, colu.jottings,
                                            ca_atts.whole_station_number,
                                            ca_atts.dec_station_num,
                                            ca_atts.gps_shot, ca_atts.grade_shot,
                                            ca_atts.cover, ca_atts.notes))
                bendy = hf.collect_bend()
                bnd_atts = sc.Bend(*bendy)
                cur.execute(
                    "INSERT INTO %s (%s, %s, %s, %s) VALUES ('%s','%s','%s','%s');" %
                    (colu.bend_table, colu.deg, colu.bnd_dir, colu.bnd_type,
                     colu.bnd_gps, bnd_atts.degree, bnd_atts.direction, bnd_atts.type,
                     ca_atts.gps_shot))
                cmbdy = hf.collect_combo_bend()
                cmbo = sc.ComboBend(*cmbdy)
                cur.execute(
                    "INSERT INTO %s (%s, %s, %s) VALUES ('%s','%s','%s');" %
                    (colu.cmb_bend_table, colu.deg2, colu.bnd_dir2, colu.c_bnd_gps,
                     cmbo.degree_2, cmbo.direction_2, ca_atts.gps_shot))
                conn.commit()
            except pg2.Error as e:
                print(e.pgerror)
    elif go_or_stop == "SEARCH":
        # Using this variable for how many records the user wants returned from the query.
        how_many = str(input("How many Records?\nChoose \"One\" or \"All\" available: ")).upper()
        if how_many == "ONE":
            # Getting the GPS Point from the user to search. This is critical as this is a key found in all database
            # tables.
            find_me = int(input("Enter the GPS Point to Search: "))
            # Getting the code to search for here, in order to call the proper function to use for the query.
            which_code = str(input("Which Code to Search: ")).upper()
            for code in code_choices:
                print(code)
            if which_code == "BEND":
                db_helper.single_bend_query(find_me, cur, conn)
            elif which_code == "COMBO BEND":
                db_helper.single_cmbo_bend_query(find_me, cur, conn)
            else:
                db_helper.single_weld_query(find_me, cur, conn)
        elif how_many == "ALL":
            # Getting the code to search for here, in order to call the proper function to use for the query.
            which_code = str(input("Which Code to Search: ")).upper()
            if which_code == "BEND":
                db_helper.all_bend_query(cur, conn)
            elif which_code == "COMBO BEND":
                db_helper.all_cmbo_bend_query(cur, conn)
            else:
                db_helper.all_weld_query(cur, conn)
if cur:
    cur.close()
