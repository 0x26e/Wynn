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
        f"{(ef.bold + 'Total Level' + ef.rs):^61}| {stats['Level']:>7,} / {(max_total := max_stats['total'] * max_characters):>6,}  |"
        f" {color_percentage(stats['Level'] / max_total)}")
    print(f"{(ef.bold + 'Combat' + ef.rs):^61}| {stats['Combat']:>7,} / {(max_combat := max_stats['combat'] * max_characters):>6,}  |"
          f" {color_percentage(stats['Combat'] / max_combat)}")

    # Profs
    for prof in ["Farming", "Fishing", "Mining", "Woodcutting"]:
        print(f"{(fg(197, 118, 246) + prof + fg.rs):^46}| {stats[prof]:>7,} /"
              f" {(single_prof_level := max_stats['gathering'] * max_characters):>6,}  | {color_percentage(stats[prof] / single_prof_level)}")
    
    for prof in ["Alchemism", "Armouring", "Cooking", "Jeweling", "Scribing", "Tailoring", "Weaponsmithing", "Woodworking"]:
        print(f"{(fg(197, 118, 246) + prof + fg.rs):^46}| {stats[prof]:>7,} /"
              f" {(single_prof_level := max_stats['crafting'] * max_characters):>6,}  | {color_percentage(stats[prof] / single_prof_level)}")

    # Quests
    print(f"{(fg(0, 150, 255) + 'Main Quests' + fg.rs):^44}| {stats['Quests']:>7,} /"
          f" {(total_quests := 138 * max_characters):>6,}  |"
          f" {color_percentage(stats['Quests'] / total_quests)}")
    print(f"{(fg(0, 150, 255) + 'Slaying Mini-Quests' + fg.rs):^44}|"
          f" {stats['Slaying Mini-Quests']:>7,} / {(total_slaying := max_characters * 29):>6}  |"
          f" {color_percentage(stats['Slaying Mini-Quests'] / total_slaying)}")
    print(f"{(fg(0, 150, 255) + 'Gathering Mini-Quests' + fg.rs):^44}|"
          f" {stats['Gathering Mini-Quests']:>7,} / {(total_gathering := 96 * max_characters):>6,}  |"
          f" {color_percentage(stats['Gathering Mini-Quests'] / total_gathering)}")

    # # # Completionist
    print(f"{(fg(46, 204, 113) + 'Discoveries' + fg.rs):^45}|"
          f" {stats['Discoveries']:>7,} / {(total_discoveries := (105 + 494) * max_characters):>6,}  |"
          f" {color_percentage(stats['Discoveries'] / total_discoveries)}")
    
    # Dungeons
    print(f"{(fg(46, 204, 113) + 'Unique Dungeons' + fg.rs):^45}|"
          f" {stats['Unique Dungeon Completions']:>7,} / {(total_dungeons := max_characters * 17):>6,}  |"
          f" {color_percentage(stats['Unique Dungeon Completions'] / total_dungeons)}")
    if five_completions:
        print(f"{(fg(46, 204, 113) + 'Dungeon Completions' + fg.rs):^45}|"
              f" {stats['Dungeon Completions']:>7,} / {(five_dungeons := max_characters * 85):>6}  |"
              f" {color_percentage(stats['Dungeon Completions'] / five_dungeons)}")

    # Raids
    print(f"{(fg(46, 204, 113) + 'Unique Raids' + fg.rs):^45}|"
          f" {stats['Unique Raid Completions']:>7,} / {(total_raids := 3 * max_characters):>6,}  |"
          f" {color_percentage(stats['Unique Raid Completions'] / total_raids)}")
    if five_completions:
        print(f"{(fg(46, 204, 113) + 'Raid Completions' + fg.rs):^45}|"
              f" {stats['Raid Completions']:>7,} / {(five_raids := max_characters * 15):>6}  |"
              f" {color_percentage(stats['Raid Completions'] / five_raids)}")
    
    # Extra Info
    if additional_information:
        print(f"{(fg(255, 192, 203) + 'Mobs Killed' + fg.rs):^46}|"
              f" {stats['Mobs Killed']:>16,}")
        print(f"{(fg(255, 192, 203) + 'Blocks Walked' + fg.rs):^46}|"
              f" {stats['Blocks Walked']:>16,}")


