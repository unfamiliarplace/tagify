from prompts.prompts import Prompts as p
from prompts.prompts import PromptFlows as pf
from pathlib import Path
import csv

SEP = '|'
PATH_OUT = Path('output')

def get_track_details(ask_artist: bool=True) -> tuple[str, str]:
    title = p.str('Track title (blank = stop)', allow_blank=True)
    if not title:
        return None
    
    if ask_artist:
        artist = p.str('Track artist (blank = use default)', allow_blank=True)
    else:
        artist = ''

    return (title, artist)

def do_album() -> None:
    aa = p.str('Album artist', allow_blank=True)

    da = aa
    kwargs = {'ask_artist': False}

    album = p.str('Album title', allow_blank=True)

    aa_for_all = p.bool('Use album artist as artist for all tracks (default Y)', strict=True, allow_blank=True)
    if not aa_for_all:        
        da = p.str('Default track artist (blank = use album artist)', allow_blank=True)
        if not da:
            da = aa

        one_ta = p.bool('Same artist for all tracks (default Y)', strict=True, allow_blank=True)
        if not one_ta:
            kwargs['ask_artist'] = True

    year = p.int('Year', allow_blank=True)

    print()
    tracks = pf.loop(get_track_details, kwargs=kwargs, do_while=True, ask_continue=False, count=True, between=print)
    print()

    if not tracks:
        print('No tracks entered; album not saved')
        print()
        return

    rows = []
    for (i, (track, ta)) in enumerate(tracks):
        if not ta:
            ta = da

        rows.append([aa, ta, album, year, i + 1, track])

    if not Path.exists(PATH_OUT):
        PATH_OUT.mkdir(parents=True, exist_ok=True)

    path = PATH_OUT / f'{aa} - {album}.csv'
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=SEP, quoting=csv.QUOTE_MINIMAL, quotechar='^')
        for row in rows:
            writer.writerow(row)

    # LOL have to remove the final newline for mp3tag to like it
    with open(path, 'r', encoding='utf-8') as f:
        contents = f.read()[:-1]
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(contents)

    print(f'Saved album to {path}')
    print()

if __name__ == '__main__':
    pf.until_quit(do_album, do_while=True, continue_string='do another album', between=print)
