import csv
import json
import random

from MTSpanish_helpers import get_lessons_learned_text

file_path = "/Users/valentinamendoza/Downloads/MT Spanish/Spanish lessons_learned_text.csv"

lessons_learned_dict = get_lessons_learned_text(file_path)


def create_long_scenario_page_group(label, scenario_description, unique_image, thoughts_lst, feelings_lst, behaviors_lst):
    """

    :param unique_image: Bool, False means that the photos for each group are all the same
    :param label: The title of the long scenario
    :param scenario_description: The text for the scenario
    :param thoughts_lst: list of thoughts to show for long scenarios
    :param feelings_lst: list of feelings to show for long scenarios
    :param behaviors_lst: list of behaviors to show for long scenarios
    :return: a page group for the long scenario
    """
    page_group = {"Name": "Long Scenario: " + label.strip(),
                  "Title": "Escenario Largo: " + label.strip(),  # changed
                  "Type": "Scenario",
                  "DoseSize": 10,  # dose size is 10 because for microdoses with a long scenario, we
                  # just show one long scenario & one resource (DoseSize=1)
                  "Pages": [

                  ]}

    # This CSV has the generic structure for each long scenario page group.
    # We will change Scenario_Name and [Scenario_Description]
    with open("/Users/valentinamendoza/Downloads/MT Spanish/Spanish htc_long_scenarios_structure.csv",
              "r", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # skipping first line
        for row_str in csv_reader:
            label_str = row_str[0].replace("[Scenario_Name]",
                                           label)  # replacing [scenario_name] with the parameter that is the title of the long scenario
            text = row_str[4].replace("[Scenario_Description]", scenario_description).replace("\u2013", " - ").replace("\u2014", " - ").replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u2019", "'").replace("\u00e1", "á").replace("\u00e9", "é").replace("\u00ed", "í").replace("\u00f3", "ó").replace("\u00fa", "ú").replace(u'\xf1', 'n').replace("\u00fc", "ü").replace("\u00c1", "Á").replace("\u00c9", "É").replace("\u00cd", "Í").replace("\u00d3", "Ó").replace("\u00da", "Ú").replace("\u00d1", "Ñ").replace("\u00dc", "Ü").replace("  ", " ")


            # replacing the text in the csv with the parameter for the scenario description
            input_1 = row_str[6]
            input_2 = row_str[7]
            image_bool = row_str[10]
            if image_bool == "TRUE":
                image_bool = True  # only 1 row has this set as TRUE

            if unique_image:
                image_url = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/tree/main/HTC/protocols/Spanish/media/images" + label.strip().replace(
                    " ", "_") + ".jpeg"
            else:
                image_url = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/tree/main/HTC/protocols/Spanish/media/images" + label.strip().replace(
                    " ", "_") + ".jpeg"

            if image_bool:  # if image_bool is true, add a page with 2 inputs, one for the text and one for the image
                page = {
                    "Name": label.strip(),
                    "Title": label_str,
                    "Inputs": [{
                        "Type": "Text",
                        "Parameters": {
                            "Text": text
                        }
                    },
                        {
                            "Type": "Media",
                            "Frame": True,
                            "Parameters": {
                                "ImageUrl": image_url,
                                "ImageType": "image/jpeg"
                            }
                        }]
                }
            else:  # if there is no image then just add a page with a text input
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
                page["Timeout"] = int(row_str[13])  # changing the string number from the csv to an int
                page["ShowButtons"] = "AfterTimeout"  # adding these items to the page dictionary

            # if there's an entry
            if "Entry" in input_1:
                page["Inputs"].append({  # adding the entry as an input in the page dictionary
                    "Type": "Entry",
                    "Name": row_str[0].replace("[Scenario_Name]: ", label + "_")
                })
            # if there's timedtext
            if input_1 == "TimedText":
                page["ShowButtons"] = "WhenCorrect"
                if "pensamientos" in text:  # changed
                    page["Inputs"].append({
                        "Type": "TimedText",
                        "Parameters": {
                            "Text": thoughts_lst,  # corresponds to thoughts in csv
                            "Duration": 15
                        }
                    })
                elif "sentimientos" in text:  # changed
                    random.shuffle(feelings_lst)
                    page["Inputs"].append({
                        "Type": "TimedText",
                        "Parameters": {
                            "Text": feelings_lst,
                            "Duration": 15
                        }
                    })
                elif "comportamientos" in text:  # changed
                    random.shuffle(behaviors_lst)
                    page["Inputs"].append({
                        "Type": "TimedText",
                        "Parameters": {
                            "Text": behaviors_lst,
                            "Duration": 15
                        }
                    })

            image_bool = False
            page_group["Pages"].append(
                page)  # adding the page you just created to the pages list within the page_group dictionary
    return page_group


