import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import conv
import get_matches
import numpy as np


def Parse_all(data):
    dataframe = []
    for unique_match in data:
        r = requests.get(unique_match)
        soup = BeautifulSoup(r.content, "html5lib")
        temp_list = []
        temp_df = []
        try:
            temp_list.append(soup.time.attrs['datetime'])
        except:
            temp_list.append(np.nan)
        try:
            temp_list.append(soup.find("span", attrs={"class": "match__region"}).text)
        except:
            temp_list.append(np.nan)
        try:
            temp_list.append(soup.find("span", attrs={"class": "match__season-number"}).text)
        except:
            temp_list.append(np.nan)
        bans = soup.select("li[class*='list-group-item op']")
        try:
            temp_list.append(bans[0].span.find("span").text)
        except:
            temp_list.append(np.nan)
        try:
            temp_list.append(bans[1].span.find("span").text)
        except:
            temp_list.append(np.nan)
        for ban in bans:
            try:
                temp_list.append(ban.span.find("strong").text)
            except:
                temp_list.append(np.nan)
        ATK = soup.select("td[class*='sp__atk js-heatmap-ignore py-0']")
        DEF = soup.select("td[class*='sp__def js-heatmap-ignore py-0']")
        for operator in range(10):
            try:
                temp_list.append(ATK[operator].span.text)
            except:
                temp_list.append(np.nan)
            try:
                temp_list.append(DEF[operator].span.text)
            except:
                temp_list.append(np.nan)
        match = soup.select("li[class*='log__line']")
        try:
            temp_list.append(" ".join(conv.convert([match[-1].find("strong").next_sibling])[1:]))
        except:
            temp_list.append(np.nan)
        for round in range(len(match) - 1):
            new_list = temp_list.copy()
            temp_text = conv.convert([match[round].find("strong").next_sibling])
            try:
                new_list.append(round + 1)
            except:
                new_list.append(np.nan)
            try:
                new_list.append(match[round].find("strong").text)
            except:
                new_list.append(np.nan)
            try:
                if (temp_text[1] == "Aviator/Game"):
                    new_list.append("Aviator/Game Room")
                elif (temp_text[1] == "Open"):
                    new_list.append("Open Area/Kitchen")
                elif (temp_text[1] == "Armory/Throne"):
                    new_list.append("Armory/Throne Room")
                elif (temp_text[1] == "Bunk/Day"):
                    new_list.append("Bunk/Day Care")
                elif (temp_text[1] == "Initiatiom"):
                    new_list.append("Initiation Room/Office")
                else:
                    new_list.append(temp_text[1])
            except:
                new_list.append(np.nan)
            try:
                if temp_text[2] != "attack" and temp_text[2] != "defense":
                    new_list.append(temp_text[3])
                else:
                    new_list.append(temp_text[2])
            except:
                new_list.append(np.nan)
            try:
                new_list.append(" ".join(temp_text[4:]))
            except:
                new_list.append(np.nan)
            dataframe.append(new_list)
        time.sleep(5)
    return pd.DataFrame(dataframe, columns=["date of game", "region of game", "season", "Team 1", "Team 2", "1st ban", "2nd ban", "3rd ban", "4th ban", "Operator on ATK1", "Operator on DEF1", "Operator on ATK2", "Operator on DEF2", "Operator on ATK3", "Operator on DEF3", "Operator on ATK4", "Operator on DEF4", "Operator on ATK5", "Operator on DEF5", "Operator on ATK6", "Operator on DEF6", "Operator on ATK7", "Operator on DEF7", "Operator on ATK8", "Operator on DEF8", "Operator on ATK9", "Operator on DEF9", "Operator on ATK10", "Operator on DEF10", "Map name", "round number", "Round winner", "Site location", "Which side won", "How they won"])

if __name__ == "__main__":
    raw_data = Parse_all(get_matches.get_match_list(4, "https://siege.gg/matches?tab=results&league=PL&region%5B%5D=NA&region%5B%5D=EU&region%5B%5D=LATAM&region%5B%5D=APAC&season=11&date=&page=1&tab=results&region%5B0%5D=NA&region%5B1%5D=EU&region%5B2%5D=LATAM&region%5B3%5D=APAC&season=11&league=PL&date=&page="))
    raw_data.to_csv("C:\\Users\\Jan\\Desktop\\Projects\\SiegeStatsWebsite\\raw_data.csv", index = False)
