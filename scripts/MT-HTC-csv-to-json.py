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


def get_resources(file_path):
    # first do resources
    academics = []
    homelife = []
    finances = []
    mental = []
    physical = []
    social = []
    romantic = []

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
                # print(i)
                # print("row i", er_strategy)
                if er_strategy not in (None, ""):
                    tip_num += 1
                    ER_lookup[domain][1].append(["Emotion Regulation Strategy #" + str(tip_num), er_strategy])

    return ER_lookup


def get_tips(file_path):
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


undergrad_resources_lookup = get_resources(file_path="/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/"
                                                     "undergrad_resources.csv")
grad_resources_lookup = get_resources(file_path="/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/"
                                                "grad_resources.csv")
faculty_resources_lookup = get_resources(file_path="/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/"
                                                   "faculty_resources.csv")
staff_resources_lookup = get_resources(file_path="/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/"
                                                 "staff_resources.csv")
ER_lookup = get_ER(file_path="/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/ER_strategies.csv")
tip_lst = get_tips("/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/tips.csv")


# adds a scenario page group to scenario_list (which is passed in)
def create_scenario_page_group(domain, label, scenario_num, group, puzzle_text_1, word_1, comp_question,
                               answers_lst, correct_answer, unique_image, word_2=None, puzzle_text_2=None,
                               can_be_favorited=False,
                               letters_missing=1, lessons_learned=False, lessons_learned_dict=None):
    # to go within pages of the scenario page group
    if lessons_learned == True:
        scenario_list = [{
            "Name": "Lessons Learned",
            "Inputs": [{
                "Type": "Text",
                "Parameters": {
                    "Text": lessons_learned_dict[domain].replace("\u2019", "'").replace(
                        "\u2013", "--").replace("\u2014", "--").replace(
                        "\u201c", '"').replace("\u201d", '"').replace("\\", "/").replace("\u00f4", "ô"). \
                        strip()
                }

            }, {
                "Type": "Entry",
                "Name": "lessons_learned_" + domain + "_" + str(scenario_num)
            }
            ]
        }]
    else:
        scenario_list = []

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

    scenario_list.append({
        "Name": label,
        "ImageUrl": image_url,
        "ImageType": "image/jpeg",
        "Inputs": [{
            "Type": "Label",
            "Parameters": {
                "Text": label,
                "Framed": True,
            }
        }]
    })
    scenario_list.append({
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
                    "Words": [word_1]
                }
            }]
    })
    if letters_missing == "1" or letters_missing == "2":
        if lessons_learned == True:
            new_index = 2
        else:
            new_index = 1
        scenario_list[new_index]["Inputs"][1]["Parameters"]["MissingLetterCount"] = int(letters_missing)
    elif letters_missing == "all":
        # change second input of the second page to be an entry, not a word puzzle
        scenario_list[1]["Inputs"] = [{
            "Type": "Text",
            "Parameters": {"Text": puzzle_text_1}
        },
            {
                "Type": "Entry",
                "Name": label + "_" + domain + "_entry"
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
                        "Words": [word_2]
                    }

                }]
        })
        if letters_missing == "1" or letters_missing == "2":
            scenario_list[2]["Inputs"][1]["Parameters"]["MissingLetterCount"] = int(letters_missing)
        elif letters_missing == "all":
            # change second input of the second page to be an entry, not a word puzzle
            scenario_list[2]["Inputs"] = [{
                "Type": "Text",
                "Parameters": {"Text": puzzle_text_1}
            },
                {
                    "Type": "Entry",
                    "Name": label + "_" + domain + "_entry"
                }
            ]
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
        "DoseSize": 1,
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
        "DoseSize": 1,
        "Pages": resource
    }

    return page_group


def create_discrimination_page(conditions_lst, text, items_lst, input_1,
                               input_name, title):
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

    if input_1 == "Checkbox":
        add = {"Type": "Buttons",
               "Name": input_name,
               "Parameters": {
                   "Buttons": items_list,
                   "Selectable": True,
                   "AllowMultipleSelections": True
               }}
        add["Parameters"]["Buttons"] = items_list
        page_dict["Inputs"].append(add)
    if input_1 == "Entry":
        add = {"Type": "Entry",
               "Name": input_name}
        page_dict["Inputs"].append(add)

    return page_dict


