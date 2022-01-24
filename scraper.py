import os, requests, re, time
from bs4 import BeautifulSoup

# "https://www.???.???" - replace it with correct URL
MAIN_URL = "https://www.euroleague.net"
# Considering only last three seasons
seasons = ["E2018", "E2019", "E2020"]
# Considering only teams, which participated in each season between 2018-2021
teams_of_seasons_2018_2021 = ["IST", "MIL", "CSK", "BAR", "MUN", "ULK", "KHI", "TEL", "OLY", "PAN", "MAD", "BAS", "ZAL"] 
team = "/competition/teams/showteam?clubcode={}&seasoncode={}"
covid_season_URL = "/competition/teams?seasoncode=E2019"

# This function can be used to read the matcreport data directly after making the request.
def getMatchReport(URL):
    players_data = {"home_team": [],
                    "away_team": []}
    player_data_statistics = {"shirtnumber": "",
                                "name": "",
                                "minutes": "",
                                "points": "",
                                "2fg": "",
                                "3fg": "",
                                "ft": "",
                                "o": "",
                                "d": "",
                                "t": "",
                                "as": "",
                                "st": "",
                                "to": "",
                                "fv": "",
                                "ag": "",
                                "cm": "",
                                "rv": "",
                                "pir": "",
                                "player_id_link": ""
                            }

    data = requests.get(URL)
    data_text = data.text
    soup = BeautifulSoup(data_text, 'html.parser')
    list_of_soup_elements = list(soup)
    list_of_soup_elements2 = list(list_of_soup_elements[2])
    list_of_soup_elements3 = (str(list_of_soup_elements2[3])).split("\n")

    matchday = None
    referees = None
    attendance = None
    home_team = None
    home_team_quarter_points = None
    away_team = None
    away_team_quarter_points = None
    main_data_counter = 0
    home_team_done = False
    both_teams_done = 0
    can_start_processing_away_team = False
    for souped_line in list_of_soup_elements3:
        #Date data
        if re.match("<div class=\"date cet\">.*", souped_line):
            matchday = souped_line.split(">")[1].split("<")[0]
        #Main data
        if (re.match("<td>.*</td>", souped_line) or re.match("<td class=\"PlayerContainer\">.*", souped_line)) and both_teams_done < 2:
            statistics_data_line = re.sub("<td>|</td>", "", souped_line)
            if "\xa0" in statistics_data_line:
                statistics_data_line = statistics_data_line.replace("\xa0", "")
            main_data_counter += 1
            if main_data_counter == 1:
                player_data_statistics["shirtnumber"] = statistics_data_line
            elif main_data_counter == 2:
                if statistics_data_line.startswith('<td class="PlayerContainer">'):
                    player = statistics_data_line.split(">")
                    name = player[-2].replace("</a", "").strip()
                    name_splitted = name.split(",")
                    full_name = name_splitted[-1].strip() + " " + name_splitted[0].strip()
                    player_data_statistics["name"] = full_name
                    link = ""
                    if 'class="PlayerStartFive"' not in statistics_data_line:
                        link = player[1].split("\"")[1].replace("&amp;", "&")
                    else:
                        link = player[1].split("\"")[3].replace("&amp;", "&")
                    player_data_statistics["player_id_link"] = link
            elif main_data_counter == 3:
                player_data_statistics["minutes"] = statistics_data_line
            elif main_data_counter == 4:
                player_data_statistics["points"] = statistics_data_line
            elif main_data_counter == 5:
                player_data_statistics["2fg"] = statistics_data_line
            elif main_data_counter == 6:
                player_data_statistics["3fg"] = statistics_data_line
            elif main_data_counter == 7:
                player_data_statistics["ft"] = statistics_data_line
            elif main_data_counter == 8:
                player_data_statistics["o"] = statistics_data_line
            elif main_data_counter == 9:
                player_data_statistics["d"] = statistics_data_line
            elif main_data_counter == 10:
                player_data_statistics["t"] = statistics_data_line
            elif main_data_counter == 11:
                player_data_statistics["as"] = statistics_data_line
            elif main_data_counter == 12:
                player_data_statistics["st"] = statistics_data_line
            elif main_data_counter == 13:
                player_data_statistics["to"] = statistics_data_line
            elif main_data_counter == 14:
                player_data_statistics["fv"] = statistics_data_line
            elif main_data_counter == 15:
                player_data_statistics["ag"] = statistics_data_line
            elif main_data_counter == 16:
                player_data_statistics["cm"] = statistics_data_line
            elif main_data_counter == 17:
                player_data_statistics["rv"] = statistics_data_line
            elif main_data_counter == 18:
                player_data_statistics["pir"] = statistics_data_line
                main_data_counter = 0
                if both_teams_done < 2:
                    if can_start_processing_away_team == False and home_team_done == False:
                        players_data["home_team"].append(player_data_statistics)
                        player_data_statistics = player_data_statistics.fromkeys(player_data_statistics, "")
                    else:
                        if can_start_processing_away_team == True and home_team_done == True:
                            players_data["away_team"].append(player_data_statistics)
                        player_data_statistics = player_data_statistics.fromkeys(player_data_statistics, "")
            if re.match("<td.*Team</a>.*", statistics_data_line):
                player_data_statistics = player_data_statistics.fromkeys(player_data_statistics, "")
                home_team_done = True
                main_data_counter = 0
                both_teams_done += 1
            if re.match("<span.*AverageFreeThrowsPercent.*", statistics_data_line):
                can_start_processing_away_team = True
                main_data_counter = 0
        #Referees
        if re.match("<span.*>Referees: </span>", souped_line):
            if referees is None:
                referees_names_list = souped_line.split(">")[3].split(";")
                referee_name = []
                for refname in referees_names_list:
                    refname_parts = refname.split(",")
                    referee_name.append((refname_parts[1].replace("</span", "").strip() + " " + refname_parts[0].replace("</span", "").strip()).replace("</span", "").strip())
                referees = referee_name
        #Attendance number
        if re.match("<span.*>Attendance: </span>", souped_line):
            if attendance is None:
                attendance = souped_line.split(">")[3].replace("</span", "").strip()
        #Home and away team; quarters data
        if re.match("<td class=\"PartialsClubNameContainer\">.*", souped_line):
            data3_line_splitted = souped_line.split(">")
            if home_team is not None and away_team is None:
                away_team = data3_line_splitted[1].split("<")[0]
                quarters1 = []
                for q1 in range(3, len(data3_line_splitted), 2):
                    possible_quarter = data3_line_splitted[q1].replace("</td", "")
                    if re.match("\d+", possible_quarter):
                        quarters1.append(possible_quarter)
                away_team_quarter_points = quarters1
            if home_team is None and away_team is None:
                home_team = data3_line_splitted[1].split("<")[0]
                quarters2 = []
                for q2 in range(3, len(data3_line_splitted), 2):
                    possible_quarter = data3_line_splitted[q2].replace("</td", "")
                    if re.match("\d+", possible_quarter):
                        quarters2.append(possible_quarter)
                home_team_quarter_points = quarters2

    return matchday, players_data, referees, attendance, home_team, home_team_quarter_points, away_team, away_team_quarter_points


