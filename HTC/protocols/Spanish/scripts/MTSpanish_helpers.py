import csv


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def get_resources(file_path):
    """A function that reads in the file of resources and outputs a dictionary with the resources for each domain

    :param file_path: string path to resources file (.csv)
    :return: dictionary {"Domain" : [index, [ [resource, text], [resource, text]...] ] }
        * keys (str) = domains
        * fields (list) = [index, domain_list_of_resources]
        * domain_list_of_resources (list of lists) = [[resource_1, text_1], [resource_2, text_2]]
            * each list WITHIN the list is [resource, text]

    File I used to make this: https://docs.google.com/spreadsheets/d/1kenROWNI498AcMhjElrFQD9IjOmnVGInVB8BShSYSx8/edit#gid=437897459
    """
    academics = []
    homelife = []
    finances = []
    mental = []
    physical = []
    social = []
    romantic = []
    discrimination = []

    # The number for each domain is the index for the start
    # For example, "Academics/Work/Career Development" starts at column 1, "Family & Home Life" starts at column 2, etc.
    resources_lookup = {  # changed
        "Académicos/Trabajo/Desarrollo Profesional": [1, academics],
        "Vida Familiar y Doméstica": [3, homelife],
        "Finanzas": [5, finances],
        "Salud Mental": [7, mental],
        "Salud Física": [9, physical],
        "Situaciones Sociales": [11, social],
        "Relaciones Románticas": [13, romantic],
        "Discriminación/Microagresiones": [15, discrimination]
    }

    for domain in resources_lookup:
        i = resources_lookup[domain][0]
        with open(file_path, 'r', encoding='utf-8') as read_obj:
            reader = csv.reader(read_obj)
            next(reader)
            next(reader)
            for row in reader:
                resource = row[i].strip()
                text = row[i + 1].strip() + "\n\n Vaya a la libreria de recursos disponibles para obtener el enlace a este recurso." # changed
                if resource not in (None, ""):
                    resources_lookup[domain][1].append([resource, text])
    return resources_lookup


def get_ER(file_path):
    """A function that reads in the file of emotion regulation tips and outputs a dictionary with the ER tips for
    each domain

        :param file_path: string path to ER tips file (.csv)
        :return: dictionary {"Domain" : [index, [ [resource, text], [resource, text]...] ] }
            * keys (str) = domains
            * fields (list) = [index, domain_list_of_ER_tips]
            * domain_list_of_ER_tips (list of lists) = [[Estrategia de Regulación Emocional # 1, text_1], [Estrategia de Regulación Emocional# 2, text_2]]
                * each list WITHIN the list is [Estrategia de Regulación Emocional # 1, text]

        File I used to make this: https://docs.google.com/spreadsheets/d/1kenROWNI498AcMhjElrFQD9IjOmnVGInVB8BShSYSx8/edit#gid=0
        """
    academics = []
    homelife = []
    finances = []
    mental = []
    physical = []
    social = []
    romantic = []
    other = []

    ER_lookup = {  # changed
        "Académicos/Trabajo/Desarrollo Profesional": [1, academics],
        "Vida Familiar y Doméstica": [2, homelife],
        "Finanzas": [3, finances],
        "Salud Mental": [4, mental],
        "Salud Física": [5, physical],
        "Situaciones Sociales": [6, social],
        "Relaciones Románticas": [7, romantic],
        "Otro": [8, other]
    }

    for domain in ER_lookup:
        i = ER_lookup[domain][0]
        tip_num = 0
        with open(file_path, 'r', encoding='utf-8') as read_obj:
            reader = csv.reader(read_obj)
            next(reader)
            for row in reader:
                er_strategy = row[i]
                if er_strategy not in (None, ""):
                    tip_num += 1
                    ER_lookup[domain][1].append(["Estrategia de Regulación Emocional #" + str(tip_num), er_strategy]) # changed
    return ER_lookup


def get_tips(file_path):
    """ Function that reads in the tips file and outputs a list of the tips

    :param file_path:
    :return: list of lists,[ [Tip #1, text], [Tip #2, text]...]

    https://docs.google.com/spreadsheets/d/1kenROWNI498AcMhjElrFQD9IjOmnVGInVB8BShSYSx8/edit#gid=2086298502
    """
    tip_lst = []
    tip_num = 0
    with open(file_path, 'r', encoding='utf-8') as read_obj:
        reader = csv.reader(read_obj)
        next(reader)
        for row in reader:
            tip = row[1]
            if tip not in (None, ""):
                tip_num += 1
                tip_lst.append(["Consejo #" + str(tip_num), tip]) # changed
    return tip_lst


def get_lessons_learned_text(file_path):
    """
    A function that reads in the file that has the text for each lesson learned.

    :param file_path: file path for lessons learned text (.csv)
    :return: lessons learned dictionary, key = domain, field = lessons learned text for that domain

    https://docs.google.com/spreadsheets/d/1kM80BHglwtsBgxntJDRdfNj-cusgGGJ0sx814ctB1pk/edit#gid=0
    """
    with open(file_path, 'r', encoding='utf-8') as read_obj:
        lessons_learned_dict = {}
        reader = csv.reader(read_obj)
        next(reader)
        for row in reader:
            domain = row[0]
            text = row[1]
            lessons_learned_dict[domain] = text
    return lessons_learned_dict