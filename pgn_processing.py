def parse_tagpair(tagpair):
    """Parses a single PGN metadata element [tag, tag_data]."""
    tagpair = tagpair[1:-1]  # discard square brackets
    split_tagpair = tagpair.split(" ", 1)
    tag = split_tagpair[0]
    tag_data = " ".join(split_tagpair[1:]).replace('"', '')  # remove quotation marks
    return tag, tag_data

def is_terminating(line):
    """Determines if a PGN movetext line is the last line in the game."""
    if line.endswith("0-1"):
        return True
    elif line.endswith("1-0"):
        return True
    elif line.endswith("1/2-1/2"):
        return True
    else:
        return False
    
def parse_pgnfile(pgnpath):
    """Parses a pgn file and returns a list of gameresult dicts."""
    is_movetext = False
    movetext = ""
    gamedata = {}
    gamedatas = []
    with open(pgnpath, "r") as infile:
        for line in infile:
            line = line.strip("\n")

            if line.startswith("["):
                is_movetext = False  # back in the metadata
                tag, tag_data = parse_tagpair(line)
                if tag in ["WhiteElo", "BlackElo", "Result"]:  # only store what we need
                    gamedata[tag] = tag_data

            if line.startswith("1."):  # now we're in the movetext so start storing
                is_movetext = True

            if is_movetext:
                if movetext != "":  # add spacing if it's not the first movetext line
                    movetext += " "
                movetext += line

            if is_terminating(line):  # game's finished, so store & reset
                assert line.split(" ")[-1] == gamedata["Result"]  # consistency check
                gamedata["movetext"] = movetext
                gamedatas.append(gamedata)
                movetext = ""
                gamedata = {}

    return gamedatas