import psycopg2 as pg2
import survey_codes as sc
import collector_functions as cf
import database_manager as db_manager
import db_query_helpers as db_helper
import db_column_cons as col

code_choices = ("BEND", "WELD", "COMBO BEND")
cur = None
conn = None

try:
    conn = pg2.connect("host=127.0.0.1 dbname=as_built2 user=postgres password={} port=5433".format(col.password))
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
                       " Database, Delete to delete an existing record, or Exit"
                       " to leave the program. ")).upper()
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
            bendy = cf.collect_bend()
            bnd_atts = sc.Bend(*common,*bendy)
            db_manager.attributes_insert(cur, conn, bnd_atts.whole_station_number,
                                         bnd_atts.dec_station_num, bnd_atts.gps_shot,
                                         bnd_atts.grade_shot, bnd_atts.cover,
                                         bnd_atts.notes)
            db_manager.bend_insert(cur, conn, bnd_atts.degree, bnd_atts.direction,
                                   bnd_atts.type, bnd_atts.gps_shot)
        elif choice == code_choices[1]:  # Weld
            common = cf.collect_common_atts()
            weldy = cf.collect_weld()
            wld_atts = sc.Weld(*common, *weldy)
            db_manager.attributes_insert(cur, conn, wld_atts.whole_station_number,
                                         wld_atts.dec_station_num, wld_atts.gps_shot,
                                         wld_atts.grade_shot, wld_atts.cover,
                                         wld_atts.notes)
            db_manager.weld_insert(cur, conn, wld_atts.weld_type, wld_atts.weld_id,
                                   wld_atts.up_asset, wld_atts.down_asset,
                                   wld_atts.length_ah, wld_atts.heat,
                                   wld_atts.wall_change, wld_atts.ditch,
                                   wld_atts.welder_inits, wld_atts.gps_shot)
        else:  # Combo Bend
            # ComboBend was chosen so calling the needed methods and assigning to variables for tuple unpacking on
            # insert
            common = cf.collect_common_atts()
            bendy = cf.collect_bend()
            cmbdy = cf.collect_combo_bend()
            # Unpacking all the tuples from the collect functions into the
            # ComboBend class params for object creation.
            cmbo_bnd = sc.ComboBend(*common, *bendy, *cmbdy)
            db_manager.attributes_insert(cur, conn, cmbo_bnd.whole_station_number,
                                         cmbo_bnd.dec_station_num, cmbo_bnd.gps_shot,
                                         cmbo_bnd.grade_shot, cmbo_bnd.cover,
                                         cmbo_bnd.notes)
            db_manager.bend_insert(cur, conn, cmbo_bnd.degree, cmbo_bnd.direction,
                                   cmbo_bnd.type, cmbo_bnd.gps_shot)
            db_manager.comb_bend_insert(cur, conn, cmbo_bnd.degree_2,
                                        cmbo_bnd.direction_2, cmbo_bnd.gps_shot)
    elif go_or_stop == "SEARCH":
        # Using this variable for how many records the user wants returned from the query.
        how_many = str(input("How many Records?\nChoose \"One\" , \"Multiple\" "
                             " or \"All\" available: ")).upper()
        if how_many == "ONE":
            # Getting the GPS Point from the user to search. This is critical as this is a key found in all database
            # tables.
            find_me = int(input("Enter the GPS Point to Search: "))
            for code in code_choices:
                print(code)
            # Getting the code to search for here, in order to call the proper function to use for the query.
            which_code = str(input("Which Code to Search: ")).upper()
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
        else:  # MULTIPLE
            which_code = str(input("Which Code to Search: ")).upper()
            for code in code_choices:
                print(code)
            num_of_results = int(input("How many records to return? "))
            if which_code == "BEND":
                db_helper.counted_bend_query(cur, conn, num_of_results)
            elif which_code == "COMBO BEND":
                db_helper.counted_cmbo_query(cur, conn, num_of_results)
            else:
                db_helper.counted_weld_query(cur, conn, num_of_results)
    else:
        gps_to_delete = int(input("GPS Point of the Record to Delete: "))
        db_manager.remove_record(cur, conn, gps_to_delete)

    go_or_stop = str(input("Enter Collect to collect Data, Search to search"
                           " the Database or Exit to leave the program. ")).upper()
if cur:
    cur.close()
