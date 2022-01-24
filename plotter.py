import matplotlib.pyplot as plt
import re
from collections import Counter

# Turning match report file (list of tuples) to processable datatype.
def evaluate():
    with open("matchreports.txt", "r") as f:
        data = eval(f.read())
    return data

matchreports = evaluate()

season_first_half_months = ["August", "September", "October", "November", "December"]
season_second_half_months = ["January", "February", "March", "April", "May", "June", "July"]
# Sponsor parts of names would make same team into different tems. Comparing each team in iteration with this list helps to avoid that situation.
key_parts_of_team_names = ["Anadolu", "Milan", "CSKA", "Barcelona", "Bayern", "Fenerbahce", "Khimki", "Maccabi", "Olympiacos", "Panathinaikos", "Madrid", "Baskonia", "Kaunas"]
main_names = ["Anadolu Efes Istanbul", "Olimpia Milan", "CSKA Moscow", "Barcelona", "Bayern Munich", "Fenerbahce Istanbul", "Khimki Moscow Region", "Maccabi Tel Aviv", "Olympiacos Piraeus", "Panathinaikos Athens", "Real Madrid", "Baskonia", "Žalgiris Kaunas"]

def checkValidTeam(team):
    isvalid = False
    for k in key_parts_of_team_names:
        if k in team:
            isvalid = True
            break
    return isvalid

def plotBar(title, names, values):
    plt.bar(names, values)
    plt.title(title)
    plt.yticks(values)
    plt.xlabel("Team")
    plt.ylabel("Wins")
    plt.xticks(rotation='vertical')
    plt.show()

zero_attendance_games_2019 = []
zero_attendance_games_2020 = []
zero_attendance_games_2021 = []
non_zero_attendance_games_2019 = []
non_zero_attendance_games_2020 = []
non_zero_attendance_games_2021 = []
for mr in matchreports:
    # May 30, 2021 CET: 20:30
    # mr = (matchday, players_data, referees, attendance, home_team, home_team_quarter_points, away_team, away_team_quarter_points)
    if mr[0] is not None:
        # Check if attendance is not higher than zero
        month = mr[0].split()[0]
        if not re.match("^[1-9]\d*$", mr[3]):
            if ("2018" in mr[0] and month in season_first_half_months) or ("2019" in mr[0] and month in season_second_half_months):
                zero_attendance_games_2019.append(mr)
            elif ("2019" in mr[0] and month in season_first_half_months) or ("2020" in mr[0] and month in season_second_half_months):
                zero_attendance_games_2020.append(mr)
            elif ("2020" in mr[0] and month in season_first_half_months) or ("2021" in mr[0] and month in season_second_half_months):
                zero_attendance_games_2021.append(mr)
        else:
            if ("2018" in mr[0] and month in season_first_half_months) or ("2019" in mr[0] and month in season_second_half_months):
                non_zero_attendance_games_2019.append(mr)
            elif ("2019" in mr[0] and month in season_first_half_months) or ("2020" in mr[0] and month in season_second_half_months):
                non_zero_attendance_games_2020.append(mr)
            elif ("2020" in mr[0] and month in season_first_half_months) or ("2021" in mr[0] and month in season_second_half_months):
                non_zero_attendance_games_2021.append(mr)

