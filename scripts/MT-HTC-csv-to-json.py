import csv
import imghdr
import json
import math
import random
import numpy as np
import pandas as pd

## FIRST GET ALL RESOURCES / TIPS
import csv
import numpy as np


# adds a scenario page group to scenario_list (which is passed in)
def create_scenario_page_group(domain, label, scenario_num, group, puzzle_text_1, word_1, comp_question,
                    answers_lst, correct_answer, word_2=None, puzzle_text_2=None, can_be_favorited=False,
                               letters_missing=1):
    # to go within pages of the scenario page group
    scenario_list = [{
        "Name": label,
        "ImageUrl": "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/"
                    "protocols/protocol1/media/images/" + group + "/pic" +
                    str(scenario_num - 1) + ".jpeg",
        "ImageType": "image/jpeg",
        "Inputs": [{
            "Type": "Label",
            "Parameters": {
                "Text": label,
                "Framed": True,
            }
        }]
    },
        {
            "Name": "Puzzle",
            "Inputs": [{
                "Type": "Text",
                "Parameters": {"Text": puzzle_text_1}
            },
                {
                    "Type": "WordPuzzle",
                    "Name": label + "_" + domain + "_puzzle",
                    "CorrectFeedback": "Correct!",
                    "IncorrectFeedback": "Whoops! That doesn't look right. Please wait a moment "
                                         "and try again.",
                    "CorrectScore": 0.5,
                    "IncorrectDelay": 5000,
                    "CauseNavigation": True,
                    "Parameters": {
                        "Words": word_1,
                        "MissingLetterCount": letters_missing
                    }
                }]
        }
    ]
    if word_2:
        scenario_list.append({
            "Name": "Puzzle",
            "Inputs": [{
                "Type": "Text",

                "Parameters": {"Text": puzzle_text_2}
            },
                {
                    "Type": "WordPuzzle",
                    "CorrectFeedback": "Correct!",
                    "IncorrectFeedback": "Whoops! That doesn't look right. Please wait a "
                                         "moment and try again.",
                    "Name": label + "_" + domain + "_puzzle_word2",
                    "CorrectScore": 0.5,
                    "IncorrectDelay": 5000,
                    "CauseNavigation": True,
                    "Parameters": {
                        "Words": word_2,
                        "MissingLetterCount": letters_missing
                    }

                }]
        })
    scenario_list.append({
        "Name": "Question",
        "ShowButtons": "WhenCorrect",
        "Inputs": [
            {
                "Type": "Text",
                "Parameters": {
                    "Text": comp_question
                }
            },
            {
                "Type": "Buttons",
                "Name": label + "_" + domain + "_comp_question",
                "CorrectFeedback": "Correct!",
                "IncorrectFeedback": "Whoops! That doesn't look right. Please wait a moment and "
                                     "try again.",
                "CorrectScore": 0.5,
                "IncorrectDelay": 5000,
                "Parameters": {
                    "Buttons": answers_lst,
                    "ColumnCount": 2,
                    "Answer": correct_answer
                }
            }
        ]
    })

    page_group = {
        "Name": label,
        "Type": "Scenario",
        "DoseSize": 11,
        "Pages": scenario_list
    }
    if can_be_favorited:
        page_group['CanBeFavorited'] = True

    # TO DO: add resources

    # if "[RESOURCE]" in label and domain in resources_lookup.keys():
    #     random_i = random.randint(0, len(resources_lookup[domain][1]) - 1)
    #     name = list(resources_lookup[domain][1])[random_i]
    #     resource_page = {
    #         "Name": name,
    #         "Type": "Resource/Tip",
    #         "DoseSize": "11",
    #         "Pages": [{
    #             "Name": name,
    #             "Inputs": [{
    #                 "Type": "Text",
    #                 "Parameters": {
    #                     "Text": resources_lookup[domain][1][name]
    #                 }
    #             }]
    #         }]
    #     }
    #     if "Tip" in name:
    #         resource_page["Inputs"].append({
    #             "Type": "Entry",
    #             "Name": input_name
    #         })
    #     page_group["Pages"].append(resource_page)

    return page_group


