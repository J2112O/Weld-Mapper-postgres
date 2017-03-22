import psycopg2 as pg2
import survey_codes as sc
import collector_functions as cf
import db_column_cons as colu
import database_manager as db_manager
import db_query_helpers as db_helper

code_choices = ("BEND", "WELD", "COMBO BEND")
cur = None
conn = None

try:
    conn = pg2.connect("host=127.0.0.1 dbname=as_built2 user=postgres password=Narmar123 port=5433")
    cur = conn.cursor()
    print("Connected to {} database.".format("as_built2"))
except pg2.DatabaseError as e:
    print(e.pgerror)

# Using the db_manager object to create all tables. Note: all create_table functions are
# wrapped in individual try/except clauses in their respective bodies already.
db_manager.create_attributes_table(cur, conn)  # Creating the attributes table.
db_manager.create_bend_table(cur, conn)  # Creating the bend table.
db_manager.create_cmbo_bnd_table(cur, conn)  # Creating the combo_bend table.
db_manager.create_weld_table(cur, conn)  # Creating the weld table.

go_or_stop = str(input("Enter Collect to collect Data, Search to search the"
                       "Database or Exit to leave the program. ")).upper()
while go_or_stop != "EXIT":
    if go_or_stop == "COLLECT":
        for code in code_choices:
            print(code)
        print()
        choice = str(input("Enter the Survey Code to input data for: ")).upper()
        if choice == code_choices[0]:  # Bend
            # Assigning the results of the collect_common_atts() function to this for
            # tuple unpacking on insert.
            common = cf.collect_common_atts()
            # Assigning the above collected values to the Common Attributes class
            ca_atts = sc.CommonAttributes(*common)
            db_manager.attributes_insert(cur, conn, ca_atts)
        elif choice == code_choices[1]:
            # Assigning the results of the collect_common_atts() function to this for
            # tuple unpacking on insert.
            common = cf.collect_common_atts()
            # Assigning the above collected values to the Common Attributes class
            #ca_atts = sc.CommonAttributes(*common)
            bendy = cf.collect_bend()
            bnd_atts = sc.Bend(*common,*bendy)
            db_manager.attributes_insert(cur, conn, bnd_atts)
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
                     ca_atts.gps_shot))
                conn.commit()
            except pg2.Error as e:
                print(e.pgerror)
        elif choice == code_choices[2]:
            # ComboBend was chosen so calling the needed methods and assigning to variables for tuple unpacking on
            # insert
            common = cf.collect_common_atts()
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
                bendy = cf.collect_bend()
                bnd_atts = sc.Bend(*bendy)
                cur.execute(
                    "INSERT INTO %s (%s, %s, %s, %s) VALUES ('%s','%s','%s','%s');" %
                    (colu.bend_table, colu.deg, colu.bnd_dir, colu.bnd_type,
                     colu.bnd_gps, bnd_atts.degree, bnd_atts.direction, bnd_atts.type,
                     ca_atts.gps_shot))
                cmbdy = cf.collect_combo_bend()
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
