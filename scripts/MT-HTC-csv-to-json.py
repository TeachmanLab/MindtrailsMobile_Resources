import csv
import imghdr
import json
import math
import random
import numpy as np
import pandas as pd
from HTC_helpers import rreplace
from HTC_helpers import get_resources
from HTC_helpers import get_ER
from HTC_helpers import get_tips
from HTC_create_pages import create_survey_page, create_resource_page_group_new
from HTC_create_pages import create_resource_page_group
from HTC_create_pages import create_discrimination_page
from HTC_create_pages import create_scenario_page_group
from HTC_create_pages import create_json_file

## First, read in all resources and tips
undergrad_resources_lookup = get_resources(file_path="/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/"
                                                     "undergrad_resources.csv")
grad_resources_lookup = get_resources(file_path="/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/"
                                                "grad_resources.csv")
faculty_resources_lookup = get_resources(file_path="/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/"
                                                   "faculty_resources.csv")
staff_resources_lookup = get_resources(file_path="/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/"
                                                 "staff_resources.csv")

# Set up empty JSONs
undergraduate_json = {}
graduate_json = {}
faculty_json = {}
staff_json = {}

groups = {
    "Undergraduate": [4, 4, undergraduate_json],
    "Graduate": [10, 21, graduate_json],
    "Faculty": [16, 38, faculty_json],
    "Staff": [22, 55, staff_json]
}

