import csv
from PIL import Image
from github import Github
import os
import gdown

git_token = input('What is your github token? ')

def compression(short=True):
    # NOTE: directories "images" and "new_images" must exist for this to work
    groups = {
        "undergrad": [9, 5],
        "grad": [15, 22],
        "faculty": [21, 39],
        "staff": [27, 56]
    }
    lst_of_unique = []
    others = []
    if short:
        name = "/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/HTC_scenarios.csv"
        i_list = [9, 15, 21, 27]
    else:
        name = "/Users/emmymandm/PycharmProjects/MindTrails/HTC/csv_files/HTC_long_scenarios.csv"
        i_list = [5, 22, 39, 56]

    with open(name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        pic_counter = 0
        next(reader)
        for row in reader:
            # check and see if it's different across groups. most photos are the same across all groups, so we
            # don't have to download them 4x. These are the ones that are NOT the same across groups, so we will
            # deal with them separately.
            label = row[3].strip().replace(" ", "_")
            print("Creating photo...", label)

            if not (row[i_list[0]].strip() == row[i_list[1]].strip() == row[i_list[2]].strip() == row[
                i_list[3]].strip()):  # if they're not all equal
                print(label, "IS UNIQUE")
                for group in groups:
                    if short:
                        i = groups[group][0]
                    else:
                        i = groups[group][1]
                    label = row[3].strip().replace(" ", "_")
                    gdrive_link = row[i]
                    print('G drive is', gdrive_link)
                    if "https://drive.google.com/" in gdrive_link:
                        pic_name = label + "_" + group
                        lst_of_unique.append(pic_name)
                        start = gdrive_link.find("file/d/")
                        end = gdrive_link.find("/view?usp")
                        file_id = gdrive_link[start + 7:end]
                        url = "https://drive.google.com/uc?export=download&id=" + file_id
                        destination = '/Users/emmymandm/PycharmProjects/MindTrails/HTC/images/' + pic_name + '.jpeg'
                        pic_counter += 1
                        message = "download url for pic" + pic_name + " is " + url
                        print(message)
                        print("normal url for pic", pic_name, "is", gdrive_link)
                        try:
                            gdown.download(url, destination, quiet=False)
                            print("downloaded UNIQUE image", pic_name)
                        except:
                            print("could not download UNIQUE image from google drive")

            else:
                if short:
                    i = 9
                else:
                    i = 5
                label = row[3].strip().replace(" ", "_")
                gdrive_link = row[i]
                print("gdrive link is", gdrive_link)
                if "https://drive.google.com/" in gdrive_link:
                    pic_name = label  # + "_" + group
                    others.append(pic_name)
                    start = gdrive_link.find("file/d/")
                    end = gdrive_link.find("/view?usp")
                    file_id = gdrive_link[start + 7:end]
                    url = "https://drive.google.com/uc?export=download&id=" + file_id
                    destination = '/Users/emmymandm/PycharmProjects/MindTrails/HTC/images/' + pic_name + '.jpeg'
                    pic_counter += 1
                    message = "download url for pic" + pic_name + " is " + url
                    print(message)
                    print("normal url for pic", pic_name, "is", gdrive_link)
                    try:
                        gdown.download(url, destination, quiet=False)
                        print("downloaded image", pic_name)
                    except:
                        print("could not download from google drive")

    with open(name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        pic_counter = 0
        next(reader)
        lst_of_unique = []
        others = []
        for row in reader:
            if not (row[i_list[0]].strip() == row[i_list[1]].strip() == row[i_list[2]].strip() == row[i_list[3]].strip()):
                for group in groups:
                    pic_name = row[3].strip().replace(" ", "_") + "_" + group
                    lst_of_unique.append(pic_name)
            else:
                pic_name = row[3].strip().replace(" ", "_")
                others.append(pic_name)
        total = lst_of_unique + others
        # total = others

        for pic_name in total:
            try:
                path = '/Users/emmymandm/PycharmProjects/MindTrails/HTC/images/' + pic_name + '.jpeg'
                image = Image.open(path)
                image.thumbnail((1300, 2600))  # 640
                image.save('/Users/emmymandm/PycharmProjects/MindTrails/HTC/new_images/' + pic_name + '.jpeg')
                print("saved compressed image", pic_name)
            except:
                print("could not open or resize image", pic_name)
            finally:
                pass

            # upload to github
            try:
                token = os.getenv('GITHUB_TOKEN', git_token)
                g = Github(token)
                repo = g.get_repo("TeachmanLab/MindtrailsMobile_Resources")
                with open("/Users/emmymandm/PycharmProjects/MindTrails/HTC/new_images/" + pic_name + ".jpeg",
                          'rb') as f:
                    content = f.read()
                git_file = "HTC/protocols/protocol1/media/new_images/" + pic_name + ".jpeg"
                # try:
                #     repo.delete_file(git_file, message="Deleting old image", sha="Deleting old file")
                # finally:
                try:
                    repo.create_file(path=git_file, message="committing images", content=content, branch="main")
                    print(git_file + " uploaded to github")
                except:
                    print("Could not upload " + git_file)
                finally:
                    pass
            except:
                print("Could not upload " + pic_name)


compression(short=True)
compression(short=False)
