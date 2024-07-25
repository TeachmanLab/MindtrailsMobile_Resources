import csv
import json
import random

import numpy as np

from MTSpanish_create_pages import create_discrimination_page
from MTSpanish_create_pages import create_json_file
from MTSpanish_create_pages import create_scenario_page_group
from MTSpanish_create_pages import create_survey_page, create_resource_page_group_new, create_long_scenario_page_group
from MTSpanish_helpers import rreplace, get_resources, get_ER, get_tips

spanish_resources_lookup = get_resources(file_path="/Users/valentinamendoza/Downloads/MT Spanish/Spanish_Resources.csv") #8/9  # changed
spanish_json = {} #8/9  # changed
spanish_groups = {   # changed
    "Español": [4, 4, spanish_json] # changed
}

for group in spanish_groups.keys():  # changed
    ER_lookup = get_ER(file_path="/Users/valentinamendoza/Downloads/MT Spanish/ER_Strategies.csv")
    tip_lst = get_tips(file_path="/Users/valentinamendoza/Downloads/MT Spanish/tips.csv")

    long_page_groups ={  # changed
        "Situaciones Sociales": [],
        "Salud Física": [],
        "Académicos/Trabajo/Desarrollo Profesional": [],
        "Vida Familiar y Doméstica": [],
        "Finanzas": [],
        "Salud Mental": [],
        "Relaciones Románticas": [],
    }

    with open("/Users/valentinamendoza/Downloads/MT Spanish/Spanish_Long_Scenarios.csv", "r",encoding="utf-8") as read_file:
        reader = csv.reader(read_file)
        next(reader)  # skip line 1
        next(reader)  # skip line 2
        i = spanish_groups[group][1]  # 4  # changed
        for row in reader:
            if not row or all(field.strip() == '' for field in row):  # Skip empty lines
                continue
            if len(row) > max(i + 16, 3):  # Ensure the row has enough columns
                domain = row[0].strip()
                domain_2 = row[1]
                label = row[3]
                scenario_description = row[i]
                thoughts_lst = [row[i + 2], row[i + 3], row[i + 4], row[i + 5], row[i + 6]]
                feelings_lst = [row[i + 7], row[i + 8], row[i + 9], row[i + 10], row[i + 11]]
                behaviors_lst = [row[i + 12], row[i + 13], row[i + 14], row[i + 15], row[i + 16]]
                # check if the images across all groups all the same (this changes the image url)
                unique_image = False

                print("Label:", label, "IS NOT unique")

                if scenario_description not in (None, "", "NA", "N/A") and label not in (None, ""):
                    # create long scenario page group
                    page_group = create_long_scenario_page_group(label=label, scenario_description=scenario_description,
                                                                 unique_image=unique_image, thoughts_lst=thoughts_lst,
                                                                 feelings_lst=feelings_lst, behaviors_lst=behaviors_lst)
                    long_page_groups[domain].append(page_group)  # add page group to correct domain's list
                    if domain_2 not in (
                    None, ""):  # if it also belongs to a second domain, add the page group to that list
                        long_page_groups[domain_2].append(page_group)

            else:
                print(f"Skipping incomplete row: {row}")

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
              "Biweekly_Semana 2": biweekly_2,
              "Biweekly_Semana 4": biweekly_4,
              "Biweekly_Semana 6": biweekly_6,
              "Biweekly_Semana 8": biweekly_8,
              "Biweekly_Control_Semana 2": biweekly_2_control,
              "Biweekly_Control_Semana 4": biweekly_4_control,
              "Biweekly_Control_Semana 6": biweekly_6_control,
              "Biweekly_Control_Semana 8": biweekly_8_control,
              "ReasonsForEnding_All": reasons
              }
    scenario_dicts = {}

    # Open the file with all the content
    with open("/Users/valentinamendoza/Downloads/MT Spanish/MTSpanish_survey_questions.csv", "r", encoding="utf-8") as read_obj:
        reader = csv.reader(read_obj)
        next(reader)  # skip first line
        for row in reader:  # each row is a page
            lookup_code = row[3] + "_" + row[2]
            if row[0] == "Práctica de CBM-I": # changed
                # In the special case that it's "Practice CBM-I", then we have to create scenarios

                with open("/Users/valentinamendoza/Downloads/MT Spanish/Spanish_dose1_scenarios.csv", "r", encoding="utf-8") as dose1_read_obj:  # scenarios for first dose in file
                    dose1_reader = csv.reader(dose1_read_obj)
                    next(dose1_reader)
                    dose1_scenario_num = 0
                    for row_1 in dose1_reader:
                        # First, add the video that goes before each scenario
                        lookup[lookup_code]["Video" + str(dose1_scenario_num)] = {
                            "Name": "Video " + str(dose1_scenario_num + 1),
                            "Pages": [{
                                "Inputs": [{ "Type": "Text",
                                              "Parameters": {
                                                    "Text": "¡Presione play en el video de entrenamiento a continuación para obtener más información!"
                                                    }},
                                    {
                                    "Type": "Media",
                                    "Parameters": {
                                        "ImageUrl": "https://github.com/TeachmanLab/MindtrailsMobile_Resources/raw"
                                                    "/main/HTC/protocols/protocol1/media/videos/Staff/video" +
                                                    str(dose1_scenario_num + 1) + ".mp4", #need to create new videos for MT Spanish
                                        "ImageType": "video/mp4"
                                    },
                                    "Frame": True
                                }]}]
                        }

                        # Then, create the scenario
                        label = row_1[3]
                        i = spanish_groups[group][0]  # index for short scenarios
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
                        unique_image = False

                        # Create scenario page group for the practice
                        page_group = create_scenario_page_group(domain=domain, label=label, scenario_num=dose1_scenario_num,
                                                                puzzle_text_1=puzzle_text_1, word_1=word_1,
                                                                comp_question=comp_question, answers_lst=answers_lst,
                                                                correct_answer=correct_answer, word_2=word_2,
                                                                puzzle_text_2=puzzle_text_2, unique_image=unique_image,
                                                                 row_num=dose1_scenario_num)

                        lookup[lookup_code]["Anything" + str(dose1_scenario_num)] = page_group  # change?
                        if dose1_scenario_num == 0:
                            page_group = {"Name": "Make it your own!",
                                          "Title": "¡Hazlo tuyo!",  # changed
                                          "Type": "Survey",
                                          "Pages": [

                                          ]}
                            make_it_your_own_text =  "Queremos que MindTrails Español satisfaga sus necesidades. Cuando complete " \
                                                     "sesiones de capacitación en la aplicación o buscar recursos en " \
                                                     "biblioteca de recursos bajo demanda, verá un botón que parece " \
                                                     "como una estrella en la esquina superior derecha de la pantalla. Por " \
                                                     "haciendo clic en la estrella, puedes agregar la información que más te parezca " \
                                                     "útil (por ejemplo, historias cortas, consejos para controlar el estrés) para su " \
                                                     "propia página personal de Favoritos. Luego podrás volver a visitar tu favorito " \
                                                     "partes de la aplicación cuando quieras eligiendo Favoritos " \
                                                     "¡mosaico de la página de inicio de MindTrails Español!"  # changed

                            make_it_your_own_page = create_survey_page(text=make_it_your_own_text,
                                                                       title="¡Hazlo tuyo!")  # changed
                            page_group["Pages"].append(make_it_your_own_page)

                            lookup[lookup_code]["Anything_MIYO" + str(dose1_scenario_num)] = page_group

                        dose1_scenario_num += 1
                dose1_scenario_num = 0
            else:
                # create survey page
                if row[2]:  # if it's not blank
                    text = row[4].replace("\u00e2\u20ac\u2122", "'").replace("\u2026", "...").replace("\u2013", " - ").replace("\u2014", " - ").replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2019", "'").replace("\u00e1", "á").replace("\u00e9", "é").replace("\u00ed", "í").replace("\u00f3", "ó").replace("\u00fa", "ú").replace(u'\xf1', 'n').replace("\u00fc", "ü").replace("\u00c1", "Á").replace("\u00c9", "É").replace("\u00cd", "Í").replace("\u00d3", "Ó").replace("\u00da", "Ú").replace("\u00d1", "Ñ").replace("\u00dc", "Ü").replace("  ", " ")


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
    title = "MindTrails Español"   # changed
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
                 "Title": "MindTrails Español",  # changed
                 "DoseSize": 11,
                 "Sections": [
                     {
                         "Name": "BeforeDomain_All",
                         "PageGroups": list(before_domains_dicts.values())
                     },
                     {
                         "Name": "Domains",
                         "Description":  "Los dominios enumerados aquí son algunas áreas que pueden hacerte sentir "
                                         "ansioso. Seleccione en qué le gustaría trabajar durante el día de hoy"
                                         "formación. \n\nTe animamos a elegir diferentes dominios para practicar "
                                         "¡Pensar con flexibilidad en todas las áreas de tu vida!",
                         "CanBeFavorited": True,
                         "Domains": []
                     },
                     {
                         "Name": "AfterDomain",
                         "PageGroups": list(after_domains_dicts.values())
                     }

                 ]}

    with open("/Users/valentinamendoza/Downloads/MT Spanish/Spanish_Short_Scenarios.csv","r", encoding="utf-8", newline='') as read_obj:
        csv_reader = csv.reader(read_obj)
        next(csv_reader)
        i = spanish_groups[group][0] #index for short scenario
        domains_dict = {}
        scenario_num = 0
        page_groups_dict = {}
        titles_list = []
        titles_count = {}

        domains_lookup = {   # changed
            "Situaciones Sociales": [{}, 0],
            "Salud Física": [{}, 0],
            "Académicos/Trabajo/Desarrollo Profesional": [{}, 0],
            "Vida Familiar y Doméstica": [{}, 0],
            "Finanzas": [{}, 0],
            "Salud Mental": [{}, 0],
            "Relaciones Románticas": [{}, 0]
        }

        # First, add the discrimination domain because it is different than the others. We use a separate
        # file to create this one
        domains_dict["Discrimination"] = { #adding discrimiation as key with corresponding dictionary value that holds page group
            "Name": "Discrimination",
            "Title": "Discriminación",   # changed
            "PageGroups": [{
                "Name": "Discrimination",
                "Title": "Discriminación",   # changed
                "Type": "Discrimination",
                "DoseSize": 11,
                "Pages": []
            }]
        }
        with open("/Users/valentinamendoza/Downloads/MT Spanish/Discrimination.csv", "r", encoding="utf-8") as read_obj:
            discrimination_reader = csv.reader(read_obj)
            next(discrimination_reader)
            for d_row in discrimination_reader:
                title = d_row[0]
                text = d_row[1].replace("\u00e2\u20ac\u2122", "'").replace("\u2026", "...").replace("\u2013", " - ").replace("\u2014", " - ").replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'").replace("\u00e1", "á").replace("\u00e9", "é").replace("\u00ed", "í").replace("\u00f3", "ó").replace("\u00fa", "ú").replace(u'\xf1', 'n').replace("\u00fc", "ü").replace("\u00c1", "Á").replace("\u00c9", "É").replace("\u00cd", "Í").replace("\u00d3", "Ó").replace("\u00da", "Ú").replace("\u00d1", "Ñ").replace("\u00dc", "Ü").replace("  ", " ").strip().replace("\\n", "\n")
                text = 'Vaya a la libreria de recursos disponibles los enlaces a estos recursos.\n\n' + text
                input_1 = d_row[2]
                # each group (undergrad, grad, etc.) has slightly different text
                # need to only take the rows that correspond to the given participant group.
                participant_group = d_row[3]  # this is the participant group
                input_name = d_row[15]
                conditions_lst = d_row[14].split('; ')
                items_list = d_row[7].replace("\u00e2\u20ac\u2122", "'").replace("\u2026", "...").replace("\u2013", " - ").replace("\u2014", " - ").replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2019", "'").replace("\u00e1", "á").replace("\u00e9", "é").replace("\u00ed", "í").replace("\u00f3", "ó").replace("\u00fa", "ú").replace(u'\xf1', 'n').replace("\u00fc", "ü").replace("\u00c1", "Á").replace("\u00c9", "É").replace("\u00cd", "Í").replace("\u00d3", "Ó").replace("\u00da", "Ú").replace("\u00d1", "Ñ").replace("\u00dc", "Ü").replace("  ", " ").strip().split("; ")
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
                        "Write Your Own" not in label:  # if it's a scenario that hasn't already been added 3 times # changed?
                    if domain not in domains_dict.keys():  # first, create domains. Every time you enter a new domain have to create a new key-value pair
                        domains_dict[domain] = {
                            "Name": domain,
                            "Title": domain,
                            "PageGroups": [] #same set-up as discrimination key-value pair
                        }
                        #if titles_list.count(label) <= 3:  # NEW 6/12
                    #titles_list.append(label)
                    scenario_num += 1 #increase this counter with every scenario
                    puzzle_text_1 = row[i].replace("\u00e2\u20ac\u2122", "'").replace("\u2026", "...").replace("\u2013", " - ").replace("\u2014", " - ").replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2019", "'").replace("\u00e1", "á").replace("\u00e9", "é").replace("\u00ed", "í").replace("\u00f3", "ó").replace("\u00fa", "ú").replace(u'\xf1', 'n').replace("\u00fc", "ü").replace("\u00c1", "Á").replace("\u00c9", "É").replace("\u00cd", "Í").replace("\u00d3", "Ó").replace("\u00da", "Ú").replace("\u00d1", "Ñ").replace("\u00dc", "Ü").replace("  ", " ").replace(",..", ",")
                    word_1 = row[i].split()[-1] #getting last word in scenario body
                    if row[i].strip()[-1] == ".":
                        word_1 = row[i].split()[-1][:-1] #if it ends in a period take everything but the period
                    word_2 = None
                    puzzle_text_2 = None
                    puzzle_text_1 = rreplace(puzzle_text_1, " " + word_1, "..", 1) #replacing the last word in scenario body with ...


                    if "N/A" in row[i + 1] or row[i + 1] in (None, ""):
                        pass
                    else:
                        puzzle_text_2 = row[i + 1].replace("\u00e2\u20ac\u2122", "'").replace("\u2026", "...").replace("\u2013", " - ").replace("\u2014", " - ").replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2019", "'").replace("\u00e1", "á").replace("\u00e9", "é").replace("\u00ed", "í").replace("\u00f3", "ó").replace("\u00fa", "ú").replace(u'\xf1', 'n').replace("\u00fc", "ü").replace("\u00c1", "Á").replace("\u00c9", "É").replace("\u00cd", "Í").replace("\u00d3", "Ó").replace("\u00da", "Ú").replace("\u00d1", "Ñ").replace("\u00dc", "Ü").replace("  ", " ")
                        word_2 = row[i + 1].split()[-1][:-1]
                        puzzle_text_2 = rreplace(puzzle_text_2, " " + word_2, "..", 1) #replacing last word with ...
                    comp_question = row[i + 2]
                    answers_lst = [row[i + 3], row[i + 4]]
                    if row[i + 3].strip() == "Si" or row[i + 3].strip() == "si":   # changed
                        answers_lst.pop() #removing the row[i +4] element and adding No there
                        answers_lst.append("No")
                    if row[i + 3].strip() == "No" or row[i + 3].strip() == "no":
                        answers_lst.pop()
                        answers_lst.append("Si") #removing the row[i + 4] element and adding Yes there  # changed
                    np.random.shuffle(answers_lst) #shuffling them so they're not always in the same order
                    correct_answer = row[i + 3]

                            # get list of words
                    if row[10] not in (None, ""):
                        letters_missing = row[10] #letters missing column

                    lessons_learned = False
                    if (row_num - 1) % 40 == 0 and (
                        row_num - 1) != 0:  # if it's a multiple of 40 and not the first row, we have to add a lessons learned
                        lessons_learned = True
                    unique_image = False

                    page_group = create_scenario_page_group(domain=domain, label=label, scenario_num=scenario_num,
                                                            puzzle_text_1=puzzle_text_1, word_1=word_1,
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
                        if group == "Español":
                            resources_lookup = spanish_resources_lookup

                        page_group = create_resource_page_group_new(resources_lookup, tip_lst, ER_lookup, domain) #randomly picks a resource, tip, or strategy page to add
                        domains_dict[domain]["PageGroups"].append(page_group) #adding resource page group to PageGroups list

                    if row_num % 50 == 0:  # if it's a multiple of 50, add a long scenario and a resource
                        if len(long_page_groups[domain]) != 0:  # check to see there are still long scenarios left
                                    # new
                            long_page_group = long_page_groups[domain].pop(0)
                            long_page_groups[domain].append(long_page_group)

                            domains_dict[domain]["PageGroups"].append(long_page_group) #add long page group to PageGroups list
                            if group == "Español":
                                resources_lookup = spanish_resources_lookup

                            page_group = create_resource_page_group_new(resources_lookup, tip_lst, ER_lookup, domain)
                            domains_dict[domain]["PageGroups"].append(page_group)

                    row_num += 1 #bumps the row number after every row used
                if "Write Your Own" in label:
                    row_num += 10 #bump the row by 10 (because the dose size of a long scenario = 10)
                    page_group = {"Name": "Write Your Own",
                                  "Title": "Escribe El tuyo",  # changed
                                  "Type": "Survey",
                                  "DoseSize": 10,
                                  "Pages": [

                                  ]}
                    with open("/Users/valentinamendoza/Downloads/MT Spanish/Spanish_write_your_own.csv", "r", encoding="utf-8") \
                            as read_obj_wyo:
                        wyo_reader = csv.reader(read_obj_wyo)
                        next(wyo_reader)
                        for wyo_row in wyo_reader:
                            name = wyo_row[0]
                            title = wyo_row[1]
                            if text not in (None, ""):
                                text = wyo_row[4].replace("\u00e2\u20ac\u2122", "'").replace("\u2026", "...").replace("\u2013", " - ").replace("\u2014", " - ").replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2019", "'").replace("\u00e1", "á").replace("\u00e9", "é").replace("\u00ed", "í").replace("\u00f3", "ó").replace("\u00fa", "ú").replace(u'\xf1', 'n').replace("\u00fc", "ü").replace("\u00c1", "Á").replace("\u00c9", "É").replace("\u00cd", "Í").replace("\u00d3", "Ó").replace("\u00da", "Ú").replace("\u00d1", "Ñ").replace("\u00dc", "Ü").replace("  ", " ")

                                input = wyo_row[5]
                                input_name = wyo_row[18]
                                page = create_survey_page(text=text, input_1=input, title=title, input_name=input_name)
                                page_group["Pages"].append(page)

                    domains_dict[domain]["PageGroups"].append(page_group)

                    # now add a resource page
                    if group == "Español":
                        resources_lookup = spanish_resources_lookup

                    page_group = create_resource_page_group_new(resources_lookup, tip_lst, ER_lookup, domain)

                    domains_dict[domain]["PageGroups"].append(page_group)
    json_dict["Sections"][1]["Domains"] = list(domains_dict.values())  # HELLO CHANGED FROM 2

    new_json_dict = spanish_groups[group][2]
    json_file = group + ".json"
    with open(json_file, 'w', encoding='utf-8') as outfile:
        json.dump(json_dict, outfile, indent=4, ensure_ascii=False)  # data instead of json_dict


#### Now, create each additional json file that are not group-specific ####

## Create end of day survey
file_name = "Spanish_EOD.json"
name = "Nightly Survey"
title = "Encuesta Nocturna"  # changed
sections = [
    {
        "Name": "Nightly Survey",  # change?
        "PageGroups": list(end_of_day.values())
    }
]
create_json_file(file_name, name=name, title=title, sections=sections)

## Create biweekly survey
# "Dose by section" means that each section is considered a "dose." The app will therefore
# skip from section to section every 2 weeks (this timeframe is set by Ben)
file_name = "Spanish_Biweekly.json"
name = "Follow Your Progress"
title = "Sigue Tu Progreso"  # changed
dose_by_section = True
sections = [
    {
        "Name": "Sigue Tu Progreso - Semana 2", # changed?
        "PageGroups": list(biweekly.values()) + list(biweekly_2.values())
    },
    {
        "Name": "Sigue Tu Progreso - Semana 4",
        "PageGroups": list(biweekly.values()) + list(biweekly_4.values())
    },
    {
        "Name": "Sigue Tu Progreso - Semana 6",
        "PageGroups": list(biweekly.values()) + list(biweekly_6.values())
    },
    {
        "Name": "Sigue Tu Progreso - Semana 8",
        "PageGroups": list(biweekly.values()) + list(biweekly_8.values())
    }
]
create_json_file(file_name, name, title, sections, dose_by_section=dose_by_section)



# Create reasons for ending file
file_name = "Spanish_ReasonsForEnding.json"
name = "Reasons For Ending"
title = "Razones Para Terminar"  # changed
cancel_button_text = "Salir"  # changed
sections = [{
    "Name": "Reasons For Ending",  # change?
    "PageGroups": list(reasons.values())
}]
create_json_file(file_name, name, title, sections, cancel_button_text=cancel_button_text)

