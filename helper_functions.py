# this module contains helper functions
import psycopg2 as pg
import survey_codes as sc
import db_column_cons as col

bend_directions = ('SAG', 'OVERBEND', 'PI-LT', 'PI-RT') # A tuple of bend directions
bend_types = ('FIELD', 'FORGED', 'FACTORY','HOT') # A tuple of bend types
weld_types = ('MAINLINE', 'TIE-IN', 'FACTORY', 'REPAIR', 'FABRICATION', 'EXISTING', 'VALVE SITE')


def station_convert():
    """
    Using this method to extract the whole and decimal number value out of the linear referencing station num
    :param station_num: passed in String version of the station number collected from the user.
    :return: a whole station int and a decimal float station offset numbers for use in storing in the database
    """
    m_station_num = str(input("Station number: "))
    number_element = m_station_num.split('+')
    whole_stat_num = int(number_element[0])
    dec_stat_num = float(number_element[1])
    return whole_stat_num, dec_stat_num


def collect_common_atts():
    """
    This function collects all the survey data for the common attributes
    :return: all collected variables into a tuple
    """
    m_station_num = str(input("Station number: "))
    number_element = m_station_num.split('+')
    m_whole_stat_num = int(number_element[0])
    m_dec_stat_num = float(number_element[1])
    while True:
        try:
            m_gps_shot = int(input("GPS Shot: "))
        except ValueError:
            print("Whole numbers only")
        else:
            break
    while True:
        try:
            m_grade_shot = int(input("Existing Grade GPS: "))
        except ValueError:
            print("Whole numbers only")
        else:
            break
    while True:
        try:
            m_cover = float(input("Cover: "))
        except ValueError:
            print("Decimal numbers only")
        else:
            break
    m_notes = str(input("Notes: ")).upper()
    return m_whole_stat_num, m_dec_stat_num, m_gps_shot, m_grade_shot, m_cover, m_notes


def collect_weld():
    """
    This function collects all the survey data for a weld.
    :return: All collected variables into a tuple
    """
    for weld in weld_types:
        print(weld)
    print()
    m_weld_type = str(input("Weld Type: ")).upper()
    m_weld_id = str(input("Weld Id: ")).upper()
    m_upstream_asset = str(input("Upstream Asset: ")).upper()
    m_down_asset = str(input("Downstream Asset: ")).upper()
    while True:
        try:
            m_length_ah = float(input("Length Ahead: "))
        except ValueError:
            print("Decimal numbers only")
        else:
            break
    m_heat = str(input("Heat: ")).upper()
    m_wall_change = str(input("Wall Change (Yes or No): ")).upper()
    m_ditch = str(input("Pipe In Ditche (Yes or No): ")).upper()
    m_welder_in = str(input("Welder Initials: ")).upper()
    return m_weld_type, m_weld_id, m_upstream_asset, m_down_asset, m_length_ah,\
            m_heat, m_wall_change, m_ditch, m_welder_in


def collect_bend():
    """
    This function collects the basic bend attributes
    :return: the degree, direction, type of bend
    """
    m_degree = 0.0
    while True:
        try:
            m_degree = float(input("Degree: "))
        except ValueError:
            print("Decimal Numbers only")
        else:
            break
    for direction in bend_directions:
        print(direction)
    print()
    m_direction = str(input("Bend Direction: ")).upper()

    for b_types in bend_types:
        print(b_types)
    print()
    m_type = str(input("Bend Type: ")).upper()
    return m_degree, m_direction, m_type


def collect_combo_bend():
    """
    This function collects the addition two needed attributes for a combo bend
    :return: all collected variables to a tuple
    """
    m_degree_2 = 0.0
    for direction in bend_directions:
        print(direction)
    print()
    m_direction_2 = str(input("Direction 2: ")).upper()
    while True:
        try:
            m_degree_2 = float(input("Degree 2: "))
        except ValueError:
            print("Decimal Numbers Only.")
        else:
            break

    return m_direction_2, m_degree_2


