import requests
from pprint import pprint
from sty import fg, ef


def getInfo(call):
    r = requests.get(call)
    return r.json()


isUUID = False
name = "ShamanOnly"
uuid = "c8db30d3-b1b0-49d7-9b60-1b29a782b4fd"
five_completions = False
enforce_limits = False
max_useful = False
additional_information = True

# Max stats for goals
max_stats = {"total": 1690, "combat": 106, "gathering": 132, "crafting": 132}
if max_useful:
    max_stats = {"total": 1369, "combat": 105, "gathering": 110, "crafting": 103}


url = f"https://api.wynncraft.com/v2/player/{uuid if isUUID else name}/stats"
resp = getInfo(url)


def color_percentage(color_value):
    if color_value >= 1:
        return ef.bold + fg(0, 255, 0) + f" {color_value:>7.3%} " + fg.rs + ef.rs

    if color_value <= 0:
        return ef.bold + fg(255, 0, 0) + f" {color_value:>7.3%} " + fg.rs + ef.rs

    green_value = min(round(color_value * 510), 255)
    red_value = min(abs(510 - round(color_value * 510)), 255)

    return fg(red_value, green_value, 0) + f" {color_value:>7.3%} " + fg.rs


def show_total_progress(stats):
    # Big ones
    print(
        f"{(ef.bold + 'Total Level' + ef.rs):^61}| {stats['Level']:>7,} / {(max_total := max_stats['total'] * max_classes):>6,}  |"
        f" {color_percentage(stats['Level'] / max_total)}")
    print(f"{(ef.bold + 'Combat' + ef.rs):^61}| {stats['Combat']:>7,} / {(max_combat := max_stats['combat'] * max_classes):>6,}  |"
          f" {color_percentage(stats['Combat'] / max_combat)}")

    # Profs
    for prof in ["Farming", "Fishing", "Mining", "Woodcutting"]:
        print(f"{(fg(197, 118, 246) + prof + fg.rs):^46}| {stats[prof]:>7,} /"
              f" {(single_prof_level := max_stats['gathering'] * max_classes):>6,}  | {color_percentage(stats[prof] / single_prof_level)}")
    
    for prof in ["Alchemism", "Armouring", "Cooking", "Jeweling", "Scribing", "Tailoring", "Weaponsmithing", "Woodworking"]:
        print(f"{(fg(197, 118, 246) + prof + fg.rs):^46}| {stats[prof]:>7,} /"
              f" {(single_prof_level := max_stats['crafting'] * max_classes):>6,}  | {color_percentage(stats[prof] / single_prof_level)}")

    # Quests
    print(f"{(fg(0, 150, 255) + 'Main Quests' + fg.rs):^44}| {stats['Quests']:>7,} /"
          f" {(total_quests := 135 * max_classes):>6,}  |"
          f" {color_percentage(stats['Quests'] / total_quests)}")
    print(f"{(fg(0, 150, 255) + 'Slaying Mini-Quests' + fg.rs):^44}|"
          f" {stats['Slaying Mini-Quests']:>7,} / {(total_slaying := max_classes * 29):>6}  |"
          f" {color_percentage(stats['Slaying Mini-Quests'] / total_slaying)}")
    print(f"{(fg(0, 150, 255) + 'Gathering Mini-Quests' + fg.rs):^44}|"
          f" {stats['Gathering Mini-Quests']:>7,} / {(total_gathering := 96 * max_classes):>6,}  |"
          f" {color_percentage(stats['Gathering Mini-Quests'] / total_gathering)}")

    # # # Completionist
    print(f"{(fg(46, 204, 113) + 'Discoveries' + fg.rs):^45}|"
          f" {stats['Discoveries']:>7,} / {(total_discoveries := (249 + 406) * max_classes):>6,}  |"
          f" {color_percentage(stats['Discoveries'] / total_discoveries)}")
    
    # Dungeons
    print(f"{(fg(46, 204, 113) + 'Unique Dungeons' + fg.rs):^45}|"
          f" {stats['Unique Dungeon Completions']:>7,} / {(total_dungeons := max_classes * 17):>6,}  |"
          f" {color_percentage(stats['Unique Dungeon Completions'] / total_dungeons)}")
    if five_completions:
        print(f"{(fg(46, 204, 113) + 'Dungeon Completions' + fg.rs):^45}|"
              f" {stats['Dungeon Completions']:>7,} / {(five_dungeons := max_classes * 85):>6}  |"
              f" {color_percentage(stats['Dungeon Completions'] / five_dungeons)}")

    # Raids
    print(f"{(fg(46, 204, 113) + 'Unique Raids' + fg.rs):^45}|"
          f" {stats['Unique Raid Completions']:>7,} / {(total_raids := 3 * max_classes):>6,}  |"
          f" {color_percentage(stats['Unique Raid Completions'] / total_raids)}")
    if five_completions:
        print(f"{(fg(46, 204, 113) + 'Raid Completions' + fg.rs):^45}|"
              f" {stats['Raid Completions']:>7,} / {(five_raids := max_classes * 15):>6}  |"
              f" {color_percentage(stats['Raid Completions'] / five_raids)}")
    
    # Extra Info
    if additional_information:
        print(f"{(fg(255, 192, 203) + 'Mobs Killed' + fg.rs):^46}|"
              f" {stats['Mobs Killed']:>16,}")
        print(f"{(fg(255, 192, 203) + 'Blocks Walked' + fg.rs):^46}|"
              f" {stats['Blocks Walked']:>16,}")