sessionNum = 0
for group in groups.keys():

    ER_lookup = get_ER(file_path="/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/ER_strategies.csv")
    tip_lst = get_tips(file_path="/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/tips.csv")

    # deal w/ long scenarios
    # make list of page groups
    long_page_groups = {
        "Social Situations": [],
        "Physical Health": [],
        "Academics/Work/Career Development": [],
        "Family & Home Life": [],
        "Finances": [],
        "Mental Health": [],
        "Romantic Relationships": [],
    }
    with open("/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/HTC_long_scenarios.csv") as read_file:
        reader = csv.reader(read_file)
        next(reader)
        next(reader)
        i = groups[group][1]
        for row in reader:

            domain = row[0].strip()
            domain_2 = row[1]
            label = row[3]
            scenario_description = row[i]
            image = row[i + 1]
            unique_image = False
            if not (row[9].strip() == row[15].strip() == row[21].strip() == row[27].strip()):
                unique_image = True
            if group == "Undergraduate":
                group_name = "undergrad"
            if group == "Graduate":
                group_name = "grad"
            if group == "Faculty":
                group_name = "faculty"
            else:
                group_name = "staff"
            if unique_image:
                image_url = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/HTC/protocols/protocol1/" \
                            "media/images/" + label.strip().replace(" ", "_") + "_" + group_name + ".jpeg"
            else:
                image_url = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/HTC/protocols/protocol1/" \
                            "media/images/" + label.strip().replace(" ", "_") + ".jpeg"
            if label not in (None, ""):
                # each row corresponds to one page group
                page_group = {"Name": "Long Scenario: " + label.strip(),
                              "Title": "Long Scenario: " + label.strip(),
                              "Type": "Scenario",
                              "DoseSize": 10,
                              "Pages": [

                              ]}
                # scenario_list =
                if scenario_description not in (
                        None, "") and scenario_description != "NA" and scenario_description != "N/A":
                    with open("HTC/csv_files/htc_long_scenarios_structure.csv", "r") as csvfile:
                        csv_reader = csv.reader(csvfile)
                        next(csv_reader)
                        next(csv_reader)
                        image_bool = False
                        for row_str in csv_reader:
                            if "[Scenario_Description]" in row_str[0]:
                                image_bool = True
                            label_str = row_str[0].replace("[Scenario_Name]", label)
                            text = row_str[4].replace("[Scenario_Description]", scenario_description). \
                                replace("\u2013", " - ").replace("\u2014", " - "). \
                                replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2019",
                                                                                                           "'").replace(
                                "  ", " ")
                            input_1 = row_str[6]
                            input_2 = row_str[7]

                            if image_bool:
                                page = {
                                    "Name": label.strip(),
                                    "Title": label_str,
                                    "ImageUrl": image_url,
                                    "ImageType": "image/jpeg",
                                    "Inputs": [{
                                        "Type": "Text",
                                        "Parameters": {
                                            "Text": text
                                        }
                                    }]
                                }
                            else:
                                # print("Creating page", label)
                                page = {
                                    "Name": label.strip(),
                                    "Title": label_str,
                                    "Inputs": [{
                                        "Type": "Text",
                                        "Parameters": {
                                            "Text": text
                                        }
                                    }]
                                }

                            # if there's a timeout
                            if row_str[13] not in (None, ""):
                                page["Timeout"] = int(row_str[13])
                                page["ShowButtons"] = "AfterTimeout"

                            # if there's an entry
                            if "Entry" in input_1:
                                page["Inputs"].append({
                                    "Type": "Entry",
                                    "Name": row_str[0].replace("[Scenario_Name]: ", row[3] + "_")
                                })
                            # if there's timedtext
                            if input_1 == "TimedText":
                                page["ShowButtons"] = "WhenCorrect"
                                if "thoughts" in text:
                                    thoughts_lst = [row[i + 2], row[i + 3], row[i + 4], row[i + 5], row[i + 6]]
                                    page["Inputs"].append({
                                        "Type": "TimedText",
                                        "Parameters": {
                                            "Text": [row[i + 2], row[i + 3], row[i + 4],
                                                     row[i + 5], row[i + 6]],  # corresponds to thoughts in csv
                                            "Duration": 15
                                        }
                                    })
                                if "feelings" in text:
                                    feelings_lst = [row[i + 7], row[i + 8], row[i + 9], row[i + 10], row[i + 11]]
                                    random.shuffle(feelings_lst)
                                    page["Inputs"].append({
                                        "Type": "TimedText",
                                        "Parameters": {
                                            "Text": feelings_lst,
                                            "Duration": 15
                                        }
                                    })
                                if "behaviors" in text:
                                    behaviors_lst = [row[i + 12], row[i + 13], row[i + 14], row[i + 15], row[i + 16]]
                                    random.shuffle(behaviors_lst)
                                    page["Inputs"].append({
                                        "Type": "TimedText",
                                        "Parameters": {
                                            "Text": behaviors_lst,
                                            "Duration": 15
                                        }
                                    })

                            image_bool = False
                            page_group["Pages"].append(page)
                long_page_groups[domain].append(page_group)
                if domain_2 not in (None, ""):
                    long_page_groups[domain_2].append(page_group)

    for domain in long_page_groups:
        random.shuffle(long_page_groups[domain])
        for long_scenario in long_page_groups[domain]:
            print(long_scenario["Title"])

    sessionNum += 1

    domains_data = []
    before_domains_data = []
    after_domains_data = []

    # before_domains_data
    with open("HTC/csv_files/HTC_before_after.csv", "r") as read_obj:
        reader = csv.reader(read_obj)
        next(reader)
        before_domains_dicts = {}
        before_domains_dicts_1 = {}
        domains_dicts = {}
        after_domains_dicts = {}
        after_domains_dicts_1 = {}
        end_of_day = {}
        biweekly = {}
        biweekly_2 = {}
        biweekly_4 = {}
        biweekly_6 = {}
        biweekly_8 = {}
        biweekly_2_control = {}
        biweekly_4_control = {}
        biweekly_6_control = {}
        biweekly_8_control = {}
        reasons = {}
        control_1 = {}

        # parse before after
        lookup = {"BeforeDomain_1": before_domains_dicts_1,
                  "BeforeDomain_All": before_domains_dicts,
                  "AfterDomain_1": after_domains_dicts_1,
                  "AfterDomain_All": after_domains_dicts,
                  "BeforeDomain_1 Control": control_1,
                  "EOD_EOD": end_of_day,
                  "Biweekly_Biweekly": biweekly,
                  "Biweekly_Week 2": biweekly_2,
                  "Biweekly_Week 4": biweekly_4,
                  "Biweekly_Week 6": biweekly_6,
                  "Biweekly_Week 8": biweekly_8,
                  "Biweekly_Control_Week 2": biweekly_2_control,
                  "Biweekly_Control_Week 4": biweekly_4_control,
                  "Biweekly_Control_Week 6": biweekly_6_control,
                  "Biweekly_Control_Week 8": biweekly_8_control,
                  "ReasonsForEnding_ReasonsForEnding": reasons
                  }
        scenario_dicts = {}
        for row in reader:  # each row is a page
            if row[0] == "Practice CBM-I":
                lookup_code = row[3] + "_" + row[2]  # this is BeforeDomain_1 for e
                with open("HTC/csv_files/dose1_scenarios.csv") as read_obj:
                    dose1_reader = csv.reader(read_obj)
                    next(dose1_reader)
                    scenario_num = 0
                    for row_1 in dose1_reader:
                        # first add the video that goes before each scenario
                        lookup[lookup_code]["Video" + str(scenario_num)] = {
                            "Name": "Video " + str(scenario_num + 1),
                            "Pages": [{
                                "Inputs": [{
                                    "Type": "Media",
                                    "Parameters": {
                                        "ImageUrl": "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw"
                                                    "/main/HTC/protocols/protocol1/media/videos/" + group + "/video" +
                                                    str(scenario_num + 1) + ".mp4",
                                        "ImageType": "video/mp4"
                                    },
                                    "Frame": True
                                }]}]
                        }

                        label = row_1[3]
                        i = groups[group][0]
                        domain = row_1[0].strip()

                        puzzle_text_1 = row_1[i]

                        word_1 = row_1[i].split()[-1]
                        if row_1[i].strip()[-1] == ".":
                            word_1 = row_1[i].split()[-1][:-1]
                        word_2 = None
                        puzzle_text_2 = None
                        puzzle_text_1 = rreplace(puzzle_text_1, " " + word_1, "..", 1)
                        if "N/A" in row_1[i + 1] or row_1[i + 1] in (None, ""):
                            pass
                        else:
                            puzzle_text_2 = row_1[i + 1]  # if there's a second puzzle
                            word_2 = row_1[i + 1].split()[-1][:-1]
                            puzzle_text_2 = rreplace(puzzle_text_2, " " + word_2, "..", 1)
                        comp_question = row_1[i + 2]
                        answers_lst = [row_1[i + 3], row_1[i + 4]]
                        if row_1[i + 3].strip() == "Yes":
                            answers_lst.pop()
                            answers_lst.append("No")
                        if row_1[i + 3].strip() == "No":
                            answers_lst.pop()
                            answers_lst.append("Yes")
                        np.random.shuffle(answers_lst)
                        correct_answer = row_1[i + 3]
                        # get list of words

                        # then create scenario page group for the practice
                        page_group = create_scenario_page_group(domain=domain, label=label, scenario_num=scenario_num,
                                                                group=group, puzzle_text_1=puzzle_text_1, word_1=word_1,
                                                                comp_question=comp_question, answers_lst=answers_lst,
                                                                correct_answer=correct_answer, word_2=word_2,
                                                                puzzle_text_2=puzzle_text_2, can_be_favorited=True,
                                                                unique_image=False, row_num=scenario_num)

                        lookup[lookup_code]["anything" + str(scenario_num)] = page_group
                        if scenario_num == 0:
                            page_group = {"Name": "Make it your own!",
                                          "Title": "Make it your own!",
                                          "Type": "Survey",
                                          "Pages": [

                                          ]}
                            make_it_your_own_text = "We want Hoos Think Calmly to meet your needs. When you complete " \
                                                    "training sessions in the app or browse resources in the on-demand " \
                                                    "resource library, you’ll notice a button that looks like a star on " \
                                                    "the top right-hand corner of your screen. By clicking on the star, " \
                                                    "you can add the info you find most helpful (e.g., short stories, " \
                                                    "tips for managing stress) to your own personal Favorites page. You " \
                                                    "can then revisit your favorite parts of the app whenever you’d like " \
                                                    "by choosing the Favorites tile from the Hoos Think Calmly homepage!"
                            make_it_your_own_page = create_survey_page(text=make_it_your_own_text,
                                                                       title="Make it your own!")
                            page_group["Pages"].append(make_it_your_own_page)

                            lookup[lookup_code]["Make_it_your_own" + str(scenario_num)] = page_group

                        scenario_num += 1
                scenario_num = 0
            else:
                # create survey page
                if row[2]:
                    doses = row[2]
                    lookup_code = row[3] + "_" + row[2]  # this is BeforeDomain_1 for ex
                    before_after = row[3]
                    text = row[4].replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014", " - "). \
                        replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n"). \
                        replace("\u2026", "...")
                    page_group = row[0]
                    title = row[1].strip()
                    input_1 = row[5]
                    input_2 = row[6]
                    minimum = row[7]
                    maximum = row[8]
                    media = row[9]
                    other_choices = row[10]
                    image_framed = row[11]
                    timeout = row[12]
                    show_buttons = row[13]
                    variable_name = row[16]
                    conditions_lst = row[17].split('; ')
                    input_name = row[18]
                    # if page group does not exist already, create one
                    if page_group not in lookup[lookup_code].keys():
                        scenario_dict = {"Name": page_group,
                                         "Title": page_group,
                                         "Type": "Survey",
                                         "Pages": [

                                         ]}
                        # if input_1 in (None, "") and timeout in (None, "") and other_choices in (None, ""):
                        #     scenario_dict["Type"] = "Information"
                        lookup[lookup_code][page_group] = scenario_dict

                    # create page

                    page = create_survey_page(conditions_lst=conditions_lst, text=text,
                                              show_buttons=show_buttons, media=media, image_framed=image_framed,
                                              other_choices=other_choices, input_1=input_1, input_2=input_2,
                                              variable_name=variable_name, title=title, page_group=page_group,
                                              input_name=input_name, minimum=minimum, maximum=maximum,
                                              timeout=timeout)
                    lookup[lookup_code][page_group]["Pages"].append(page)

    json_dict = {"Name": group,
                 "Title": "Hoos Think Calmly",
                 "TimeToComplete": "00:10:00",
                 "Sections": [
                     {
                         "Name": "BeforeDomain_1",
                         "Doses": [1],
                         "PageGroups": list(before_domains_dicts_1.values())
                     },
                 ]}
    json_file = "HTC/json_files/" + group + "_dose_1.json"
    with open(json_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)  # data instead of json_dict

    json_dict = {"Name": group,
                 "Title": "Hoos Think Calmly",
                 "TimeToComplete": "00:10:00",
                 "DoseSize": 11,
                 "Sections": [
                     {
                         "Name": "BeforeDomain_All",
                         "PageGroups": list(before_domains_dicts.values())
                     },
                     {
                         "Name": "Domains",
                         "Description": "The domains listed here are some areas that may cause you to feel "
                                        "anxious. Please select the one that you'd like to work on during today's "
                                        "training. \n\nWe encourage you to choose different domains to practice "
                                        "thinking flexibly across areas of your life!",
                         "Domains": []
                     },
                     {
                         "Name": "AfterDomain",
                         "PageGroups": list(after_domains_dicts.values())
                     }

                 ]}
    # df = pd.read_csv("/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/HTC_scenarios.csv",
    #                  header=None,
    #                  skiprows=1)
    #
    # ds = df.sample(frac=1)
    #
    # ds.to_csv("HTC/csv_files/shuffled_scenarios.csv", index=False)

    with open("/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/HTC_scenarios.csv", newline='') as read_obj:
        csv_reader = csv.reader(read_obj)
        next(csv_reader)
        i = groups[group][0]
        domains_dict = {}
        scenario_num = 0
        page_groups_dict = {}
        # {} below are all the page group dicts
        # Microdose {count / 10 } : page_group
        # Microdose {count / 10 } : page_group
        # domains_lookup = {
        #     "Social Situations": [{}, 0], # {} will have all the page groups, 0 is the counter of scenarios
        #     "Physical Health": [{}, 0],
        #     "Academics/Work/Career Development": [{}, 0],
        #     "Family & Home Life": [{}, 0],
        #     "Finances": [{}, 0],
        #     "Mental Health/Self-Evaluation": [{}, 0],
        #     "Romantic Relationships": [{}, 0],
        #     "Unspecified": [{}, 0],
        #     "Indecision/Decision-Making": [{}, 0]
        # }
        domains_lookup = {
            "Social Situations": [{}, 0],  # {} will have all the page groups, 0 is the counter of scenarios
            "Physical Health": [{}, 0],
            "Academics/Work/Career Development": [{}, 0],
            "Family & Home Life": [{}, 0],
            "Finances": [{}, 0],
            "Mental Health": [{}, 0],
            "Romantic Relationships": [{}, 0],
            "Discrimination": [{}, 0]
        }
        domains_dict["Discrimination"] = {
            "Name": "Discrimination",
            "Title": "Discrimination",
            "PageGroups": [{
                "Name": "Discrimination",
                "Title": "Discrimination",
                "Type": "Discrimination",
                "DoseSize": 11,
                "Pages": []
            }]
        }

        # # first deal with discrimination file
        with open("HTC/csv_files/Discrimination.csv", "r") as read_obj:
            discrimination_reader = csv.reader(read_obj)
            next(discrimination_reader)
            times = 0
            for d_row in discrimination_reader:
                title = d_row[0]
                text = d_row[1].replace("\u2019", "'").replace(
                    "\u2013", "--").replace("\u2014", "--").replace(
                    "\u201c", '"').replace("\u201d", '"').strip().replace("\\n", "\n")  # replace("\\", "\\")
                text = 'Go to the on-demand library to get the links to these resources.\n\n' + text
                input_1 = d_row[2]
                participant_group = d_row[3]
                input_name = d_row[15]
                conditions_lst = d_row[14].split('; ')
                items_list = d_row[7].replace("\u2019", "'").replace(
                    "\u2013", "--").replace("\u2014", "--").replace(
                    "\u201c", '"').replace("\u201d", '"').replace("\\n", "\n"). \
                    strip().split("; ")
                if group in participant_group:
                    discrimination_page = create_discrimination_page(conditions_lst=conditions_lst,
                                                                     text=text,
                                                                     items_lst=items_list,
                                                                     input_1=input_1,
                                                                     input_name=input_name,
                                                                     title=title)

                    domains_dict["Discrimination"]["PageGroups"][0]["Pages"].append(discrimination_page)

            # lookup[lookup_code][page_group]["Pages"].append(page_dict)

        row_num = 1
        current_domain = "Holder"
        for row in csv_reader:
            domain = row[0].strip()
            if current_domain != domain and domain not in (
                    None, ""):  # when we change domains, bring row num back to 1 8/29
                # print(row[3])
                print("Domain is...", domain)
                current_domain = domain
                row_num = 1
            # domain_2 = row[1]
            # domain_3 = row[2]
            label = row[3]  # scenario name
            if domain not in (None, "") and domain:  # if there is a domain

                ## CREATE scenario pages
                if label not in (None, "") and row[i] not in (None, "") and row[i] != "NA" and row[i] != "N/A" and \
                        "Write Your Own" not in label:  # if it's a scenario
                    if domain not in domains_dict.keys():  # first, create domains
                        domains_dict[domain] = {
                            "Name": domain,
                            "Title": domain,
                            "PageGroups": []
                        }
                    scenario_num += 1
                    puzzle_text_1 = row[i].replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014", " - "). \
                        replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n"). \
                        replace("\u2026", "...").replace(",..", ",")
                    word_1 = row[i].split()[-1]
                    if row[i].strip()[-1] == ".":
                        word_1 = row[i].split()[-1][:-1]
                    word_2 = None
                    puzzle_text_2 = None
                    puzzle_text_1 = rreplace(puzzle_text_1, " " + word_1, "..", 1)

                    if "N/A" in row[i + 1] or row[i + 1] in (None, ""):
                        pass
                    else:
                        puzzle_text_2 = row[i + 1].replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014",
                                                                                                           " - "). \
                            replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n"). \
                            replace("\u2026", "...")  # if there's a second puzzle
                        word_2 = row[i + 1].split()[-1][:-1]
                        puzzle_text_2 = rreplace(puzzle_text_2, " " + word_2, "..", 1)
                    comp_question = row[i + 2]
                    answers_lst = [row[i + 3], row[i + 4]]
                    if row[i + 3].strip() == "Yes":
                        answers_lst.pop()
                        answers_lst.append("No")
                    if row[i + 3].strip() == "No":
                        answers_lst.pop()
                        answers_lst.append("Yes")
                    np.random.shuffle(answers_lst)
                    correct_answer = row[i + 3]

                    # get list of words
                    if row[28] not in (None, ""):
                        letters_missing = row[28]

                    lessons_learned = False
                    if (row_num - 1) % 40 == 0 and (
                            row_num - 1) != 0:  # if it's a multiple of 30, we have to add a lessons learned
                        lessons_learned = True
                    unique_image = False
                    if not (row[9].strip() == row[15].strip() == row[21].strip() == row[27].strip()):
                        unique_image = True
                    page_group = create_scenario_page_group(domain=domain, label=label, scenario_num=scenario_num,
                                                            group=group, puzzle_text_1=puzzle_text_1, word_1=word_1,
                                                            comp_question=comp_question, answers_lst=answers_lst,
                                                            correct_answer=correct_answer, word_2=word_2,
                                                            puzzle_text_2=puzzle_text_2,
                                                            can_be_favorited=True, letters_missing=letters_missing,
                                                            lessons_learned=lessons_learned,
                                                            unique_image=unique_image,
                                                            row_num=row_num)
                    domains_dict[domain]["PageGroups"].append(page_group)
                    if row_num % 10 == 0:  # if it's a multiple of 10, add a resource/tip/ER strategy
                        # new 12/13
                        if group == "Undergraduate":
                            resources_lookup = undergrad_resources_lookup
                        elif group == "Graduate":
                            resources_lookup = grad_resources_lookup
                        elif group == "Staff":
                            resources_lookup = staff_resources_lookup
                        else:
                            resources_lookup = faculty_resources_lookup

                        page_group = create_resource_page_group_new(resources_lookup, tip_lst, ER_lookup, domain)
                        domains_dict[domain]["PageGroups"].append(page_group)
                        # new 12/13

                        #
                        # choices = ["Resources", "Tip", "ER"]
                        # # figure out weights with % that they make up of the pool
                        # type = random.choices(choices, weights=(34, 33, 33), k=1)
                        #
                        #
                        #
                        # if type[0] == "Resources":
                        #     if group == "Undergraduate":
                        #         label = undergrad_resources_lookup[domain][1][0][0]
                        #         text = undergrad_resources_lookup[domain][1][0][1]
                        #         undergrad_resources_lookup[domain][1].pop(0)  # pop from front
                        #         undergrad_resources_lookup[domain][1].append([label, text])  # place at back
                        #         text = label + "\n\n" + text
                        #     elif group == "Graduate":
                        #         label = grad_resources_lookup[domain][1][0][0]
                        #         text = grad_resources_lookup[domain][1][0][1]
                        #         grad_resources_lookup[domain][1].pop(0)
                        #         grad_resources_lookup[domain][1].append([label, text])
                        #         text = label + "\n\n" + text
                        #     elif group == "Faculty":
                        #         label = faculty_resources_lookup[domain][1][0][0]
                        #         text = faculty_resources_lookup[domain][1][0][1]
                        #         faculty_resources_lookup[domain][1].pop(0)
                        #         faculty_resources_lookup[domain][1].append([label, text])
                        #         text = label + "\n\n" + text
                        #     else:
                        #         label = staff_resources_lookup[domain][1][0][0]
                        #         text = staff_resources_lookup[domain][1][0][1]
                        #
                        #         staff_resources_lookup[domain][1].pop(0)
                        #         staff_resources_lookup[domain][1].append([label, text])
                        #         text = label + "\n\n" + text
                        #     page_group = create_resource_page_group(title=label, type=type[0], text=text, domain=domain)
                        # elif type[0] == "Tip":
                        #     tip = tip_lst.pop(0)
                        #     label = tip[0]
                        #     text = tip[1]
                        #     tip_lst.append(tip)
                        #     page_group = create_resource_page_group(title=label, type=type[0], text=text, domain=domain)
                        # elif type[0] == "ER":
                        #     ER = ER_lookup[domain][1].pop(0)
                        #     label = ER[0]
                        #     text = ER[1]
                        #     ER_lookup[domain][1].append(ER)
                        #     page_group = create_resource_page_group(title=label, type=type[0], text=text, domain=domain)
                        #domains_dict[domain]["PageGroups"].append(page_group)

                    if row_num % 50 == 0:  # if it's a multiple of 50, add a long scenario and a resource
                        print(len(long_page_groups[domain]))
                        if len(long_page_groups[domain]) != 0: # check to see there are still long scenarios left
                            # new
                            long_page_group = long_page_groups[domain].pop(0)
                            long_page_groups[domain].append(long_page_group)

                            # new

                            # old , uncomment
                            # long_page_group = long_page_groups[domain].pop()

                            domains_dict[domain]["PageGroups"].append(long_page_group)
                            if group == "Undergraduate":
                                resources_lookup = undergrad_resources_lookup
                            elif group == "Graduate":
                                resources_lookup = grad_resources_lookup
                            elif group == "Staff":
                                resources_lookup = staff_resources_lookup
                            else:
                                resources_lookup = faculty_resources_lookup

                            page_group = create_resource_page_group_new(resources_lookup, tip_lst, ER_lookup, domain)
                            domains_dict[domain]["PageGroups"].append(page_group)


                    row_num += 1
                if "Write Your Own" in label: # 12/13 changed from elif
                    print("Creating write your own...")

                    if (row_num-1) % 50 == 0:  # if it's a multiple of 50, add a long scenario and a resource
                        print('Creating long scenario...')
                        print("row_num is", row_num)
                        print(len(long_page_groups[domain]))
                        if len(long_page_groups[domain]) != 0:
                            long_page_group = long_page_groups[domain].pop(0)
                            long_page_groups[domain].append(long_page_group)
                            domains_dict[domain]["PageGroups"].append(long_page_group)
                    row_num += 10
                    print("row_num is", row_num)
                    page_group = {"Name": "Write Your Own",
                                  "Title": "Write Your Own",
                                  "Type": "Survey",
                                  "DoseSize": 10,
                                  "Pages": [

                                  ]}
                    with open("/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/write_your_own.csv") \
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
                    # new
                    if group == "Undergraduate":
                        resources_lookup = undergrad_resources_lookup
                    elif group == "Graduate":
                        resources_lookup = grad_resources_lookup
                    elif group == "Staff":
                        resources_lookup = staff_resources_lookup
                    else:
                        resources_lookup = faculty_resources_lookup

                    page_group = create_resource_page_group_new(resources_lookup, tip_lst, ER_lookup, domain)
                    # new
                    # choices = ["Resources", "Tip", "ER"]
                    # type = random.choices(choices, weights=(34, 33, 33), k=1)
                    # if type[0] == "Resources":
                    #     if group == "Undergraduate":
                    #         label = undergrad_resources_lookup[domain][1][0][0]
                    #         text = undergrad_resources_lookup[domain][1][0][1]
                    #         undergrad_resources_lookup[domain][1].pop(0)  # pop from front
                    #         undergrad_resources_lookup[domain][1].append([label, text])  # place at back
                    #         text = label + "\n\n" + text
                    #     elif group == "Graduate":
                    #         label = grad_resources_lookup[domain][1][0][0]
                    #         text = grad_resources_lookup[domain][1][0][1]
                    #         grad_resources_lookup[domain][1].pop(0)
                    #         grad_resources_lookup[domain][1].append([label, text])
                    #         text = label + "\n\n" + text
                    #     elif group == "Faculty":
                    #         label = faculty_resources_lookup[domain][1][0][0]
                    #         text = faculty_resources_lookup[domain][1][0][1]
                    #         faculty_resources_lookup[domain][1].pop(0)
                    #         faculty_resources_lookup[domain][1].append([label, text])
                    #         text = label + "\n\n" + text
                    #     else:
                    #         label = staff_resources_lookup[domain][1][0][0]
                    #         text = staff_resources_lookup[domain][1][0][1]
                    #         staff_resources_lookup[domain][1].pop(0)
                    #         staff_resources_lookup[domain][1].append([label, text])
                    #         text = label + "\n\n" + text
                    #     page_group = create_resource_page_group(title=label, type=type[0], text=text, domain=domain)
                    # if type[0] == "Tip":
                    #     tip = tip_lst.pop(0)
                    #     label = tip[0]
                    #     text = tip[1]
                    #     tip_lst.append(tip)
                    #     page_group = create_resource_page_group(title=label, type=type[0], text=text, domain=domain)
                    # if type[0] == "ER":
                    #     ER = ER_lookup[domain][1].pop(0)
                    #     print('popping', ER)
                    #     label = ER[0]
                    #     text = ER[1]
                    #     ER_lookup[domain][1].append(ER)
                    #     page_group = create_resource_page_group(title=label, type=type[0], text=text, domain=domain)

                    domains_dict[domain]["PageGroups"].append(page_group)
    json_dict["Sections"][1]["Domains"] = list(domains_dict.values())  # HELLO CHANGED FROM 2

    new_json_dict = groups[group][2]
    json_file = "HTC/json_files/" + group + ".json"
    with open(json_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)  # data instead of json_dict


