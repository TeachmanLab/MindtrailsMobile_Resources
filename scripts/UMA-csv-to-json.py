import csv
import json
import random
import numpy as np
from HTC_helpers import rreplace, get_resources, get_ER, get_tips
from UMA_create_pages import create_survey_page, create_resource_page_group_new, create_long_scenario_page_group
from UMA_create_pages import create_discrimination_page
from UMA_create_pages import create_scenario_page_group
from UMA_create_pages import create_json_file

uma_resources_lookup = get_resources(file_path=r"C:\Users\maddie\Desktop\python\UMA resources.csv") #8/9

uma_json = {} #8/9
uma_groups = {
    "UMA": [4, 4, uma_json]
}

for group in uma_groups.keys():
    ER_lookup = get_ER(file_path=r"C:\Users\maddie\Desktop\python\ER_strategies.csv")
    tip_lst = get_tips(file_path=r"C:\Users\maddie\Desktop\python\tips.csv")

    long_page_groups ={
        "Social Situations": [],
        "Physical Health": [],
        "Academics/Work/Career Development": [],
        "Family & Home Life": [],
        "Finances": [],
        "Mental Health": [],
        "Romantic Relationships": [],
    }
    with open(r"C:\Users\maddie\Desktop\python\UMA long scenarios.csv", "r", encoding="utf-8") as read_file:
        reader = csv.reader(read_file)
        next(reader)  # skip line 1
        next(reader)  # skip line 2
        i = uma_groups[group][1]  #4
        for row in reader:
            #unique_names = unique
            #others_names = others
            domain = row[0].strip()
            domain_2 = row[1]
            label = row[3]
            scenario_description = row[i]
            thoughts_lst = [row[i + 2], row[i + 3], row[i + 4], row[i + 5], row[i + 6]]
            feelings_lst = [row[i + 7], row[i + 8], row[i + 9], row[i + 10], row[i + 11]]
            behaviors_lst = [row[i + 12], row[i + 13], row[i + 14], row[i + 15], row[i + 16]]
            # check if the images across all groups all the same (this changes the image url)
            #unique_image = False
            if label in unique:
                unique_image = True
            else:
                unique_image = False
               # if all 4 image links aren't equal, then each has a unique image
               # print("Label:", label, "IS unique")
          #  else:
                #print("Label:", label, "IS NOT unique")

            if scenario_description not in (None, "", "NA", "N/A") and label not in (None, ""):
                # create long scenario page group
                page_group = create_long_scenario_page_group(label=label, scenario_description=scenario_description,
                                                             unique_image=unique_image, group=group,
                                                             thoughts_lst=thoughts_lst,
                                                             feelings_lst=feelings_lst, behaviors_lst=behaviors_lst)
                long_page_groups[domain].append(page_group)  # add page group to correct domain's list
                if domain_2 not in (None, ""):  # if it also belongs to a second domain, add the page group to that list
                    long_page_groups[domain_2].append(page_group)
    # shuffle each list of long scenario page groups
    for domain in long_page_groups:
        random.shuffle(long_page_groups[domain])


    ##### Create the dictionaries for all the json files #######
    before_domains_dicts = {}
    dose_1 = {}
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
    control_dose_1 = {}

    # The keys in this dictionary correspond to the HTC_survey_questions.csv lookup codes ([Subject]_[Doses])
    # You can see all the lookup codes and their meanings below:
    # https://docs.google.com/spreadsheets/d/1Z_syG-HbyFT2oqMsHnAbidRtlH97IVxnBqbNKZWbwLY/edit#gid=0
    lookup = {"Dose_1": dose_1,
              "BeforeDomain_All": before_domains_dicts,
              "AfterDomain_1": after_domains_dicts_1,
              "AfterDomain_All": after_domains_dicts,
              "Control_Dose_1": control_dose_1,
              "EOD_All": end_of_day,
              "Biweekly_All": biweekly,
              "Biweekly_Week 2": biweekly_2,
              "Biweekly_Week 4": biweekly_4,
              "Biweekly_Week 6": biweekly_6,
              "Biweekly_Week 8": biweekly_8,
              "Biweekly_Control_Week 2": biweekly_2_control,
              "Biweekly_Control_Week 4": biweekly_4_control,
              "Biweekly_Control_Week 6": biweekly_6_control,
              "Biweekly_Control_Week 8": biweekly_8_control,
              "ReasonsForEnding_All": reasons
              }
    scenario_dicts = {}

    # Open the file with all the content
    with open(r"C:\Users\maddie\Desktop\python\UMA_survey_questions.csv", "r", encoding="utf-8") as read_obj:
        reader = csv.reader(read_obj)
        next(reader)  # skip first line
        for row in reader:  # each row is a page
            lookup_code = row[3] + "_" + row[2]
            if row[0] == "Practice CBM-I":
                # In the special case that it's "Practice CBM-I", then we have to create scenarios

                with open(r"C:\Users\maddie\Desktop\python\UMA dose1_scenarios.csv", "r", encoding="utf-8") as dose1_read_obj:  # scenarios for first dose in file
                    dose1_reader = csv.reader(dose1_read_obj)
                    next(dose1_reader)
                    dose1_scenario_num = 0
                    for row_1 in dose1_reader:
                        # First, add the video that goes before each scenario
                        lookup[lookup_code]["Video" + str(dose1_scenario_num)] = {
                            "Name": "Video " + str(dose1_scenario_num + 1),
                            "Pages": [{
                                "Inputs": [{
                                    "Type": "Media",
                                    "Parameters": {
                                        "ImageUrl": "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw"
                                                    "/main/HTC/protocols/protocol1/media/videos/Staff/video" +
                                                    str(dose1_scenario_num + 1) + ".mp4", #need to create new videos
                                        "ImageType": "video/mp4"
                                    },
                                    "Frame": True
                                }]}]
                        }

                        # Then, create the scenario
                        label = row_1[3]
                        i = uma_groups[group][0]  # index for short scenarios
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
                        else:
                            puzzle_text_2 = row_1[i + 1]  # if there's a second puzzle
                            word_2 = row_1[i + 1].split()[-1][:-1]
                            puzzle_text_2 = rreplace(puzzle_text_2, " " + word_2, "..", 1)
                        comp_question = row_1[i + 2]
                        answers_lst = [row_1[i + 3], row_1[i + 4]]
                        np.random.shuffle(answers_lst)
                        correct_answer = row_1[i + 3]
                        #unique_image = False
                        if label in unique:
                            unique_image = True
                        else:
                            unique_image = False
                        # Create scenario page group for the practice
                        page_group = create_scenario_page_group(domain=domain, label=label, scenario_num=dose1_scenario_num,
                                                                group=group, puzzle_text_1=puzzle_text_1, word_1=word_1,
                                                                comp_question=comp_question, answers_lst=answers_lst,
                                                                correct_answer=correct_answer, word_2=word_2,
                                                                puzzle_text_2=puzzle_text_2,
                                                                unique_image=unique_image, row_num=dose1_scenario_num)

                        lookup[lookup_code]["Anything" + str(dose1_scenario_num)] = page_group
                        if dose1_scenario_num == 0:
                            page_group = {"Name": "Make it your own!",
                                          "Title": "Make it your own!",
                                          "Type": "Survey",
                                          "Pages": [

                                          ]}
                            make_it_your_own_text = "We want Hoos Think Calmly to meet your needs. When you complete " \
                                                    "training sessions in the app or browse resources in the " \
                                                    "on-demand resource library, you’ll notice a button that looks " \
                                                    "like a star on the top right-hand corner of your screen. By " \
                                                    "clicking on the star, you can add the info you find most " \
                                                    "helpful (e.g., short stories, tips for managing stress) to your " \
                                                    "own personal Favorites page. You can then revisit your favorite " \
                                                    "parts of the app whenever you’d like by choosing the Favorites " \
                                                    "tile from the Hoos Think Calmly homepage!"

                            make_it_your_own_page = create_survey_page(text=make_it_your_own_text,
                                                                       title="Make it your own!")
                            page_group["Pages"].append(make_it_your_own_page)

                            lookup[lookup_code]["Anything_MIYO" + str(dose1_scenario_num)] = page_group

                        dose1_scenario_num += 1
                dose1_scenario_num = 0
            else:
                # create survey page
                if row[2]:  # if it's not blank
                    text = row[4].replace("\u2019", "'").replace("\u00e2\u20ac\u2122", "'").replace("\u2013", " - ")\
                        .replace("\u2014", " - ").replace("\u201c", '"').replace("\u201d", '"').replace("\u00e9", "é")\
                        .replace("\\n", "\n").replace("\u2026", "...").replace("\u00e9", "é")
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

    #### Create dose 1 JSON file ####
    file_name = group + "_dose_1.json"
    name = group
    title = "Hoos Think Calmly"
    sections = [
                     {
                         "Name": "dose_1",
                         "Doses": [1],
                         "PageGroups": list(dose_1.values())
                     },
                 ]
    create_json_file(file_name, name=name, title=title, sections=sections)

    ### Create group-specific JSON dict ####
    json_dict = {"Name": group,
                 "Title": "Hoos Think Calmly",
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
                         "CanBeFavorited": True,
                         "Domains": []
                     },
                     {
                         "Name": "AfterDomain",
                         "PageGroups": list(after_domains_dicts.values())
                     }

                 ]}

    with open(r"C:\Users\maddie\Desktop\python\UMA scenarios.csv","r", encoding="utf-8", newline='') as read_obj:
        csv_reader = csv.reader(read_obj)
        next(csv_reader)
        i = uma_groups[group][0] #index for short scenario
        domains_dict = {}
        scenario_num = 0
        page_groups_dict = {}
        titles_list = []
        titles_count = {}

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

        # First, add the discrimination domain because it is different than the others. We use a separate
        # file to create this one
        domains_dict["Discrimination"] = { #adding discrimiation as key with corresponding dictionary value that holds page group
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
        with open(r"C:\Users\maddie\Desktop\python\UMA discrimination.csv", "r", encoding="utf-8") as read_obj:
            discrimination_reader = csv.reader(read_obj)
            next(discrimination_reader)
            for d_row in discrimination_reader:
                title = d_row[0]
                text = d_row[1].replace("\u2019", "'").replace("\u00e2\u20ac\u2122", "'").replace(
                    "\u2013", "--").replace("\u2014", "--").replace("\u00e9", "é")\
                    .replace("\u201c", '"').replace("\u201d", '"').strip().replace("\\n", "\n")  # replace("\\", "\\")
                text = 'Go to the on-demand library to get the links to these resources.\n\n' + text
                input_1 = d_row[2]
                # each group (undergrad, grad, etc.) has slightly different text
                # need to only take the rows that correspond to the given participant group.
                participant_group = d_row[3]  # this is the participant group
                input_name = d_row[15]
                conditions_lst = d_row[14].split('; ')
                items_list = d_row[7].replace("\u2019", "'").replace("\u00e2\u20ac\u2122", "'")\
                    .replace("\u2013", "--").replace("\u2014", "--").replace("\u201c", '"')\
                    .replace("\u201d", '"').replace("\\n", "\n"). \
                    strip().split("; ")
                if group in participant_group:  # checking if it corresponds to the group we're dealing with
                    discrimination_page = create_discrimination_page(conditions_lst=conditions_lst,
                                                                     text=text,
                                                                     items_lst=items_list,
                                                                     input_1=input_1,
                                                                     input_name=input_name,
                                                                     title=title)

                    domains_dict["Discrimination"]["PageGroups"][0]["Pages"].append(discrimination_page) #adding this page info into the empty list value for the discrimination page

        row_num = 1
        current_domain = "Holder"
        for row in csv_reader:
            domain = row[0].strip() #Broad domain 1
            if current_domain != domain and domain not in (
                    None, ""):  # when we change domains, bring row num back to 1 8/29
                # (row[3])
                #print("Domain is...", domain)
                current_domain = domain
                row_num = 1
            # domain_2 = row[1]
            # domain_3 = row[2]
            label = row[3]  # scenario name, Hoos TC title column
            if domain not in (None, "") and domain:  # if there is a domain
                #if label not in titles_count.keys():
                 #       titles_count[label] = 1
                #else:
                 #   titles_count[label] += 1

                ## CREATE scenario pages
                if label not in (None, "") and row[i] not in (None, "") and row[i] != "NA" and row[i] != "N/A" and \
                        "Write Your Own" not in label:  # if it's a scenario that hasn't already been added 3 times
                    if domain not in domains_dict.keys():  # first, create domains. Every time you enter a new domain have to create a new key-value pair
                        domains_dict[domain] = {
                            "Name": domain,
                            "Title": domain,
                            "PageGroups": [] #same set-up as discrimination key-value pair
                        }
                        #if titles_list.count(label) <= 3:  # NEW 6/12
                    #titles_list.append(label)
                    scenario_num += 1 #increase this counter with every scenario
                    puzzle_text_1 = row[i].replace("\u2019", "'").replace("\u00e2\u20ac\u2122", "'")\
                        .replace("\u2013", " - ").replace("\u2014", " - ").replace("\u00e9", "é")\
                        .replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n"). \
                        replace("\u2026", "...").replace(",..", ",") #getting scenario body
                    word_1 = row[i].split()[-1] #getting last word in scenario body
                    if row[i].strip()[-1] == ".":
                        word_1 = row[i].split()[-1][:-1] #if it ends in a period take everything but the period
                    word_2 = None
                    puzzle_text_2 = None
                    puzzle_text_1 = rreplace(puzzle_text_1, " " + word_1, "..", 1) #replacing the last word in scenario body with ...


                    if "N/A" in row[i + 1] or row[i + 1] in (None, ""):
                        pass
                    else:
                        puzzle_text_2 = row[i + 1].replace("\u2019", "'").replace("\u00e2\u20ac\u2122", "'")\
                            .replace("\u2013", " - ").replace("\u2014"," - ").replace("\u00e9", "é")\
                            .replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n"). \
                            replace("\u2026", "...")  # if there's a second scenario body
                        word_2 = row[i + 1].split()[-1][:-1]
                        puzzle_text_2 = rreplace(puzzle_text_2, " " + word_2, "..", 1) #replacing last word with ...
                    comp_question = row[i + 2]
                    answers_lst = [row[i + 3], row[i + 4]]
                    if row[i + 3].strip() == "Yes" or row[i + 3].strip() == "yes":
                        answers_lst.pop() #removing the row[i +4] element and adding No there
                        answers_lst.append("No")
                    if row[i + 3].strip() == "No" or row[i + 3].strip() == "no":
                        answers_lst.pop()
                        answers_lst.append("Yes") #removing the row[i + 4] element and adding Yes there
                    np.random.shuffle(answers_lst) #shuffling them so they're not always in the same order
                    correct_answer = row[i + 3]

                            # get list of words
                    if row[10] not in (None, ""):
                        letters_missing = row[10] #letters missing column

                    lessons_learned = False
                    if (row_num - 1) % 40 == 0 and (
                        row_num - 1) != 0:  # if it's a multiple of 40 and not the first row, we have to add a lessons learned
                        lessons_learned = True
                    if label in unique:
                        unique_image = True
                    else:
                        unique_image = False
                    page_group = create_scenario_page_group(domain=domain, label=label, scenario_num=scenario_num,
                                                            group=group, puzzle_text_1=puzzle_text_1, word_1=word_1,
                                                            comp_question=comp_question, answers_lst=answers_lst,
                                                            correct_answer=correct_answer, word_2=word_2,
                                                            puzzle_text_2=puzzle_text_2,
                                                            letters_missing=letters_missing,
                                                            lessons_learned=lessons_learned,
                                                            unique_image=unique_image,
                                                            row_num=row_num)
                    domains_dict[domain]["PageGroups"].append(page_group) #adding this to the PageGroups list
                        #print(domains_dict[domain]["PageGroups"][0]["Name"]) TEST 6/12
                    if row_num % 10 == 0:  # if it's a multiple of 10, add a resource/tip/ER strategy
                                # new 12/13
                        if group == "UMA":
                            resources_lookup = uma_resources_lookup

                        page_group = create_resource_page_group_new(resources_lookup, tip_lst, ER_lookup, domain) #randomly picks a resource, tip, or strategy page to add
                        domains_dict[domain]["PageGroups"].append(page_group) #adding resource page group to PageGroups list

                    if row_num % 50 == 0:  # if it's a multiple of 50, add a long scenario and a resource
                        if len(long_page_groups[domain]) != 0:  # check to see there are still long scenarios left
                                    # new
                            long_page_group = long_page_groups[domain].pop(0)
                            long_page_groups[domain].append(long_page_group)

                            domains_dict[domain]["PageGroups"].append(long_page_group) #add long page group to PageGroups list
                            if group == "UMA":
                                resources_lookup = uma_resources_lookup

                            page_group = create_resource_page_group_new(resources_lookup, tip_lst, ER_lookup, domain)
                            domains_dict[domain]["PageGroups"].append(page_group)

                    row_num += 1 #bumps the row number after every row used
                if "Write Your Own" in label:
                    row_num += 10 #bump the row by 10 (because the dose size of a long scenario = 10)
                    page_group = {"Name": "Write Your Own",
                                  "Title": "Write Your Own",
                                  "Type": "Survey",
                                  "DoseSize": 10,
                                  "Pages": [

                                  ]}
                    with open(r"C:\Users\maddie\Desktop\python\write_your_own.csv", "r", encoding="utf-8") \
                            as read_obj_wyo:
                        wyo_reader = csv.reader(read_obj_wyo)
                        next(wyo_reader)
                        for wyo_row in wyo_reader:
                            name = wyo_row[0]
                            title = wyo_row[1]
                            if text not in (None, ""):
                                text = wyo_row[4].replace("\u2019", "'").replace("\u00e2\u20ac\u2122", "'")\
                                    .replace("\u2013", " - ").replace("\u2014"," - ").replace("\u00e9", "é")\
                                    .replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2026",
                                                                                                               "...")
                                input = wyo_row[5]
                                input_name = wyo_row[18]
                                page = create_survey_page(text=text, input_1=input, title=title, input_name=input_name)
                                page_group["Pages"].append(page)

                    domains_dict[domain]["PageGroups"].append(page_group)

                    # now add a resource page
                    if group == "UMA":
                        resources_lookup = uma_resources_lookup

                    page_group = create_resource_page_group_new(resources_lookup, tip_lst, ER_lookup, domain)

                    domains_dict[domain]["PageGroups"].append(page_group)
    json_dict["Sections"][1]["Domains"] = list(domains_dict.values())  # HELLO CHANGED FROM 2

    new_json_dict = uma_groups[group][2]
    json_file = group + ".json"
    with open(json_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)  # data instead of json_dict


