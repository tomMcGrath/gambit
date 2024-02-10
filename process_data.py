import os
import pgn_processing
import sys

pgnpath = sys.argv[1]
out_dir = sys.argv[2]
games_per_file = int(sys.argv[3])

game_iterator = pgn_processing.make_game_iterator(pgnpath)
games_count = 0
file_count = 0

for game in game_iterator:
    write_filename = str(file_count) + '.txt'
    outpath = sys.path.join(out_dir, write_filename)
    