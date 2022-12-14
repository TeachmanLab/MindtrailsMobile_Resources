import csv
import json
from HTC_helpers import get_lessons_learned_text
import random

# text for all the lessons learned

file_path = "/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/lessons_learned_text.csv"

lessons_learned_dict = get_lessons_learned_text(file_path)

# adds a scenario page group to scenario_list (which is passed in)
def create_scenario_page_group(domain, label, scenario_num, group, puzzle_text_1, word_1,
                               comp_question, answers_lst, correct_answer, unique_image, row_num, word_2=None, puzzle_text_2=None,
                               can_be_favorited=False,
                               letters_missing=1, lessons_learned=False, lessons_learned_dict=lessons_learned_dict):
    # to go within pages of the scenario page group
    if lessons_learned == True:
        scenario_list = [{
            "Name": "Lessons Learned" + str(row_num),
            "Title": "Lessons Learned",
            "Inputs": [{
                "Type": "Text",
                "Parameters": {
                    "Text": lessons_learned_dict[domain].replace("\u2019", "'").replace(
                        "\u2013", "--").replace("\u2014", "--").replace(
                        "\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u00f4", "ô"). \
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
    if letters_missing == "all" and (int(row_num) - 1) % 10 == 0: # if all letters missing, and it's the first scenario
        scenario_list.append({
            "Name": label + " Instructions",
            "Title": "Instructions",
            "Inputs": [{
                "Type": "Text",
                "Parameters": {
                    "Text": "The stories you're about to see are a little bit different than ones you've "
                            "seen before. Rather than fill in missing letters to complete the final word, "
                            "we're going to challenge you to generate your own final word that will complete "
                            "the story. Your goal is to think of a word that will end the story on a "
                            "positive note. The ending doesn’t have to be so positive that it doesn’t "
                            "seem possible, but we want you to imagine you are handling the situation well.",
                }
            }]
        })
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
        "Name": label + str(row_num),
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
        # 9/8 Added
        if (int(row_num) - 1) % 10 == 0:
            if lessons_learned == True:
                new_index = 3 # 2
            else:
                new_index = 2 # 1
        else:
            if lessons_learned == True:
                new_index = 2 # 2
            else:
                new_index = 1 # 1
        scenario_list[new_index]["Inputs"] = [{
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
            "Name": "Puzzle 2",
            "Inputs": [{
                "Type": "Text",

                "Parameters": {"Text": puzzle_text_2}
            },
                {
                    "Type": "WordPuzzle",
                    "Name": label + "_" + domain + "_puzzle_word2",
                    "CorrectFeedback": "Correct!",
                    "IncorrectFeedback": "Whoops! That doesn't look right. Please wait a "
                                         "moment and try again.",
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
            if (int(row_num) - 1) % 10 == 0:
                if lessons_learned == True:
                    new_index = 4  # 2
                else:
                    new_index = 3  # 1
            else:
                if lessons_learned == True:
                    new_index = 3  # 2
                else:
                    new_index = 2  # 1
            scenario_list[new_index]["Inputs"] = [{
                "Type": "Text",
                "Parameters": {"Text": puzzle_text_2}
            },
                {
                    "Type": "Entry",
                    "Name": label + "_" + domain + "_entry2"
                }
            ]
    if letters_missing != "all":
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
                        "ColumnCount": 1,
                        "Answer": correct_answer
                    }
                }
            ]
        })

    page_group = {
        "Name": label + "_____" + str(row_num),
        "Title": label,
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


def create_resource_page_group_new(resources_lookup, tip_lst, ER_lookup, domain):
    choices = ["Resources", "Tip", "ER"]
    # figure out weights with % that they make up of the pool
    type = random.choices(choices, weights=(34, 33, 33), k=1)
    if type[0] == "Resources":
        label = resources_lookup[domain][1][0][0]
        text = resources_lookup[domain][1][0][1]
        resources_lookup[domain][1].pop(0)  # pop from front
        resources_lookup[domain][1].append([label, text])  # place at back
        text = label + "\n\n" + text
        #page_group = create_resource_page_group(title=label, type=type[0], text=text, domain=domain)
    elif type[0] == "Tip":
        tip = tip_lst.pop(0)
        label = tip[0]
        text = tip[1]
        tip_lst.append(tip)
    elif type[0] == "ER":
        ER = ER_lookup[domain][1].pop(0)
        label = ER[0]
        text = ER[1]
        ER_lookup[domain][1].append(ER)
    resource = [{
        "Name": label,
        "Title": "Resource: " + domain,
        "CanBeFavorited": True,
        "Inputs": [{
            "Type": "Text",
            "Parameters": {
                "Text": text,
            }
        }]
    }]
    if type[0] == "Tip":  # this applies to everyone
        resource[0]["Title"] = "Apply to Daily Life: Make It Work for You!"
        resource[0]["Inputs"].append({"Type": "Entry",
                                      "Name": label + "_entry"})
        resource[0]["Name"] = "Tip to Apply!"
    elif type[0] == "ER":
        resource[0]["Title"] = "Manage Your Feelings: " + domain  # domain name
        resource[0]["Name"] = "Emotion Regulation Tip"

    page_group = {
        "Name": "Resource/Tip/ER",
        "Title": "Resource/Tip/ER",
        "Type": "Resource/Tip/ER",
        "DoseSize": 1,
        "Pages": resource,
        "CanBeFavorited": True
    }
    return page_group

# if it is a resource/EMA/Tip, then we will do this. this can also be favorited
def create_resource_page_group(type, text, title="Resource", domain="noooooone"):

    resource = [{
        "Name": title,
        "Title": "Resource: " + domain,
        "CanBeFavorited": True,
        "Inputs": [{
            "Type": "Text",
            "Parameters": {
                "Text": text,
            }
        }]
    }]
    if type == "Tip":  # this applies to everyone
        resource[0]["Title"] = "Apply to Daily Life: Make It Work for You!"
        resource[0]["Inputs"].append({"Type": "Entry",
                                      "Name": title + "_entry"})
        resource[0]["Name"] = "Tip to Apply!"
    elif type == "ER":
        resource[0]["Title"] = "Manage Your Feelings: " + domain# domain name
        resource[0]["Name"] = "Emotion Regulation Tip"

    page_group = {
        "Name": "Resource/Tip/ER",
        "Title": "Resource/Tip/ER",
        "Type": "Resource/Tip/ER",
        "DoseSize": 1,
        "Pages": resource,
        "CanBeFavorited": True
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
            "Title": title,
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
                   "Buttons": items_lst,
                   "Selectable": True,
                   "AllowMultipleSelections": True
               }}
        add["Parameters"]["Buttons"] = items_lst
        page_dict["Inputs"].append(add)
    if input_1 == "Entry":
        add = {"Type": "Entry",
               "Name": input_name}
        page_dict["Inputs"].append(add)

    return page_dict


# changed show_buttons to none 6/21
def create_survey_page(text=None, media=None, image_framed=None, other_choices=None, input_1=None, input_2=None,
                       variable_name=None, title=None, page_group=None, input_name=None, minimum=None, maximum=None,
                       show_buttons=None, conditions_lst=None, timeout=None):
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
        page_dict = {
            "Title": title,
            "Inputs": [
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
                "\u201c", '"').replace("\u201d", '"').replace("\\n", '\n').replace("\u00f4", "ô"). \
                strip().split("; ")
        times = 1
        add = {}
        if input_1 == input_2:
            times = 2
        if input_1 == "Picker" or input_2 == "Picker":
            for i in range(times):
                add = {
                    "Type": "Picker",
                    "Name": input_name,
                    "Parameters": {
                        "Items": items_list
                    }
                }
        if input_1 == "Slider" or input_2 == "Slider":
            if items_list not in (None, [""], ""):
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
                    "Name": input_name,
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
                "Type": "Scheduler",
                "Name": "schedule_session",
                "Parameters": {
                    "Message": "It’s time to practice thinking flexibly! Head over to Hoos Think Calmly for your "
                               "scheduled session."
                }
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


# page groups per section --> include a page group for each section
# sections should be a list of dicts
def create_json_file(file_name, name, title, time_to_complete, sections, dose_by_section=False, cancel_button_text=None):
    json_dict = {
        "Name": name,
        "Title": title,
        "TimeToComplete": time_to_complete,
        "Sections": sections  # list of dicts
    }
    if dose_by_section:
        json_dict["DoseMethod"] = "OnRun"
        json_dict["DoseBySection"] = True
    if cancel_button_text not in (None, ""):
        json_dict["CancelButtonText"] = cancel_button_text
    with open(file_name, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)