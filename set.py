from PIL import Image, ImageFont, ImageDraw
from inky.auto import auto as get_board
import requests
import arrow

import math


def get_departures():
    departures = requests.get("https://v5.bvg.transport.rest/stops/900000110017/departures").json()
    lst = []
    
    for d in departures:
        now = arrow.now()
        next_dep = arrow.get(d['when'])
        next_seconds = (next_dep - now).seconds
        next_minutes = math.floor(next_seconds/60)
        if 0 < next_minutes < 60:
            lst.append({
                'line': d['line']['name'], 
                "direction":d['direction'][:20],
                "minutes":next_minutes,  
                })
    lst.append({'line':'M0','direction':'oo','minutes':66})
    return lst

def draw(screen, lst):
    base = Image.open("backdrop.png")
    image = ImageDraw.Draw(base)

    fnt = ImageFont.truetype('IBMPlexSans-SemiBold.ttf', 13)

    for i, x in enumerate(lst):

        image.text((0,10+(20*i)), x['line'] + " " + x['direction'], font=fnt, fill=screen.YELLOW)
        image.text((180,10+(20*i)), str(x['minutes'])+"m", font=fnt, fill=screen.YELLOW)
    
    image.rotate(180)
    screen.set_image(base)
    screen.set_border(screen.BLACK)
    screen.show()

if __name__ == "__main__":
    screen = get_board()
    
    lst = get_departures()
    draw(screen, lst)