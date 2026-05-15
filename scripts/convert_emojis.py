import json
import sys


def add_logtime(body: str, sep: str, comment: str, dt: str) -> str:
    words = body.split()
    try:
        _ = words.index("--dt")
        return " ".join([body, sep, comment])
    except ValueError:
        pass

    if sep:
        new_line = " ".join([body, "--dt", dt, sep, comment])
    else:
        new_line = " ".join([body, "--dt", dt])
    return new_line


def remove_options(line: str, dt: str) -> str:
    words = line.split()
    clean: list[str] = []

    i = 0
    while i < len(words):
        word = words[i]

        if word == "--dt":
            if i + 1 >= len(words):
                raise ValueError("--dt requires a value")

            if words[i + 1] == dt:
                i += 2
                continue
        clean.append(word)
        i += 1
    return " ".join(clean)


def replace_emoji(line: str) -> str:
    body, sep, comment = line.partition("#")
    tokens = tuple(body.split())
    eb = tokens[0].encode()
    try:
        name = EMOJIS[eb]
    except KeyError:
        print("NO EMOJIS FOUND", eb.decode())
        return line
    try:
        eb = single_char2complete[eb]
    except KeyError:
        pass
    e = eb.decode()
    if name.lower() == "bjj" or name == "grappling":
        unit_name = "grappling"
    elif name == "boxing":
        unit_name = "boxing"
    elif name == "globe":
        unit_name = "log"
    elif name == "barbell":
        unit_name = "barbell"
    elif name == "kyokushin":
        unit_name = "kyokushin"
    elif name == "shark":
        unit_name = "swimming"
    elif name == "helicopter":
        unit_name = "benchpress"
    elif name == "seal":
        unit_name = "overheadpress"
    elif name == "shinto" or name == "1_shinto":
        unit_name = "squat"
    elif name == "construction_site" or name == "1_construction_site":
        unit_name = "deadlift"
    elif name == "turtle":
        unit_name = "rows"
    elif name == "cyborg_arm":
        unit_name = "curls"
    elif name == "saturn":
        unit_name = "wimhof"
    elif name == "sword" or name == "1_sword":
        unit_name = "split_machine"
    elif name == "bison":
        unit_name = "shrugs"
    elif name == "magnet":
        unit_name = "core"
    elif name == "helmet" or name == "sneaker":
        unit_name = "running"
    elif name == "satellite":
        unit_name = "work"
    elif name == "eight_ball":
        unit_name = "shoulders"
    elif name == "balance" or name == "1_balance":
        unit_name = "scale"
    elif name == "scissors" or name == "1_scissors":
        unit_name = "stretching"
    elif name == "reminder_ribbon" or name == "1_reminder_ribbon":
        unit_name = "skipping"
    elif name == "eagle":
        unit_name = "pullups"
    elif name == "1_orbital" or name == "orbital":
        unit_name = "work"
    else:
        unit_name = e
        print("unit", unit_name, "emoji", e.encode())
    new_line = line.replace(e, unit_name, count=1)
    return new_line


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python convert_emojis.py <file.json>")

    with open(sys.argv[1], "r") as f:
        data = json.load(f)

    lst = []
    for item in data:
        line = item["line"]
        line = remove_options(line, item["local_datetime"])
        body, sep, comment = line.partition("#")
        line = add_logtime(body, sep, comment, item["local_datetime"])
        lst.append({"line": line, "local_datetime": item["local_datetime"]})

    with open("units.json", "w") as f:
        f.write(json.dumps(lst, indent=2, ensure_ascii=False))


