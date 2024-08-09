from prompts.prompts import Prompts as p
from prompts.prompts import PromptFlows as pf
from pathlib import Path
import csv

SEP = ';'
PATH_OUT = Path('output')

def do_track() -> None:
    title = p.str('Track title (blank = stop)', allow_blank=True)
    if not title:
        return None
    
    artist = p.str('Track artist (blank = use default)', allow_blank=True)
    return (title, artist)

def do_album() -> None:
    album = p.str('Album title', allow_blank=True)
    aa = p.str('Album artist', allow_blank=True)
    da = p.str('Default track artist (blank = use album artist)', allow_blank=True)
    if not da:
        da = aa
    year = p.int('Year', allow_blank=True)

    tracks = pf.loop(do_track, do_while=True, ask_continue=False, count=True)
    print()

    rows = []
    for (i, (track, ta)) in enumerate(tracks):
        if not ta:
            ta = da

        rows.append([aa, ta, album, year, i + 1, track])

    if not Path.exists(PATH_OUT):
        PATH_OUT.mkdir(parents=True, exist_ok=True)

    path = PATH_OUT / f'{aa} - {album}.csv'
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)

    print(f'Saved album to {path}')
    print()

if __name__ == '__main__':
    pf.until_quit(do_album, do_while=True, continue_string='do an album')
