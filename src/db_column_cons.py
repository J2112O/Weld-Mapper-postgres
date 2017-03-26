# Provides constants used for database table names and column names.

attributes_table = "attributes"
weld_table = "weld"
bend_table = "bend"
cmb_bend_table = "combo_bend"

# Common Attributes table columns here
ca_uid = "id"
whole_station = "whole_station"
offset_station = "offset_station"
gps_point = "gps_shot"
grade_point = "grade_shot"
depth_cover = "cover"
jottings = "notes"

# Bend Table columns here
bnd_uid = "id"
deg = "degree"
bnd_dir = "direction"
bnd_type = "type"
bnd_gps = "gps_shot"

# ComboBend Table columns here
cmbo_uid = "id"
deg2 = "degree_2"
bnd_dir2 = "direction_2"
c_bnd_gps = "gps_shot"

# Weld Table columns here
weld_uid = "id"
wld_type = "type"
wld_x_id = "weld_id"
upstream_jt = "upstream_joint"
downstream_jt = "downstream_joint"
ah_length = "length_ahead"
ht = "heat"
wll_chng = "wall_change"
ditch_loc = "location"
welder_initials = "welder_initials"
wld_gps = "gps_shot"