EMOJIS = {
    b"kyokushin": "kyokushin",
    b"barbell": "barbell",
    b"grappling": "grappling",
    b"bjj": "grappling",
    b"BJJ": "grappling",
    b"boxing": "boxing",
    # animals
    b"\xf0\x9f\xa6\x8d": "gorilla",
    b"\xf0\x9f\xa6\x88": "shark",
    b"\xf0\x9f\x90\x9d": "honeybee",
    b"\xf0\x9f\x90\xa2": "turtle",
    b"\xf0\x9f\xa6\xad": "seal",
    b"\xf0\x9f\x90\x87": "rabbit",
    b"\xf0\x9f\xa6\xa1": "badger",
    b"\xf0\x9f\x90\xa7": "penguin",
    b"\xf0\x9f\xa6\x89": "owl",
    b"\xf0\x9f\x90\x82": "ox",
    b"\xf0\x9f\xa6\x85": "eagle",
    b"\xf0\x9f\x90\xba": "wolf",
    b"\xf0\x9f\xa6\x8f": "rhino",
    b"\xf0\x9f\x90\x85": "tiger",
    b"\xf0\x9f\x90\x8e": "horse",
    b"\xf0\x9f\xa6\xac": "bison",
    b"\xf0\x9f\x90\xbc": "panda_bear",
    b"\xf0\x9f\xa6\xa5": "climbing_ape",
    b"\xf0\x9f\x95\x8a": "1_dove",
    b"\xf0\x9f\x95\x8a\xef\xb8\x8f": "dove",
    b"\xf0\x9f\x95\xb8\xef\xb8\x8f": "spiderweb",
    # nature
    b"\xf0\x9f\x8c\xaa": "1_tornado",
    b"\xf0\x9f\x8c\xaa\xef\xb8\x8f": "tornado",
    b"\xf0\x9f\x8c\xb4": "palm_tree",
    b"\xf0\x9f\xa7\xac": "dna",
    b"\xe2\x98\xa0": "1_dead",
    b"\xe2\x98\xa0\xef\xb8\x8f": "dead",
    b"\xf0\x9f\xaa\x90": "saturn",
    b"\xe2\x98\x95\xef\xb8\x8f": "coffee",
    b"\xf0\x9f\x94\xa5": "fire",
    b"\xf0\x9f\x8d\x93": "strawberry",
    b"\xf0\x9f\x91\xbd": "alien",
    b"\xf0\x9f\x8c\x8b": "volcano",
    b"\xe2\x9c\xa8": "stars",
    # military
    b"\xf0\x9f\x8e\x96": "1_military_medal",
    b"\xf0\x9f\x8e\x96\xef\xb8\x8f": "military_medal",
    b"\xf0\x9f\xaa\x96": "helmet",
    b"\xe2\x9a\x94": "1_sword",
    b"\xe2\x9a\x94\xef\xb8\x8f": "sword",
    b"\xf0\x9f\x8f\xb9": "cross_and_bow",
    b"\xf0\x9f\x9b\xa1\xef\xb8\x8f": "shield",
    b"\xf0\x9f\x94\xb1": "trident",
    b"\xf0\x9f\x92\xa3": "bomb",
    b"\xf0\x9f\x97\xa1": "dagger",
    # training
    b"\xf0\x9f\xa5\x8a": "boxing_gloves",
    b"\xf0\x9f\xa5\x8b": "martial_arts",
    # tech
    b"\xf0\x9f\x93\xa1": "satellite",
    b"\xf0\x9f\x9b\xb0": "1_orbital",
    b"\xf0\x9f\x9b\xb0\xef\xb8\x8f": "orbital",
    b"\xf0\x9f\xa6\xbe": "cyborg_arm",
    b"\xf0\x9f\xa6\xbf": "cyborg_leg",
    b"\xf0\x9f\x94\xad": "telescope",
    b"\xf0\x9f\x94\xac": "micro",
    b"\xf0\x9f\x9b\xb8": "flying_saucer",
    b"\xf0\x9f\xa7\xb2": "magnet",
    b"\xf0\x9f\xa7\xaa": "chemical",
    b"\xf0\x9f\x8c\x90": "globe",
    b"\xf0\x9f\x8c\x80": "spiral",
    b"\xe2\x9a\xa1": "1_electro",
    b"\xe2\x9a\xa1\xef\xb8\x8f": "electro",
    b"\xf0\x9f\xaa\xa9": "disco",
    b"\xf0\x9f\x94\x8c": "plug",
    b"\xf0\x9f\x94\x8b": "battery",
    b"\xe2\x9a\x93": "1_anchor",
    b"\xe2\x9a\x93\xef\xb8\x8f": "anchor",
    b"\xe2\x9b\x93": "1_chains",
    b"\xe2\x9b\x93\xef\xb8\x8f": "chains",
    b"\xf0\x9f\x92\xa1": "light_bulb",
    # transport
    b"\xf0\x9f\x9a\x80": "rocket",
    b"\xf0\x9f\x9b\xab": "airplane_departure",
    b"\xf0\x9f\x9a\x81": "helicopter",
    b"\xf0\x9f\x9a\x82": "locomotive",
    b"\xf0\x9f\x9a\x88": "train",
    b"\xf0\x9f\x91\x9f": "sneaker",
    b"\xf0\x9f\x9b\xb6": "rowboat",
    b"\xf0\x9f\x9a\xb2": "bike",
    b"\xf0\x9f\x9b\xa9": "1_small_airplane",
    b"\xf0\x9f\x9b\xa9\xef\xb8\x8f": "small_airplane",
    b"\xf0\x9f\x9b\xb7": "sled",
    # buildings
    b"\xf0\x9f\x8f\x97": "1_construction_site",
    b"\xf0\x9f\x8f\x97\xef\xb8\x8f": "construction_site",
    b"\xe2\x9b\xa9": "1_shinto",
    b"\xe2\x9b\xa9\xef\xb8\x8f": "shinto",
    b"\xf0\x9f\x8f\x9b": "1_greek_house",
    b"\xf0\x9f\x8f\x9b\xef\xb8\x8f": "greek_house",
    b"\xf0\x9f\x8f\xaf": "japanese_castle",
    b"\xe2\x9b\xaa": "1_church",
    b"\xe2\x9b\xaa\xef\xb8\x8f": "church",
    # symbols
    b"\xe2\x98\xa3": "1_biohazard",
    b"\xe2\x98\xa3\xef\xb8\x8f": "biohazard",
    b"\xe2\x98\xa2": "1_radioactive",
    b"\xe2\x98\xa2\xef\xb8\x8f": "radioactive",
    b"\xe2\x98\xaf": "1_yinyang",
    b"\xe2\x98\xaf\xef\xb8\x8f": "yinyang",
    b"\xe2\x98\xb8": "1_wheel_of_buddha",
    b"\xe2\x98\xb8\xef\xb8\x8f": "wheel_of_buddha",
    # achievements
    b"\xf0\x9f\x8f\x85": "sport_medal",
    b"\xf0\x9f\xa5\x87": "gold_medal",
    b"\xf0\x9f\xa5\x88": "silver_medal",
    b"\xf0\x9f\xa5\x89": "bronze_medal",
    b"\xf0\x9f\x8f\x86": "trophy",
    # objects
    b"\xe2\x9a\x96": "1_balance",
    b"\xe2\x9a\x96\xef\xb8\x8f": "balance",
    b"\xe2\x9c\x82": "1_scissors",
    b"\xe2\x9c\x82\xef\xb8\x8f": "scissors",
    b"\xf0\x9f\xaa\x83": "boomerang",
    b"\xf0\x9f\x8c\xac": "wind_face",
    b"\xf0\x9f\x8e\x97": "1_reminder_ribbon",
    b"\xf0\x9f\x8e\x97\xef\xb8\x8f": "reminder_ribbon",
    b"\xf0\x9f\x92\xb4": "money_plus",
    b"\xf0\x9f\x92\xb8": "money_minus",
    b"\xf0\x9f\x92\xbb": "laptop",
    b"\xf0\x9f\x93\x96": "book",
    b"\xf0\x9f\x91\xbb": "ghost",
    b"\xf0\x9f\x94\x91": "key",
    b"\xf0\x9f\x8e\xa1": "ferris_wheel",
    b"\xf0\x9f\x8e\xa3": "fishing_rod",
    b"\xf0\x9f\x92\x8a": "pill",
    b"\xf0\x9f\xa5\x8f": "frisbee",
    b"\xf0\x9f\x92\x8e": "gem_stone",
    b"\xf0\x9f\x92\xa6": "sweat_drops",
    b"\xf0\x9f\x91\x99": "bikini",
    b"\xe2\x99\x9f": "1_chess_pawn",
    b"\xe2\x99\x9f\xef\xb8\x8f": "chess_pawn",
    b"\xf0\x9f\xab\xa7": "bubble",
    b"\xf0\x9f\x8e\xb1": "eight_ball",
}


