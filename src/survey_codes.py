# This module has classes of survey codes.


class CommonAttributes:
    def __init__(self, whole_station_number, dec_station_num, gps_shot, grade_shot, cover, notes):
        self.whole_station_number = whole_station_number
        self.dec_station_num = dec_station_num
        self.gps_shot = gps_shot
        self.grade_shot = grade_shot
        self.cover = cover
        self.notes = notes


class Weld(CommonAttributes):
    def __init__(self, whole_station_number, dec_station_num, gps_shot,
                 grade_shot, cover, notes, weld_type, weld_id, up_asset,
                 down_asset, length_ah, heat, wall_change, ditch, welder_inits):
        super().__init__(whole_station_number, dec_station_num, gps_shot,
                         grade_shot, cover, notes)
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
    def __init__(self, whole_station_number, dec_station_num, gps_shot,
                 grade_shot, cover, notes, degree, direction, kind):
        super().__init__(whole_station_number, dec_station_num, gps_shot,
                         grade_shot, cover, notes)
        self.degree = degree
        self.direction = direction
        self.type = kind


class ComboBend(Bend):
    def __init__(self, whole_station_number, dec_station_num, gps_shot,
                 grade_shot, cover, notes, degree, direction, kind,
                 direction_2, degree_2):
        super().__init__(whole_station_number, dec_station_num, gps_shot,
                         grade_shot, cover, notes, degree, direction, kind)
        self.direction_2 = direction_2
        self.degree_2 = degree_2
