import psycopg2 as pg
import survey_codes as sc
import helper_functions as hf
import db_column_cons as colu

conn = pg.connect("dbname=delta user=postgres password=Narmar123 port=5433")

cur = conn.cursor()

# Creating the Common Attributes table here.
cur.execute("CREATE TABLE IF NOT EXISTS {} ({} SERIAL PRIMARY KEY, {} INTEGER NOT NULL,"
            "{} REAL NOT NULL, {} INTEGER NOT NULL, {} INTEGER NOT NULL,"
            "{} REAL NOT NULL, {} VARCHAR(25) DEFAULT 'N/A');").format(colu.attributes_table, colu.ca_uid,
                                                                       colu.whole_station, colu.offset_station,
                                                                       colu.gps_point, colu.grade_point,
                                                                       colu.depth_cover, colu.jottings)

# Creating the Bend Table here.
cur.execute("CREATE TABLE IF NOT EXISTS {} ({} SERIAL PRIMARY KEY "
            "REFERENCES {}({}), {} REAL NOT NULL,"
            "{} VARCHAR(25) NOT NULL, {} VARCHAR(25));").format(colu.bend_table, colu.bnd_uid,
                                                                colu.attributes_table, colu.ca_uid,
                                                                colu.deg, colu.bnd_dir, colu.bnd_type)

# Creating the ComboBend Table here.
cur.execute("CREATE TABLE {} ({} SERIAL PRIMARY KEY REFERENCES {}({}) , {} REAL NOT NULL, "
            "{} VARCHAR(25));").format(colu.cmb_bend_table, colu.cmbo_uid,
                                       colu.attributes_table, colu.ca_uid,
                                       colu.deg2, colu.bnd_dir2)
