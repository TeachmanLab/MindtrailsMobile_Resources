import csv
import json
import imghdr
# from compression import compression

sessions = {"Session1_short": 1, "Session2_short": 2, "Session3_short": 3,
            "Session4_short": 4, "Session5_short": 5}

sessionNum = 0


for session in sessions.keys():
    sessionNum += 1
    scenario_count = 0
    domains_data = []
    before_domains_data = []
    after_domains_data = []


    # before_domains_data
    before_scenario_count = 0
    after_scenario_count = 100
    lemon_num = 0
    quick_thinking_num = 0
    with open("csv_files/Before_After_Domains.csv", "r") as read_obj:
        reader = csv.reader(read_obj)
        for row in reader:
            if str(sessions[session]) in row[1] and session[-1 == "t"] and "Short" in row[3]:
                description_list = [row[4].replace("\u2019", "'").replace(
                                     "\u2013", "--").replace("\u2014", "--").replace(
                                     "\u201c", '"').replace("\u201d", '"')]

                scenario_dict = {"Name": row[0],
                                 "Title": row[0],
                                 "Description": description_list,
                                 "Type": "Single"}
                if row[9] not in (None, ""):
                    scenario_dict["Image"] = row[9]
                    print('row 9 is', row[9])
                if "Slider" in row[6]:
                    input_dict = {"Type": row[6],
                                  "Parameters": {
                                      "Minimum": row[7],
                                      "Maximum": row[8]
                                  }}
                    scenario_dict["Input"] = input_dict
                if "Picker" in row[6]:
                    items_list = row[10].strip().split(";")
                    input_dict = {"Type": row[6],
                                  "Parameters": {
                                      "Items": items_list
                                  }}
                    scenario_dict["Input"] = input_dict
                if "Entry" in row[6]:
                    input_dict = {"Type": row[6]}
                    scenario_dict["Input"] = input_dict
                if "seconds" in row[4]:
                    time = row[4].split("seconds")[0][-2:] + "seconds"
                    if "Entry" in row[6]:
                        input_dict = {"Type": "Entry",
                                      "Parameters": {
                                          "Duration": time
                                      }}
                    else:
                        input_dict = {"Type": "None",
                                      "Parameters": {
                                          "Duration": time
                                      }}
                if "Lemon" in row[0]:
                    if lemon_num != 0:
                        scenario_dict[
                            "Image"] = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/" \
                                       "protocols/protocol1/media/images/lemon/pic" + str(lemon_num) + ".jpeg"
                    lemon_num += 1
                if "Quick Thinking" in row[0]:
                    if row[6] == "Entry":
                        scenario_dict["Image"] = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/" \
                        "protocols/protocol1/media/images/quickthinking/pic" + str(sessions[session]) + ".jpeg"
                if row[2] == "BeforeDomain":
                    scenario_dict["Number"] = before_scenario_count
                    before_domains_data.append(scenario_dict)
                    before_scenario_count -= 1
                else:
                    scenario_dict["Number"] = after_scenario_count
                    after_domains_data.append(scenario_dict)
                    after_scenario_count += 1

    json_dict = {"Number": sessions[session], "Name": session,
                 "Title": "Week " + str(sessions[session]) + ": Part 1",
                 "TimeToComplete": "00:05:00",
                 "BeforeDomain": before_domains_data,
                 "Domains": "",
                 "AfterDomain": after_domains_data}

    domains = ["academics", "social situations", "physical health", "social media", "home life", "general"]
    # compression(session) # uncomment this when there are new images
    for domain in domains:
        # create dictionary for each domain
        domain_dict = {}
        domain_dict['Name'] = domain.capitalize()
        domain_dict['Title'] = domain.capitalize()
        domain_dict['Scenarios'] = []  # create list of the scenarios
        read_file = "csv_files/" + session + ".csv"

        with open(read_file, newline='') as csvfile:
            domain_var = False
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:  # for each row
                if row[1].strip().lower() in domains:  # if the second column of the row is in the domains
                    # if empty string, false
                    if row[1].strip().lower() == domain.strip().lower():  # if it's the domain we're dealing with
                        domain_var = True
                    else:
                        domain_var = False
                if domain_var:
                    if row[1] not in (None, "") and row[1].strip().lower() not in domains and \
                            row[1].strip().lower() != "scenario":  # if it's not a blank line or a heading line
                        scenario_count += 1  # add to scenario count
                        # create dictionary for EACH scenario
                        image_link = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/" \
                                     "protocols/protocol1/media/images/" + session + "/pic" + str(scenario_count - 1) + ".jpeg" # - 20
                        scenario_dict = {'Number': scenario_count, 'Name': "Scenario" + str(scenario_count), # - 19
                                         'Title': "Scenario " + str(scenario_count - 19), 'Caption': row[0],
                                         'Image': image_link,
                                         'ImageType': "image/jpeg", 'ImageEmbedded': "true", "ImageFromUrl": "true",
                                         "Type": "short_scenario"}
                        if row[0] is "":
                            scenario_dict["Type"] = "Information"
                        if row[2] is not "":  # if there is a second part
                            description_list = [row[1].strip(), row[2].strip()]
                        else:
                            description_list = [row[1].strip()]
                        scenario_dict["Description"] = description_list
                        scenario_dict["CorrectFeedback"] = "Correct!"
                        scenario_dict[
                            "IncorrectFeedback"] = "Whoops! That doesn't look right. Please wait a moment and try again."
                        word_lst = []
                        if ';' in row[5]:
                            semi_loc = row[5].find(';')
                            word1 = row[5][0:semi_loc].strip()
                            word2 = row[5][semi_loc + 1:].strip()
                            word_lst.append(word1)
                            word_lst.append(word2)
                        else:
                            word_lst.append(row[5].strip())
                        scenario_dict["Words"] = word_lst
                        scenario_dict["Question"] = row[6].strip()
                        if row[7] == 'Y':
                            answer = "Yes"
                        if row[7] == 'N':
                            answer = "No"
                        scenario_dict['Answer'] = answer
                        domain_dict["Scenarios"].append(scenario_dict)
            domains_data.append(domain_dict)
            ## add stuff for end of session
            ## within scenario

    json_dict["Domains"] = domains_data

    json_file = "json_files/" + session + ".json"
    with open(json_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)  # data instead of json_dict


