import psycopg2 as pg
import survey_codes as sc
import helper_functions as hf
import db_column_cons as colu

code_choices = ("BEND", "WELD", "COMBO BEND")

try:
    conn = pg.connect("dbname=delta user=postgres password=Narmar123 port=5433")
    cur = conn.cursor()
except ConnectionError:
    print("Could not connect to the database. ")


# Creating the Common Attributes table.
cur.execute(
    """CREATE TABLE IF NOT EXISTS {} ({} SERIAL PRIMARY KEY, {} INTEGER NOT NULL,"
    "{} REAL NOT NULL, {} INTEGER NOT NULL, {} INTEGER NOT NULL, {} REAL NOT
    NULL, {} VARCHAR(25) DEFAULT 'N/A');"""
    ).format(colu.attributes_table, colu.ca_uid, colu.whole_station,
             colu.offset_station, colu.gps_point, colu.grade_point,
             colu.depth_cover, colu.jottings)

# Creating the Bend Table.
cur.execute(
    """CREATE TABLE IF NOT EXISTS {} ({} SERIAL PRIMARY KEY REFERENCES {}({}),
    {} REAL NOT NULL, {} VARCHAR(25) NOT NULL, {} VARCHAR(25));"""
    ).format(colu.bend_table, colu.bnd_uid, colu.attributes_table,
             colu.ca_uid, colu.deg, colu.bnd_dir, colu.bnd_type)

# Creating the ComboBend Table.
cur.execute(
    """CREATE TABLE {} ({} SERIAL PRIMARY KEY REFERENCES {}({}), {} REAL NOT
    NULL, {} VARCHAR(25));"""
    ).format(colu.cmb_bend_table, colu.cmbo_uid, colu.attributes_table,
             colu.ca_uid, colu.deg2, colu.bnd_dir2)

# Creating the Weld Table.
cur.execute(
    """CREATE TABLE {} ({} SERIAL PRIMARY KEY REFERENCES {}({}), {} VARCHAR(25)
    NOT NULL, {} VARCHAR(25) NOT NULL, {} VARCHAR(25), {} VARCHAR(25), {} REAL
    NOT NULL, {} VARCHAR(25), {} VARCHAR(25) DEFAULT 'N/A', {} VARCHAR(25) NOT
    NULL, {} VARCHAR(25) DEFAULT 'N/A');"""
    ).format(colu.weld_table, colu.weld_uid, colu.attributes_table, colu.ca_uid,
             colu.wld_type, colu.wld_x_id, colu.upstream_jt, colu.downstream_jt,
             colu.ah_length, colu.ht, colu.wll_chng, colu.ditch_loc, colu.welder_initials)

for code in code_choices:
    print(code)

print()
choice = str(input("Enter the Survey Code to input data for: ")).upper()

if choice == code_choices[0]:
    # Bend was chosen so calling the needed methods and assigning to variables for tuple unpacking on insert
    station = hf.station_convert()
    common = hf.collect_common_atts()
    # Assigning the above collect values to the Common Attributes class
    ca_atts = sc.CommonAttributes(station[0], station[1], common[0], common[1],
                                  common[2], common[3])
    # Inserting into the Common Attributes table
    cur.execute(
        "INSERT INTO {} ({}, {}, {}, {}, {}, {}) VALUES ({},{},{},{},{},{});"
    ).format(colu.attributes_table, colu.whole_station,
             colu.offset_station, colu.gps_point, colu.grade_point,
             colu.depth_cover, colu.jottings, ca_atts.whole_station_number,
    ca_atts.dec_station_num, ca_atts.gps_shot, ca_atts.grade_shot, ca_atts.cover,
    ca_atts.notes)
    bendy = hf.collect_bend()
    bnd_atts = sc.Bend(bendy[0], bendy[1], bendy[3])
    cur.execute(
        "INSERT INTO {} ({}, {}, {}) VALUES ({},{},{});"
    ).format(colu.bend_table, colu.deg, colu.bnd_dir, colu.bnd_type,
             bnd_atts.degree, bnd_atts.direction, bnd_atts.type)
    cur.close()
elif choice == code_choices[1]:
    # Weld was chosen so calling the needed methods and assigning to variables for tuple unpacking on insert
    station = hf.station_convert()
    common = hf.collect_common_atts()
    ca_atts = sc.CommonAttributes(station[0], station[1], common[0], common[1],
                                  common[2], common[3])
    # Inserting into the Common Attributes table
    cur.execute(
        "INSERT INTO {} ({}, {}, {}, {}, {}, {}) VALUES ({},{},{},{},{},{});"
    ).format(colu.attributes_table, colu.whole_station,
             colu.offset_station, colu.gps_point, colu.grade_point,
             colu.depth_cover, colu.jottings, ca_atts.whole_station_number,
             ca_atts.dec_station_num, ca_atts.gps_shot, ca_atts.grade_shot, ca_atts.cover,
             ca_atts.notes)
    weldy = hf.collect_weld()
    wld_atts = sc.Weld(weldy[0], weldy[1], weldy[2], weldy[3], weldy[4],
                       weldy[5], weldy[6], weldy[7], weldy[8])
    cur.execute(
        """INSERT INTO {} ({}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES ({},{}
        ,{},{},{},{},{},{},{});"""
    ).format(colu.weld_table, colu.wld_type, colu.wld_x_id, colu.upstream_jt,
             colu.downstream_jt, colu.ah_length, colu.ht, colu.ht, colu.wll_chng,
             colu.ditch_loc, colu.welder_initials, wld_atts.weld_type, wld_atts.weld_id,
             wld_atts.up_asset, wld_atts.down_asset, wld_atts.length_ah,
             wld_atts.heat, wld_atts.wall_change, wld_atts.ditch,
             wld_atts.welder_inits)
    cur.close()
elif choice == code_choices[2]:
    # ComboBend was chosen so calling the needed methods and assigning to variables for tuple unpacking on insert
    station = hf.station_convert()
    common = hf.collect_common_atts()
    ca_atts = sc.CommonAttributes(station[0], station[1], common[0], common[1],
                                  common[2], common[3])
    # Inserting into the Common Attributes table
    cur.execute(
        "INSERT INTO {} ({}, {}, {}, {}, {}, {}) VALUES ({},{},{},{},{},{});"
    ).format(colu.attributes_table, colu.whole_station,
             colu.offset_station, colu.gps_point, colu.grade_point,
             colu.depth_cover, colu.jottings, ca_atts.whole_station_number,
             ca_atts.dec_station_num, ca_atts.gps_shot, ca_atts.grade_shot, ca_atts.cover,
             ca_atts.notes)
    bendy = hf.collect_bend()
    bnd_atts = sc.Bend(bendy[0], bendy[1], bendy[2])
    cur.execute(
        "INSERT INTO {} ({}, {}, {}) VALUES ({},{},{});"
    ).format(colu.bend_table, colu.deg, colu.bnd_dir, colu.bnd_type,
             bnd_atts.degree, bnd_atts.direction,bnd_atts.type)
    cmbdy = hf.collect_combo_bend()
    cmbo = sc.ComboBend(cmbdy[0], cmbdy[1])
    cur.execute(
        "INSERT INTO {} ({}, {}) VALUES ({},{});"
    ).format(colu.cmb_bend_table, colu.deg2, colu.bnd_dir2, cmbo.degree_2,
             cmbo.direction_2)
    cur.close()
