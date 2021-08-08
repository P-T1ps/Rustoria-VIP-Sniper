import requests


def convert_gbp_usd(amount, round_it=True):
    amount = float(amount)
    conv_url = f"https://www.currency.me.uk/convert/gbp/usd"
    amt = float(float(requests.get(conv_url).text.split
                             ("<input id=\"to\" name=\"to\" value=\"USD\" type=\"hidden\">")[1].split(
        "<input id=\"answer\" name=\"answer\" value=\"")[1].split("\" disabled>")[0]) * amount)
    amt = round(amt, 2) if round_it else amt
    return amt


def discord_styler(description):
    description = description.replace("<strong>", "**").replace("</strong>", "**")
    description = description.split("\n")
    a = ""
    for i in description:
        i = i.split("<p")[1].split("\">")[1].replace("</p>", "")
        a += i + "\n"
    return a