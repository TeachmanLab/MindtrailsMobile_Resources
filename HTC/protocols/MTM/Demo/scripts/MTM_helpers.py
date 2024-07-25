import csv


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence) #old is the separator and occurance is the maxsplit
    return new.join(li) #put new between each value in li


def get_motivation(file_path):
    """ Function that reads in the tips file and outputs a list of the motivational statements

      :param file_path:
      :return: list of lists,[ [Motivational Statement #1, text], [Motivational Statement #2, text]...]

    File I used to make this: https://docs.google.com/spreadsheets/d/10rLLCNmwuo9tkN7XE62bTU8XvY3de4m2GxNrCgqJK2Y/edit#gid=1573494789
    """
    motivation_lst = []
    motivation_num = 0
    with open(file_path, "r") as read_obj:
        reader = csv.reader(read_obj)
        next(reader)
        for row in reader:
            motivation = row[1]
            if motivation not in (None, ""):
                motivation_num += 1
                motivation_lst.append(["Motivational Statement #" + str(motivation_num), motivation])

    return motivation_lst

def get_ER(file_path, group):
    """A function that reads in the file of emotion regulation tips and outputs a dictionary with the ER tips for
    each domain

        :param file_path: string path to ER tips file (.csv)
        :return: dictionary {"Domain" : [index, [ [resource, text], [resource, text]...] ] }
            * keys (str) = domains
            * fields (list) = [index, domain_list_of_ER_tips]
            * domain_list_of_ER_tips (list of lists) = [[Emotion Regulation Strategy # 1, text_1], [Emotion Regulation Strategy # 2, text_2]]
                * each list WITHIN the list is [Emotion Regulation Strategy # 1, text]

        File I used to make this: https://docs.google.com/spreadsheets/d/10rLLCNmwuo9tkN7XE62bTU8XvY3de4m2GxNrCgqJK2Y/edit#gid=1311588813
        """
    career = []
    homelife = []
    finances = []
    mental = []
    physical = []
    social = []
    romantic = []
    early_midstage = []
    presympomatic = []

    ER_lookup = {}
    if group == "HD":
        ER_lookup = {
            "Work/Career Development": [1, career],
            "Family & Home Life": [2, homelife],
            "Finances": [3, finances],
            "Mental Health": [4, mental],
            "Physical Health": [5, physical],
            "Social Situations": [6, social],
            "Romantic Relationships": [7, romantic],
            "Presymptomatic": [8, presympomatic],
            "Early/Mid-Stage Symptoms": [9, early_midstage]
        }
    if group == "PD":
        ER_lookup = {
            "Work/Career Development": [1, career],
            "Family & Home Life": [2, homelife],
            "Finances": [3, finances],
            "Mental Health": [4, mental],
            "Physical Health": [5, physical],
            "Social Situations": [6, social],
            "Romantic Relationships": [7, romantic],
            "Early/Mid-Stage Symptoms": [8, early_midstage]
        }

    for domain in ER_lookup:
        i = ER_lookup[domain][0]
        tip_num = 0

        with open(file_path, "r", encoding="utf-8") as read_obj:
            reader = csv.reader(read_obj)
            next(reader)

            for row in reader:
                # print(row)
                # print(i)
                er_strategy = row[i]
                if er_strategy not in (None, ""):
                    tip_num += 1
                    ER_lookup[domain][1].append(["Emotion Regulation Strategy #" + str(tip_num), er_strategy])
    return ER_lookup

def get_tips(file_path):
    """ Function that reads in the tips file and outputs a list of the tips

    :param file_path:
    :return: list of lists,[ [Tip #1, text], [Tip #2, text]...]

    https://docs.google.com/spreadsheets/d/10rLLCNmwuo9tkN7XE62bTU8XvY3de4m2GxNrCgqJK2Y/edit#gid=0
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