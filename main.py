import psycopg2 as pg
import survey_codes as sc
import helper_functions as hf
import db_column_cons as colu

code_choices = ("BEND", "WELD", "COMBO BEND")
cur = None
conn = None

try:
    conn = pg.connect("host=127.0.0.1 dbname=as_built user=postgres password=Narmar123 port=5433")
    cur = conn.cursor()
    print("Connected to database. ")
except pg.DatabaseError as e:
    print(e)


try:
    # Creating the Common Attributes table.
    cur.execute(
        """CREATE TABLE IF NOT EXISTS %s (%s SERIAL PRIMARY KEY, %s INTEGER NOT NULL, %s
        REAL NOT NULL, %s INTEGER NOT NULL, %s INTEGER NOT NULL, %s REAL NOT
        NULL, %s VARCHAR(25));""" % (colu.attributes_table, colu.ca_uid,
                                     colu.whole_station, colu.offset_station,
                                     colu.gps_point, colu.grade_point,
                                     colu.depth_cover, colu.jottings))
    conn.commit()
    print("{} table created.".format(colu.attributes_table))

    # Creating the Bend Table.
    cur.execute(
        """CREATE TABLE IF NOT EXISTS %s (%s SERIAL PRIMARY KEY REFERENCES %s(%s),
        %s REAL NOT NULL, %s VARCHAR(25) NOT NULL, %s VARCHAR(25));"""
        % (colu.bend_table, colu.bnd_uid, colu.attributes_table,
                colu.ca_uid, colu.deg, colu.bnd_dir, colu.bnd_type))
    conn.commit()
    print("{} table created.".format(colu.bend_table))

    # Creating the ComboBend Table.
    cur.execute(
        """CREATE TABLE IF NOT EXISTS %s (%s SERIAL PRIMARY KEY REFERENCES %s(%s), %s REAL NOT
        NULL, %s VARCHAR(25));"""
        % (colu.cmb_bend_table, colu.cmbo_uid, colu.attributes_table,
                colu.ca_uid, colu.deg2, colu.bnd_dir2))
    conn.commit()
    print("{} table created.".format(colu.cmb_bend_table))

    # Creating the Weld Table.
    cur.execute(
        """CREATE TABLE IF NOT EXISTS %s (%s SERIAL PRIMARY KEY REFERENCES %s(%s), %s VARCHAR(25)
        NOT NULL, %s VARCHAR(25) NOT NULL, %s VARCHAR(25), %s VARCHAR(25), %s REAL
        NOT NULL, %s VARCHAR(25), %s VARCHAR(25) DEFAULT 'N/A', %s VARCHAR(25) NOT
        NULL, %s VARCHAR(25) DEFAULT 'N/A');"""
        % (colu.weld_table, colu.weld_uid, colu.attributes_table, colu.ca_uid,
                colu.wld_type, colu.wld_x_id, colu.upstream_jt, colu.downstream_jt,
                colu.ah_length, colu.ht, colu.wll_chng, colu.ditch_loc, colu.welder_initials))
    conn.commit()
    print("{} table created.".format(colu.weld_table))
except pg.Error as e:
    print(e.pgerror)
#finally:
    #if cur:
        #cur.close()


go_or_stop = str(input("Collect Data? (Yes or No) ")).upper()
while go_or_stop == "YES":
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
        except pg.Error as e:
            print(e.pgerror)
        try:
            bendy = hf.collect_bend()
            bnd_atts = sc.Bend(*bendy)
            cur.execute(
                "INSERT INTO %s (%s, %s, %s) VALUES ('%s','%s','%s');" %
                (colu.bend_table, colu.deg, colu.bnd_dir, colu.bnd_type,
                    bnd_atts.degree, bnd_atts.direction, bnd_atts.type))
            conn.commit()
        except pg.Error as e:
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
                """INSERT INTO %s (%s, %s, %s, %s, %s, %s, %s, %s, %s) VALUES
                ('%s','%s','%s','%s','%s','%s','%s','%s','%s');""" %
                (colu.weld_table, colu.wld_type, colu.wld_x_id,
                 colu.upstream_jt, colu.downstream_jt, colu.ah_length, colu.ht,
                 colu.wll_chng, colu.ditch_loc, colu.welder_initials,
                 wld_atts.weld_type, wld_atts.weld_id, wld_atts.up_asset,
                 wld_atts.down_asset, wld_atts.length_ah, wld_atts.heat,
                 wld_atts.wall_change, wld_atts.ditch, wld_atts.welder_inits))
            conn.commit()
        except pg.Error as e:
            print(e.pgerror)
    elif choice == code_choices[2]:
        # ComboBend was chosen so calling the needed methods and assigning to variables for tuple unpacking on insert
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
                "INSERT INTO %s (%s, %s, %s) VALUES ('%s','%s','%s');" %
                (colu.bend_table, colu.deg, colu.bnd_dir, colu.bnd_type,
                 bnd_atts.degree, bnd_atts.direction,bnd_atts.type))
            cmbdy = hf.collect_combo_bend()
            cmbo = sc.ComboBend(*cmbdy)
            cur.execute(
                "INSERT INTO %s (%s, %s) VALUES ('%s','%s');" %
                (colu.cmb_bend_table, colu.deg2, colu.bnd_dir2, cmbo.degree_2,
                 cmbo.direction_2))
            conn.commit()
        except pg.Error as e:
            print(e.pgerror)


if cur:
    cur.close()
