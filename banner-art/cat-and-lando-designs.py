"""Carbonfox ASCII art designs: cat (Chase) + lando-2 (border collie).
Each row carries ONE [hex]...[/] tag per row (carbonfox hero convention).
Palette: bg #161616, black coat=#7f8489(dim gray, visible on dark bg),
white=#f2f4f8, cyan eyes/accent=#33b1ff, blue collar=#78a9ff, amber eyes=#ff9e64.
"""
import re

CAT = [
    "[#7f8489]        ,-.      _,---._ __   ",  # L ear, R ear
    "[#7f8489]       /  )   .-'       `.   \\",
    "[#7f8489]      (  (  ,'      .---. `.  |",
    "[#7f8489]       \\  `-\"     |  o  |  `.|",
    "[#33b1ff]        `.      |     |    / ",  # cyan eyes row
    "[#7f8489]         /`.    |  o  |   /  ",
    "[#7f8489]        (       `-----'  |  '",
    "[#78a9ff]        |  ,-.    ,-'    |  /",  # blue collar
    "[#7f8489]        |  | (   |       | / ",
    "[#7f8489]        )  |  \\  `.___.__|/  ",
    "[#7f8489]        `--'   `--'        ",
]

# lando-2: sitting border collie, flopped L ear, perked R ear, white blaze+chest,
# black coat, amber eyes, white-tipped tail on viewer's right.
LANDO = [
    "[#7f8489]       __                 __  ",
    "[#7f8489]      /  \\     ______    /  \\ ",  # flopped L ear, perked R ear
    "[#7f8489]     |    |   |      |  /    \\",
    "[#7f8489]     |    |   |  oo  | |      |",  # amber eyes: /w/ flag
    "[#ff9e64]     |  oo|   |      | |   oo |",  # eyes
    "[#f2f4f8]     |    |   |  --- | |      |",  # white blaze+forehead
    "[#f2f4f8]     |    |    \\___/  |      |",  # white muzzle
    "[#f2f4f8]      \\  /      |     /      /",
    "[#7f8489]       \\/   ____|____        /",
    "[#7f8489]      ___  |        |    ___/ ",
    "[#7f8489]     /   \\ |  W W   |   /   \\ ",
    "[#f2f4f8]    /  W  \\|  W W   |  /  W  \\",  # white chest + paws
    "[#7f8489]   |       |        | |       |",
    "[#7f8489]   |       |        | |       |",  # front legs
    "[#f2f4f8]   |  oo   |   oo   |  |  oo  |",  # paws
    "[#7f8489]   \\______/ \\______/   \\______/",
]

def art_width(rows):
    return max(len(re.sub(r"\[[^\]]+\]|\[/\]", "", r)) for r in rows)

print("CAT rows:", len(CAT), "width:", art_width(CAT))
print("LANDO rows:", len(LANDO), "width:", art_width(LANDO))
for name, art in [("CAT", CAT), ("LANDO", LANDO)]:
    print(f"--- {name} ---")
    for r in art:
        print(re.sub(r"\[[^\]]+\]", "", r).replace("[/]", "").rstrip())