## TO DO: create the create resource page group
# if it is a resource/EMA/Tip, then we will do this. this can also be favorited
def create_resource_page_group(type, text, title="Resource"):

    resource = [{
        "Name": title,
        "CanBeFavorited": True,
        "Inputs": [{
            "Type": "Text",
            "Parameters": {
                "Text": text,
            }
        }]
    }]

    if type == "Tip":  # this applies to everyone
        resource[0]["Inputs"].append({"Type": "Entry",
                                      "Name": title + "_entry"})
        resource[0]["Name"] = "Tip to Apply!"
    elif type == "ER":
        resource[0]["Name"] = "Emotion Regulation Tip"

    page_group = {
        "Name": label,
        "Type": "Resource/Tip/ER",
        "DoseSize": 11,
        "Pages": resource
    }

    return page_group



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
        # parse before after
        lookup = {"BeforeDomain_1": before_domains_dicts_1,
                  "BeforeDomain_All": before_domains_dicts,
                  "AfterDomain_1": after_domains_dicts_1,
                  "AfterDomain_All": after_domains_dicts,
                  "EOD_EOD": end_of_day,
                  "Biweekly_EOD": end_of_day}
        scenario_dicts = {}
        for row in reader:  # each row is a page
            if row[0] == "Practice CBM-I":
                lookup_code = row[3] + "_" + row[2]  # this is BeforeDomain_1 for e
                print("getting to practice cbm i")
                with open("HTC/csv_files/dose1_scenarios.csv") as read_obj:
                    dose1_reader = csv.reader(read_obj)
                    next(dose1_reader)
                    scenario_num = 0
                    for row_1 in dose1_reader:
                        label = row_1[3]
                        i = groups[group][0]
                        domain = row_1[0]

                        puzzle_text_1 = row_1[i]
                        # print("Label:", label)
                        # print("i", i)
                        # print("Puzzle text: ", puzzle_text_1)
                        word_1 = row_1[i].split()[-1][:-1]
                        word_2 = None
                        puzzle_text_2 = None
                        puzzle_text_1 = puzzle_text_1.replace(" " + word_1, "..")
                        # print(puzzle_text_1)
                        if "N/A" in row_1[i + 1] or row_1[i + 1] in (None, ""):
                            pass
                        else:
                            puzzle_text_2 = row_1[i + 1]  # if there's a second puzzle
                            word_2 = row_1[i + 1].split()[-1][:-1]
                            puzzle_text_2.replace(word_2, "..")
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
                        page_group = create_scenario_page_group(domain=domain, label=label, scenario_num=scenario_num,
                                                                group=group, puzzle_text_1=puzzle_text_1, word_1=word_1,
                                                                comp_question=comp_question, answers_lst=answers_lst,
                                                                correct_answer=correct_answer, word_2=word_2,
                                                                puzzle_text_2=puzzle_text_2, can_be_favorited=True)

                        # scenario_dict = {"Name": page_group,
                        #                  "Title": page_group,
                        #                  "Type": "Survey",
                        #                  "Pages": [
                        #
                        #                  ]}
                        # # if input_1 in (None, "") and timeout in (None, "") and other_choices in (None, ""):
                        # #     scenario_dict["Type"] = "Information"
                        lookup[lookup_code]["anything" + str(scenario_num)] = page_group
                        scenario_num += 1

                scenario_num = 0
            else:
                if row[2]:
                    doses = row[2]
                    lookup_code = row[3] + "_" + row[2]  # this is BeforeDomain_1 for ex
                    before_after = row[3]
                    text = row[4].replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014", " - "). \
                        replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2026", "...")
                    page_group = row[0]
                    input_1 = row[5]
                    input_2 = row[6]
                    media = row[9]
                    other_choices = row[10]
                    image_framed = row[11]
                    timeout = row[12]
                    show_buttons = row[13]
                    variable_name = row[16]
                    conditions_lst = row[17].split('; ')
                    input_name = row[18]


                    # if page group does not exist already, create one
                    # print(lookup_code)
                    # print(page_group)
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

                    if conditions_lst != ['']:  # if conditions list isn't empty
                        value = conditions_lst[1].strip()
                        if "," in value:
                            value = value.split(", ")
                            new_value = []
                            for each in value:
                                try:
                                    val = int(each)
                                    new_value.append(val)
                                except:
                                    pass
                        else:
                            new_value = value
                        page_dict = {
                            "Conditions": [
                                {
                                    "VariableName": conditions_lst[0].strip(),
                                    "Value": new_value
                                }
                            ],
                            "Inputs": [
                                {"Type": "Text",
                                 "Parameters": {
                                     "Text": text}
                                 }]
                            }
                    else:
                        page_dict = {"Inputs": [
                            {"Type": "Text",
                             "Parameters": {
                                 "Text": text}
                             }]
                        }

                    if timeout not in (None, ""):
                        page_dict["Timeout"] = int(timeout)
                        if show_buttons not in (None, ""):
                            page_dict["ShowButtons"] = show_buttons
                    # add media
                    if media not in (None, ""):  # if there is an image/video
                        if media[-3:] == "mp4":
                            type = "video/mp4"
                        if media[-4:] == "jpeg":
                            type = "image/jpeg"
                        # add a media input:
                        media = {"Type": "Media",

                                 "Parameters": {
                                     "ImageUrl": media,
                                     "ImageType": type}
                                 }
                        if image_framed == "TRUE":
                            media["Frame"] = True
                        page_dict["Inputs"].append(media)

                    if input_1 not in (None, ""):
                        items_list = other_choices.replace("\u2019", "'").replace(
                            "\u2013", "--").replace("\u2014", "--").replace(
                            "\u201c", '"').replace("\u201d", '"').replace("\\", "/").replace("\u00f4", "ô"). \
                            strip().split("; ")
                        times = 1
                        if input_1 == input_2:
                            times = 2
                        if input_1 == "Picker" or input_2 == "Picker":
                            for i in range(times):
                                add = {
                                    "Type": "Picker",
                                    "Parameters": {
                                        "Items": items_list
                                    }
                                }
                        if input_1 == "Slider" or input_2 == "Slider":
                            if items_list != [""]:
                                for i in range(times):  # basically if both = slider
                                    add =  {"Type": "Slider",
                                         "Parameters": {
                                             "Minimum": row[7],
                                             "Maximum": row[8],
                                             "OtherChoices": items_list
                                         }
                                         }
                            else:
                                for i in range(times):  # basically if both = slider
                                    add ={"Type": "Slider",
                                         "Parameters": {
                                             "Minimum": row[7],
                                             "Maximum": row[8]
                                         }
                                         }
                        if input_1 == "Entry" or input_2 == "Entry":
                            for i in range(times):
                                add = {"Type": "Entry",
                                       "Name": input_name}
                        if input_1 == "Puzzle" or input_2 == "Puzzle":
                            for i in range(times):
                                print("name is", row[0] + row[1], "items list is", items_list[0])
                                add = {
                                    "Type": "WordPuzzle",
                                    "Name": row[0] + row[1],
                                    "CorrectFeedback": "Correct!",
                                    "IncorrectFeedback": "Whoops! That doesn't look right. Please wait a moment and "
                                                         "try again.",
                                    "CorrectScore": 0.5,
                                    "IncorrectDelay": 5000,
                                    "CauseNavigation": True,
                                    "Parameters": {
                                        "Words": items_list
                                    }
                                }
                        if input_1 == "Buttons" or input_2 == "Buttons":
                            for i in range(times):
                                add = {"Type": "Buttons",
                                       "Name": input_name,
                                     "Parameters": {
                                         "Buttons": items_list,
                                         "Selectable": True
                                     }}
                            new_items_list = []
                            for each in items_list:
                                if "Other" in each:
                                    new_items_list.append("!" + each)
                                    # add["Parameters"]["OtherValue"] = [each]
                                else:
                                    new_items_list.append(each)
                            add["Parameters"]["Buttons"] = new_items_list
                        if input_1 == "Checkbox" or input_2 == "Checkbox":
                            for i in range(times):
                                add = {"Type": "Buttons",
                                       "Name": input_name,
                                       "Parameters": {
                                         "Buttons": items_list,
                                         "Selectable": True,
                                         "AllowMultipleSelections": True
                                     }}
                            new_items_list = []
                            for each in items_list:
                                if "Other" in each:
                                    new_items_list.append("!" + each)
                                    # add["Parameters"]["OtherValue"] = [each]
                                else:
                                    new_items_list.append(each)
                            add["Parameters"]["Buttons"] = new_items_list


                        if variable_name not in (None, ""):
                            add["VariableName"] = variable_name
                        page_dict["Inputs"].append(add)
                    lookup[lookup_code][page_group]["Pages"].append(page_dict)


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
                 "Sections": [
                     {
                         "Name": "BeforeDomain_All",
                         "PageGroups": list(before_domains_dicts.values())
                     },
                     {
                         "Name": "Domains",
                         "Description": "The domains listed here are some areas that may cause teens to feel "
                                        "anxious. Please select the one that you'd like to work on during today's "
                                        "training. "
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
            "Social Situations": [{}, 0], # {} will have all the page groups, 0 is the counter of scenarios
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
            "PageGroups": []
        }
        # # first deal with discrimination file
        # with open("Discrimination.csv", "r") as read_obj:
        #     discrimination_reader = csv.reader(read_obj)
        #     times = 0
        #     for d_row in discrimination_reader:
        #         title = d_row[0]
        #         text = d_row[1]
        #         input_1 = d_row[2]
        #         input_2 = d_row[3]
        #         items_list = d_row[7].replace("\u2019", "'").replace(
        #             "\u2013", "--").replace("\u2014", "--").replace(
        #             "\u201c", '"').replace("\u201d", '"').replace("\\", "/"). \
        #             strip().split("; ")
        #         if input_1 == input_2:
        #             times = 2
        #         if input_1 == "Checkbox" or input_2 == "Checkbox":
        #             for i in range(times):
        #                 add = {"Type": "Buttons",
        #                        "Name": input_name,
        #                        "Parameters": {
        #                            "Buttons": items_list,
        #                            "Selectable": True,
        #                            "AllowMultipleSelections": True
        #                        }}
        #             add["Parameters"]["Buttons"] = items_list

        for row in csv_reader:
            domain = row[0]
            # domain_2 = row[1]
            # domain_3 = row[2]
            label = row[3]  # scenario name
            if domain not in (None, "") and domain:  # if there is a domain
                # first, create domains
                # if domain not in domains_dict.keys():
                #     domains_dict[domain] = {
                #         "Name": domain,
                #         "Title": domain,
                #         "PageGroups": []
                #     }

                # check if it needs a resources

                ## CREATE scenario pages
                if label not in (None, "") and row[i] not in (None, "") and row[i] != "NA" and row[i] != "N/A" and \
                    row[0] is not "Tips to apply to lesson learned" and row[0] is not "ER Strategies" and row[0] is \
                        not "Resources":  # if it's a scenario
                    if domain not in domains_dict.keys(): # first, create domains
                        domains_dict[domain] = {
                            "Name": domain,
                            "Title": domain,
                            "PageGroups": []
                        }
                    scenario_num += 1
                    puzzle_text_1 = row[i]
                    # print("Label:", label)
                    # print("i", i)
                    # print("Puzzle text: ", puzzle_text_1)
                    word_1 = row[i].split()[-1][:-1]
                    word_2 = None
                    puzzle_text_2 = None
                    puzzle_text_1 = puzzle_text_1.replace(" " + word_1, "..")
                    # print(puzzle_text_1)
                    if "N/A" in row[i + 1] or row[i + 1] in (None, ""):
                        pass
                    else:
                        puzzle_text_2 = row[i + 1]  # if there's a second puzzle
                        word_2 = row[i + 1].split()[-1][:-1]
                        puzzle_text_2.replace(word_2, "..")
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
                        letters_missing = int(row[28])

                    page_group = create_scenario_page_group(domain=domain, label=label, scenario_num=scenario_num,
                                                            group=group, puzzle_text_1=puzzle_text_1, word_1=word_1,
                                                            comp_question=comp_question, answers_lst=answers_lst,
                                                            correct_answer=correct_answer, word_2=word_2,
                                                            puzzle_text_2=puzzle_text_2,
                                                            can_be_favorited=True, letters_missing=letters_missing)
                if row[1] == "Tips to Apply Lessons Learned" or row[1] == "ER Strategies" or row[1] == "Resources":
                    print("yes here")
                    if row[1] == "Tips to Apply Lessons Learned":
                        type = "Tip"
                        text = row[4]  # applies to every group
                        label = row[3]
                    if row[1] == "ER Strategies":
                        type = "ER"
                        text = row[4]  # applies to every group
                        label = row[3]
                    if row[1] == "Resources":
                        type = "Resources"
                        text = row[i + 1]
                        print("text is", text)
                        label = row[i]  # different per group

                    page_group = create_resource_page_group(title=label, type=type, text=text)

                domains_dict[domain]["PageGroups"].append(page_group)
                # if domain_2:
                #     domains_dict[domain_2]["PageGroups"].append(page_group)
                # if domain_3:
                #     domains_dict[domain_2]["PageGroups"].append(page_group)

        # for domain in domains_lookup:
        #     domains_dict[domain]["PageGroups"] = list(domains_lookup[domain][0].values())
    with open("/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/HTC_long_scenarios.csv") as read_file:
        reader = csv.reader(read_file)
        next(reader)
        next(reader)
        i = groups[group][1]
        for row in reader:
            domain = row[0]
            # domain_2 = row[1]
            # domain_3 = row[2]
            label = row[3]
            scenario_description = row[i]
            image = row[i + 1]

            # each row corresponds to one page group
            page_group = {"Name": "Long Scenario: " + label.strip(),
                             "Title": "Long Scenario: " + label.strip(),
                             "Type": "Scenario",
                          "DoseSize": 2,
                             "Pages": [

                             ]}
            # scenario_list =
            if scenario_description not in (None, "") and scenario_description != "NA" and scenario_description != "N/A":
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
                                replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2019", "'")
                        input_1 = row_str[6]
                        input_2 = row_str[7]

                        if image_bool:
                            page = {
                                "Name": label.strip(),
                                "ImageUrl": image,
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
                            page["ShowButtons"] ="AfterTimeout"

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
                                                                row[i + 5], row[i + 6]], # corresponds to thoughts in csv
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
                        # print(domain_num, domain)
                ################### here ##########################
            # TO DO: resources here
            # if domain in resources_lookup.keys():
            #     random_i = random.randint(0, len(resources_lookup[domain][1]) - 1)
            #     name = list(resources_lookup[domain][1])[random_i]
            #     resource_page = {
            #         "Name": name,
            #         "Type": "Resource/Tip",
            #         "DoseSize": "11",
            #         "Pages": [{
            #             "Name": name,
            #             "Inputs": [{
            #                 "Type": "Text",
            #                 "Parameters": {
            #                     "Text": resources_lookup[domain][1][name]
            #                 }
            #             }]
            #         }]
            #     }
            #     page_group["Pages"].append(resource_page)

    json_dict["Sections"][2]["Domains"] = list(domains_dict.values())
    # print(range(len(json_dict["Sections"][1]["Domains"])))

    # UNDO THIS
    # for domain in range(len(json_dict["Sections"][2]["Domains"])): # shuffle page groups
    #    random.shuffle(json_dict["Sections"][2]["Domains"][domain]["PageGroups"])


    # print(json_dict["Sections"][1]["Domains"][0])


    new_json_dict = groups[group][2]
    json_file = "HTC/json_files/" + group + ".json"
    with open(json_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)  # data instead of json_dict
    #json_dict = {}

json_dict_EOD = json_dict = {"Name": group,
                 "Title": "Hoos Think Calmly",
                 "TimeToComplete": "00:5:00",
                 "Sections": [
                     {
                         "Name": "EOD",
                         "Doses": [1],
                         "PageGroups": list(end_of_day.values())
                     },
                 ]}

json_file = "HTC/json_files/EOD.json"
with open(json_file, 'w') as outfile:
    json.dump(json_dict_EOD, outfile, indent=4)  # data instead of json_dict