#### Now, create each additional json file that are not group-specific ####

## Create end of day survey
file_name = "UMA_EOD.json"
name = "Nightly Survey"
title = "Nightly Survey"
sections = [
    {
        "Name": "Nightly Survey",
        "PageGroups": list(end_of_day.values())
    }
]
create_json_file(file_name, name=name, title=title, sections=sections)

## Create biweekly survey
# "Dose by section" means that each section is considered a "dose." The app will therefore
# skip from section to section every 2 weeks (this timeframe is set by Ben)
file_name = "UMA_Biweekly.json"
name = "Track Your Progress"
title = "Track Your Progress"
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
create_json_file(file_name, name, title, sections, dose_by_section=dose_by_section)

## Create biweekly survey for control (non-intervention) participants
file_name = "UMA_Biweekly_control.json"
name = "Track Your Progress"
title = "Track Your Progress"
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
create_json_file(file_name, name, title, sections, dose_by_section=dose_by_section)

## Create the first dose file for control
file_name = "Dose1_control.json"
name = "Dose 1"
title = "Get started!"
sections = [{"Name": "Dose 1",
             "PageGroups": list(control_dose_1.values())
             }]
create_json_file(file_name, name, title, sections)

## Create reasons for ending file
file_name = "UMA_ReasonsForEnding.json"
name = "Reasons for Ending"
title = "Reasons for Ending"
cancel_button_text = "Exit"
sections = [{
    "Name": "Reasons For Ending",
    "PageGroups": list(reasons.values())
}]
create_json_file(file_name, name, title, sections, cancel_button_text=cancel_button_text)


