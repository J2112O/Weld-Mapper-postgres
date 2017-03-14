# this module contains helper functions


def station_convert(station_num):
    """
    Using this method to extract the whole and decimal number value out of the linear referencing station num
    :param station_num: passed in String version of the station number collected from the user.
    :return: a whole station int and a decimal float station offset numbers for use in storing in the database
    """
    number_element = station_num.split('+')
    whole_stat_num = int(number_element[0])
    dec_stat_num = float(number_element[1])
    return whole_stat_num, dec_stat_num


def collect_common_atts():
    """
    This function collects all the survey data for the common attributes
    :return: all collected variables into a tuple
    """
    m_station_num = str(input("Station number: "))
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
    return m_station_num, m_gps_shot, m_grade_shot, m_cover, m_notes


def collect_bend():
    m_degree = 0.0
    """
    This function collects all the information for a bend.
    :return: all collected variables are returned to a tuple
    """
    m_direction = str(input("Bend Direction: ")).upper()
    m_type = str(input("Bend Type: ")).upper()
    while True:
        try:
            m_degree = float(input("Degree: "))
        except ValueError:
            print("Decimal Numbers only")
        else:
            break

        return m_direction, m_type, m_degree


def collect_combo_bend():
    m_degree_2 = 0.0
    """
    This function collects the addition two needed attributes for a combo bend
    :return: all collected variables to a tuple
    """
    m_direction_2 = str(input("Direction 2: ")).upper()
    while True:
        try:
            m_degree_2 = float(input("Degree 2: "))
        except ValueError:
            print("Decimal Numbers Only.")
        else:
            break

        return m_direction_2, m_degree_2


def main():


    '''
if __name__ == '__main__':
    main()
'''