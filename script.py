import requests
import os
import json

def get_latest_ddragon_version():
    try:
        response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        response.raise_for_status()
        versions = response.json()
        return versions[0]  
    except requests.RequestException as e:
        print(f"Error fetching Data Dragon version: {e}")
        return None

def get_champion_data(version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["data"]
    except requests.RequestException as e:
        print(f"Error fetching champion data: {e}")
        return None

def download_champion_icon(champion_name, version, save_folder="champion_icons"):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    champion_data = get_champion_data(version)
    if not champion_data:
        return
    
    champion = None
    for champ_id, data in champion_data.items():
        if data["name"] == champion_name:
            champion = data
            break
    
    if not champion:
        print(f"Champion {champion_name} not found")
        return
    
    champion_id = champion["id"]
    file_name = f"{champion_id}Square.png"
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion_id}.png"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        if 'image/png' not in response.headers.get('Content-Type', ''):
            print(f"Image not found for {champion_name}")
            return
        
        save_path = os.path.join(save_folder, file_name)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {champion_name} icon to {save_path}")
        
    except requests.RequestException as e:
        print(f"Error downloading {champion_name} icon: {e}")

if __name__ == "__main__":
    version = get_latest_ddragon_version()
    if not version:
        print("Cannot proceed without a valid Data Dragon version")
        exit(1)
    
    champions = ["Yone", "Aurora", "Skarner", "Ashe", "Jax", "Rell", "Kalista", "Gnar",
                 "Ziggs", "Kai'Sa", "Vi", "Orianna", "Rumble", "Poppy", "Sejuani", "Ezreal",
                 "Renekton", "Rakan", "Leona", "Jhin", "K'Sante", "Ahri", "Renata Glasc",
                 "Nocturne", "Sylas", "Xayah", "Alistar", "Maokai", "Smolder", "Braum", "Lucian",
                 "Wukong", "Syndra", "Nautilus", "Neeko", "Akali", "Nidalee", "Ivern", "Miss Fortune",
                 "LeBlanc", "Tristana", "Varus", "Brand", "Jarvan IV"]
    for champ in champions:
        download_champion_icon(champ, version)