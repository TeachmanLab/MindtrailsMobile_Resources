import csv
import imghdr
import json
import random

# sessions = {"Session1_short": 1, "Session2_short": 2, "Session3_short": 3,
#             "Session4_short": 4, "Session5_short": 5}

# first, get short session scenarios
sessions = {"Session1_short": 1,
            "Session1_long": 1,
            "Session2_short": 2,
            "Session2_long": 2,
            "Session3_short": 3,
            "Session3_long": 3,
            "Session4_short": 4,
            "Session4_long": 4,
            "Session5_short": 5,
            "Session5_long": 5}

sessionNum = 0
for session in sessions.keys():
    sessionNum += 1

    domains_data = []
    before_domains_data = []
    after_domains_data = []

    # before_domains_data
    with open("csv_files/Before_After_Domains.csv", "r") as read_obj:
        reader = csv.reader(read_obj)
        before_domains_dicts = {}
        domains_dicts = {}
        after_domains_dicts = {}

        long_before_domains_dicts = {}
        long_domains_dicts = {}
        long_after_domains_dicts = {}

        lookup = {"BeforeDomain_Short": before_domains_dicts,
                  "AfterDomain_Short": after_domains_dicts,
                  "BeforeDomain_Long": long_before_domains_dicts,
                  "AfterDomain_Long": long_after_domains_dicts}
        scenario_dicts = {}
        for row in reader:  # each row is a page
            lookup_code = row[2] + '_' + row[3]
            if str(sessions[session]) in row[1] and session[session.find("_") + 1:] == row[3].lower():  # AND it's long or short ... and session[-1 == "t"] and "Short" in row[3]
                page_group = row[0]
                before_after = row[2]
                text = row[4].replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014", " - "). \
                    replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n")
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
                                     "Type": "Exercise",
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
                                 "Name": row[14],
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
                                {"Type": "Entry",
                                 "Name": row[14]}
                            )
                    if input_1 == "Buttons" or input_2 == "Buttons":
                        for i in range(times):
                            page_dict["Inputs"].append(
                                {"Type": "Buttons",
                                 "Name": row[14],
                                 "Parameters": {
                                     "Buttons": items_list,
                                     "Selectable": True
                                 }}
                            )
                lookup[lookup_code][page_group]["Pages"].append(page_dict)

    #before_domains_data = list(scenario_dicts.values())

    short_json_dict = {"Name": session,
                 "Title": "Week " + str(sessions[session]) + ": Part 1",
                 "TimeToComplete": "00:10:00",
                 "Sections": [
                     {
                         "Name": "BeforeDomain",
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
    if session == "Session1_short":
        short_json_dict["TimeToComplete"] = "00:15:00"
    long_json_dict = {"Name": session,
                       "Title": "Week " + str(sessions[session]) + ": Part 2",
                       "TimeToComplete": "00:15:00",
                       "Sections": [
                           {
                               "Name": "BeforeDomain",
                               "PageGroups": list(long_before_domains_dicts.values())
                           },
                           {
                               "Name": "Domains",
                               "Description": "The domains listed here are some areas that may cause teens to feel "
                                              "anxious. Please select the one that you'd like to work on during today's"
                                              " training. ",
                               "Domains": [{
                                     "Name": "Academics",
                                     "Title": "Academics"
                               },
                                 {
                                     "Name": "Social Situations",
                                     "Title": "Social Situations"
                                 },
                                 {
                                     "Name": "Physical Health",
                                     "Title": "Physical Health"
                                 },
                                 {
                                     "Name": "Social Media",
                                     "Title": "Social Media"
                                 },
                                 {
                                     "Name": "Home Life",
                                     "Title": "Home Life"
                                 },
                                 {
                                     "Name": "General",
                                     "Title": "General"
                                 }
                                 ]
                           },
                           {
                               "Name": "AfterDomain",
                               "PageGroups": list(long_after_domains_dicts.values())
                           }

                       ]}
    if session[-1] == "t":  # deal with the short one
        read_file = "csv_files/" + session + ".csv"
        with open(read_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            domains_dict = {}
            scenario_num = 0
            for row in reader:
                label = row[0]  # scenario name
                domain = row[9]
                unique_name = row[4] + "_" + session + "_" + domain
                if domain not in (None, "") and domain != "Domain":  # if there is a domain
                    if domain not in domains_dict.keys():
                        domains_dict[domain] = {
                                "Name": domain,
                                "Title": domain,
                                "PageGroups": []
                            }
                    if label not in (None, ""):  # if it's a scenario\
                        scenario_num += 1
                        puzzle_text_1 = row[1]
                        puzzle_text_2 = row[2]  # if there's a second puzzle
                        comp_question = row[6]
                        if row[7] == "N":
                            answer = "No"
                        else:
                            answer = "Yes"
                        # get list of words
                        word_lst = []
                        word1 = ""
                        word2 = ""
                        if ';' in row[5]:
                            semi_loc = row[5].find(';')
                            word1 = row[5][0:semi_loc].strip()
                            word2 = row[5][semi_loc + 1:].strip()
                            word_lst.append(word1)
                            word_lst.append(word2)
                        elif ',' in row[5]:
                            semi_loc = row[5].find(',')
                            word1 = row[5][0:semi_loc].strip()
                            word2 = row[5][semi_loc + 1:].strip()
                            word_lst.append(word1)
                            word_lst.append(word2)
                        else:
                            word_lst.append(row[5].strip())

                        # to go within pages of the scenario page group
                        scenario_list = [{
                                "Name": label,
                                "ImageUrl": "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/"
                                            "protocols/protocol1/media/images/" + session + "/pic" +
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
                                "ShowButtons": "WhenCorrect",
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
                                        "Name": unique_name + "_puzzle",
                                        "Parameters": {
                                            "Words": [word_lst[0]]
                                        }
                                    }]
                            }
                        ]
                        if word2:
                            scenario_list.append({
                                "Name": "Puzzle",
                                "ShowButtons": "WhenCorrect",
                                "Inputs": [{
                                    "Type": "Text",
                                    "Parameters": {"Text": puzzle_text_2}
                                },
                                         {
                                             "Type": "WordPuzzle",
                                             "CorrectFeedback": "Correct!",
                                             "Name": unique_name + "_puzzle2",
                                             "IncorrectFeedback": "Whoops! That doesn't look right. Please wait a "
                                                                  "moment and try again.",
                                             "CorrectScore": 0.5,
                                             "IncorrectDelay": 5000,
                                             "Parameters": {
                                                 "Words": [word_lst[1]]
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
                                        "Name": unique_name + "_question",
                                        "CorrectFeedback": "Correct!",
                                        "IncorrectFeedback": "Whoops! That doesn't look right. Please wait a moment and "
                                                             "try again.",
                                        "CorrectScore": 0.5,
                                        "IncorrectDelay": 5000,
                                        "Parameters": {
                                            "Buttons": [
                                                "Yes",
                                                "No"
                                            ],
                                            "ColumnCount": 2,
                                            "Answer": answer
                                        }
                                    }
                                ]
                            })
                        page_group = {
                            "Name": "Scenario " + str(scenario_num),
                            "Type": "Scenario",
                            "Pages": scenario_list
                        }
                    else:  # an info page
                        page_group = {
                            "Name": "Great job!",
                            "Type": "Information",
                            "Pages": [{
                                    "Name": "Great job!",
                                    "Inputs": [{
                                            "Type": "Text",
                                            "Parameters": {
                                                "Text": row[1]}}]
                                }]
                        }
                    domains_dict[domain]["PageGroups"].append(page_group)
            short_json_dict["Sections"][1]["Domains"] = list(domains_dict.values())



                # at the end, add to short_json_dict["Sections"][1]["Domains"] = domains
    # deal with long
    # numbers just correspond to first image for that domain
    domains = {"Academics": 0,
               "Social Situations": 3,
               "Physical Health": 6,
               "Social Media": 9,
               "Home Life": 12,
               "General": 15}
    if session[-1:] == "g":
        read_file = "csv_files/" + session + ".csv"
        long_domains_dicts = []
        domain_num = 0
        for domain in domains.keys():  # for each domain, go through the session file
            domain_num += 1
            with open(read_file, newline='') as csvfile:  # open session file
                reader = csv.reader(csvfile)
                row_num = 0
                domain_var = False
                for row in reader:
                    row_num += 1
                    if row[0].strip().lower() == domain.lower():
                        # print("loop 1: domain", row[0].strip().lower() == domain.lower(), row[0].lower(), domain)
                        row_num = 0
                        domain_var = True
                        thoughts_1 = []
                        thoughts_2 = []
                        thoughts_3 = []
                        feelings_1 = []
                        feelings_2 = []
                        feelings_3 = []
                        behaviors_1 = []
                        behaviors_2 = []
                        behaviors_3 = []
                        domain_dict = {
                            "Name": domain,
                            "Title": domain,
                            "PageGroups": []
                        }
                        page_groups = {}
                        image_link_1 = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/" \
                                       "protocols/protocol1/media/images/" + \
                                       session + "/pic" + str(domains[domain]) + ".jpeg"
                        image_link_2 = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/" \
                                       "protocols/protocol1/media/images/" + \
                                       session + "/pic" + str(domains[domain] + 1) + ".jpeg"
                        image_link_3 = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/" \
                                       "protocols/protocol1/media/images/" + \
                                       session + "/pic" + str(domains[domain] + 2) + ".jpeg"
                    # print(row_num, domain_var)
                    if domain_var and row_num == 1:
                        scenario_1 = row[2]
                        scenario_2 = row[3]
                        scenario_3 = row[4]
                    if domain_var and row_num == 2:
                        unique_name_1 = row[2] + "_" + session + "_" + domain
                        unique_name_2 = row[3] + "_" + session + "_" + domain
                        unique_name_3 = row[4] + "_" + session + "_" + domain
                    if domain_var and row_num == 3:
                        label_1 = row[2]
                        label_2 = row[3]
                        label_3 = row[4]
                        # print(label_1, label_2, label_3)
                    if domain_var and 3 < row_num <= 8:
                        thoughts_1.append(row[2])
                        thoughts_2.append(row[3])
                        thoughts_3.append(row[4])
                    if domain_var and 8 < row_num <= 13:
                        feelings_1.append(row[2])
                        feelings_2.append(row[3])
                        feelings_3.append(row[4])
                    if domain_var and 13 < row_num <= 18:
                        behaviors_1.append(row[2])
                        behaviors_2.append(row[3])
                        behaviors_3.append(row[4])
                    if row_num == 18:
                        domain_var = False
                        row_num = 0
            random.shuffle(feelings_1)
            random.shuffle(feelings_2)
            random.shuffle(feelings_3)
            random.shuffle(thoughts_1)
            random.shuffle(thoughts_2)
            random.shuffle(thoughts_3)
            random.shuffle(behaviors_1)
            random.shuffle(behaviors_2)
            random.shuffle(behaviors_3)
            with open("csv_files/long_scenarios_structure.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                image_bool = False
                for row in reader:
                    label = row[0]
                    text = row[4].replace("[Scenario 1]", scenario_1).replace("[Scenario 2]", scenario_2).\
                        replace("\u2019", "'").replace("[Scenario 3]", scenario_3). \
                            replace("\u2013", " - ").replace("\u2014", " - "). \
                            replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n")
                    if "1" in row[0]:
                        page_group = "Scenario 1"
                        page_type = "Scenario"
                        # text = row[4].replace("[Scenario 1]", scenario_1).replace("\u2019", "'"). \
                        #     replace("\u2013", " - ").replace("\u2014", " - "). \
                        #     replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n")
                    elif "2" in row[0]:
                        page_group = "Scenario 2"
                        page_type = "Scenario"
                        # text = row[4].replace("[Scenario 2]", scenario_2). \
                        #     replace("[Scenario 3]", scenario_3). \
                        #     replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014", " - "). \
                        #     replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n")
                    elif "3" in row[0]:
                        page_group = "Scenario 3"
                        page_type = "Scenario"
                        # text = row[4].replace("[Scenario 3]", scenario_3). \
                        #     replace("\u2019", "'").replace("\u2013", " - ").replace("\u2014", " - "). \
                        #     replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n")
                    else:
                        page_group = "Intro"
                        page_type = "Information"
                    input_1 = row[6]
                    if "Scenario 1" in row[0] and row[10] == "TRUE":
                        image_bool = True
                        image = image_link_1
                        label = label_1
                        unique_name = unique_name_1
                    if "Scenario 2" in row[0] and row[10] == "TRUE":
                        image_bool = True
                        image = image_link_2
                        label = label_2
                        unique_name = unique_name_2
                    if "Scenario 3" in row[0] and row[10] == "TRUE":
                        image_bool = True
                        image = image_link_3
                        label = label_3
                        unique_name = unique_name_3
                    if page_group not in page_groups:
                        # print("Creating page group", page_group, session)
                        scenario_dict = {"Name": page_group,
                                         "Title": page_group,
                                         "Type": page_type,
                                         "Pages": [

                                         ]}
                        # print("Creating page group", page_group)
                        page_groups[page_group] = scenario_dict

                    if image_bool:
                        print("image", row[0])
                        page = {
                            "Name": label,
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
                            "Name": label,
                            "Inputs": [{
                                "Type": "Text",
                                "Parameters": {
                                    "Text": text
                                }
                            }]
                        }
                    # timeout
                    if row[13] not in (None, ""):
                        page["Timeout"] = int(row[13])
                        page["ShowButtons"] ="AfterTimeout"

                    feelings_lookup = {
                        "1": feelings_1,
                        "2": feelings_2,
                        "3": feelings_3
                    }

                    thoughts_lookup = {
                        "1": thoughts_1,
                        "2": thoughts_2,
                        "3": thoughts_3
                    }

                    behaviors_lookup = {
                        "1": behaviors_1,
                        "2": behaviors_2,
                        "3": behaviors_3
                    }


                    if input_1 == "Entry":
                        page["Inputs"].append({
                            "Name": unique_name,
                            "Type": "Entry"
                        })
                    if input_1 == "TimedText":
                        page["ShowButtons"] = "WhenCorrect"
                        if "feelings" in text:
                            page["Inputs"].append({
                                "Type": "TimedText",
                                "Parameters": {
                                    "Text": feelings_lookup[page_group[-1:]],
                                    "Duration": 15
                                }
                            })
                        if "thoughts" in text:
                            page["Inputs"].append({
                                "Type": "TimedText",
                                "Parameters": {
                                    "Text": thoughts_lookup[page_group[-1:]],
                                    "Duration": 15
                                }
                            })
                        if "behaviors" in text:
                            page["Inputs"].append({
                                "Type": "TimedText",
                                "Parameters": {
                                    "Text": behaviors_lookup[page_group[-1:]],
                                    "Duration": 15
                                }
                            })

                    page_groups[page_group]["Pages"].append(page)
                    # print(domain_num, domain)
                    long_json_dict["Sections"][1]["Domains"][domain_num - 1]["PageGroups"] = list(page_groups.values())


                    image_bool = False

    if session[-1] == "t":
        json_file = "json_files/" + session + ".json"
        with open(json_file, 'w') as outfile:
            json.dump(short_json_dict, outfile, indent=4)  # data instead of json_dict
    else:
        json_file = "json_files/" + session + ".json"
        with open(json_file, 'w') as outfile:
            json.dump(long_json_dict, outfile, indent=4)  # data instead of json_dict