# 1. See if during 2018/19 season the away or home team won more matches when attendance was 0
def analyzeZeroAttendanceRelations():
    home_team_won1 = 0
    away_team_won1 = 0
    winners1 = []
    winners_home1 = []
    winners_away1 = []
    for z1 in zero_attendance_games_2019:
        home_team_scored_points1 = sum(map(int, z1[5]))
        away_team_scored_points1 = sum(map(int, z1[7]))
        if home_team_scored_points1 > away_team_scored_points1:
            if checkValidTeam(z1[4]) == True:
                home_team_won1 += 1
                winners_home1.append(z1[4])
                winners1.append(z1[4])
        else:
            if checkValidTeam(z1[6]) == True:
                away_team_won1 += 1
                winners_away1.append(z1[6])
                winners1.append(z1[6])
    print("During season 2018/19 the home team won", home_team_won1, "games and the away team won", away_team_won1, "games, when attendance was 0.")
    plt_variables1 = Counter(winners_home1)
    print("Home team winners during 2018/19 season, when attendance was 0:", plt_variables1)
    plotBar("Home team winners during 2018/19 season (attendance 0)", list(plt_variables1.keys()), list(plt_variables1.values()))
    plt_variables2 = Counter(winners_away1)
    print("Away team winners during 2018/19 season, when attendance was 0:", plt_variables2)
    plotBar("Away team winners during 2018/19 season (attendance 0)", list(plt_variables2.keys()), list(plt_variables2.values()))
    plt_variables3 = Counter(winners1)
    print("Overall winners during 2018/19 season, when attendance was 0:", plt_variables3)
    plotBar("Overall winners during 2018/19 season (attendance 0)", list(plt_variables3.keys()), list(plt_variables3.values()))
    # 2. See if during 2019/20 season the away or home team won more matches when attendance was 0
    home_team_won2 = 0
    away_team_won2 = 0
    winners2 = []
    winners_home2 = []
    winners_away2 = []
    for z2 in zero_attendance_games_2020:
        home_team_scored_points2 = sum(map(int, z2[5]))
        away_team_scored_points2 = sum(map(int, z2[7]))
        if home_team_scored_points2 > away_team_scored_points2:
            if checkValidTeam(z2[4]) == True:
                home_team_won2 += 1
                winners_home2.append(z2[4])
                winners2.append(z2[4])
        else:
            if checkValidTeam(z2[6]) == True:
                away_team_won2 += 1
                winners_away2.append(z2[6])
                winners2.append(z2[6])
    print("During season 2019/20 the home team won", home_team_won2, "games and the away team won", away_team_won2, "games, when attendance was 0.")
    plt_variables4 = Counter(winners_home2)
    print("Home team winners during 2019/20 season, when attendance was 0:", plt_variables4)
    plotBar("Home team winners during 2019/20 season (attendance 0)", list(plt_variables4.keys()), list(plt_variables4.values()))
    plt_variables5 = Counter(winners_away2)
    print("Away team winners during 2019/20 season, when attendance was 0:", plt_variables5)
    plotBar("Away team winners during 2019/20 season (attendance 0)", list(plt_variables5.keys()), list(plt_variables5.values()))
    plt_variables6 = Counter(winners2)
    print("Overall winners during 2019/20 season, when attendance was 0:", plt_variables6)
    plotBar("Overall winners during 2019/20 season (attendance 0)", list(plt_variables6.keys()), list(plt_variables6.values()))
    # 3. See if during 2020/21 season the away or home team won more matches when attendance was 0
    home_team_won3 = 0
    away_team_won3 = 0
    winners3 = []
    winners_home3 = []
    winners_away3 = []
    for z3 in zero_attendance_games_2021:
        home_team_scored_points3 = sum(map(int, z3[5]))
        away_team_scored_points3 = sum(map(int, z3[7]))
        if home_team_scored_points3 > away_team_scored_points3:
            if checkValidTeam(z3[4]) == True:
                home_team_won3 += 1
                winners_home3.append(z3[4])
                winners3.append(z3[4])
        else:
            if checkValidTeam(z3[6]) == True:
                away_team_won3 += 1
                winners_away3.append(z3[6])
                winners3.append(z3[6])
    print("During season 2020/21 the home team won", home_team_won3, "games and the away team won", away_team_won3, "games, when attendance was 0.")
    plt_variables7 = Counter(winners_home3)
    print("Home team winners during 2020/21 season, when attendance was 0:", plt_variables7)
    plotBar("Home team winners during 2020/21 season (attendance 0)", list(plt_variables7.keys()), list(plt_variables7.values()))
    plt_variables8 = Counter(winners_away3)
    print("Away team winners during 2020/21 season, when attendance was 0:", plt_variables8)
    plotBar("Away team winners during 2020/21 season (attendance 0)", list(plt_variables8.keys()), list(plt_variables8.values()))
    plt_variables9 = Counter(winners3)
    print("Overall winners during 2020/21 season, when attendance was 0:", plt_variables9)
    plotBar("Overall winners during 2020/21 season (attendance 0)", list(plt_variables9.keys()), list(plt_variables9.values()))