#print(getMatchReport("https://www.euroleague.net/main/results/showgame?gamecode=148&seasoncode=E2021"))

# This function gives all the matchreport links from seasons 2018/19, 2019/20 and 2020/21
# Running it again will take unreasonable amount of time. Therefore I wrote the results of this function to a textfile as well.
def getAllMatchLinksOfCertainSeason():
    match_report_links = []
    with open("matchreport_links.txt", "w") as m:
        for season in seasons:
            print(season)
            for team_short_form in teams_of_seasons_2018_2021:
                print(team_short_form)
                data = requests.get((MAIN_URL + team).format(team_short_form, season))
                data_text = data.text
                soup = BeautifulSoup(data_text, 'html.parser')
                list_of_soup_elements = list(soup)
                list_of_soup_elements2 = list(list_of_soup_elements[2])
                list_of_soup_elements3 = (str(list_of_soup_elements2[3])).split("\n")
                for souped_line in list_of_soup_elements3:
                    if re.match("<a href=\"/main/results/showgame.*", souped_line):
                        if souped_line not in match_report_links:
                            match_report_links.append(souped_line)
                            m.write(souped_line[9:-2].replace("&amp;", "&") + "\n")
        print(match_report_links)
        print(len(match_report_links))

#start_time = time.time()
#getAllMatchLinksOfCertainSeason()
#end_time = time.time()
# Time took for function getAllMatchLinksOfCertainSeason(): 28.21211528778076 seconds.
#print("Time took for function getAllMatchLinksOfCertainSeason():", end_time - start_time, "seconds.")

