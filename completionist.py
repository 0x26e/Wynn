import requests
from pprint import pprint
from sty import fg, ef, rs


def getInfo(call):
    r = requests.get(call)
    return r.json()

isUUID = True
name = "ShamanOnly"
uuid = "c8db30d3-b1b0-49d7-9b60-1b29a782b4fd"
fiveCompletions = False

url = f"https://api.wynncraft.com/v2/player/{uuid if isUUID else name}/stats"
resp = getInfo(url)

def color_percentage(value):

    if(value >= 1):
        return ( ef.bold + fg(0, 255, 0) + f" {value:>7.3%} " + fg.rs + ef.rs)
    
    if(value <= 0):
        return ( ef.bold + fg(255, 0, 0) + f" {value:>7.3%} " + fg.rs + ef.rs)

    green_value = min( round(value * 510) , 255)
    red_value = min( abs( 510 - round(value * 510) ) , 255)

    return ( fg(red_value, green_value, 0) + f" {f'{value:.3%}'.rjust(7, ' ')} " + fg.rs)


def show_total_progress(stats):
    # Big ones
    print(f"""{(ef.bold + 'Total Level' + ef.rs):^61}| {stats['Level']:>7,} / {'23,660':>6}  | { color_percentage( stats['Level'] / 23660 ) }""")
    print(f"""{(ef.bold + 'Combat' + ef.rs):^61}| {stats['Combat']:>7,} / {'1,484':>6}  | { color_percentage( stats['Combat'] / 1484 ) }""")

    # Profs
    for prof in ["Farming", "Fishing", "Mining", "Woodcutting", "Alchemism", "Armouring", "Cooking", "Jeweling", "Scribing", "Tailoring", "Weaponsmithing", "Woodworking"]:
        print(f"""{(fg(197, 118, 246) + prof + fg.rs):^46}| {stats[prof]:>7,} / {'1,848':>6}  | { color_percentage( stats[prof] / 1848 ) }""")

    # Quests
    print(f"""{(fg(0, 150, 255) + 'Main Quests' + fg.rs):^44}| {stats['Quests']:>7,} / {'1,890':>6}  | { color_percentage( stats['Quests'] / 1890 ) }""")
    print(f"""{(fg(0, 150, 255) + 'Slaying Mini-Quests' + fg.rs):^44}| {stats['Slaying Mini-Quests']:>7,} / {'406':>6}  | { color_percentage( stats['Slaying Mini-Quests'] / 406 ) }""")
    print(f"""{(fg(0, 150, 255) + 'Gathering Mini-Quests' + fg.rs):^44}| {stats['Gathering Mini-Quests']:>7,} / {'1,344':>6}  | { color_percentage( stats['Gathering Mini-Quests'] / 1344 ) }""")

    # Completionist
    print(f"""{(fg(46, 204, 113) + 'Discoveries' + fg.rs):^45}| {stats['Discoveries']:>7,} / {'8,320':>6}  | { color_percentage( stats['Discoveries'] / 8320 ) }""")
    print(f"""{(fg(46, 204, 113) + 'Unique Dungeons' + fg.rs):^45}| {stats['Unique Dungeon Completions']:>7,} / {'238':>6}  | { color_percentage( stats['Unique Dungeon Completions'] / 238 ) }""")
    if(fiveCompletions):
        print(f"""{(fg(46, 204, 113) + 'Dungeon Completions' + fg.rs):^45}| {stats['Dungeon Completions']:>7,} / {'1,190':>6}  | { color_percentage( stats['Dungeon Completions'] / 1190 ) }""")
    print(f"""{(fg(46, 204, 113) + 'Unique Raids' + fg.rs):^45}| {stats['Unique Raid Completions']:>7,} / {'42':>6}  | { color_percentage( stats['Unique Raid Completions'] / 42 ) }""")
    if(fiveCompletions):
        print(f"""{(fg(46, 204, 113) + 'Raid Completions' + fg.rs):^45}| {stats['Raid Completions']:>7,} / {'210':>6}  | { color_percentage( stats['Raid Completions'] / 210 ) }""")
    

classes = resp["data"][0]["classes"]
shamans = []
account_total = {
    "Level": 0 ,
    "Combat": 0,
    "Farming": 0,
    "Fishing": 0,
    "Mining": 0,
    "Woodcutting": 0,
    "Alchemism": 0,
    "Armouring": 0,
    "Cooking": 0,
    "Jeweling": 0,
    "Scribing": 0,
    "Tailoring": 0,
    "Weaponsmithing": 0,
    "Woodworking": 0,
    "Quests": 0,
    "Slaying Mini-Quests": 0,
    "Gathering Mini-Quests": 0,
    "Discoveries": 0,
    "Unique Dungeon Completions": 0,
    "Dungeon Completions": 0,
    "Unique Raid Completions": 0,
    "Raid Completions": 0
}
class_totals = {

}

for wynn_class in classes:

    # Class link
    cur_class = [
        wynn_class["name"],
        wynn_class["professions"]["combat"]["level"] + wynn_class["professions"]["combat"]["xp"] / 100
    ]

    # Quest sorting
    content_quests = 0
    slaying_quests = 0
    prof_quests = 0
    for quest in wynn_class["quests"]["list"]:
        if("Mini-Quest - Gather" in quest):
            prof_quests += 1
        elif("Mini-Quest" in quest):
            slaying_quests += 1
        else:
            content_quests += 1
    
    dungeons_completed = 0
    for dungeon in wynn_class["dungeons"]["list"]:
        dungeons_completed += min(dungeon["completed"], 5)
    
    raids_completed = 0
    for raid in wynn_class["raids"]["list"]:
        raids_completed += min(raid["completed"], 5)

    # Class info
    class_totals[wynn_class["name"]] = {
        "Level": wynn_class["level"] + 12,
        "Combat": wynn_class["professions"]["combat"]["level"],
        "Farming": wynn_class["professions"]["farming"]["level"],
        "Fishing": wynn_class["professions"]["fishing"]["level"],
        "Mining": wynn_class["professions"]["mining"]["level"],
        "Woodcutting": wynn_class["professions"]["woodcutting"]["level"],
        "Alchemism": wynn_class["professions"]["alchemism"]["level"],
        "Armouring": wynn_class["professions"]["armouring"]["level"],
        "Cooking": wynn_class["professions"]["cooking"]["level"],
        "Jeweling": wynn_class["professions"]["jeweling"]["level"],
        "Scribing": wynn_class["professions"]["scribing"]["level"],
        "Tailoring": wynn_class["professions"]["tailoring"]["level"],
        "Weaponsmithing": wynn_class["professions"]["weaponsmithing"]["level"],
        "Woodworking": wynn_class["professions"]["woodworking"]["level"],
        "Quests": content_quests,
        "Slaying Mini-Quests": slaying_quests,
        "Gathering Mini-Quests": prof_quests,
        "Discoveries": wynn_class["discoveries"],
        "Unique Dungeon Completions": len(wynn_class["dungeons"]["list"]),
        "Dungeon Completions": dungeons_completed,
        "Unique Raid Completions": len(wynn_class["raids"]["list"]),
        "Raid Completions": raids_completed,
    }

    # Add values to total
    for key, value in account_total.items():
        account_total[key] = value + class_totals[wynn_class["name"]][key]

    # Append to account list
    shamans.append( tuple(cur_class) )

shamans.sort(key = lambda x: -x[1])

# Shows order of your classes id sorted by combat xp 
# pprint(shamans)

show_total_progress(account_total)
