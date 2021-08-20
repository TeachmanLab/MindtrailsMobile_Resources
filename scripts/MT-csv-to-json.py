import csv
import json
import imghdr
from compression import compression

sessions = {"Session1_short": 1, "Session2_short": 2, "Session3_short": 3,
            "Session4_short": 4, "Session5_short": 5}


for session in sessions.keys():
    domains_data = []
    domains = ["academics", "social situations", "physical health", "social media", "home life"]
    compression(session)

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
            scenario_count = 0
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
                        image_link = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/tree/main/images/" + \
                                     session + "/pic" + str(scenario_count) + ".jpeg"
                        scenario_dict = {'Number': scenario_count, 'Name': "Scenario" + str(scenario_count),
                                         'Title': "Scenario " + str(scenario_count), 'Caption': row[0], 'Image': image_link,
                                         'ImageType': "image/jpeg", 'ImageEmbedded': "true", "ImageFromUrl": "true"}
                        if row[2] is not "":  # if there is a second part
                            description_list = [row[1].strip(), row[2].strip()]
                        else:
                            description_list = [row[1].strip()]
                        scenario_dict["Description"] = description_list
                        scenario_dict["CorrectFeedback"] = "Correct!"
                        scenario_dict["IncorrectFeedback"] = "Whoops! That doesn't look right. Please wait a moment and try again."
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

    json_dict = {"Number": 1, "Name": session, "Title": "Session " + str(sessions[session]), "Subtitle": "A session",
                 "TimeToComplete": "00:02:00", "Domains": domains_data}

    json_file = "json_files/" + session + ".json"
    with open(json_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)  # data instead of json_dict
