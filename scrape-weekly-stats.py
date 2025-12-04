from bs4 import BeautifulSoup
from random import randint
import requests
import time


def get_player_position(url: str) -> tuple:
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')

    section_top = soup.find("div", class_="sectiontop")
    divs = section_top.find_all("div", class_="td")
    
    # Get position's 'b' tag and extract the next object's text
    position = section_top.find("b", string="Position:").next_sibling.strip()

    return position


def scrape_week_stats(week: str, player_positions: dict):
    url = f"https://www.footballdb.com/fantasy-football/index.html?yr=2025&pos=OFF&wk={week}&key=b6406b7aea3872d5bb677f064673c57f"
    

    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find("table", class_="statistics")
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")
    
    week_stats = ""
    for row in rows:  # For each player
        data = row.find_all("td")
        player_stats = ""
        for i,s in enumerate(data):  # for each stat
            if i == 0:
                names_array = s.text.strip().split()
                name = f"{names_array[0]} {names_array[1]}"
                player_stats += f"{name},"

                if name not in player_positions.keys():
                    # Get position and add to stat string
                    player_url = f"https://www.footballdb.com{row.find('a').get('href')}"
                    time.sleep(randint(0,1))  # sleep to avoid detection
                    position = get_player_position(player_url)
                    player_positions[name] = position
                    player_stats += f"{position},"
                
                else:
                    player_stats += f"{player_positions[name]},"
                
            else:
                stat = s.text.strip()
                player_stats += f"{stat},"
         
        week_stats += f"{player_stats}{week},\n"
        print(f"{name} done.")

    return week_stats


if __name__ == "__main__":
    with open ("weekly.csv", "w") as f:
        csv = ""
        player_positions = {}
        for i in range(1,15):
            print(f"{'='*20}\nScraping week {i}...\n{'='*20}")
            csv += scrape_week_stats(i, player_positions)

        f.write(csv)
