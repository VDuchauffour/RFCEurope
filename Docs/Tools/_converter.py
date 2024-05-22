import html.entities as e
import sys


def convert(filename):
    with open(filename, "r") as file:
        text = file.read()
        for k, v in e.name2codepoint.items():
            text = text.replace("&" + k + ";", "&#" + str(v) + ";")

    with open(filename, "w") as file:
        file.write(text)


convert(filename=sys.argv[1])
