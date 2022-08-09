import csv

#on_demand_files = ["faculty_on-demand.csv", "grad_on-demand.csv", "staff_on-demand.csv", "undergrad_on-demand.csv"]
import json

on_demand_files = {
    "Staff": "staff_on-demand.csv",
    "Undergrad": "undergrad_on-demand.csv",
    "Grad": "graduate_on-demand.csv",
    "Faculty": "faculty_on-demand.csv",

}


for group in on_demand_files.keys():
    file = on_demand_files[group]
    domains = {
        "Academics/Work/Career Development": {},
        "Family & Home Life": {},
        "Finances": {},
        "Mental Health": {},
        "Physical Health": {},
        "Romantic Relationships": {},
        "Social Situations": {},
        "Discrimination/Microaggressions": {}
    }
    with open(file, "r") as read_obj:
        reader = csv.reader(read_obj)
        next(reader)
        next(reader)
        for row in reader:
            domain = row[0]
            subdomain = row[1]
            resource_name = row[2]
            resource_link = row[3]
            resource_text = row[4]
            if subdomain not in domains[domain].keys():
                domains[domain][subdomain] = []
            if resource_text not in (None, ""):
                domains[domain][subdomain].append("<b><font color='#9769ED'>" + resource_name + "</font></b>" + "<br><br>" + resource_text + "<br><br><a>" + resource_link + "<a><br><br><br><br>")
    for domain in domains.keys():
        for subdomain in domains[domain].keys():
            print("..............................................")
            print("Subdomain: ", subdomain)
            subdomain_text = ""
            for resource in domains[domain][subdomain]:
                subdomain_text = subdomain_text + resource
            domains[domain][subdomain] = subdomain_text
    json_dict = {
            "Name": group,
            "Title": "Resources",
            "Sections": [
                {
                    "Name": "Domains",
                    "Description": "Please click on any topic to learn about resources that can help you manage that "
                                   "part of your life.",
                    "Domains": []
                }
            ]
        }
    for domain in domains.keys():
        domain_dict = {
                "Name": domain,
                "Title": domain + " Resources",
                "PageGroups": [ ]
                }

        # add first page showing the subdomain options

        domain_dict["PageGroups"].append({
            "Name": "Which subdomain?",
            "Type": "Survey",
            "Pages": [{
                "ShowButton": "Never",
                "CausesNavigation": True,
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
                        "Buttons": []
                    }
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
                    "Title": domain + ': ' + subdomain,
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

    json_file = "/HTC/json_files/On-demand/on-demand_" + group + ".json"
    with open(json_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)  # data instead of json_dict