#### Now, create each additional json file ####



## Create end of day survey
file_name = "HTC/json_files/EOD.json"
name = "Nightly Survey"
title = "Nightly Survey"
time_to_complete = "00:5:00"
sections = [
    {
    "Name": "Nightly Survey",
     "PageGroups": list(end_of_day.values())
     }
]
create_json_file(file_name, name=name, title=title, time_to_complete=time_to_complete, sections=sections)

## Create biweekly survey
# "Dose by section" means that each section is considered a "dose." The app will therefore
# skip from section to section every 2 weeks (this timeframe is set by Ben)
file_name = "HTC/json_files/Biweekly.json"
name = "Track Your Progress"
title = "Track Your Progress"
time_to_complete = "00:5:00"
dose_by_section = True
sections = [
                          {
                              "Name": "Track Your Progress - Week 2",
                              "PageGroups": list(biweekly.values()) + list(biweekly_2.values())
                          },
                          {
                              "Name": "Track Your Progress - Week 4",
                              "PageGroups": list(biweekly.values()) + list(biweekly_4.values())
                          },
                          {
                              "Name": "Track Your Progress - Week 6",
                              "PageGroups": list(biweekly.values()) + list(biweekly_6.values())
                          },
                          {
                              "Name": "Track Your Progress - Week 8",
                              "PageGroups": list(biweekly.values()) + list(biweekly_8.values())
                          }
                      ]
