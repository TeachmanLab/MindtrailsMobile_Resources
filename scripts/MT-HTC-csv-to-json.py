import csv
import imghdr
import json
import math
import random
import numpy as np
import pandas as pd


groups = {
    "Undergraduate": [4, 4],
    "Graduate": [9, 21],
    "Faculty": [14, 38],
    "Staff": [19, 55]
}

sessionNum = 0
for group in groups.keys():
    sessionNum += 1

    domains_data = []
    before_domains_data = []
    after_domains_data = []

    # before_domains_data
    with open("HTC/csv_files/HTC_Before_After_Domains.csv", "r") as read_obj:
        reader = csv.reader(read_obj)
        next(reader)
        before_domains_dicts = {}
        before_domains_dicts_1 = {}
        domains_dicts = {}
        after_domains_dicts = {}
        after_domains_dicts_1 = {}
        # parse before after
        lookup = {"BeforeDomain_1": before_domains_dicts_1,
                  "BeforeDomain_All": before_domains_dicts,
                  "AfterDomain_1": after_domains_dicts_1,
                  "AfterDomain_All": after_domains_dicts}
        scenario_dicts = {}
        for row in reader:  # each row is a page
            if row[2]:
                doses = row[1]
                lookup_code = row[2] + "_" + row[1]  # this is BeforeDomain_1 for ex
                before_after = row[2]
                text = row[4].replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014", " - "). \
                    replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n")
                page_group = row[0]
                input_1 = row[5]
                input_2 = row[6]
                media = row[9]
                other_choices = row[10]
                image_framed = row[11]
                timeout = row[12]
                show_buttons = row[13]

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
                        "\u201c", '"').replace("\u201d", '"').replace("\\", "/"). \
                        strip().split("; ")
                    times = 1
                    if input_1 == input_2:
                        times = 2
                    if input_1 == "Slider" or input_2 == "Slider":
                        for i in range(times):  # basically if both = slider
                            page_dict["Inputs"].append(
                                {"Type": "Slider",
                                 "Parameters": {
                                     "Minimum": row[7],
                                     "Maximum": row[8],
                                     "OtherChoices": items_list
                                 }
                                 }
                            )
                    if input_1 == "Entry" or input_2 == "Entry":
                        for i in range(times):
                            page_dict["Inputs"].append(
                                {"Type": "Entry"}
                            )
                    if input_1 == "Buttons" or input_2 == "Buttons":
                        for i in range(times):
                            page_dict["Inputs"].append(
                                {"Type": "Buttons",
                                 "Parameters": {
                                     "Buttons": items_list,
                                     "Selectable": True
                                 }}
                            )
                    if input_1 == "Checkbox" or input_2 == "Checkbox":
                        for i in range(times):
                            page_dict["Inputs"].append(
                                {"Type": "Buttons",
                                 "Parameters": {
                                     "Buttons": items_list,
                                     "Selectable": True,
                                     "AllowMultipleSelections": True
                                 }}
                            )
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
                         "Name": "AfterDomain_1",
                         "Doses": [1],
                         "PageGroups": list(after_domains_dicts_1.values())
                     },
                     {
                         "Name": "AfterDomain",
                         "PageGroups": list(after_domains_dicts.values())
                     }

                 ]}
    df = pd.read_csv("/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/HTC_scenarios.csv",
                     header=None,
                     skiprows=1)

    ds = df.sample(frac=1)

    ds.to_csv("HTC/csv_files/shuffled_scenarios.csv", index=False)
    with open("HTC/csv_files/shuffled_scenarios.csv", newline='') as read_obj:
        csv_reader = csv.reader(read_obj)
        next(csv_reader)
        i = groups[group][0]
        domains_dict = {}
        scenario_num = 0
        page_groups_dict = {}
        # {} below are all the page group dicts
        # Microdose {count / 10 } : page_group
        # Microdose {count / 10 } : page_group
        domains_lookup = {
            "Social Situations": [{}, 0], # {} will have all the page groups, 0 is the counter of scenarios
            "Physical Health": [{}, 0],
            "Academics/Work/Career Development": [{}, 0],
            "Family & Home Life": [{}, 0],
            "Finances": [{}, 0],
            "Mental Health/Self-Evaluation": [{}, 0],
            "Romantic Relationships": [{}, 0],
            "Unspecified": [{}, 0],
            "Indecision/Decision-Making": [{}, 0]
        }
        for row in csv_reader:
            domain = row[0]
            domain_2 = row[1]
            domain_3 = row[2]
            label = row[3]  # scenario name
            if domain not in (None, "") and domain:  # if there is a domain

                # first, create domains
                if domain not in domains_dict.keys():
                    domains_dict[domain] = {
                        "Name": domain,
                        "Title": domain,
                        "PageGroups": []
                    }
                if domain_2 not in domains_dict.keys() and domain_2:
                    domains_dict[domain_2] = {
                        "Name": domain_2,
                        "Title": domain_2,
                        "PageGroups": []
                    }
                if domain_3 not in domains_dict.keys() and domain_3:
                    domains_dict[domain_3] = {
                        "Name": domain_3,
                        "Title": domain_3,
                        "PageGroups": []
                    }

                # create scenario pages
                if label not in (None, ""):  # if it's a scenario\
                    scenario_num += 1
                    puzzle_text_1 = row[i]
                    print("Label:", label)
                    print("i", i)
                    print("Puzzle text: ", puzzle_text_1)
                    word_1 = row[i].split()[-1][:-1]
                    word_2 = ""
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
                    np.random.shuffle(answers_lst)
                    correct_answer = row[i + 3]
                    # get list of words

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
                                "Framed": "true",
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
                                    "CorrectFeedback": "Correct!",
                                    "IncorrectFeedback": "Whoops! That doesn't look right. Please wait a moment "
                                                         "and try again.",
                                    "CorrectScore": 0.5,
                                    "IncorrectDelay": 5000,
                                    "CauseNavigation": "true",
                                    "Parameters": {
                                        "Words": word_1
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
                                    "CorrectScore": 0.5,
                                    "IncorrectDelay": 5000,
                                    "CauseNavigation": "true",
                                    "Parameters": {
                                        "Words": word_2
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
                    domain_lst = [domain]
                    if domain_2:
                        domain_lst = [domain, domain_2]
                        if domain_3:
                            domain_lst = [domain, domain_2, domain_3]
                    for domain in domain_lst:
                        if domains_lookup[domain][1] % 10 == 0 or domains_lookup[domain][1] == 0: # if it's a multiple of 10
                            # create new page group
                            counter = domains_lookup[domain][1]
                            if counter == 0:
                                microdose_num = 0
                            else:
                                microdose_num = str(math.floor(counter / 10))


                            page_group = {
                                "Name": "Microdose " + str(microdose_num),
                                "Type": "Scenario",
                                "Pages": scenario_list
                            }

                            domains_lookup[domain][0]["Microdose " + str(microdose_num)] = page_group
                        else:
                            counter = domains_lookup[domain][1]
                            print(counter)
                            for page in scenario_list:
                                domains_lookup[domain][0]["Microdose " + str(math.floor(counter / 10))]["Pages"].append(page)
                        domains_lookup[domain][1] += 1
                    print(domain, domains_lookup[domain][1])
                        # the most recent


                # domains_dict[domain]["PageGroups"].append(page_group)
                # if domain_2:
                #     domains_dict[domain_2]["PageGroups"].append(page_group)
                # if domain_3:
                #     domains_dict[domain_2]["PageGroups"].append(page_group)
        for domain in domains_lookup:
            domains_dict[domain]["PageGroups"] = list(domains_lookup[domain][0].values())
    with open("/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/HTC_long_scenarios.csv") as read_file:
        reader = csv.reader(read_file)
        next(reader)
        next(reader)
        i = groups[group][1]
        for row in reader:
            domain = row[0]
            domain_2 = row[1]
            domain_3 = row[2]
            label = row[3]
            scenario_description = row[i]
            image = row[i + 1]

            # each row corresponds to one page group
            page_group = {"Name": "Long Scenario: " + label.strip(),
                             "Title": "Long Scenario: " + label.strip(),
                             "Type": "Scenario",
                             "Pages": [

                             ]}
            # scenario_list =
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
                    input_1 = row_str[4]
                    input_2 = row_str[5]

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
                    if input_1 == "Entry":
                        page["Inputs"].append({
                            "Type": "Entry"
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
            domains_dict[domain]["PageGroups"].append(page_group)
            if domain_2:
                domains_dict[domain_2]["PageGroups"].append(page_group)
            if domain_3:
                domains_dict[domain_2]["PageGroups"].append(page_group)

    json_dict["Sections"][2]["Domains"] = list(domains_dict.values())
    # print(range(len(json_dict["Sections"][1]["Domains"])))
    for domain in range(len(json_dict["Sections"][2]["Domains"])):
       random.shuffle(json_dict["Sections"][2]["Domains"][domain]["PageGroups"])
    # print(json_dict["Sections"][1]["Domains"][0])
    json_file = "HTC/json_files/" + group + ".json"
    with open(json_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)  # data instead of json_dict

