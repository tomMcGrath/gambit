import os
import pgn_processing
import sys
import tqdm

pgnpath = sys.argv[1]
out_dir = sys.argv[2]
games_per_file = int(sys.argv[3])

game_iterator = pgn_processing.make_game_iterator(pgnpath)
games_written = 0
num_files_written = 0

for game in tqdm.tqdm(game_iterator):
    write_filename = str(num_files_written) + '.txt'
    outpath = os.path.join(out_dir, write_filename)
    processed_movetext = pgn_processing.process_movetext(game['movetext'])
    processed_movetext += '\n'
    with open(outpath, 'a+') as f:
        f.write(processed_movetext)

    games_written += 1
    if games_written == games_per_file:
        num_files_written += 1
        games_written = 0
