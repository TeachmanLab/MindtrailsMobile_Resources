import csv
import json

on_demand_files = { #come from the excel resources for on-demand library (for app tabs)
    "MTM-HD": r"/Users/xinyinzhang/Desktop/PACT Lab Training/MTM_csv/MTM on demand HD.csv"
}

json_dict = {
    "Name": "On-demand resources",
    "Title": "Resources",
    "Sections": []
}

group_num = 0
for group in on_demand_files.keys():
    group_num += 1
    file = on_demand_files[group]
    domains = {
        "Huntington's Disease": {},
        "Mental Health": {}
    }

    with open(file, "r", encoding="utf-8") as read_obj:
        reader = csv.reader(read_obj)
        next(reader)
        for row in reader:
            domain = row[0]
            subdomain = row[1]
            resource_name = row[2]
            resource_link = row[3]
            resource_text = row[4]
            if subdomain not in domains[domain].keys():
                domains[domain][subdomain] = []
            # we could make it a list of page groups , each subdomain has a list of page groups
            if resource_text not in (None, ""):
                domains[domain][subdomain].append('<b><font color="#9769ED" size=6>' + resource_name + '</font></b>' +
                                                  '<br /><br />' + resource_text + '<br /><br /><a href="' +
                                                  resource_link + '">' + resource_link
                                                  + "</a><br /><br /><br /><br />")
    for domain in domains.keys():
        for subdomain in domains[domain].keys():
            print("..............................................")
            print("Subdomain: ", subdomain)
            subdomain_text = ""
            for resource in domains[domain][subdomain]:
                subdomain_text = subdomain_text + resource
            domains[domain][subdomain] = subdomain_text
    json_dict["Sections"].append(
        {
            "Name": "Domains",
            "Description": "Please click on any topic to learn about resources that can help you manage that "
                           "part of your life. \n\n  Though resources were carefully selected by our team of researchers and clinicians, the University of Virginia does not endorse these resources.",
            "Domains": []
        }
    )
    for domain in domains.keys():
        domain_dict = {
                "Name": domain,
                "Title": domain + " Resources",
                "PageGroups": []
                }

        # add first page showing the subdomain options

        domain_dict["PageGroups"].append({
            "Name": "Which subdomain?",
            "Type": "Survey",
            "Pages": [{
                #"ShowButtons": "Never",
                #"CausesNavigation": True,
                "Inputs": [{
                    "Type": "Text",
                    "Parameters": {
                        "Text": "Click on the specific topic to see associated resources."
                    }
                },
                {
                    "Type": "Buttons",
                    "Name": "subdomain_chosen",
                    "VariableName": "subdomain_chosen",
                    "Parameters": {
                        "Buttons": [],
                        "Selectable": True,
                        #"CausesNavigation": True
                    },

                }]
            }]
        }
        )
        subdomains = []
        for subdomain in domains[domain].keys():
            subdomain_with_condition = subdomain.replace(" ", "_") + "::" + subdomain
            domain_dict["PageGroups"][0]["Pages"][0]["Inputs"][1]["Parameters"]["Buttons"].append(subdomain_with_condition)

        # add pages with . ONE page group per subdomain

        for subdomain in domains[domain].keys():
            text = ""
            subdomain_page_group =  {
                    "Name": subdomain,
                    "Title": subdomain,
                    "Type": "Survey",
                    "Pages": [
                        {
                            "Conditions": [
                                {"VariableName": "subdomain_chosen",
                                    "Value": subdomain.replace(" ", "_")}
                            ],
                            "Inputs": [{
                                "Type": "Text",
                                "Parameters": {
                                    "IsHtml": True,
                                    "Text": domains[domain][subdomain]
                                }
                            }],
                            "CanBeFavorited": True
                        }
                        ]
            }
            domain_dict["PageGroups"].append(subdomain_page_group)

            ## add the text, create it as a large string of teh subdomain list separated by \n \n etc

        json_dict["Sections"][0]["Domains"].append(domain_dict)

json_file = "on-demand_MTM_HD.json"
#json_file = "/Users/emmymandm/PycharmProjects/MindTrails/HTC/json_files/On-demand/on-demand_all_groups.json"
with open(json_file, 'w') as outfile:
    json.dump(json_dict, outfile, indent=4)  # data instead of json_dict