# There are 848 matchreport files. It reasonable to save the content files to disk and then process them later, rather than making every time requests.
# Downloaded a total of 38MB data.
def saveRequestsResponsesToFiles(match_report_link):
    with open(match_report_link, "r") as mrl:
        content = mrl.readlines()
        for count, c in enumerate(content):
            print("Processing", str(count + 1) + "/" + str(len(content)))
            c = c.replace("\n", "")
            link_name_splitted = c.split("&")
            file_name = link_name_splitted[0].split("?")[1] + link_name_splitted[1] + ".html"
            data = requests.get(MAIN_URL + c)
            open(file_name, "wb").write(data.content)

#saveRequestsResponsesToFiles("matchreport_links.txt")

# The purpose of this function is basically the same and actually is almost the same as getMatchReport(), but with the small difference of reading already saved html-files from disk 
# (assuming the files are in the same directory as scraper.py).
def getMatchReportsDirectlyFromFile(html_file):
    players_data = {"home_team": [],
                    "away_team": []}
    player_data_statistics = {"shirtnumber": "",
                                "name": "",
                                "minutes": "",
                                "points": "",
                                "2fg": "",
                                "3fg": "",
                                "ft": "",
                                "o": "",
                                "d": "",
                                "t": "",
                                "as": "",
                                "st": "",
                                "to": "",
                                "fv": "",
                                "ag": "",
                                "cm": "",
                                "rv": "",
                                "pir": "",
                                "player_id_link": ""
                            }
    if html_file.endswith(".html"):
        with open(html_file, "rb") as f:
            data_text = f.read()
            soup = BeautifulSoup(data_text, 'html.parser')
            list_of_soup_elements = list(soup)
            list_of_soup_elements2 = list(list_of_soup_elements[2])
            list_of_soup_elements3 = (str(list_of_soup_elements2[3])).split("\n")

            matchday = None
            referees = None
            attendance = None
            home_team = None
            home_team_quarter_points = None
            away_team = None
            away_team_quarter_points = None
            main_data_counter = 0
            home_team_done = False
            both_teams_done = 0
            can_start_processing_away_team = False
            for souped_line in list_of_soup_elements3:
                #Date data
                if re.match("<div class=\"date cet\">.*", souped_line):
                    matchday = souped_line.split(">")[1].split("<")[0]
                #Main data
                if (re.match("<td>.*</td>", souped_line) or re.match("<td class=\"PlayerContainer\">.*", souped_line)) and both_teams_done < 2:
                    statistics_data_line = re.sub("<td>|</td>", "", souped_line)
                    if "\xa0" in statistics_data_line:
                        statistics_data_line = statistics_data_line.replace("\xa0", "")
                    main_data_counter += 1
                    if main_data_counter == 1:
                        player_data_statistics["shirtnumber"] = statistics_data_line
                    elif main_data_counter == 2:
                        if statistics_data_line.startswith('<td class="PlayerContainer">'):
                            player = statistics_data_line.split(">")
                            name = player[-2].replace("</a", "").strip()
                            name_splitted = name.split(",")
                            full_name = name_splitted[-1].strip() + " " + name_splitted[0].strip()
                            player_data_statistics["name"] = full_name
                            link = ""
                            if 'class="PlayerStartFive"' not in statistics_data_line:
                                link = player[1].split("\"")[1].replace("&amp;", "&")
                            else:
                                link = player[1].split("\"")[3].replace("&amp;", "&")
                            player_data_statistics["player_id_link"] = link
                    elif main_data_counter == 3:
                        player_data_statistics["minutes"] = statistics_data_line
                    elif main_data_counter == 4:
                        player_data_statistics["points"] = statistics_data_line
                    elif main_data_counter == 5:
                        player_data_statistics["2fg"] = statistics_data_line
                    elif main_data_counter == 6:
                        player_data_statistics["3fg"] = statistics_data_line
                    elif main_data_counter == 7:
                        player_data_statistics["ft"] = statistics_data_line
                    elif main_data_counter == 8:
                        player_data_statistics["o"] = statistics_data_line
                    elif main_data_counter == 9:
                        player_data_statistics["d"] = statistics_data_line
                    elif main_data_counter == 10:
                        player_data_statistics["t"] = statistics_data_line
                    elif main_data_counter == 11:
                        player_data_statistics["as"] = statistics_data_line
                    elif main_data_counter == 12:
                        player_data_statistics["st"] = statistics_data_line
                    elif main_data_counter == 13:
                        player_data_statistics["to"] = statistics_data_line
                    elif main_data_counter == 14:
                        player_data_statistics["fv"] = statistics_data_line
                    elif main_data_counter == 15:
                        player_data_statistics["ag"] = statistics_data_line
                    elif main_data_counter == 16:
                        player_data_statistics["cm"] = statistics_data_line
                    elif main_data_counter == 17:
                        player_data_statistics["rv"] = statistics_data_line
                    elif main_data_counter == 18:
                        player_data_statistics["pir"] = statistics_data_line
                        main_data_counter = 0
                        if both_teams_done < 2:
                            if can_start_processing_away_team == False and home_team_done == False:
                                players_data["home_team"].append(player_data_statistics)
                                player_data_statistics = player_data_statistics.fromkeys(player_data_statistics, "")
                            else:
                                if can_start_processing_away_team == True and home_team_done == True:
                                    players_data["away_team"].append(player_data_statistics)
                                player_data_statistics = player_data_statistics.fromkeys(player_data_statistics, "")
                    if re.match("<td.*Team</a>.*", statistics_data_line):
                        player_data_statistics = player_data_statistics.fromkeys(player_data_statistics, "")
                        home_team_done = True
                        main_data_counter = 0
                        both_teams_done += 1
                    if re.match("<span.*AverageFreeThrowsPercent.*", statistics_data_line):
                        can_start_processing_away_team = True
                        main_data_counter = 0
                #Referees
                if re.match("<span.*>Referees: </span>", souped_line):
                    if referees is None:
                        referees_names_list = souped_line.split(">")[3].split(";")
                        referee_name = []
                        for refname in referees_names_list:
                            refname_parts = refname.split(",")
                            referee_name.append((refname_parts[1].replace("</span", "").strip() + " " + refname_parts[0].replace("</span", "").strip()).replace("</span", "").strip())
                        referees = referee_name
                #Attendance number
                if re.match("<span.*>Attendance: </span>", souped_line):
                    if attendance is None:
                        attendance = souped_line.split(">")[3].replace("</span", "").strip()
                #Home and away team; quarters data
                if re.match("<td class=\"PartialsClubNameContainer\">.*", souped_line):
                    data3_line_splitted = souped_line.split(">")
                    if home_team is not None and away_team is None:
                        away_team = data3_line_splitted[1].split("<")[0]
                        quarters1 = []
                        for q1 in range(3, len(data3_line_splitted), 2):
                            possible_quarter = data3_line_splitted[q1].replace("</td", "")
                            if re.match("\d+", possible_quarter):
                                quarters1.append(possible_quarter)
                        away_team_quarter_points = quarters1
                    if home_team is None and away_team is None:
                        home_team = data3_line_splitted[1].split("<")[0]
                        quarters2 = []
                        for q2 in range(3, len(data3_line_splitted), 2):
                            possible_quarter = data3_line_splitted[q2].replace("</td", "")
                            if re.match("\d+", possible_quarter):
                                quarters2.append(possible_quarter)
                        home_team_quarter_points = quarters2

        return matchday, players_data, referees, attendance, home_team, home_team_quarter_points, away_team, away_team_quarter_points

def readMatchReportsFromHTMLFiles():
    files_in_drive = os.listdir(".")
    all_match_report_list_of_tuples = []
    for c, file_in_drive in enumerate(files_in_drive):
        if file_in_drive.endswith(".html"):
            #print("Processing file:", file_in_drive, c + 1, "of 848 done.")
            data = getMatchReportsDirectlyFromFile(file_in_drive)
            try:
                if data[0] is None:
                    print(file_in_drive)
            except:
                print(file_in_drive)
            all_match_report_list_of_tuples.append(data)
    return all_match_report_list_of_tuples
#start_time = time.time()
#matchreports = readMatchReportsFromHTMLFiles()
#end_time = time.time()
# Time took for function readMatchReportsFromHTMLFiles(): 28.889304161071777 seconds.
#print("Time took for function readMatchReportsFromHTMLFiles():", end_time - start_time, "seconds.")


# Again, to save time, we write the list of match report tuples to a file. Then, using Python's built-in function eval we can parse it later with a few seconds.
def writeMatchReportsToFile():
    with open("matchreports.txt", "w") as mr:
        matchreports = readMatchReportsFromHTMLFiles()
        mr.write(str(matchreports))
writeMatchReportsToFile()