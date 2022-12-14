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

    File I used to make this: https://docs.google.com/spreadsheets/d/1rlWnl_J4n7GF5rWBxKUQSYS0KClIltzZclpcIWo2b7I/edit#gid=918074648
    """
    academics = []
    homelife = []
    finances = []
    mental = []
    physical = []
    social = []
    romantic = []

    # The number for each domain is the index for the start
    # For example, "Academics/Work/Career Development" starts at column 1, "Family & Home Life" starts at column 2, etc.
    resources_lookup = {
        "Academics/Work/Career Development": [1, academics],
        "Family & Home Life": [3, homelife],
        "Finances": [5, finances],
        "Mental Health": [7, mental],
        "Physical Health": [9, physical],
        "Social Situations": [11, social],
        "Romantic Relationships": [13, romantic]
    }

    for domain in resources_lookup:
        i = resources_lookup[domain][0]
        with open(file_path, 'r') as read_obj:
            reader = csv.reader(read_obj)
            next(reader)
            next(reader)
            for row in reader:
                resource = row[i].strip()
                text = row[i + 1].strip() + "\n\n Go to the on-demand library to get the link to this resource."
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
            * domain_list_of_ER_tips (list of lists) = [[Emotion Regulation Strategy # 1, text_1], [Emotion Regulation Strategy # 2, text_2]]
                * each list WITHIN the list is [Emotion Regulation Strategy # 1, text]

        File I used to make this: https://docs.google.com/spreadsheets/d/1rlWnl_J4n7GF5rWBxKUQSYS0KClIltzZclpcIWo2b7I/edit#gid=1311588813
        """
    academics = []
    homelife = []
    finances = []
    mental = []
    physical = []
    social = []
    romantic = []

    ER_lookup = {
        "Academics/Work/Career Development": [1, academics],
        "Family & Home Life": [2, homelife],
        "Finances": [3, finances],
        "Mental Health": [4, mental],
        "Physical Health": [5, physical],
        "Social Situations": [6, social],
        "Romantic Relationships": [7, romantic]
    }

    for domain in ER_lookup:
        i = ER_lookup[domain][0]
        tip_num = 0
        with open(file_path, "r") as read_obj:
            reader = csv.reader(read_obj)
            next(reader)
            for row in reader:
                er_strategy = row[i]
                if er_strategy not in (None, ""):
                    tip_num += 1
                    ER_lookup[domain][1].append(["Emotion Regulation Strategy #" + str(tip_num), er_strategy])
    return ER_lookup


def get_tips(file_path):
    """ Function that reads in the tips file and outputs a list of the tips

    :param file_path:
    :return: list of lists,[ [Tip #1, text], [Tip #2, text]...]

    https://docs.google.com/spreadsheets/d/1rlWnl_J4n7GF5rWBxKUQSYS0KClIltzZclpcIWo2b7I/edit#gid=0
    """
    tip_lst = []
    tip_num = 0
    with open(file_path, "r") as read_obj:
        reader = csv.reader(read_obj)
        next(reader)
        for row in reader:
            tip = row[1]
            if tip not in (None, ""):
                tip_num += 1
                tip_lst.append(["Tip #" + str(tip_num), tip])
    return tip_lst


def get_lessons_learned_text(file_path):
    """
    A function that reads in the file that has the text for each lesson learned. 

    :param file_path: file path for lessons learned text (.csv)
    :return: lessons learned dictionary, key = domain, field = lessons learned text for that domain

    https://docs.google.com/spreadsheets/d/1q-C6dz9lVrrUCfurm4WOnvomxRCYWhVzW76iEGcceVA/edit#gid=0
    """
    with open(file_path, "r") as read_obj:
        lessons_learned_dict = {}
        reader = csv.reader(read_obj)
        next(reader)
        for row in reader:
            domain = row[0]
            text = row[1]
            lessons_learned_dict[domain] = text
    return lessons_learned_dict