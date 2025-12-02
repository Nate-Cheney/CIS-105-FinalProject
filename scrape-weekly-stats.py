from bs4 import BeautifulSoup
import requests


def scrape_week_stats(week: str):
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
    for row in rows:
        data = row.find_all("td")
        player_stats = ""
        for i,s in enumerate(data):
            if i == 0:
                names_array = s.text.strip().split()
                name = f"{names_array[0]} {names_array[1]}"
                player_stats += f"{name},"
            else:
                stat = s.text.strip()
                player_stats += f"{stat},"
        
        week_stats += f"{player_stats}{week},\n"

    return week_stats


if __name__ == "__main__":
    with open ("weekly.csv", "w") as f:
        csv = ""
        for i in range(1,15):
            csv += scrape_week_stats(i)

        f.write(csv)