characters = resp["data"][0]["characters"]
rank = resp["data"][0]['meta']['tag']['value']
max_characters = {None: 6, "VIP": 9, "VIP+": 11, "HERO": 14, "CHAMPION": 14}[rank]
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
char_totals = {}

for char_uuid, wynn_char in characters.items():

    # Class link
    cur_char = [char_uuid,
                 wynn_char["professions"]["combat"]["level"] + wynn_char["professions"]["combat"]["xp"] / 100]

    # Quest sorting
    content_quests = 0
    slaying_quests = 0
    prof_quests = 0
    for quest in wynn_char["quests"]["list"]:
        if "Mini-Quest - Gather" in quest:
            prof_quests += 1
        elif "Mini-Quest" in quest:
            slaying_quests += 1
        else:
            content_quests += 1

    dungeons_completed = 0
    for dungeon in wynn_char["dungeons"]["list"]:
        dungeons_completed += min(dungeon["completed"], 5)

    raids_completed = 0
    for raid in wynn_char["raids"]["list"]:
        raids_completed += min(raid["completed"], 5)

    # Class info
    char_totals[char_uuid] = {
        "Level": wynn_char["level"] + 12,
        "Combat": wynn_char["professions"]["combat"]["level"],
        "Farming": wynn_char["professions"]["farming"]["level"],
        "Fishing": wynn_char["professions"]["fishing"]["level"],
        "Mining": wynn_char["professions"]["mining"]["level"],
        "Woodcutting": wynn_char["professions"]["woodcutting"]["level"],
        "Alchemism": wynn_char["professions"]["alchemism"]["level"],
        "Armouring": wynn_char["professions"]["armouring"]["level"],
        "Cooking": wynn_char["professions"]["cooking"]["level"],
        "Jeweling": wynn_char["professions"]["jeweling"]["level"],
        "Scribing": wynn_char["professions"]["scribing"]["level"],
        "Tailoring": wynn_char["professions"]["tailoring"]["level"],
        "Weaponsmithing": wynn_char["professions"]["weaponsmithing"]["level"],
        "Woodworking": wynn_char["professions"]["woodworking"]["level"],
        "Quests": content_quests,
        "Slaying Mini-Quests": slaying_quests,
        "Gathering Mini-Quests": prof_quests,
        "Discoveries": wynn_char["discoveries"],
        "Unique Dungeon Completions": len(wynn_char["dungeons"]["list"]),
        "Dungeon Completions": dungeons_completed,
        "Unique Raid Completions": len(wynn_char["raids"]["list"]),
        "Raid Completions": raids_completed,
        "Mobs Killed": wynn_char["mobsKilled"],
        "Blocks Walked": wynn_char["blocksWalked"] if wynn_char["blocksWalked"] > 0 else wynn_char["blocksWalked"] + 4294967296,
    }

    if enforce_limits:
        char_totals[char_uuid]["Discoveries"] = min(char_totals[char_uuid]["Discoveries"], 655)
    
    if max_useful:
        # Total
        char_totals[char_uuid]["Level"] = min(char_totals[char_uuid]["Level"], 1369)
        # Combat
        char_totals[char_uuid]["Combat"] = min(char_totals[char_uuid]["Combat"], 105)
        # Gatherings
        for prof in ["Farming", "Fishing", "Mining", "Woodcutting"]:
            char_totals[char_uuid][prof] = min(char_totals[char_uuid][prof], 110)
        # Craftings
        for prof in ["Alchemism", "Armouring", "Cooking", "Jeweling", "Scribing", "Tailoring", "Weaponsmithing", "Woodworking"]:
            char_totals[char_uuid][prof] = min(char_totals[char_uuid][prof], 103)
        

    # Add values to total
    for key, value in account_total.items():
        account_total[key] = value + char_totals[char_uuid][key]

    # Append to account list
    shamans.append(tuple(cur_char))

shamans.sort(key=lambda x: -x[1])

# Shows order of your characters id sorted by combat xp 
pprint(shamans)

# Header
print(f"""{f"{ef.bold + ef.u}{resp['data'][0]['username']}'s Road to {'Completionist' if not max_useful else 'Max Useful'}{ef.rs}":^96}\n""")

# Main data
show_total_progress(account_total)
