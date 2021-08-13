import requests
import json


def rustoria_core(url: str, title: str, tools, round_thousandths=True):
    convert = tools[0]
    target = None
    request = requests.get(url)
    request_status = request.status_code
    if request_status != 200:
        quit("Error making request.")
    json_data = json.loads(request.text.split("var packages = ")[1].split(";\n")[0].strip())
    for server in json_data:
        if server['title'].strip() == title.strip():
            target = server
    if not target:
        exit("No server with title, \"" + title + "\" found")
    target_stock = target['currentstock'].lower().strip()
    title = target['title']
    description = target['description']
    price = convert(target['price'])
    expires = target['expires']
    price = round(price, 2) if round_thousandths else price
    in_stock = (target_stock == "IN STOCK".lower().strip()) or target_stock == "LAST FEW REMAINING".lower().strip()
    game = target['game']
    servers = target['servers'].replace("&quot;", "").replace("[", "").strip("]")
    img = "https://donate.rustoria.co/" + target['img'].replace("\\", "")
    return {'title': title, "description": description, "price": price, "expires": expires, "in_stock": in_stock,
            "game": game, "server": servers, "img": img}


def rustoria_us_main(tools):
    return rustoria_core("https://donate.rustoria.co/packages.php?game=3&server=15", "VIP | US Main", tools)


def rustoria_us_main_wipe(tools):
    return rustoria_core("https://donate.rustoria.co/packages.php?game=3&server=15", "Wipe VIP | US Main", tools)


def rustoria_us_medium(tools):
    return rustoria_core("https://donate.rustoria.co/packages.php?game=3&server=24", "VIP | US Medium", tools)


def rustoria_us_long(tools):
    return rustoria_core("https://donate.rustoria.co/packages.php?game=3&server=25", "VIP | US Long", tools)


def rustoria_us_small(tools):
    return rustoria_core("https://donate.rustoria.co/packages.php?game=3&server=26", "VIP | US Small", tools)


def rustoria_eu_main(tools):
    return rustoria_core("https://donate.rustoria.co/packages.php?game=3&server=19", "VIP | EU Main", tools)


def rustoria_eu_medium(tools):
    return rustoria_core("https://donate.rustoria.co/packages.php?game=3&server=22", "VIP | EU Medium", tools)


def rustoria_eu_long(tools):
    return rustoria_core("https://donate.rustoria.co/packages.php?game=3&server=23", "VIP | EU Long", tools)


def rustoria_eu_small(tools):
    return rustoria_core("https://donate.rustoria.co/packages.php?game=3&server=27", "VIP | EU Small", tools)