create_json_file(file_name, name, title, time_to_complete, sections, dose_by_section=dose_by_section)

## Create biweekly survey for control (non-intervention) participants
file_name = "HTC/json_files/Control/Biweekly_control.json"
name = "Track Your Progress"
title = "Track Your Progress"
time_to_complete = "00:5:00"
dose_by_section = True
sections = [
                                  {
                                      "Name": "Track Your Progress - Week 2",
                                      "PageGroups": list(biweekly.values()) + list(biweekly_2_control.values())
                                  },
                                  {
                                      "Name": "Track Your Progress - Week 4",
                                      "PageGroups": list(biweekly.values()) + list(biweekly_4_control.values())
                                  },
                                  {
                                      "Name": "Track Your Progress - Week 6",
                                      "PageGroups": list(biweekly.values()) + list(biweekly_6_control.values())
                                  },
                                  {
                                      "Name": "Track Your Progress - Week 8",
                                      "PageGroups": list(biweekly.values()) + list(biweekly_8_control.values())
                                  }
                              ]
create_json_file(file_name, name, title, time_to_complete, sections, dose_by_section=dose_by_section)


## Create the first dose file for control

file_name = "HTC/json_files/Control/Dose1_control.json"
name = "Dose 1"
title = "Get started!"
time_to_complete = "00:5:00"
sections = [{"Name": "Dose 1",
             "PageGroups": list(control_1.values())
             }]
create_json_file(file_name, name, title, time_to_complete, sections)


## Create reasons for ending file
file_name = "HTC/json_files/ReasonsForEnding.json"
name = "Reasons for Ending"
title = "Reasons for Ending"
time_to_complete = "00:5:00"
cancel_button_text = "Exit"
sections = [{
            "Name": "Reasons For Ending",
            "PageGroups": list(reasons.values())
            }]
create_json_file(file_name, name, title, time_to_complete, sections, cancel_button_text=cancel_button_text)
