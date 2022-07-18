from asyncio import start_server
from multiprocessing.context import ForkServerContext
import requests
from bs4 import BeautifulSoup
import re
import sys
import os    
import json

db = dict()

def get_info(URL):
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    info = soup.find(class_="intro")

    ### name and version

    package = info.find(class_="name")
    package_info = package.text.split()

    name = package_info[0]
    version = package_info[1]
    print("Name: ", name)
    print("Version: ", version)

    ### package manager, license, latest version

    items = info.find_all("div", class_="item")

    manager = items[0].text
    license = items[3].text
    latest_version = items[4].text.lstrip()

    print("Package Manager: ", manager)
    print("License: ", license)
    print(latest_version, end="\n")

    ### health score

    health = soup.find(class_="number")
    hs = health.text.split()
    score = hs[3]
    print("Health Score: ", score, "/ 100")

    ### popularity 

    result = soup.find(id="popularity")
    results = result.find_all("div", class_="stats-item")

    counts = []

    for r in results:
        counts.append(r.find("dd").text)

    dependents = counts[0].strip()
    stars = counts[1].strip()
    forks = counts[2].strip()
    contributors = counts[3].strip()

    print("Dependents: ", dependents)
    print("Stars: ", stars)
    print("Forks: ", forks)
    print("Contributors: ", contributors)

    ### funding status

    community = soup.find(id="community")
    stats = community.find_all("div", class_="stats-item")
    status = stats[4].text.strip().split()
    funding = status[1]
    print("Funded: ", funding)

    ### maintainers

    maintenance = soup.find(id="package")
    pm = maintenance.find_all("div", class_="stats-item")
    count = pm[7].text.strip().split()
    maintainers = count[1]
    print("Maintainers: ", maintainers)

    db[name] = [version, manager, license, latest_version, score, dependents, stars, forks, contributors, funding, maintainers]


### to use command line input instead of text file
# URL = str(sys.argv[1])
# get_info(URL)

with open(os.path.join(sys.path[0], "pkgs.txt"), "r") as f:
    # URL = f.read()
    for line in f:
        get_info(line)
        print("\n")

json_object = json.dumps(db, indent=4)

with open("data.json", "w") as outfile:
    outfile.write(json_object)