single_char2complete = {
    # dove
    b"\xf0\x9f\x95\x8a": b"\xf0\x9f\x95\x8a\xef\xb8\x8f",
    # tornado
    b"\xf0\x9f\x8c\xaa": b"\xf0\x9f\x8c\xaa\xef\xb8\x8f",
    # dead
    b"\xe2\x98\xa0": b"\xe2\x98\xa0\xef\xb8\x8f",
    # military medal
    b"\xf0\x9f\x8e\x96": b"\xf0\x9f\x8e\x96\xef\xb8\x8f",
    # sword
    b"\xe2\x9a\x94": b"\xe2\x9a\x94\xef\xb8\x8f",
    # orbital
    b"\xf0\x9f\x9b\xb0": b"\xf0\x9f\x9b\xb0\xef\xb8\x8f",
    # electro
    b"\xe2\x9a\xa1": b"\xe2\x9a\xa1\xef\xb8\x8f",
    # anchor
    b"\xe2\x9a\x93": b"\xe2\x9a\x93\xef\xb8\x8f",
    # chains
    b"\xe2\x9b\x93": b"\xe2\x9b\x93\xef\xb8\x8f",
    # small airplane
    b"\xf0\x9f\x9b\xa9": b"\xf0\x9f\x9b\xa9\xef\xb8\x8f",
    # crane
    b"\xf0\x9f\x8f\x97": b"\xf0\x9f\x8f\x97\xef\xb8\x8f",
    # shinto
    b"\xe2\x9b\xa9": b"\xe2\x9b\xa9\xef\xb8\x8f",
    # greek house
    b"\xf0\x9f\x8f\x9b": b"\xf0\x9f\x8f\x9b\xef\xb8\x8f",
    # church
    b"\xe2\x9b\xaa": b"\xe2\x9b\xaa\xef\xb8\x8f",
    # biohazard
    b"\xe2\x98\xa3": b"\xe2\x98\xa3\xef\xb8\x8f",
    # radioactive
    b"\xe2\x98\xa2": b"\xe2\x98\xa2\xef\xb8\x8f",
    # yinyang
    b"\xe2\x98\xaf": b"\xe2\x98\xaf\xef\xb8\x8f",
    # wheel of buddha
    b"\xe2\x98\xb8": b"\xe2\x98\xb8\xef\xb8\x8f",
    # balance
    b"\xe2\x9a\x96": b"\xe2\x9a\x96\xef\xb8\x8f",
    # scissors
    b"\xe2\x9c\x82": b"\xe2\x9c\x82\xef\xb8\x8f",
    # reminder ribbon
    b"\xf0\x9f\x8e\x97": b"\xf0\x9f\x8e\x97\xef\xb8\x8f",
    # chess pawn
    b"\xe2\x99\x9f": b"\xe2\x99\x9f\xef\xb8\x8f",
}


if __name__ == "__main__":
    main()
