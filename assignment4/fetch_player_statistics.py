import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin

import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requesting_urls import get_html
from time_planner import strip_text

## --- Task 8, 9 and 10 --- ##

try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"
# a matplotlib color for each team name (could be a name or a #rrggbb web color string)
colors = ['red', 'orange', 'yellow', 'palegreen', 'cyan', 'blue', 'plum', 'pink']
team_names = ['Memphis', 'Dallas', 'Philadelphia', 'Boston', 'Milwaukee', 'Golden State', 'Phoenix', 'Miami']
color_table = {}
stats_dir = "NBA_player_statistics"
#os.mkdir(stats_dir) #commented out because after creating the folder for the first time error: directory already exist.
#mapping team to color
for i, team in enumerate(team_names):
    color_table[team] = colors[i]


def find_best_players(url: str) -> None:
    """Find the best players in the semifinals of the nba.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams(url)
    # assert len(teams) == 8

    # Gets the player for every team and stores in dict (get_players)
    all_players = {}
    None_points = {"points" : 0.0}
    # get player statistics for each player,
    for item in teams:
        all_players[item.get("name")] = get_players(item.get("url"))

    # using get_player_stats
    for team, players in all_players.items():
        for item in players:
            html = get_html(item.get("url"))
            soup = BeautifulSoup(html, "html.parser")
            if soup.find(id="Regular_season"):# some of the player‘s pages did not have a Regular session table
                st = get_player_stats(item.get("url"), team)
                if st == {}:
                    item.update(None_points)
                item.update(st)
            else:
                item.update(None_points)
    # at this point, we should have a dict of the form:
    # {
    #     "team name": [
    #         {
    #             "name": "player name",
    #             "url": "https://player_url",
    #             # added by get_player_stats
    #             "points": 5,
    #             "assists": 1.2,
    #             # ...,
    #         },
    #     ]
    # }

    # Select top 3 for each team by points:
    best = {}
    top_stat = []
    for team, players in all_players.items():
        # Sort and extract top 3 based on points
        players = sorted(players, key=lambda d: d['points'], reverse=True) 
        top_3 = players[:3]
        best[team] = top_3
        top_stat.append(top_3)

    stats_to_plot = ["rebounds", "assists", "points"]
    for stat in stats_to_plot:
        plot_NBA_player_statistics(best, stat)


def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plots a single stat for the top 3 players from every team.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """
    for st in stat:
        plot_NBA_player_statistics(best, st)


def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")

    # lots of ways to do this,
    # but one way is to build a set of team names in the semifinal
    # and a dict of {team name: team url}

    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure
        # print([c.get_text(strip=True) for c in cols])

        # TODO:
        # 1. if First Round column, record team link from `a` tag
        # 2. if semifinal column, record team name

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    # return list of dicts (there will be 8):
    # [
    #     {
    #         "name": "team name",
    #         "url": "https://team url",
    #     }
    # ]

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str) -> list:
    """Gets all the players from a team that were in the roster for semi finals
    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """
    print(f"Finding players in {team_url}")

    # Get the table
    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Roster").find_next("table", {"class":"toccolours"})
    
    headings = table.find_all("th")
    labels = [th.text.strip() for th in headings]
    players = []
    # Loop over every row and get the names from roster
    rows = table.find_all("tr")
    rows = rows[3:]
    for row in rows:
        # Get the columns
        cols = row.find_all("a")
        # find name links (a tags)
        # and add to players a dict with
        # {'name':, 'url':}
        pnc_u = []# position-name-college url
        pnc_t =[]# position-name-college text     
        for col in cols:
            u = col.get("href")
            text = strip_text(col.get_text(strip=True))
            pnc_u.append(u)
            pnc_t.append(text)
        players.append({"name": pnc_t[1], "url": base_url+pnc_u[1]})

    # return list of players

    return players


def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    print(f"Fetching stats for player in {player_url}")

    # Get the table with stats
    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Regular_season").find_next("table", {"class":"wikitable"})

    headings = table.find_all("th")
    labels = [th.text.strip() for th in headings]
    #print(labels)
    
    stats = {}

    rows = table.find_all("tr")
    rows = rows[1:]

    # Loop over rows and extract the stats
    for j, row in enumerate(rows):
        cols = row.find_all("td")
        for i, col in enumerate(cols):
        # Check correct team (some players change team within season)
            if strip_text(col.get_text(strip=True).replace("†","")) == "2021–22":
                if strip_text(cols[1].get_text(strip=True)) == team:
        # load stats from columns
        # keys should be 'points', 'assists', etc.
                    stats["rebounds"] = float(strip_text(cols[8].get_text(strip=True).replace("*","")))
                    stats["assists"] = float(strip_text(cols[9].get_text(strip=True).replace("*","")))
                    stats["points"] = float(strip_text(cols[12].get_text(strip=True).replace("*","")))

                if col.get("rowspan") == str(2):
                    cols_2 = rows[j+1].find_all("td")
                    if strip_text(cols_2[0].get_text(strip=True)) == team:
                        stats["rebounds"] = float(strip_text(cols_2[7].get_text(strip=True).replace("*","")))
                        stats["assists"] = float(strip_text(cols_2[8].get_text(strip=True).replace("*","")))
                        stats["points"] = float(strip_text(cols_2[11].get_text(strip=True).replace("*","")))
            else:
                continue
    return stats


def plot_NBA_player_statistics(teams, stat):
    """Plot NBA player statistics. In this case, just points"""
    count_so_far = 0
    all_names = []

    # iterate through each team and the
    for team, players in teams.items():
        # pick the color for the team, from the table above
        color = color_table[team]
        # collect the points and name of each player on the team
        # you'll want to repeat with other stats as well
        points = []
        names = []
        for player in players:
            names.append(player["name"])
            points.append(player[stat])
        # record all the names, for use later in x label
        all_names.extend(names)

        # the position of bars is shifted by the number of players so far
        x = range(count_so_far, count_so_far + len(players))
        count_so_far += len(players)
        # make bars for this team's players points,
        # with the team name as the label
        bars = plt.bar(x, points, color=color, label=team)
        # add the value as text on the bars
        plt.bar_label(bars)

    # use the names, rotated 90 degrees as the labels for the bars
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    # add the legend with the colors  for each team
    plt.legend(loc=0)
    # turn off gridlines
    plt.grid(False)
    # set the title
    plt.title(f"{stat} per game")
    # save the figure to a file
    filename = f"{stat}-points.png"
    print(f"Creating {filename}")
    plt.savefig(filename)



# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)
