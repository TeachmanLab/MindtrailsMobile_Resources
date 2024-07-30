import csv
import json
import random
import numpy as np
from MTM_helpers import get_motivation, get_ER, get_tips, rreplace
from MTM_create_pages_DEMO import clean_json, create_long_scenario_page_group, create_survey_page, create_resource_page_group_new, create_scenario_page_group, create_json_file

HD_motivation_lookup = get_motivation(r"/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/HD Motivational Statements.csv")
PD_motivation_lookup = get_motivation(r"/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/PD Motivational Statements.csv")

HD_json = {}
PD_json = {}
HD_json_control = {}
PD_json_control = {}

groups = {
    "HD": [4, 4, 4, HD_json], #short scenario index, long scenario index, dose 1 scenarios index
    "PD": [4, 4, 10, PD_json]
}

for group in groups.keys():  # Go through files for each group

    tip_lst = get_tips(file_path=r"/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM tips.csv")

    if group == "HD":
        short_scenarios = "/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM Short Scenarios HD Final Demo.csv"
        ER_lookup = get_ER(file_path=r"/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM ER Strategies- HD.csv", group = group)

    else:
        short_scenarios = "/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM Short Scenarios PD Final Demo.csv"
        ER_lookup = get_ER(file_path=r"/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM ER Strategies- PD.csv", group = group)


    if group == "HD":
        long_page_groups = {
            "Social Situations": [],
            "Physical Health": [],
            "Work/Career Development": [],
            "Family & Home Life": [],
            "Finances": [],
            "Mental Health": [],
            "Romantic Relationships": [],
            "Presymptomatic": [],
            "Early/Mid-Stage Symptoms": []
        }

    else:
        long_page_groups = {
            "Social Situations": [],
            "Physical Health": [],
            "Work/Career Development": [],
            "Family & Home Life": [],
            "Finances": [],
            "Mental Health": [],
            "Romantic Relationships": [],
            "Early/Mid-Stage Symptoms": []
        }


    # added: long scenarios
    if group == "HD":
        long_scenarios_path = "/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM Long Scenarios-HD.csv"
    else:
        long_scenarios_path = "/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM Long Scenarios-PD.csv"

    # print(group)
    with open(long_scenarios_path, "r", encoding="utf-8") as read_file:
        reader = csv.reader(read_file)
        next(reader)  # skip line 1
        next(reader)  # skip line 2

        # print("groups: " + str(groups))
        i = groups[group][1]  # 2nd number in the list is the index (column #) for long scenarios
        for row in reader:
            # print("row" + str(row))
            domain = row[0].strip()
            domain_2 = row[1]
            label = row[3]
            scenario_description = row[i]
            thoughts_lst = [row[i + 2], row[i + 3], row[i + 4], row[i + 5], row[i + 6]]
            feelings_lst = [row[i + 7], row[i + 8], row[i + 9], row[i + 10], row[i + 11]]
            # print("i: " + str(i))
            behaviors_lst = [row[i + 12], row[i + 13], row[i + 14], row[i + 15], row[i + 16]]
            # behaviors_lst = []

            if scenario_description not in (None, "", "NA", "N/A", "n/a", "N/a", "n/A") and label not in (None, ""):
                # create long scenario page group
                page_group = create_long_scenario_page_group(label=label, scenario_description=scenario_description,
                                                             thoughts_lst=thoughts_lst,
                                                             feelings_lst=feelings_lst, behaviors_lst=behaviors_lst)

                # print(group)
                long_page_groups[domain].append(page_group)  # add page group to correct domain's list
                if domain_2 not in (None, ""):  # if it also belongs to a second domain, add the page group to that list
                    long_page_groups[domain_2].append(page_group)
    # shuffle each list of long scenario page groups
    for domain in long_page_groups:
        random.shuffle(long_page_groups[domain])




    # dictionaries for HD
    HD_before_domains_dicts = {}
    HD_dose_1 = {}
    HD_domains_dicts = {}
    HD_after_domains_dicts = {}
    HD_after_domains_dicts_1 = {}
    HD_end_of_day = {}
    HD_biweekly = {}
    HD_biweekly_2 = {}
    HD_biweekly_4 = {}
    HD_biweekly_6 = {}
    HD_biweekly_8 = {}
    HD_biweekly_10 = {}
    HD_biweekly_2_control = {}
    HD_biweekly_4_control = {}
    HD_biweekly_6_control = {}
    HD_biweekly_8_control = {}
    HD_biweekly_10_control = {}
    HD_biweekly_control = {}
    HD_reasons = {}
    HD_reasons_control = {}
    HD_control_dose_1 = {}
    HD_follow_up_control = {}
    HD_biweekly_control_all = {}

    # dictionaries for PD
    PD_before_domains_dicts = {}
    PD_dose_1 = {}
    PD_domains_dicts = {}
    PD_after_domains_dicts = {}
    PD_after_domains_dicts_1 = {}
    PD_end_of_day = {}
    PD_biweekly = {}
    PD_biweekly_2 = {}
    PD_biweekly_4 = {}
    PD_biweekly_6 = {}
    PD_biweekly_8 = {}
    PD_biweekly_10 = {}
    PD_biweekly_2_control = {}
    PD_biweekly_4_control = {}
    PD_biweekly_6_control = {}
    PD_biweekly_8_control = {}
    PD_biweekly_10_control = {}
    PD_biweekly_control = {}
    PD_reasons = {}
    PD_reasons_control = {}
    PD_control_dose_1 = {}
    PD_follow_up_control = {}
    PD_biweekly_control_all = {}

    if group == "HD":
        lookup = {"HD_Dose_1": HD_dose_1,
                  "HD_BeforeDomain_All": HD_before_domains_dicts,
                  "HD_AfterDomain_1": HD_after_domains_dicts_1,
                  "HD_AfterDomain_All": HD_after_domains_dicts,
                  "HD_Control_Dose_1": HD_control_dose_1,
                  "HD_EOD_All": HD_end_of_day,
                  "HD_Biweekly_All": HD_biweekly,
                  "HD_Control_Biweekly": HD_biweekly_control,
                  "HD_Control_Follow-up": HD_follow_up_control,
                  "HD_Biweekly_Week 2": HD_biweekly_2,
                  "HD_Biweekly_Week 4": HD_biweekly_4,
                  "HD_Biweekly_Week 6": HD_biweekly_6,
                  "HD_Biweekly_Week 8": HD_biweekly_8,
                  "HD_Biweekly_Week 10": HD_biweekly_10,
                  "HD_Biweekly_Control_Week 2": HD_biweekly_2_control,
                  "HD_Biweekly_Control_Week 4": HD_biweekly_4_control,
                  "HD_Biweekly_Control_Week 6": HD_biweekly_6_control,
                  "HD_Biweekly_Control_Week 8": HD_biweekly_8_control,
                  "HD_Biweekly_Control_Week 10": HD_biweekly_10_control,
                  "HD_Biweekly_Control_All": HD_biweekly_control_all,
                  "HD_ReasonsforEnding_All": HD_reasons,
                  "HD_ReasonsforEnding_Control_All": HD_reasons_control
                  }
        survey_path = "/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM_survey_questions - Final_HD.csv" #once lemon links updated
    else:
        lookup = {"PD_Dose_1": PD_dose_1,
                  "PD_BeforeDomain_All": PD_before_domains_dicts,
                  "PD_AfterDomain_1": PD_after_domains_dicts_1,
                  "PD_AfterDomain_All": PD_after_domains_dicts,
                  "PD_Control_Dose_1": PD_control_dose_1,
                  "PD_EOD_All": PD_end_of_day,
                  "PD_Biweekly_All": PD_biweekly,
                  "PD_Control_Biweekly": PD_biweekly_control,
                  "PD_Control_Follow-up": PD_follow_up_control,
                  "PD_Biweekly_Week 2": PD_biweekly_2,
                  "PD_Biweekly_Week 4": PD_biweekly_4,
                  "PD_Biweekly_Week 6": PD_biweekly_6,
                  "PD_Biweekly_Week 8": PD_biweekly_8,
                  "PD_Biweekly_Week 10": PD_biweekly_10,
                  "PD_Biweekly_Control_Week 2": PD_biweekly_2_control,
                  "PD_Biweekly_Control_Week 4": PD_biweekly_4_control,
                  "PD_Biweekly_Control_Week 6": PD_biweekly_6_control,
                  "PD_Biweekly_Control_Week 8": PD_biweekly_8_control,
                  "PD_Biweekly_Control_Week 10": PD_biweekly_10_control,
                  "PD_Biweekly_Control_All": PD_biweekly_control_all,
                  "PD_ReasonsforEnding_All": PD_reasons,
                  "PD_ReasonsforEnding_Control_All": PD_reasons_control
                  }
        survey_path = "/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM_survey_questions - Final_PD.csv"
    scenario_dicts = {}

    # Open the file with all the content
    with open(survey_path, "r", encoding="utf-8") as read_obj:
        reader = csv.reader(read_obj)
        next(reader)  # skip first line
        for row in reader:  # each row is a page
            lookup_code = row[3] + "_" + row[2]
            if row[0] == "Practice CBM-I":
                # In the special case that it's "Practice CBM-I", then we have to create scenarios

                with open(r"/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM dose1.csv", "r",
                          encoding="utf-8") as dose1_read_obj:  # scenarios for first dose in file
                    dose1_reader = csv.reader(dose1_read_obj)
                    next(dose1_reader)
                    dose1_scenario_num = 0
                    for row_1 in dose1_reader:
                        # First, add the video that goes before each scenario
                        lookup[lookup_code]["Video" + str(dose1_scenario_num)] = {
                            "Name": "Video " + str(dose1_scenario_num + 1),
                            "Pages": [{
                                "Inputs": [{
                                    "Type": "Text",
                                    "Parameters": {
                                        "Text": "Please press play on the training video below to learn more!"
                                    }
                                },
                                    {
                                        "Type": "Media",
                                        "Parameters": {
                                            "ImageUrl": "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/HTC/protocols/MTM/media/videos/video" +
                                                        str(dose1_scenario_num + 1) + ".mp4",
                                            "ImageType": "video/mp4"
                                        },
                                        "Frame": True
                                    }]}]
                        }

                        # Then, create the scenario
                        label = row_1[3]
                        i = groups[group][2]  # index for dose 1 scenarios
                        domain = row_1[0].strip()
                        puzzle_text_1 = row_1[i]
                        word_1 = row_1[i].split()[-1]
                        if row_1[i].strip()[-1] == ".":  # if there's a period at the end, take all but last char
                            word_1 = row_1[i].split()[-1][:-1]
                        word_2 = None
                        puzzle_text_2 = None
                        puzzle_text_1 = rreplace(puzzle_text_1, " " + word_1, "..", 1)
                        if "N/A" in row_1[i + 1] or row_1[i + 1] in (None, ""):
                            pass
                        elif "N/a" in row_1[i + 1] or row_1[i + 1] in (None, ""):
                            pass
                        elif "n/A" in row_1[i + 1] or row_1[i + 1] in (None, ""):
                            pass
                        elif "n/a" in row_1[i + 1] or row_1[i + 1] in (None, ""):
                            pass
                        else:
                            puzzle_text_2 = row_1[i + 1]  # if there's a second puzzle
                            word_2 = row_1[i + 1].split()[-1][:-1]
                            puzzle_text_2 = rreplace(puzzle_text_2, " " + word_2, "..", 1)
                        comp_question = row_1[i + 2]
                        answers_lst = [row_1[i + 3], row_1[i + 4]]
                        np.random.shuffle(answers_lst)
                        correct_answer = row_1[i + 3]
                        unique_image = False
                        if not (row_1[9].strip() == row_1[15].strip()):
                            unique_image = True
                        # Create scenario page group for the practice
                        page_group = create_scenario_page_group(domain=domain, label=label,
                                                                scenario_num=dose1_scenario_num,
                                                                group=group, puzzle_text_1=puzzle_text_1, word_1=word_1,
                                                                comp_question=comp_question, answers_lst=answers_lst,
                                                                correct_answer=correct_answer, word_2=word_2,
                                                                puzzle_text_2=puzzle_text_2,
                                                                row_num=dose1_scenario_num)

                        lookup[lookup_code]["Anything" + str(dose1_scenario_num)] = page_group
                        if dose1_scenario_num == 0:
                            page_group = {"Name": "Make it your own!",
                                          "Title": "Make it your own!",
                                          "Type": "Survey",
                                          "Pages": [

                                          ]}
                            make_it_your_own_text = "We want Mindtrails Movement to meet your needs. When you complete " \
                                                    "training sessions in the app or browse resources in the " \
                                                    "on-demand resource library, you’ll notice a button that looks " \
                                                    "like a star on the top right-hand corner of your screen. By " \
                                                    "clicking on the star, you can add the info you find most " \
                                                    "helpful (e.g., short stories, tips for managing stress) to your " \
                                                    "own personal Favorites page. You can then revisit your favorite " \
                                                    "parts of the app whenever you’d like by choosing the Favorites " \
                                                    "tile from the Mindtrails Movement homepage!"
                            # do they want to keep this?

                            make_it_your_own_page = create_survey_page(text=make_it_your_own_text,
                                                                       title="Make it your own!")
                            page_group["Pages"].append(make_it_your_own_page)

                            lookup[lookup_code]["Anything_MIYO" + str(dose1_scenario_num)] = page_group

                        dose1_scenario_num += 1
                dose1_scenario_num = 0
            else:
                # create survey page
                if row[2]:  # if it's not blank
                    text = row[4].replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014", " - "). \
                        replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n"). \
                        replace("\u2026", "...")
                    page_group_name = row[0]
                    title = row[1].strip()
                    input_1 = row[5]
                    input_2 = row[6]
                    minimum = row[7]
                    maximum = row[8]
                    media = row[9]
                    items = row[10]
                    image_framed = row[11]
                    timeout = row[12]
                    show_buttons = row[13]
                    variable_name = row[16]
                    conditions_lst = row[17].split('; ')
                    input_name = row[18]

                    # if page group does not exist already, create one
                    # print(lookup)
                    # print(lookup_code)
                    # print(lookup[lookup_code])
                    if page_group_name not in lookup[lookup_code].keys():
                        scenario_dict = {"Name": page_group_name,
                                         "Title": page_group_name,
                                         "Type": "Survey",
                                         "Pages": [

                                         ]}

                        lookup[lookup_code][page_group_name] = scenario_dict

                        # create survey page
                    page = create_survey_page(conditions_lst=conditions_lst, text=text,
                                              show_buttons=show_buttons, media=media, image_framed=image_framed,
                                              items=items, input_1=input_1, input_2=input_2,
                                              variable_name=variable_name, title=title, input_name=input_name,
                                              minimum=minimum, maximum=maximum, timeout=timeout)

                    lookup[lookup_code][page_group_name]["Pages"].append(page)  # add to proper page group

    #### Create dose 1 JSON files ####
    file_name = group + "_dose_1_DEMO.json"
    name = group
    title = "Mindtrails Movement"
    if group == "HD":
        sections = [
            {
                "Name": "dose_1",
                "Doses": [1],
                "PageGroups": list(HD_dose_1.values())
            }
        ]
    else:
        sections = [
            {
                "Name": "dose_1",
                "Doses": [1],
                "PageGroups": list(PD_dose_1.values())
            }
        ]

    create_json_file(file_name, name=name, title=title, sections=sections)

    ### Create group-specific JSON dicts ####
    if group == "HD":
        json_dict = {"Name": group,
                     "Title": "Mindtrails Movement",  # most likely have to change this to MTM
                     "DoseSize": 11,
                     "Sections": [
                         {
                             "Name": "BeforeDomain_All",
                             "PageGroups": list(HD_before_domains_dicts.values())
                         },
                         {
                             "Name": "Domains",
                             "Description": "The domains listed here are some areas that may cause you to feel "
                                            "anxious. Please select the one that you'd like to work on during today's "
                                            "training. \n\nWe encourage you to choose different domains to practice "
                                            "thinking flexibly across areas of your life!",
                             "CanBeFavorited": True,
                             "Domains": []
                         },
                         {
                             "Name": "AfterDomain",
                             "PageGroups": list(HD_after_domains_dicts.values())
                         }

                     ]}
    else:
        json_dict = {"Name": group,
                     "Title": "Mindtrails Movement",  # most likely have to change this to MTM
                     "DoseSize": 11,
                     "Sections": [
                         {
                             "Name": "BeforeDomain_All",
                             "PageGroups": list(PD_before_domains_dicts.values())
                         },
                         {
                             "Name": "Domains",
                             "Description": "The domains listed here are some areas that may cause you to feel "
                                            "anxious. Please select the one that you'd like to work on during today's "
                                            "training. \n\nWe encourage you to choose different domains to practice "
                                            "thinking flexibly across areas of your life!",
                             "CanBeFavorited": True,
                             "Domains": []
                         },
                         {
                             "Name": "AfterDomain",
                             "PageGroups": list(PD_after_domains_dicts.values())
                         }

                     ]}
    control_json_dict = {"Name": group + " control",
                         "Title": "Mindtrails Movement",  # most likely have to change this to MTM
                         "DoseSize": 11,
                         "Sections": [
                             {
                                 "Name": "Domains",
                                 "Description": "The domains listed here are some areas that may cause you to feel "
                                                "anxious. Please select the one that you'd like to work on during today's "
                                                "training. \n\nWe encourage you to choose different domains to practice "
                                                "thinking flexibly across areas of your life!",
                                 "CanBeFavorited": True,
                                 "Domains": []
                             },
                         ]}

    with open(short_scenarios, "r", encoding="utf-8", newline='') as read_obj:
        csv_reader = csv.reader(read_obj)
        next(csv_reader)
        i = groups[group][0]
        domains_dict = {}
        scenario_num = 0
        page_groups_dict = {}

        if group == "HD":
            domains_lookup = {
                "Social Situations": [{}, 0],  # {} will have all the page groups, 0 is the counter of scenarios
                "Physical Health": [{}, 0],
                "Work/Career Development": [{}, 0],
                "Family & Home Life": [{}, 0],
                "Finances": [{}, 0],
                "Mental Health": [{}, 0],
                "Romantic Relationships": [{}, 0],
                "Presymptomatic": [{}, 0],
                "Early/Mid-Stage Symptoms": [{}, 0],
            }
        else:
            domains_lookup = {
                "Social Situations": [{}, 0],  # {} will have all the page groups, 0 is the counter of scenarios
                "Physical Health": [{}, 0],
                "Work/Career Development": [{}, 0],
                "Family & Home Life": [{}, 0],
                "Finances": [{}, 0],
                "Mental Health": [{}, 0],
                "Romantic Relationships": [{}, 0],
                "Early/Mid-Stage Symptoms": [{}, 0],
            }


        row_num = 1
        current_domain = "Holder"
        for row in csv_reader:
            domain = row[0].strip()  # Broad domain 1
            if current_domain != domain and domain not in (
                    None, ""):  # when we change domains, bring row num back to 1 8/29
                # (row[3])
                # print("Domain is...", domain)
                current_domain = domain
                row_num = 1
            # domain_2 = row[1]
            # domain_3 = row[2]
            label = row[3]  # scenario name, MTM title column
            # print(label)

            if domain not in (None, "") and domain:  # if there is a domain

                ## CREATE scenario pages
                if label not in (None, "") and row[i] not in (None, "") and row[i] != "NA" and row[i] != "N/A" and row[i] != "n/a" \
                    and row[i] != "N/a" and row [i] != "n/A" and \
                        "Write Your Own" not in label:  # if it's a scenario
                    if domain not in domains_dict.keys():  # first, create domains. Every time you enter a new domain have to create a new key-value pair
                        domains_dict[domain] = {
                            "Name": domain,
                            "Title": domain,
                            "PageGroups": []  # same set-up as discrimination key-value pair
                        }
                    scenario_num += 1  # increase this counter with every scenario
                    puzzle_text_1 = row[i].replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014", " - "). \
                        replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n"). \
                        replace("\u2026", "...").replace(",..", ",")  # getting scenario body
                    word_1 = row[i].split()[-1]  # getting last word in scenario body
                    if row[i].strip()[-1] == ".":
                        word_1 = row[i].split()[-1][:-1]  # if it ends in a period take everything but the period
                    word_2 = None
                    puzzle_text_2 = None
                    puzzle_text_1 = rreplace(puzzle_text_1, " " + word_1, "..",
                                             1)  # replacing the last word in scenario body with ...


                    if "N/A" in row_1[i + 1] or row_1[i + 1] in (None, ""):
                        pass
                    elif "N/a" in row_1[i + 1] or row_1[i + 1] in (None, ""):
                        pass
                    elif "n/A" in row_1[i + 1] or row_1[i + 1] in (None, ""):
                        pass
                    elif "n/a" in row_1[i + 1] or row_1[i + 1] in (None, ""):
                        pass

                    else:
                        puzzle_text_2 = row[i + 1].replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014",
                                                                                                           " - "). \
                            replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n"). \
                            replace("\u2026", "...")  # if there's a second scenario body
                        word_2 = row[i + 1].split()[-1][:-1]
                        puzzle_text_2 = rreplace(puzzle_text_2, " " + word_2, "..", 1)  # replacing last word with ...
                    comp_question = row[i + 2]
                    answers_lst = [row[i + 3], row[i + 4]]
                    if row[i + 3].strip() == "Yes" or row[i + 3].strip() == "yes":
                        answers_lst.pop()  # removing the row[i +4] element and adding No there
                        answers_lst.append("No")
                    if row[i + 3].strip() == "No" or row[i + 3].strip() == "no":
                        answers_lst.pop()
                        answers_lst.append("Yes")  # removing the row[i + 4] element and adding Yes there
                    np.random.shuffle(answers_lst)  # shuffling them so they're not always in the same order
                    correct_answer = row[i + 3]

                    # get list of words
                    if row[10] not in (None, ""):
                        letters_missing = row[10]  # letters missing column updated 5/14/24 for PD/HD

                    lessons_learned = False
                    if (row_num - 1) % 40 == 0 and (
                            row_num - 1) != 0:  # if it's a multiple of 40 and not the first row, we have to add a lessons learned
                        lessons_learned = True
                    page_group = create_scenario_page_group(domain=domain, label=label, scenario_num=scenario_num,
                                                            group=group, puzzle_text_1=puzzle_text_1, word_1=word_1,
                                                            comp_question=comp_question, answers_lst=answers_lst,
                                                            correct_answer=correct_answer, word_2=word_2,
                                                            puzzle_text_2=puzzle_text_2,
                                                            letters_missing=letters_missing,
                                                            lessons_learned=lessons_learned,
                                                            row_num=row_num)
                    domains_dict[domain]["PageGroups"].append(page_group)  # adding this to the PageGroups list
                    # print(domains_dict[domain]["PageGroups"][0]["Name"]) TEST 6/12
                    if row_num % 10 == 0:  # if it's a multiple of 10, add a resource/tip/ER strategy
                        # new 12/13
                        if group == "HD":
                            motivation_lookup = HD_motivation_lookup
                        else:
                            motivation_lookup = PD_motivation_lookup

                        # print(ER_lookup)
                        # print(domain)
                        page_group = create_resource_page_group_new(motivation_lookup, tip_lst, ER_lookup,
                                                                    domain)  # randomly picks a resource, tip, or strategy page to add
                        domains_dict[domain]["PageGroups"].append(
                            page_group)  # adding resource page group to PageGroups list

                    # added
                    if row_num % 30 == 0:  # if it's a multiple of 30, add a long scenario and a resource
                        if len(long_page_groups[domain]) != 0:  # check to see there are still long scenarios left
                                    # new
                            long_page_group = long_page_groups[domain].pop(0)
                            long_page_groups[domain].append(long_page_group)

                            domains_dict[domain]["PageGroups"].append(long_page_group) #add long page group to PageGroups list
                            if group == "HD":
                                motivation_lookup = HD_motivation_lookup
                            else:
                                motivation_lookup = PD_motivation_lookup

                            page_group = create_resource_page_group_new(motivation_lookup, tip_lst, ER_lookup, domain)
                            domains_dict[domain]["PageGroups"].append(page_group)

                    row_num += 1  # bumps the row number after every row used


            if "Write Your Own" in label:
                row_num += 10  # bump the row by 10 (because the dose size of a long scenario = 10)
                page_group = {"Name": "Write Your Own",
                              "Title": "Write Your Own",
                              "Type": "Survey",
                              "DoseSize": 10,
                              "Pages": [

                              ]}


                with open(r"/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM_write_your_own.csv", "r", encoding="utf-8") \
                        as read_obj_wyo:
                    wyo_reader = csv.reader(read_obj_wyo)
                    next(wyo_reader)
                    for wyo_row in wyo_reader:
                        name = wyo_row[0]
                        title = wyo_row[1]
                        if text not in (None, ""):
                            text = wyo_row[4].replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014",
                                                                                                      " - "). \
                                replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2026",
                                                                                                           "...")
                            input = wyo_row[5]
                            input_name = wyo_row[18]
                            page = create_survey_page(text=text, input_1=input, title=title, input_name=input_name)
                            page_group["Pages"].append(page)




                    domains_dict[domain]["PageGroups"].append(page_group)

                    # now add a resource page
                    if group == "HD":
                        motivation_lookup = HD_motivation_lookup
                    else:
                        motivation_lookup = PD_motivation_lookup

                    page_group = create_resource_page_group_new(motivation_lookup, tip_lst, ER_lookup, domain)

                    domains_dict[domain]["PageGroups"].append(page_group)
    json_dict["Sections"][1]["Domains"] = list(domains_dict.values())
    control_json_dict["Sections"][0]["Domains"] = list(domains_dict.values())

    new_json_dict = groups[group][2]
    json_file = group + " DEMO.json"
    #control_json_file = group + "_control_DEMO.json"

    # replacing '
    json_dict = clean_json(json_dict)

    with open(json_file, 'w', encoding = "utf-8") as outfile:
        json.dump(json_dict, outfile, indent=4)  # data instead of json_dict

    # replacing '
    #control_json_dict = clean_json(control_json_dict)

    #with open(control_json_file, 'w', encoding = "utf-8") as outfile:
        # json.dump(control_json_dict, outfile, indent=4)  # data instead of json_dict

    # change: previously the code below this line are outside of the for loop, they should be in the for loop
    #### Now, create each additional json file####

    ## Create HD end of day survey
    if group == "HD":
        file_name = "HD_EOD_DEMO.json"
        name = "Nightly Survey"
        title = "Nightly Survey"
        sections = [
            {
                "Name": "Nightly Survey",
                "PageGroups": list(HD_end_of_day.values())
            }
        ]
        create_json_file(file_name, name=name, title=title, sections=sections)

    ## Create PD end of day survery
    else:
        file_name = "PD_EOD_DEMO.json"
        name = "Nightly Survey"
        title = "Nightly Survey"
        sections = [
            {
                "Name": "Nightly Survey",
                "PageGroups": list(PD_end_of_day.values())
            }
        ]
        create_json_file(file_name, name=name, title=title, sections=sections)

    ## Create HD biweekly survey
    # "Dose by section" means that each section is considered a "dose." The app will therefore
    # skip from section to section every 2 weeks (this timeframe is set by Ben)
    if group == "HD":
        file_name = "HD_Biweekly_DEMO.json"
        name = "Track Your Progress"
        title = "Track Your Progress"
        dose_by_section = True
        sections = [
            {
                "Name": "Track Your Progress - Week 2",
                "PageGroups": list(HD_biweekly.values()) + list(HD_biweekly_2.values())
            },
            {
                "Name": "Track Your Progress - Week 4",
                "PageGroups": list(HD_biweekly.values()) + list(HD_biweekly_4.values())
            },
            {
                "Name": "Track Your Progress - Week 6",
                "PageGroups": list(HD_biweekly.values()) + list(HD_biweekly_6.values())
            },
            {
                "Name": "Follow-up - Week 10",
                "PageGroups": list(HD_biweekly.values()) + list(HD_biweekly_10.values())
            },
        ]
        create_json_file(file_name, name, title, sections, dose_by_section=dose_by_section)

        # Create biweekly survey for PD participants
    else:
        file_name = "PD_Biweekly_DEMO.json"
        name = "Track Your Progress"
        title = "Track Your Progress"
        dose_by_section = True
        sections = [
            {
                "Name": "Track Your Progress - Week 2",
                "PageGroups": list(PD_biweekly.values()) + list(PD_biweekly_2.values())
            },
            {
                "Name": "Track Your Progress - Week 4",
                "PageGroups": list(PD_biweekly.values()) + list(PD_biweekly_4.values())
            },
            {
                "Name": "Track Your Progress - Week 6",
                "PageGroups": list(PD_biweekly.values()) + list(PD_biweekly_6.values())
            },
            {
                "Name": "Follow-up - Week 10",
                "PageGroups": list(PD_biweekly.values()) + list(PD_biweekly_10.values())
            }
        ]
        create_json_file(file_name, name, title, sections, dose_by_section=dose_by_section)

        # Create biweekly survey for HD participants
    if group == "HD":
        file_name = "HD_Biweekly_control.json"
        name = "Track Your Progress"
        title = "Track Your Progress"
        dose_by_section = True
        sections = [
            {
                "Name": "Track Your Progress - Week 2",
                "PageGroups": list(HD_biweekly.values()) + list(HD_biweekly_2_control.values())
            },
            {
                "Name": "Track Your Progress - Week 4",
                "PageGroups": list(HD_biweekly.values()) + list(HD_biweekly_4_control.values())
            },
            {
                "Name": "Track Your Progress - Week 6",
                "PageGroups": list(HD_biweekly.values()) + list(HD_biweekly_6_control.values())
            },
            {
                "Name": "Follow-up - Week 10",
                "PageGroups": list(HD_biweekly.values()) + list(HD_follow_up_control.values())
            }
        ]
        create_json_file(file_name, name, title, sections, dose_by_section=dose_by_section)

        # Create biweekly survey for PD participants
    else:
        file_name = "PD_Biweekly_control.json"
        name = "Track Your Progress"
        title = "Track Your Progress"
        dose_by_section = True
        sections = [
            {
                "Name": "Track Your Progress - Week 2",
                "PageGroups": list(PD_biweekly.values()) + list(PD_biweekly_2_control.values())
            },
            {
                "Name": "Track Your Progress - Week 4",
                "PageGroups": list(PD_biweekly.values()) + list(PD_biweekly_4_control.values())
            },
            {
                "Name": "Track Your Progress - Week 6",
                "PageGroups": list(PD_biweekly.values()) + list(PD_biweekly_6_control.values())
            },
            {
                "Name": "Follow-up - Week 10",
                "PageGroups": list(PD_biweekly.values()) + list(PD_follow_up_control.values())
            }
        ]
        create_json_file(file_name, name, title, sections, dose_by_section=dose_by_section)

    """

    ## Create the first dose file for HD control
    """
    if group == "HD":
        file_name = "HD_Dose1_control.json"
        name = "Dose 1"
        title = "Get started!"
        sections = [{"Name": "Dose 1",
                     "PageGroups": list(HD_control_dose_1.values())
                     }]
        create_json_file(file_name, name, title, sections)
    # Create the first does file for PD control
    else:
        file_name = "PD_Dose1_control.json"
        name = "Dose 1"
        title = "Get started!"
        sections = [{"Name": "Dose 1",
                     "PageGroups": list(PD_control_dose_1.values())
                     }]
        create_json_file(file_name, name, title, sections)

    # Create reasons for ending for HD
    if group == "HD":
        file_name = "HD_ReasonsForEnding.json"
        name = "Reasons for Ending"
        title = "Reasons for Ending"
        cancel_button_text = "Exit"
        sections = [{
            "Name": "Reasons For Ending",
            "PageGroups": list(HD_reasons.values())
        }]
        create_json_file(file_name, name, title, sections, cancel_button_text=cancel_button_text)

    else:
        file_name = "PD_ReasonsForEnding.json"
        name = "Reasons for Ending"
        title = "Reasons for Ending"
        cancel_button_text = "Exit"
        sections = [{
            "Name": "Reasons For Ending",
            "PageGroups": list(PD_reasons.values())
        }]
        create_json_file(file_name, name, title, sections, cancel_button_text=cancel_button_text)