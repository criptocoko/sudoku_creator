
import json
import random
    
files = ['B_easy.json', 'B_med.json', 'B_hard.json', 'B_extreme.json']
all_puzzles = {'puzzles': []}
for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
    
    puzzles = data['puzzles']
    rand_int = random.randint(0, 2)
    print(len(puzzles))
    # get random puzzle and add it to the all_sudokus.json file
    puzzle = puzzles[0]
    all_puzzles['puzzles'].append(puzzle)


with open('all_sudokus_B.json', 'a') as f:
    f.write(json.dumps(all_puzzles, indent=4))