## long scenarios
sessions = {"Session1_long": 1, "Session2_long": 2, "Session3_long": 3,
            "Session4_long": 4, "Session5_long": 5}
sessionNum = 0
for session in sessions.keys():
    sessionNum += 1
    scenario_count = 0

    before_domains_data = []
    domains_data = []
    after_domains_data = []
    domains = ["academics", "social situations", "physical health", "social media", "home life", "general"]
    row_num = 0


    # before domains

    before_scenario_count = 0
    after_scenario_count = 100
    lemon_num = 0
    quick_thinking_num = 0
    with open("csv_files/Before_After_Domains.csv", "r") as read_obj:
        reader = csv.reader(read_obj)
        for row in reader:
            if str(sessions[session]) in row[1] and session[-1 == "g"] and "Long" in row[3]:
                description_list = [row[4].replace("\u2019", "'").replace(
                                     "\u2013", "--").replace("\u2014", "--").replace(
                                     "\u201c", '"').replace("\u201d", '"')]
                scenario_dict = {"Name": row[0],
                                 "Title": row[0],
                                 "Description": description_list,
                                 "Type": "Single"}
                if "Slider" in row[6]:
                    input_dict = {"Type": row[6],
                                  "Parameters": {
                                      "Minimum": row[7],
                                      "Maximum": row[8]
                                  }}
                    scenario_dict["Input"] = input_dict
                if "Picker" in row[6]:
                    items_list = row[10].strip().split(";")
                    input_dict = {"Type": row[6],
                                  "Parameters": {
                                      "Items": items_list
                                  }}
                    scenario_dict["Input"] = input_dict
                if "Entry" in row[6]:
                    input_dict = {"Type": row[6]}
                    scenario_dict["Input"] = input_dict
                if "seconds" in row[4]:
                    time = row[4].split("seconds")[0][-2:] + "seconds"
                    if "Entry" in row[6]:
                        input_dict = {"Type": "Entry",
                                      "Parameters": {
                                          "Duration": time
                                      }}
                    else:
                        input_dict = {"Type": "None",
                                      "Parameters": {
                                          "Duration": time
                                      }}
                if "Lemon" in row[0]:
                    if lemon_num != 0:
                        scenario_dict["Image"] = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/" \
                        "protocols/protocol1/media/images/lemon/pic" + str(lemon_num) + ".jpeg"
                    lemon_num += 1
                if "Quick Thinking" in row[0]:
                    if "Entry" in row[6]:
                        scenario_dict["Image"] = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/" \
                        "protocols/protocol1/media/images/quickthinking/pic" + str(sessions[session]) + ".jpeg",
                if row[2] == "BeforeDomain":
                    scenario_dict["Number"] = before_scenario_count
                    before_domains_data.append(scenario_dict)
                    before_scenario_count -= 1
                else:
                    scenario_dict["Number"] = after_scenario_count
                    after_domains_data.append(scenario_dict)
                    after_scenario_count += 1

    json_dict = {"Number": sessions[session], "Name": session,
                 "Title": "Week " + str(sessions[session]) + ": Part 2",
                 "TimeToComplete": "00:05:00",
                 "BeforeDomain": before_domains_data,
                 "Domains": "",
                 "AfterDomain": after_domains_data}

    for domain in domains:
        # create dictionary for each domain
        domain_dict = {}
        domain_dict['Name'] = domain.capitalize()
        domain_dict['Title'] = domain.capitalize()
        domain_dict['Scenarios'] = []  # create list of the scenarios
        read_file = "csv_files/" + session + ".csv"
        #scenario_count = 0

        ## before/after domains
        with open(read_file, newline='') as csvfile:
            domain_var = False
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:  # for each row
                if row[0].strip().lower() in domains:  # if the first column of the row is in the domains
                    if row[0].strip().lower() == domain.strip().lower():  # if it's the domain we're dealing with
                        domain_var = True
                        print("Domain is:", domain)
                        image_link_1 = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/" \
                                       "protocols/protocol1/media/images/" + \
                                     session + "/pic0.jpeg"
                        image_link_2 = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/" \
                                       "protocols/protocol1/media/images/" + \
                                      session + "/pic1.jpeg"
                        image_link_3 = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw/main/bbbs/" \
                                       "protocols/protocol1/media/images/" + \
                                       session + "/pic2.jpeg"
                        # each value in this dict should be a scenario dict
                        scenario_dicts = {"Topic congruent 1": {"Number": 1,
                                                                "Name": "Scenario1",
                                                                "Title": "Scenario 1",
                                                                "Caption": "",
                                                                "Image": image_link_1,
                                                                "ImageType": "image/jpeg",
                                                                "ImageEmbedded": "True",
                                                                "ImageFromURL": "True"},
                                          "Topic congruent 2": {"Number": 2,
                                                                "Name": "Scenario2",
                                                                "Title": "Scenario 2",
                                                                "Caption": "",
                                                                "Image": image_link_2,
                                                                "ImageType": "image/jpeg",
                                                                "ImageEmbedded": "True",
                                                                "ImageFromURL": "True"},
                                          "Topic incongruent": {"Number": 3,
                                                                "Name": "Scenario3",
                                                                "Title": "Scenario 3",
                                                                "Caption": "",
                                                                "Image": image_link_3,
                                                                "ImageType": "image/jpeg",
                                                                "ImageEmbedded": "True",
                                                                "ImageFromURL": "True"}
                                          }
                        scenario_count += 3
                        row_num = 0  # bring row num back to 0
                        # print("session is", session, "and row num is 0 and row[0] is", row[0])
                    else:
                        domain_var = False
                # print(row_num)
                if domain_var == True and row_num == 1:  # if we're in the section for that domain & first row
                    # the "description" of that dict
                    for scenario in scenario_dicts.values():
                        num = scenario["Number"] + 1  # this is the number row each scenario corresponds to
                        scenario["Description"] = [row[num]]
                        scenario["Words"] = None
                        input_dict = {"Type": "TimedText",
                                      "Parameters": {
                                          "Duration" : 45
                                      }}
                        scenario["Input"] = input_dict
                        # scenario_dicts["Topic congruent 1"]["Description"] = [row[2]]  # list of description
                        # scenario_dicts["Topic congruent 2"]["Description"] = [row[3]]  # list of description
                        # scenario_dicts["Topic incongruent"]["Description"] = [row[4]]  # list of description
                        # scenario_dicts["Topic congruent 1"][]
                        # scenario_dicts["Topic congruent 1"]["Words"] = None
                        # scenario_dicts["Topic congruent 2"]["Words"] = None
                        # scenario_dicts["Topic incongruent"]["Words"] = None
                if domain_var == True and row_num == 3:
                    scenario_dicts["Topic congruent 1"]["Caption"] = row[2]
                    scenario_dicts["Topic congruent 2"]["Caption"] = row[3]
                    scenario_dicts["Topic incongruent"]["Caption"] = row[4]
                if domain_var == True and row_num >= 4:  # if we're in that section and in part where they have descriptions
                    # if dict does not have that key, create it
                    if scenario_dicts["Topic congruent 1"]["Words"] is None or \
                            scenario_dicts["Topic congruent 2"]["Words"] is None or \
                            scenario_dicts["Topic incongruent"]["Words"] is None:
                        scenario_dicts["Topic congruent 1"]["Words"] = [row[2]]
                        scenario_dicts["Topic congruent 2"]["Words"] = [row[3]]
                        scenario_dicts["Topic incongruent"]["Words"] = [row[4]]
                    else:
                        scenario_dicts["Topic congruent 1"]["Words"].append(row[2])
                        scenario_dicts["Topic congruent 2"]["Words"].append(row[3])
                        scenario_dicts["Topic incongruent"]["Words"].append(row[4])
                    # if not, just append it
                if domain_var == True and row_num == 17:  # if we're done with that section
                    # create list of the scenario_dicts values
                    # then add each scenario_dict to this
                    for scenario in scenario_dicts.values():  # for each dictionary in the larger dictionary
                        # print(scenario)
                        domain_dict["Scenarios"].append(scenario)
                if domain_var == True:
                    row_num += 1  # increase row num
            domains_data.append(domain_dict)
    json_dict["Domains"] = domains_data
    json_file = "json_files/" + session + ".json"
    with open(json_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)  # data instead of json_dict
