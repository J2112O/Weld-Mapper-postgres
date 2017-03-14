# This module has survey codes in it.

import helper_functions as hf


class CommonAttributes:
    def __init__(self, station_number, gps_shot, grade_gps, cover, notes):
        self.station_number = station_number
        self.gps_shot = gps_shot
        self.existing_gpd_gps = grade_gps
        self.cover = cover
        self.notes = notes


class Bend(CommonAttributes):
    def __init__(self, station_number, gps_shot, grade_shot, cover, notes, degree, direction, kind):
        super().__init__(station_number, gps_shot, grade_shot, cover, notes)
        self.degree = degree
        self.direction = direction
        self.type = kind


class ComboBend(Bend, CommonAttributes):
    def __init__(self, station_number, gps_shot, grade_shot, cover, notes, degree, direction, kind,
                 direction_2, degree_2):
        super().__init__(station_number, gps_shot, grade_shot, cover, notes)
        super().__init__(degree, direction, kind)
        self.direction_2 = direction_2
        self.degree_2 = degree_2


def main():
    gather_ca = hf.collect_common_atts()
    common_attributes = CommonAttributes(gather_ca[0], gather_ca[1], gather_ca[2], gather_ca[3], gather_ca[4])
    gather_bnd = hf.collect_bend()
    bnd_attributes = Bend(gather_bnd[0], gather_bnd[1], gather_bnd[2]) # Need to fix this.



if __name__ == '__main__':
    main()