# This module has survey codes in it.

import helper_functions as hf


class CommonAttributes:
    def __init__(self, whole_station_number, dec_station_num, gps_shot, grade_shot, cover, notes):
        self.whole_station_number = whole_station_number
        self.dec_station_num = dec_station_num
        self.gps_shot = gps_shot
        self.grade_shot = grade_shot
        self.cover = cover
        self.notes = notes


class Weld(CommonAttributes):
    def __init__(self, whole_station_number, dec_station_num, gps_shot, grade_shot, cover, notes, weld_type, weld_id,
                 up_asset, down_asset, length_ah, heat, wall_change, ditch, welder_inits):
        super().__init__(whole_station_number, dec_station_num, gps_shot, grade_shot, cover, notes)
        self.weld_type = weld_type
        self.weld_id = weld_id
        self.up_asset = up_asset
        self.down_asset = down_asset
        self.length_ah = length_ah
        self.heat = heat
        self.wall_change = wall_change
        self.ditch = ditch
        self.welder_inits = welder_inits


class Bend(CommonAttributes):
    def __init__(self, whole_station_number, dec_station_num, gps_shot, grade_shot, cover, notes, degree, direction, kind):
        super().__init__(whole_station_number, dec_station_num, gps_shot, grade_shot, cover, notes)
        self.degree = degree
        self.direction = direction
        self.type = kind


class ComboBend(Bend):
    def __init__(self, whole_station_number, dec_station_num, gps_shot, grade_shot, cover, notes, degree, direction, kind, direction_2, degree_2):
        super().__init__(whole_station_number, dec_station_num, gps_shot, grade_shot, cover, notes, degree, direction, kind)
        self.direction_2 = direction_2
        self.degree_2 = degree_2


def main():
    # Collecting and converting the string value of the station number and assigning for tuple unpacking
    gather_station = hf.station_convert()
    # Collecting all of the common attributes and assigning for tuple unpacking
    gather_ca = hf.collect_common_atts()
    # Collecting all of the bend attributes and assigning for tuple unpacking
    gather_bnd = hf.collect_bend()
    gather_cmbo_bnd = hf.collect_combo_bend()
    bnd_attributes = ComboBend(gather_station[0], gather_station[1], gather_bnd[0], gather_bnd[1], gather_bnd[2],
                          gather_ca[0], gather_ca[1], gather_ca[2], gather_ca[3], gather_cmbo_bnd[0],
                               gather_cmbo_bnd[1])


if __name__ == '__main__':
    main()