def analyzeNonZeroAttendanceRelations():
    home_team_won1 = 0
    away_team_won1 = 0
    winners1 = []
    winners_home1 = []
    winners_away1 = []
    for z1 in non_zero_attendance_games_2019:
        home_team_scored_points1 = sum(map(int, z1[5]))
        away_team_scored_points1 = sum(map(int, z1[7]))
        if home_team_scored_points1 > away_team_scored_points1:
            if checkValidTeam(z1[4]) == True:
                home_team_won1 += 1
                winners_home1.append(z1[4])
                winners1.append(z1[4])
        else:
            if checkValidTeam(z1[6]) == True:
                away_team_won1 += 1
                winners_away1.append(z1[6])
                winners1.append(z1[6])
    print("During season 2018/19 the home team won", home_team_won1, "games and the away team won", away_team_won1, "games, when attendance was not 0.")
    plt_variables1 = Counter(winners_home1)
    print("Home team winners during 2018/19 season, when attendance was not 0:", plt_variables1)
    plotBar("Home team winners during 2018/19 season (attendance not 0) ", list(plt_variables1.keys()), list(plt_variables1.values()))
    plt_variables2 = Counter(winners_away1)
    print("Away team winners during 2018/19 season, when attendance was not 0:", plt_variables2)
    plotBar("Away team winners during 2018/19 season (attendance not 0)", list(plt_variables2.keys()), list(plt_variables2.values()))
    plt_variables3 = Counter(winners1)
    print("Overall winners during 2018/19 season, when attendance was not 0:", plt_variables3)
    plotBar("Overall winners during 2018/19 season (attendance not 0)", list(plt_variables3.keys()), list(plt_variables3.values()))
    # 2. See if during 2019/20 season the away or home team won more matches when attendance was 0
    home_team_won2 = 0
    away_team_won2 = 0
    winners2 = []
    winners_home2 = []
    winners_away2 = []
    for z2 in non_zero_attendance_games_2020:
        home_team_scored_points2 = sum(map(int, z2[5]))
        away_team_scored_points2 = sum(map(int, z2[7]))
        if home_team_scored_points2 > away_team_scored_points2:
            if checkValidTeam(z2[4]) == True:
                home_team_won2 += 1
                winners_home2.append(z2[4])
                winners2.append(z2[4])
        else:
            if checkValidTeam(z2[6]) == True:
                away_team_won2 += 1
                winners_away2.append(z2[6])
                winners2.append(z2[6])
    print("During season 2019/20 the home team won", home_team_won2, "games and the away team won", away_team_won2, "games, when attendance was not 0.")
    plt_variables4 = Counter(winners_home2)
    print("Home team winners during 2019/20 season, when attendance was not 0:", plt_variables4)
    plotBar("Home team winners during 2019/20 season (attendance not 0)", list(plt_variables4.keys()), list(plt_variables4.values()))
    plt_variables5 = Counter(winners_away2)
    print("Away team winners during 2019/20 season, when attendance was not 0:", plt_variables5)
    plotBar("Away team winners during 2019/20 season (attendance not 0)", list(plt_variables5.keys()), list(plt_variables5.values()))
    plt_variables6 = Counter(winners2)
    print("Overall winners during 2019/20 season, when attendance was not 0:", plt_variables6)
    plotBar("Overall winners during 2019/20 season (attendance not 0)", list(plt_variables6.keys()), list(plt_variables6.values()))
    # 3. See if during 2020/21 season the away or home team won more matches when attendance was 0
    home_team_won3 = 0
    away_team_won3 = 0
    winners3 = []
    winners_home3 = []
    winners_away3 = []
    for z3 in non_zero_attendance_games_2021:
        home_team_scored_points3 = sum(map(int, z3[5]))
        away_team_scored_points3 = sum(map(int, z3[7]))
        if home_team_scored_points3 > away_team_scored_points3:
            if checkValidTeam(z3[4]) == True:
                home_team_won3 += 1
                winners_home3.append(z3[4])
                winners3.append(z3[4])
        else:
            if checkValidTeam(z3[6]) == True:
                away_team_won3 += 1
                winners_away3.append(z3[6])
                winners3.append(z3[6])
    print("During season 2020/21 the home team won", home_team_won3, "games and the away team won", away_team_won3, "games, when attendance was not 0.")
    plt_variables7 = Counter(winners_home3)
    print("Home team winners during 2020/21 season, when attendance was not 0:", plt_variables7)
    plotBar("Home team winners during 2020/21 season (attendance not 0)", list(plt_variables7.keys()), list(plt_variables7.values()))
    plt_variables8 = Counter(winners_away3)
    print("Away team winners during 2020/21 season, when attendance was not 0:", plt_variables8)
    plotBar("Away team winners during 2020/21 season (attendance not 0)", list(plt_variables8.keys()), list(plt_variables8.values()))
    plt_variables9 = Counter(winners3)
    print("Overall winners during 2020/21 season, when attendance was not 0:", plt_variables9)
    plotBar("Overall winners during 2020/21 season (attendance not 0)", list(plt_variables9.keys()), list(plt_variables9.values()))

analyzeZeroAttendanceRelations()
print("---------------------------")
analyzeNonZeroAttendanceRelations()