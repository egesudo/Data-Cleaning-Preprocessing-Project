import pandas as pd
import numpy as np
import re

df = pd.read_csv("global_esports_gaming_messy.csv")

#print(df.head(60))

#print(df["player_id"].duplicated().sum())
df = df.drop_duplicates(subset=["player_id"],keep="first")
#print(df["player_id"].duplicated().sum())
#print(df["player_id"].isnull().sum())

#print(df["gamer_tag"].unique())
df["gamer_tag"] = df["gamer_tag"].fillna("Unknown")
#print(df["gamer_tag"].duplicated().sum())
df = df.drop_duplicates(subset=["gamer_tag"],keep="first")
#print(df["gamer_tag"].isnull().sum())

#print(df["favorite_game"].value_counts())
df["favorite_game"] = df["favorite_game"].replace("cs2","Counter-Strike 2")
#print(df["favorite_game"].value_counts())
#print(df["favorite_game"].isnull().sum())

#print(df["player_rank"].value_counts())
df["player_rank"] = df["player_rank"].replace("gümüş","Silver")
#print(df["player_rank"].isnull().sum())
df["player_rank"]  =df["player_rank"].fillna("Unknown")

df["matches_played"] = df["matches_played"].astype(str).str.replace(r'[^\d-]',"",regex=True)
df["matches_played"] = pd.to_numeric(df["matches_played"],errors="coerce")
df["matches_played"] = df["matches_played"].abs()
avg_match = df["matches_played"].median()
df["matches_played"] = df["matches_played"].fillna(avg_match)
df["matches_played"] = df["matches_played"].astype(int)

df["account_creation_date"] = pd.to_datetime(df["account_creation_date"],format="mixed",errors="coerce")
#print(df["account_creation_date"].info())

#print(df["hardware_type"].unique())

#print(df["preferred_region"].value_counts())
#print(df["preferred_region"].isnull().sum())

df["preferred_region"] = df["preferred_region"].str.strip().str.upper()

correct_region = {

"AVRUPA": "EU West",      
    "EU": "EU West",          
    "NORTH AMERICA": "NA",
    "NA": "NA",
    "ASIA": "Asia",
    "SOUTH AMERICA": "South America",
    "EU EAST": "EU East",
    "EU WEST": "EU West"

}

df["preferred_region"] = df["preferred_region"].replace(correct_region)
df["preferred_region"] = df["preferred_region"].fillna("Unknown")

#print(df["preferred_region"].value_counts())

#print(df["toxicity_reports"].value_counts())
#print(df["toxicity_reports"].isnull().sum())

df["toxicity_reports"] = pd.to_numeric(df["toxicity_reports"],errors="coerce")
df["toxicity_reports"] = df["toxicity_reports"].abs()
df["toxicity_reports"] = df["toxicity_reports"].fillna(0)
df["toxicity_reports"] = df["toxicity_reports"].astype(int)

#print(df["toxicity_reports"].isnull().sum())
#print(df["toxicity_reports"].value_counts())

def convert_playtime(val):
    val = str(val).lower()

    if val == "nan" :
        return np.nan

    val = val.replace(",","")

    if "k" in val :
        val = val.replace("k","")
        return float(val)*1000

    val = re.sub(r'[^\d.]','',val)

    if val == "":
        return np.nan
    return float(val)

df["total_playtime_hours"] = df["total_playtime_hours"].apply(convert_playtime)
avg_playtime = df["total_playtime_hours"].median()
df["total_playtime_hours"] = df["total_playtime_hours"].fillna(avg_playtime)

#print(df.loc[:,"matches_played" : "total_playtime_hours"].head(60))

df["win_rate_percent"] = df["win_rate_percent"].astype(str).str.replace(r'[^\d.]',"",regex=True)
df["win_rate_percent"] = pd.to_numeric(df["win_rate_percent"],errors="coerce")
df.loc[ (df["win_rate_percent"] > 100) | (df["win_rate_percent"] < 0) ,"win_rate_percent"] = np.nan
avg_win_rate = df["win_rate_percent"].median()
df["win_rate_percent"] = df["win_rate_percent"].fillna(avg_win_rate)

#print(df["win_rate_percent"].info())
#print(df["win_rate_percent"].isnull().sum())



df["average_ping_ms"] = df["average_ping_ms"].astype(str).str.replace(r'\D', '', regex=True)
df["average_ping_ms"] = pd.to_numeric(df["average_ping_ms"], errors="coerce")
df.loc[df["average_ping_ms"] > 1000, "average_ping_ms"] = np.nan
avg_ping = df["average_ping_ms"].median()
df["average_ping_ms"] = df["average_ping_ms"].fillna(avg_ping)
df["average_ping_ms"] = df["average_ping_ms"].astype(int)

#print(df["average_ping_ms"].info())
#print(df["average_ping_ms"].isnull().sum())

df.to_csv("Cleaned_global_esports_gaming_dataset.csv")


