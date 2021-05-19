from PIL import Image, ImageFont, ImageDraw
from inky import inky
import requests
import arrow

def set_display():
    resolution = (212,104)
    screen = inky.Inky(resolution=resolution,
        colour='yellow',
        h_flip=True,
        v_flip=True)
    return screen

def get_departures():
    departures = requests.get("https://3.vbb.transport.rest/stops/900000110017/departures").json()
    lst = []
    
    for d in departures:
        now = arrow.now()
        next_dep = arrow.get(d['when'])
        next_minutes = (next_dep - now).seconds/60
        if 0 < next_minutes < 60:
            lst.append({
                'line': d['line']['name'], 
                "direction":d['direction'],
                "minutes":next_minutes,  
                })
    lst.append({'line':'M0','direction':'oo','minutes':66})
    return lst

def draw(screen, lst):
    base = Image.open("backdrop.png")
    image = ImageDraw.Draw(base)

    fnt = ImageFont.truetype('IBMPlexSans-SemiBold.ttf', 15)

    for i, x in enumerate(lst):
        image.text((0,10+(20*i)), x['line'] + " " + x['direction'], font=fnt, fill=screen.YELLOW)
        image.text((180,10+(20*i)), str(x['minutes'])+"m", font=fnt, fill=screen.YELLOW)
    
    screen.set_image(base)
    screen.set_border(screen.BLACK)
    screen.show()

if __name__ == "__main__":
    screen = set_display()
    lst = get_departures()
    draw(screen, lst)