# adds a scenario page group to scenario_list (which is passed in)
def create_scenario_page_group(domain, label, scenario_num, puzzle_text_1, word_1,
                               comp_question, answers_lst, correct_answer, unique_image, row_num, word_2=None,
                               puzzle_text_2=None,
                               letters_missing=1, lessons_learned=False, lessons_learned_dict=lessons_learned_dict):
    """
    :param unique_image: Bool, False means that the photos for each group are all the sameunique
    :param domain: domain (e.g., "Romantic Relationships" or "Physical Health")
    :param label:
    :param scenario_num:
    :param puzzle_text_1: text for the first puzzle
    :param word_1: missing word for the first puzzle
    :param comp_question: comprehension question
    :param answers_lst: list of possible answers to the comprehension question
    :param correct_answer: correct answer from answers_lst
    :param row_num:
    :param word_2: missing word for the second puzzle
    :param puzzle_text_2: text for the second puzzle
    :param letters_missing:
    :param lessons_learned:
    :param lessons_learned_dict:
    :return:
    """

    if lessons_learned:  # if it should include a "lessons learned" page
        scenario_list = [{  # create list of dictionaries, starting with lessons learned page. Each dictionary is a page
            "Name": "Lessons Learned" + str(row_num),
            "Title": "Lecciones Aprendidas",  # changed
            "Inputs": [{
                "Type": "Text",
                "Parameters": {
                    "Text": lessons_learned_dict[domain].replace("\u2019", "'").replace("\u00e2\u20ac\u2122", "'").replace("\u2013", "--").replace("\u2014", "--").replace("\u201c", '"').replace("\u201d", '"').replace("\\n", "\n").replace("\u00f4", "ô").replace("\u00e1", "á").replace("\u00e9", "é").replace("\u00ed", "í").replace("\u00f3", "ó").replace("\u00fa", "ú").replace(u'\xf1', 'n').replace("\u00fc", "ü").replace("\u00c1", "Á").replace("\u00c9", "É").replace("\u00cd", "Í").replace("\u00d3", "Ó").replace("\u00da", "Ú").replace("\u00d1", "Ñ").replace("\u00dc", "Ü").strip()

                }

            }, {
                "Type": "Entry",
                "Name": "lessons_learned_" + domain + "_" + str(scenario_num)
            }
            ]
        }]
    else:
        scenario_list = []  # create an empty list, this will eventually be a list of dictionaries (scenarios)
    if letters_missing == "all" and (int(row_num) - 1) % 10 == 0:
        # if all letters missing, and it's the first scenario, add an instructions page to
        scenario_list.append({
            "Name": label + " Instructions",
            "Title": "Instrucciones",  # changed
            "Inputs": [{
                "Type": "Text",
                "Parameters": {
                    "Text": "Las historias que estás a punto de ver son un poco diferentes a las que has visto"
                            "visto antes. En lugar de completar las letras que faltan para completar la palabra final,"
                            "Vamos a desafiarte a generar tu propia última palabra que completará"
                            "la historia. Tu objetivo es pensar en una palabra que terminará la historia en un "
                            "nota positiva. El final no tiene por qué ser tan positivo como para no serlo"
                            "Parece posible, pero queremos que imagines que estás manejando bien la situación."
                    # changed
                }
            }]
        })

    if unique_image:
        image_url = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/tree/main/HTC/protocols/Spanish/media/images" + label.strip().replace(" ", "_") + ".jpeg"
    else:
        image_url = "https://github.com/TeachmanLab/MindtrailsMobile_Resources/tree/main/HTC/protocols/Spanish/media/images" + label.strip().replace(" ", "_") + ".jpeg"

    scenario_list.append({  # adding the image page
        "Name": label + str(row_num),
        "Inputs": [{
            "Type": "Label",
            "Parameters": {
                "Text": label,
                "Framed": True,
            }
        },
            {
                "Type": "Media",
                "Parameters": {
                    "ImageUrl": image_url,
                    "ImageType": "image/jpeg"
                },
                "Frame": True
            }]
    })
    scenario_list.append({  # adding the puzzle page
        "Name": "Puzzle",
        "Inputs": [{
            "Type": "Text",
            "Parameters": {"Text": puzzle_text_1}
        },
            {
                "Type": "WordPuzzle",
                "Name": label + "_" + domain + "_puzzle",
                "CorrectFeedback": "Correcto!",  # changed
                "IncorrectFeedback": "¡Vaya! Eso no parece correcto. Por favor, espere un momento "
                                     "y intenta de nuevo.",  # changed
                "CorrectScore": 0.5,
                "IncorrectDelay": 5000,
                "CauseNavigation": True,
                "Parameters": {
                    "Words": [word_1]
                }
            }]
    })
    if letters_missing == "1" or letters_missing == "2":
        if lessons_learned:  # if it should include a lessons learned page
            new_index = 2
        else:
            new_index = 1
        scenario_list[new_index]["Inputs"][1]["Parameters"]["MissingLetterCount"] = int(letters_missing)
    elif letters_missing == "all":
        # change second input of the second page to be an entry, not a word puzzle
        if (int(row_num) - 1) % 10 == 0:  # if it's the first scenario
            if lessons_learned == True:  # if there is a lessons learned page
                new_index = 3  # 2
            else:
                new_index = 2  # 1
        else:
            if lessons_learned == True:
                new_index = 2  # 2
            else:
                new_index = 1  # 1
        scenario_list[new_index]["Inputs"] = [{  # overwritting the old inputs to have an entry not word puzzle
            "Type": "Text",
            "Parameters": {"Text": puzzle_text_1}
        },
            {
                "Type": "Entry",
                "Name": label + "_" + domain + "_entry"
            }
        ]
    if word_2 not in (None, "", "NA") and puzzle_text_2 not in (
    None, "", "NA"):  # if there is a second word add this page
        scenario_list.append({
            "Name": "Puzzle 2",
            "Inputs": [{
                "Type": "Text",

                "Parameters": {"Text": puzzle_text_2}
            },
                {
                    "Type": "WordPuzzle",
                    "Name": label + "_" + domain + "_puzzle_word2",
                    "CorrectFeedback": "Correcto!",  # changed
                    "IncorrectFeedback": "¡Vaya! Eso no parece correcto. Por favor, espere un momento "
                                         "y intenta de nuevo.",  # changed
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
                    "CorrectFeedback": "Correcto!",  # changed
                    "IncorrectFeedback": "¡Vaya! Eso no parece correcto. Por favor, espere un momento "
                                         "y intenta de nuevo.",  # changed
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

    return page_group


def create_resource_page_group_new(resources_lookup, tip_lst, ER_lookup, domain):
    """
    Create a resource page group (Resource, ER strategy, or Tip)
    :param resources_lookup: Object created by get_resources()
    :param tip_lst: List created by get_tips()
    :param ER_lookup: Object created by get_ER()
    :param domain: the domain
    :return: a page group for a resource, ER strategy, or tip
    """
    choices = ["Recursos", "Consejo", "RE"]  # changed?
    resource_type = random.choices(choices, weights=(33, 33, 33), k=1)  # randomly choose one resource type
    if resource_type[0] == "Recursos":  # if you get a resource # changed
        label = resources_lookup[domain][1][0][0]  # resource name
        text = resources_lookup[domain][1][0][1]  # associated resource text
        resources_lookup[domain][1].pop(0)  # pop from front
        resources_lookup[domain][1].append([label, text])  # place at back
        text = label + "\n\n" + text
    elif resource_type[0] == "Consejo":  # changed
        tip = tip_lst.pop(0)  # pop the first list within the lists out of tip_lst
        label = tip[0]  # tip number
        text = tip[1]  # text with that tip
        tip_lst.append(tip)  # adding that tip back to the end of the list
    elif resource_type[0] == "RE":  # changed
        RE = ER_lookup[domain][1].pop(0)  # popping the first list of lists
        label = RE[0]  # resource
        text = RE[1]  # text
        ER_lookup[domain][1].append(RE)  # adding it back to the end of the list of lists
    resource = [{
        "Name": label,
        "Title": "Recurso: " + domain,  # changed
        # "CanBeFavorited": True, # 12/20
        "Inputs": [{
            "Type": "Text",
            "Parameters": {
                "Text": text,
            }
        }]
    }]
    if resource_type[0] == "Consejo":  # this applies to everyone # changed
        resource[0]["Title"] = "Aplicar a la vida diaria: ¡Haz que funcione para ti!"  # changed
        resource[0]["Inputs"].append({"Type": "Entry",
                                      "Name": label + "_entry"})  # adding another input
        resource[0]["Name"] = "¡Consejo para aplicar!"
    elif resource_type[0] == "RE":  # changed
        resource[0]["Title"] = "Maneja tus sentimientos: " + domain  # domain name  # changed
        resource[0]["Name"] = "Consejo para la regulación de las emociones"  # changed

    page_group = {
        "Name": "Resource/Tip/ER",
        "Title": "Recurso/Consejo/RE",  # changed
        "Type": "Resource/Tip/ER",
        "DoseSize": 1,
        "Pages": resource,
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
                    val = int(each)  # convert each string to an int
                    new_value.append(val)  # add each int to the empty list
                except:
                    pass
        else:
            new_value = value

        page_dict = {
            "Conditions": [
                {
                    "VariableName": conditions_lst[0].strip(),
                    "Value": new_value  # comes from conditions_lst[1]
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
               "VariableName": conditions_lst[0].strip(),
               "Parameters": {
                   "Buttons": items_lst,
                   "Selectable": True,
                   "AllowMultipleSelections": True
               }}
        add["Parameters"]["Buttons"] = items_lst
        page_dict["Inputs"].append(add)  # adding another input dictionary to the inputs list
    if input_1 == "Entry":
        add = {"Type": "Entry",
               "Name": input_name}
        page_dict["Inputs"].append(add)  # adding another input dictionary to the inputs list

    return page_dict


def create_survey_page(text=None, media=None, image_framed=None, items=None, input_1=None, input_2=None,
                       variable_name=None, title=None, input_name=None, minimum=None, maximum=None,
                       show_buttons=None, conditions_lst=None, timeout=None):
    """
    This function creates a page with a survey question.
    :param text: Text to go on the page
    :param media: Link to image or video that should be shown on that page
    :param image_framed: True/False if the image should be framed in the middle of the page (as opposed to taking up the entire screen)
    :param items: Options for buttons, or other text options ("OtherChoices") for slider questions (usually 'Prefer not to answer')
    :param input_1:  Buttons, Picker, Checkbox, Puzzle, Entry, Slider, Scheduler
    :param input_2: Second input on the page:  Buttons, Picker, Checkbox, Puzzle, Entry, Slider, Scheduler
    :param variable_name: If later pages being shown depend on the answer to this page, you need to set a VariableName for it
    :param title: title of the page
    :param input_name: the name that will pair with the survey question when the participant's data from the app is downloaded. This is very important to have for each page that you want to save a participant's response to
    :param minimum: minimum value for sliders
    :param maximum: maximum value for sliders
    :param show_buttons: "WhenCorrect" if next button is shown only after the participant answers it correctly,
                         "AfterTimeout" if next button is shown after a certain time (timeout) has happened,
                         "Never" if the next button is never shown, &  the page will automatically go to next page after timeout
    :param conditions_lst: conditions that need to be met to view the page. For example
                            "StressLevel; 6, 7" will be parsed to ["StressLevel", "6, 7"]
                            The first item in the list is the VariableName, the second item are the answers that need
                            to have been selected in order for teh page to appear.
                            In this case, someone has to pick "6" or "7" for the StressLevel question in order to
                            see the page
    :param timeout: see show_buttons "AfterTimeout"
    :return: a page for a survey question / text page
    """
    ### Create generic page with text ###
    page_dict = {
        "Title": title,
        "Inputs": [
            {"Type": "Text",
             "Parameters": {
                 "Text": text}
             }]
    }
    ### Add page-level fields: conditions, media, timeouts, etc. ###
    if conditions_lst != [''] and conditions_lst is not None:  # if conditions list isn't empty
        value = conditions_lst[1].strip()  # value that needs to be met is the second item in the list
        if "," in value:  # if there are multiple values
            value = value.split(", ")  # split into a list
            new_value = []
            for each in value:
                try:
                    val = int(each)  # may have to cast to int
                    new_value.append(val)
                except (Exception,):
                    pass
            value = new_value
        page_dict["Conditions"] = [{  # adding a new key value pair to the page_dict dictionary
            "VariableName": conditions_lst[0].strip(),  # VariableName is first item in the list
            "Value": value
        }]

    if timeout not in (None, ""):  # add time out if it's necessary
        page_dict["Timeout"] = int(timeout)
        if show_buttons not in (None, ""):
            page_dict[
                "ShowButtons"] = show_buttons  # if there is a timeout, the show_buttons is gonna be AfterTimeout automatically

    if media not in (None, ""):  # add image/video if it's there
        if media[-3:] == "mp4":  # -3: means last 3 items that are iterable
            media_type = "video/mp4"
        elif media[-4:] == "jpeg":
            media_type = "image/jpeg"
        # add a media input:
        media = {"Type": "Media",
                 "Parameters": {
                     "ImageUrl": media,
                     "ImageType": media_type}
                 }
        if image_framed == "TRUE":
            media["Frame"] = True  # adding this key value pair to media dictionary
        print('Adjuntando medios para...', title)  # changed
        page_dict["Inputs"].append(media)  # adding media dictionary to the inputs list

    #### ADD INPUT ####
    for app_input in [input_1, input_2]:
        if app_input not in (None, ""):  # if there's an input
            add = {}  # input to add
            items_list = ""
            if items not in (None, ""):  # if there are button or other choices, clean it up and split into a list
                items_list = items.replace("\u2019", "'").replace("\u2013", "--").replace("\u2014", "--").replace("\u201c", '"').replace("\u201d", '"').replace("\\n", '\n').replace("\u00f4", "ô").replace("\u00e1", "á").replace("\u00e9", "é").replace("\u00ed", "í").replace("\u00f3", "ó").replace("\u00fa", "ú").replace(u'\xf1', 'n').replace("\u00fc", "ü").replace("\u00c1", "Á").replace("\u00c9", "É").replace("\u00cd", "Í").replace("\u00d3", "Ó").replace("\u00da", "Ú").replace("\u00d1", "Ñ").replace("\u00dc", "Ü").strip().split("; ")


            ## Based on what the input is, create input "add"
            if app_input == "Picker":
                add = {
                    "Type": "Picker",
                    "Name": input_name,
                    "Parameters": {
                        "Items": items_list
                    }
                }
            elif app_input == "Slider":
                if items_list not in (None, [""], ""):
                    add = {"Type": "Slider",
                           "Name": input_name,
                           "Parameters": {
                               "Minimum": minimum,
                               "Maximum": maximum,
                               "OtherChoices": items_list
                           }}
                else:
                    add = {"Type": "Slider",
                           "Name": input_name,
                           "Parameters": {
                               "Minimum": minimum,
                               "Maximum": maximum,
                               "OtherChoices": ["^Prefiero no responder"]  # changed
                           }}
            elif app_input == "Entry":
                add = {"Type": "Entry",
                       "Name": input_name}
            elif app_input == "Puzzle":
                add = {
                    "Type": "WordPuzzle",
                    "Name": input_name,
                    "CorrectFeedback": "Correcto!",  # changed
                    "IncorrectFeedback": "¡Vaya! Eso no parece correcto. Por favor, espere un momento "
                                         "y intenta de nuevo.",  # changed
                    "CorrectScore": 0.5,
                    "IncorrectDelay": 5000,
                    "CauseNavigation": True,
                    "Parameters": {
                        "Words": items_list
                    }
                }
            elif app_input == "Buttons":
                add = {"Type": "Buttons",
                       "Name": input_name,
                       "Parameters": {
                           "Buttons": items_list,
                           "Selectable": True
                       }}
                if items_list == ["Si", "No"]:
                    add["Parameters"]["ColumnCount"] = 2  # adding key value pair in parameters dictionary
            elif app_input == "Scheduler":
                add = {
                    "Type": "Scheduler",
                    "Name": "schedule_session",
                    "Parameters": {
                        "Message": "¡Es hora de practicar el pensamiento flexible! Dirígete a MindTrails Español para tu "
                                   "sesión programada.",  # changed, but HTC goes to what?
                    }
                }
            elif app_input == "Checkbox":
                add = {"Type": "Buttons",
                       "Name": input_name,
                       "Parameters": {
                           "Buttons": items_list,
                           "Selectable": True,
                           "AllowMultipleSelections": True
                       }}

            if variable_name not in (None, ""):
                add["VariableName"] = variable_name  # adding this to the add dictionary as a key/value pair
            if add not in (None, ""):  # if stuff got added to add
                page_dict["Inputs"].append(add)  # adding this add dictionary to the inputs list
                if app_input == "Scheduler":
                    page_dict["Inputs"].append(add)
    return page_dict


def create_json_file(file_name, name, title, sections, dose_by_section=False,
                     cancel_button_text=None):
    """
    Create a JSON file.
    :param file_name: File name for the json file
    :param name: name of json file
    :param title: title that appears when user opens it
    :param sections: Sections & all the information for the JSON files
    :param dose_by_section: If true, each dose is a full section. This is used specifically for the Biweekly surveys,
    as each time it's administered a user sees the next section
    :param cancel_button_text: text for the "exit" or "cancel" button
    :return: outputs a json file
    """
    json_dict = {
        "Name": name,
        "Title": title,
        "Sections": sections  # list of dicts
    }
    if dose_by_section:
        json_dict["DoseMethod"] = "OnRun"
        json_dict["DoseBySection"] = True
    if cancel_button_text not in (None, ""):  # if there is text for "exit" or "cancel" button
        json_dict["CancelButtonText"] = cancel_button_text
    with open(file_name, 'w', encoding='utf-8') as outfile:
        json.dump(json_dict, outfile, indent=4, ensure_ascii=False)
