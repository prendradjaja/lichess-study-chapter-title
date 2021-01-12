import sys
import os
import json
from datetime import datetime

from secrets import MY_USERNAMES

assert len(sys.argv) > 1, 'Usage: ./main.sh GAME_URL'


DECISIVE = ['mate', 'resign']  # maybe also timeout?
DRAW = ['draw']  # not sure if stalemate etc are different


def main():
    url = sys.argv[1]
    gameid = url.split('/')[-1][:8]

    resptext = os.popen(f'curl https://lichess.org/api/game/{gameid}').read()

    resp = json.loads(resptext)

    speed = resp['speed']
    speedemoji = {
        'blitz': '⚡️',
        'rapid': '🐇',
    }.get(speed, '')

    date = datetime.fromtimestamp(resp['createdAt'] // 1000).strftime(' %m %d').replace(' 0', ' ').strip().replace(' ', '/')

    moves = (resp['turns'] + 1) // 2

    ids = [resp['players']['white']['userId'],
           resp['players']['black']['userId']]
    iswhite = ids[0] in MY_USERNAMES
    opponent = ids[int(iswhite)]
    assert opponent not in MY_USERNAMES
    color = 'white' if iswhite else 'black'
    colorchar = color[0].upper()

    status = resp['status']

    if status in DECISIVE:
        win = resp['winner'] == color
        statuschar = '+' if win else '-'
    elif status in DRAW:
        statuschar = '='
    else:
        print("Error: Status not handled:", status)
        print("Edit me and add this status to either DECISIVE or DRAW.")
        exit()

    result = f'{speedemoji} {date} {colorchar}{statuschar} ({moves}) OPENING v {opponent}'
    print(result)

main()