classes = resp["data"][0]["classes"]
rank = resp["data"][0]['meta']['tag']['value']
max_classes = {None: 6, "VIP": 9, "VIP+": 11, "HERO": 14, "CHAMPION": 14}[rank]
shamans = []
account_total = {
    "Level": 0,
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
    "Raid Completions": 0,
    "Mobs Killed": 0,
    "Blocks Walked": 0,
}
class_totals = {}

for wynn_class in classes:

    # Class link
    cur_class = [wynn_class["name"],
                 wynn_class["professions"]["combat"]["level"] + wynn_class["professions"]["combat"]["xp"] / 100]

    # Quest sorting
    content_quests = 0
    slaying_quests = 0
    prof_quests = 0
    for quest in wynn_class["quests"]["list"]:
        if "Mini-Quest - Gather" in quest:
            prof_quests += 1
        elif "Mini-Quest" in quest:
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
        "Mobs Killed": wynn_class["mobsKilled"],
        "Blocks Walked": wynn_class["blocksWalked"] if wynn_class["blocksWalked"] > 0 else wynn_class["blocksWalked"] + 4294967296,
    }

    if enforce_limits:
        class_totals[wynn_class["name"]]["Discoveries"] = min(class_totals[wynn_class["name"]]["Discoveries"], 655)
    
    if max_useful:
        # Total
        class_totals[wynn_class["name"]]["Level"] = min(class_totals[wynn_class["name"]]["Level"], 1369)
        # Combat
        class_totals[wynn_class["name"]]["Combat"] = min(class_totals[wynn_class["name"]]["Combat"], 105)
        # Gatherings
        for prof in ["Farming", "Fishing", "Mining", "Woodcutting"]:
            class_totals[wynn_class["name"]][prof] = min(class_totals[wynn_class["name"]][prof], 110)
        # Craftings
        for prof in ["Alchemism", "Armouring", "Cooking", "Jeweling", "Scribing", "Tailoring", "Weaponsmithing", "Woodworking"]:
            class_totals[wynn_class["name"]][prof] = min(class_totals[wynn_class["name"]][prof], 103)
        

    # Add values to total
    for key, value in account_total.items():
        account_total[key] = value + class_totals[wynn_class["name"]][key]

    # Append to account list
    shamans.append(tuple(cur_class))

shamans.sort(key=lambda x: -x[1])

# Shows order of your classes id sorted by combat xp 
# pprint(shamans)

# Header
print(f"""{f"{ef.bold + ef.u}{resp['data'][0]['username']}'s Road to {'Completionist' if not max_useful else 'Max Useful'}{ef.rs}":^96}\n""")

# Main data
show_total_progress(account_total)