# changed show_buttons to none 6/21
def create_survey_page(text=None, media=None, image_framed=None, other_choices=None, input_1=None, input_2=None,
                       variable_name=None, title=None, page_group=None, input_name=None, minimum=None, maximum=None,
                       show_buttons=None, conditions_lst=None):
    if conditions_lst != [''] and conditions_lst is not None:  # if conditions list isn't empty
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
        items_list = ""
        if other_choices not in (None, ""):
            items_list = other_choices.replace("\u2019", "'").replace(
                "\u2013", "--").replace("\u2014", "--").replace(
                "\u201c", '"').replace("\u201d", '"').replace("\\", "/").replace("\u00f4", "ô"). \
                strip().split("; ")
        times = 1
        add = {}
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
            if items_list not in (None, [""], ""):
                print("items list is", items_list)
                for i in range(times):  # basically if both = slider
                    add = {"Type": "Slider",
                           "Parameters": {
                               "Minimum": minimum,
                               "Maximum": maximum,
                               "OtherChoices": items_list
                           }
                           }
            else:
                for i in range(times):  # basically if both = slider
                    add = {"Type": "Slider",
                           "Parameters": {
                               "Minimum": minimum,
                               "Maximum": maximum
                           }
                           }
        if input_1 == "Entry" or input_2 == "Entry":
            for i in range(times):
                add = {"Type": "Entry",
                       "Name": input_name}
        if input_1 == "Puzzle" or input_2 == "Puzzle":
            for i in range(times):
                add = {
                    "Type": "WordPuzzle",
                    "Name": page_group + title,
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
                if items_list == ["Yes", "No"]:
                    add["Parameters"]["ColumnCount"] = 2
            new_items_list = []
            for each in items_list:
                if "Other" in each:
                    new_items_list.append("!" + each)
                    # add["Parameters"]["OtherValue"] = [each]
                else:
                    new_items_list.append(each)
            add["Parameters"]["Buttons"] = new_items_list
        if input_1 == "Scheduler":
            add = {
                "Type": "Scheduler"
            }
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
                elif "Prefer not to answer" in each:
                    new_items_list.append("^Prefer not to answer")
                else:
                    new_items_list.append(each)
            add["Parameters"]["Buttons"] = new_items_list

        if variable_name not in (None, ""):
            add["VariableName"] = variable_name
        if add not in (None, ""):
            page_dict["Inputs"].append(add)
            if input_1 == "Scheduler":
                page_dict["Inputs"].append(add)

    return page_dict


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
    lessons_learned_dict = {
        "Academics/Work/Career Development": "Great job! You’re making great progress trying out new "
                                             "perspectives tied to academics, work, and career development! "
                                             "Take a few minutes to reflect on the short stories you’ve read so far. "
                                             "What have you learned? What are your main takeaways? For instance, you "
                                             "might notice that nobody is perfect and it’s normal to make mistakes "
                                             "sometimes.",
        "Family & Home Life": "Great job! You’re making great progress trying out new perspectives tied to family and "
                              "home life! Take a few minutes to reflect on the short stories you’ve read so far. What "
                              "have you learned? What are your main takeaways? For instance, you might notice that "
                              "having difficult conversations can be scary, but doing so can make you feel proud of "
                              "yourself.",
        "Finances": "Great job! You’re making great progress trying out new perspectives tied to finances! Take a few"
                    " minutes to reflect on the short stories you’ve read so far. What have you learned? What are your "
                    "main takeaways? For instance, you might notice that there are many different ways to approach "
                    "financial challenges to make them feel more manageable.",
        "Mental Health": "Great job! You’re making great progress trying out new perspectives tied to mental health! "
                         "Take a few minutes to reflect on the short stories you’ve read so far. What have you "
                         "learned? What are your main takeaways? For instance, you might notice that you’re able to "
                         "function even when you’re feeling anxious.",
        "Physical Health": "Great job! You’re making great progress trying out new perspectives tied to physical "
                           "health! Take a few minutes to reflect on the short stories you’ve read so far. What "
                           "have you learned? What are your main takeaways? For instance, you might notice that "
                           "uncomfortable sensations in your body, like a racing heartbeat, are often not dangerous.",
        "Romantic Relationships": "Great job! You’re making great progress trying out new perspectives tied to "
                                  "romantic relationships! Take a few minutes to reflect on the short stories you’ve "
                                  "read so far. What have you learned? What are your main takeaways? For instance, "
                                  "you might notice that occasional conflict is a healthy and normal part of "
                                  "relationships.",
        "Social Situations": "Great job! You’re making great progress trying out new perspectives tied to social "
                             "situations! Take a few minutes to reflect on the short stories you’ve read so far. "
                             "What have you learned? What are your main takeaways? For instance, you might notice "
                             "that it’s not helpful to assume what other people are thinking."
    }
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
        "Discrimination": []
    }
    with open("/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/HTC_long_scenarios.csv") as read_file:
        reader = csv.reader(read_file)
        next(reader)
        next(reader)
        i = groups[group][1]
        for row in reader:
            domain = row[0].strip()
            # domain_2 = row[1]
            # domain_3 = row[2]
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
                                                                                                           "'")
                            input_1 = row_str[6]
                            input_2 = row_str[7]

                            if image_bool:
                                page = {
                                    "Name": label.strip(),
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
    # for domain in long_page_groups:
    #     print("Domain:", domain)
    #     for each in long_page_groups[domain]:
    #         print(each["Name"])
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

                        # then create scenario page group for the practice
                        page_group = create_scenario_page_group(domain=domain, label=label, scenario_num=scenario_num,
                                                                group=group, puzzle_text_1=puzzle_text_1, word_1=word_1,
                                                                comp_question=comp_question, answers_lst=answers_lst,
                                                                correct_answer=correct_answer, word_2=word_2,
                                                                puzzle_text_2=puzzle_text_2, can_be_favorited=True,
                                                                unique_image=False)

                        lookup[lookup_code]["anything" + str(scenario_num)] = page_group
                        scenario_num += 1
                scenario_num = 0
            else:
                # create survey page
                if row[2]:
                    doses = row[2]
                    lookup_code = row[3] + "_" + row[2]  # this is BeforeDomain_1 for ex
                    before_after = row[3]
                    text = row[4].replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014", " - "). \
                        replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2026", "...")
                    page_group = row[0]
                    title = row[1]
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
                                              input_name=input_name, minimum=minimum, maximum=maximum)
                    lookup[lookup_code][page_group]["Pages"].append(page)

    json_dict = {"Name": group,
                 "Title": "Hoos Think Calmly",
                 "TimeToComplete": "00:10:00",
                 "DoseSize": 11,
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
                                        "training. ",
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
                    "\u201c", '"').replace("\u201d", '"').replace("\\", "/"). \
                    strip().split("; ")
                input_1 = d_row[2]
                participant_group = d_row[3]
                input_name = d_row[15]
                conditions_lst = d_row[14].split('; ')
                items_list = d_row[7].replace("\u2019", "'").replace(
                    "\u2013", "--").replace("\u2014", "--").replace(
                    "\u201c", '"').replace("\u201d", '"').replace("\\", "/"). \
                    strip().split("; ")
                if participant_group == group:
                    discrimination_page = create_discrimination_page(conditions_lst=conditions_lst,
                                                                     text=text,
                                                                     items_lst=items_list,
                                                                     input_1=input_1,
                                                                     input_name=input_name,
                                                                     title=title)

                    domains_dict["Discrimination"]["PageGroups"][0]["Pages"].append(discrimination_page)

            # lookup[lookup_code][page_group]["Pages"].append(page_dict)

        row_num = 1
        for row in csv_reader:
            domain = row[0].strip()
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
                    puzzle_text_1 = row[i]
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
                        letters_missing = row[28]

                    lessons_learned = False
                    if row_num % 30 == 0:  # if it's a multiple of 30, we have to add a lessons learned
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
                                                            lessons_learned_dict=lessons_learned_dict,
                                                            unique_image=unique_image)
                    domains_dict[domain]["PageGroups"].append(page_group)
                    if row_num % 10 == 0:  # if it's a multiple of 10, add a resource/tip/ER strategy
                        choices = ["Resources", "Tip", "ER"]
                        # figure out weights with % that they make up of the pool
                        type = random.choices(choices, weights=(50, 25, 25), k=1)
                        if type[0] == "Resources":
                            if group == "Undergraduate":
                                label = undergrad_resources_lookup[domain][1][0][0]
                                text = undergrad_resources_lookup[domain][1][0][1]
                                undergrad_resources_lookup[domain][1].pop(0)  # pop from front
                                undergrad_resources_lookup[domain][1].append([label, text])  # place at back
                            elif group == "Graduate":
                                label = grad_resources_lookup[domain][1][0][0]
                                text = grad_resources_lookup[domain][1][0][1]
                                grad_resources_lookup[domain][1].pop(0)
                                grad_resources_lookup[domain][1].append([label, text])
                            elif group == "Faculty":
                                label = faculty_resources_lookup[domain][1][0][0]
                                text = faculty_resources_lookup[domain][1][0][1]
                                faculty_resources_lookup[domain][1].pop(0)
                                faculty_resources_lookup[domain][1].append([label, text])
                            else:
                                label = staff_resources_lookup[domain][1][0][0]
                                text = staff_resources_lookup[domain][1][0][1]
                                staff_resources_lookup[domain][1].pop(0)
                                staff_resources_lookup[domain][1].append([label, text])
                            page_group = create_resource_page_group(title=label, type=type[0], text=text)
                        if type[0] == "Tip":
                            label = tip_lst[0][0]
                            text = tip_lst[0][1]
                            page_group = create_resource_page_group(title=label, type=type[0], text=text)
                        if type[0] == "ER":
                            page_group = create_resource_page_group(title=label, type=type[0], text=text)
                        domains_dict[domain]["PageGroups"].append(page_group)
                    if row_num % 20 == 0:  # if it's a multiple of 20, add a long scenario and a resource
                        if len(long_page_groups[domain]) != 0:
                            long_page_group = long_page_groups[domain].pop()
                            domains_dict[domain]["PageGroups"].append(long_page_group)
                            choices = ["Resources", "Tip", "ER"]
                            # figure out weights with % that they make up of the pool
                            type = random.choices(choices, weights=(50, 25, 25), k=1)
                            if type[0] == "Resources":
                                if group == "Undergraduate":
                                    label = undergrad_resources_lookup[domain][1][0][0]
                                    text = undergrad_resources_lookup[domain][1][0][1]
                                    undergrad_resources_lookup[domain][1].pop(0)  # pop from front
                                    undergrad_resources_lookup[domain][1].append([label, text])  # place at back
                                elif group == "Graduate":
                                    label = grad_resources_lookup[domain][1][0][0]
                                    text = grad_resources_lookup[domain][1][0][1]
                                    grad_resources_lookup[domain][1].pop(0)
                                    grad_resources_lookup[domain][1].append([label, text])
                                elif group == "Faculty":
                                    label = faculty_resources_lookup[domain][1][0][0]
                                    text = faculty_resources_lookup[domain][1][0][1]
                                    faculty_resources_lookup[domain][1].pop(0)
                                    faculty_resources_lookup[domain][1].append([label, text])
                                else:
                                    label = staff_resources_lookup[domain][1][0][0]
                                    text = staff_resources_lookup[domain][1][0][1]
                                    staff_resources_lookup[domain][1].pop(0)
                                    staff_resources_lookup[domain][1].append([label, text])
                                page_group = create_resource_page_group(title=label, type=type[0], text=text)
                            if type[0] == "Tip":
                                label = tip_lst[0][0]
                                text = tip_lst[0][1]
                                page_group = create_resource_page_group(title=label, type=type[0], text=text)
                            if type[0] == "ER":
                                page_group = create_resource_page_group(title=label, type=type[0], text=text)
                            domains_dict[domain]["PageGroups"].append(page_group)
                elif "Write Your Own" in label:
                    page_group = {"Name": "Write Your Own",
                                  "Title": "Write Your Own",
                                  "Type": "Survey",
                                  "DoseSize": 11,
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
                                print(input_name, "; input name")
                                page = create_survey_page(text=text, input_1=input, title=title, input_name=input_name)
                                page_group["Pages"].append(page)
                    domains_dict[domain]["PageGroups"].append(page_group)
            row_num += 1

            # we need to do if it's a multiple of 10, we add both the page group and a resource page group
            # when used, remove that resource and add it to the back
            # first_element = lst[0]
            # lst.pop(0) --> remove first element
            # lst.append(first_element)
            # choose whether it's ER strategy, resource, or tip based on a random number, favoring resources & ER more

            # if row[1] == "Tips to Apply Lessons Learned" or row[1] == "ER Strategies" or row[1] == "Resources":
            #     print("yes here")
            #     if row[1] == "Tips to Apply Lessons Learned":
            #         type = "Tip"
            #         text = row[4]  # applies to every group
            #         label = row[3]
            #     if row[1] == "ER Strategies":
            #         type = "ER"
            #         text = row[4]  # applies to every group
            #         label = row[3]
            #     if row[1] == "Resources":
            #         type = "Resources"
            #         text = row[i + 1]
            #         print("text is", text)
            #         label = row[i]  # different per group
            #
            #     page_group = create_resource_page_group(title=label, type=type, text=text)
            #
            # domains_dict[domain]["PageGroups"].append(page_group)
            # if domain_2:
            #     domains_dict[domain_2]["PageGroups"].append(page_group)
            # if domain_3:
            #     domains_dict[domain_2]["PageGroups"].append(page_group)

        # for domain in domains_lookup:
        #     domains_dict[domain]["PageGroups"] = list(domains_lookup[domain][0].values())

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

    json_dict["Sections"][1]["Domains"] = list(domains_dict.values())  # HELLO CHANGED FROM 2
    # print(range(len(json_dict["Sections"][1]["Domains"])))

    # UNDO THIS
    # for domain in range(len(json_dict["Sections"][2]["Domains"])): # shuffle page groups
    #    random.shuffle(json_dict["Sections"][2]["Domains"][domain]["PageGroups"])

    # print(json_dict["Sections"][1]["Domains"][0])

    new_json_dict = groups[group][2]
    json_file = "HTC/json_files/" + group + ".json"
    with open(json_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)  # data instead of json_dict
    # json_dict = {}

json_dict_EOD = {"Name": "Nightly Survey",
                 "Title": "Nightly Survey",
                 "TimeToComplete": "00:5:00",
                 "Sections": [
                     {
                         "Name": "Nightly Survey",
                         "PageGroups": list(end_of_day.values())
                     },
                 ]}

json_file = "HTC/json_files/EOD.json"
with open(json_file, 'w') as outfile:
    json.dump(json_dict_EOD, outfile, indent=4)  # data instead of json_dict

# to do: make each biweekly survey a different section
json_dict_biweekly = {"Name": "Track Your Progress",
                      "Title": "Track Your Progress",
                      "TimeToComplete": "00:5:00",
                      "DoseMethod": "OnRun",
                      "DoseBySection": True,
                      "Sections": [
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
                      ]}

json_file = "HTC/json_files/Biweekly.json"
with open(json_file, 'w') as outfile:
    json.dump(json_dict_biweekly, outfile, indent=4)  # data instead of json_dict

# to do: make each biweekly survey a different section
json_dict_biweekly_control = {"Name": "Track Your Progress",
                              "Title": "Track Your Progress",
                              "TimeToComplete": "00:5:00",
                              "DoseMethod": "OnRun",
                              "DoseBySection": True,
                              "Sections": [
                                  {
                                      "Name": "Track Your Progress - Week 2",
                                      "PageGroups": list(biweekly.values())
                                  }
                              ]}

json_file = "HTC/json_files/Control/Biweekly_control.json"
with open(json_file, 'w') as outfile:
    json.dump(json_dict_biweekly, outfile, indent=4)  # data instead of json_dict


json_dict_dose1_control = {"Name": "Dose 1",
                      "Title": "Dose 1",
                      "TimeToComplete": "00:5:00",
                      "DoseMethod": "OnRun",
                      "DoseBySection": True,
                      "Sections": [
                          {
                              "Name": "Dose 1",
                              "PageGroups": list(control_1.values())
                          }
                      ]}

json_file = "HTC/json_files/Control/Dose1_control.json"
with open(json_file, 'w') as outfile:
    json.dump(json_dict_dose1_control, outfile, indent=4)  # data instead of json_dict


json_dict_R4E = {"Name": "Reasons for Ending",
                 "Title": "Reasons for Ending",
                 "TimeToComplete": "00:5:00",
                 "Sections": [
                     {
                         "Name": "Reasons For Ending",
                         "PageGroups": list(reasons.values())
                     },
                 ]}

json_file = "HTC/json_files/ReasonsForEnding.json"
with open(json_file, 'w') as outfile:
    json.dump(json_dict_R4E, outfile, indent=4)  # data instead of json_dict