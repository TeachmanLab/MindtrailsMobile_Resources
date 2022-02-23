import csv
from PIL import Image
from github import Github
import os
import gdown

def compression(session_name):
    name = "BBBS/csv_files/" + session_name + ".csv"
    with open(name, newline='') as csvfile:
        print("opened")
        reader = csv.reader(csvfile, delimiter=',')
        pic_counter = 0
        print("reading")
        for row in reader:
            if "https://drive.google.com/" in row[3]:
                # start = row[3].find("file/d/")
                # end = row[3].find("/view?usp")
                # file_id = row[3][start + 7:end]
                # url = "https://drive.google.com/uc?export=download&id=" + file_id
                # destination = '/Users/emmymandm/PycharmProjects/MindTrails/BBBS/images/' + session_name + '/pic' + str(pic_counter) + '.jpeg'
                pic_counter += 1
                # message = "download url for pic" + str(pic_counter) + " is " + url
                # print(message)
                # print("normal url for pic", str(pic_counter), "is", row[3])
                # try:
                #     gdown.download(url, destination, quiet=False)
                #     print("downloaded image", str(pic_counter))
                # except:
                #     print("could not download from google drive")
    i = 0
    while i < pic_counter: # + 1
        try:
            path = '/Users/emmymandm/PycharmProjects/MindTrails/BBBS/images/' + session_name + '/pic' + str(i) + '.jpeg'
            image = Image.open(path)
            image.thumbnail((1300, 2600)) # 640
            image.save('/Users/emmymandm/PycharmProjects/MindTrails/BBBS/newimages/' + session_name + '/pic' + str(i) + '.jpeg')
            print("saved compressed image", str(i))
        except:
            print("could not open or resize image", str(i))
        finally:
            i += 1

    # upload to github
    token = os.getenv('GITHUB_TOKEN', input("token"))
    g = Github(token)
    repo = g.get_repo("TeachmanLab/MindtrailsMobile_Resources")

    i = 0
    while i < pic_counter:
        with open("/Users/emmymandm/PycharmProjects/MindTrails/BBBS/newimages/" + session_name + "/pic" + str(i) + ".jpeg", 'rb') as f:
            content = f.read()
        git_file = "bbbs/protocols/protocol1/media/images/" + session_name + "/pic" + str(i) + ".jpeg"
        # try:
        #     repo.delete_file(git_file, message="Deleting old image", sha="Deleting old file")
        # finally:
        try:
            repo.create_file(path=git_file, message="committing images", content=content, branch="main")
            print(git_file + " uploaded to github")
        except:
            print("Could not upload " + git_file)
        finally:
            i += 1


def long_compression(session_name):
    name = "BBBS/csv_files/" + session_name + ".csv"
    with open(name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        pic_counter = 0
        for row in reader:
            if "https://drive.google.com/" in row[2]:
                for i in range(2, 5):
                    start = row[i].find("file/d/")
                    end = row[i].find("/view?usp")
                    file_id = row[i][start + 7:end]
                    url = "https://drive.google.com/uc?export=download&id=" + file_id
                    destination = '/Users/emmymandm/PycharmProjects/MindTrails/BBBS/images/' + session_name + '/pic' + str(pic_counter) + '.jpeg'
                    pic_counter += 1
                    message = "download url for pic" + str(pic_counter) + " is " + url
                    print(message)
                    print("normal url for pic", str(pic_counter), "is", row[3])
                    try:
                        gdown.download(url, destination, quiet=False)
                        print("downloaded image", str(pic_counter))
                    except:
                        print("could not download from google drive ", row[i])

    i = 0
    while i < pic_counter:
        try:
            path = '/Users/emmymandm/PycharmProjects/MindTrails/BBBS/images/' + session_name + '/pic' + str(i) + '.jpeg'
            image = Image.open(path)
            image.thumbnail((1300, 2600))
            image.save('/Users/emmymandm/PycharmProjects/MindTrails/BBBS/newimages/' + session_name + '/pic' + str(i) + '.jpeg')
            print("saved compressed image", str(i))
        except:
            print("could not open or resize image", str(i))
            image.save('/Users/emmymandm/PycharmProjects/MindTrails/BBBS/newimages/' + session_name + '/pic' + str(i) + '.jpeg')
        finally:
            i += 1

    # upload to github
    token = os.getenv('GITHUB_TOKEN', input("token: "))
    g = Github(token)
    repo = g.get_repo("TeachmanLab/MindtrailsMobile_Resources")

    i = 0
    while i < pic_counter:
        with open("/Users/emmymandm/PycharmProjects/MindTrails/BBBS/newimages/" + session_name + "/pic" + str(i) + ".jpeg", 'rb') as f:
            content = f.read()
        git_file = "bbbs/protocols/protocol1/media/images/" + session_name + "/pic" + str(i) + ".jpeg"
        try:
            repo.create_file(path=git_file, message="committing images", content=content, branch="main")
            print(git_file + " uploaded to github")
        except:
            print("Could not upload " + git_file)
        finally:
            i += 1


longs = ["Session1_long", "Session2_long", "Session3_long", "Session4_long", "Session5_long"]
shorts = ["Session1_short", "Session2_short", "Session3_short", "Session4_short", "Session5_short"]

sessions = longs + shorts

compression("Session1_short")
long_compression("Session1_long")
compression("Session2_short")
long_compression("Session2_long")
compression("Session3_short")
long_compression("Session3_long")
compression("Session4_short")
long_compression("Session4_long")
compression("Session5_short")
long_compression("Session5_long")
