"""Export consecutive dated school routes after October's first two weeks."""
import json

from tools.school_sortie_week_story_export import (
    ROOT, _date_card_metadata, add_chapter_card, catalog, date_route, july_date_card,
)

# Native text pool sizes. CH003 runs before settlement, CH001 after it,
# CH002 when leaving the workroom for school.
COUNTS = {61: 161, 64: 78, 65: 56, 66: 81, 67: 70, 68: 33, 69: 196, 70: 84}
ARRIVALS = {
    (10, 3): (61, None, None),
    (10, 4): (64, None, None),
    (10, 5): (65, None, None),
    (11, 1): (66, 67, 68),
    (11, 2): (69, 70, None),
}


def build(counts=COUNTS, dates=ARRIVALS):
    data = catalog(counts)
    scenes = {scene['chapter']: scene for scene in data['scenes']}
    arrivals = []
    for (month, week), chapters in dates.items():
        prior = (month, week-1) if week > 1 else (month-1, 5)
        routes = [date_route('CH003', *prior), date_route('CH001', month, week),
                  date_route('CH002', month, week)]
        sections = []
        for chapter, route in zip(chapters, routes, strict=True):
            target = f'data/adv/dat/Chapter{chapter:03}.ybc' if chapter else None
            assert route['target'] == target
            effects = route.get('effects', []) + (scenes[chapter]['effects'] if chapter else [])
            for event in effects:
                departure = {71:2, 76:4}.get(chapter)
                assert (event['opcode'] in (91, 151) or
                        (chapter == 69 and event['opcode'] == 153 and event['operands'] == [1, 6, 0]) or
                        (departure is not None and event == {'opcode':145,'offset':20,'operands':[departure]}))
            sections.append({'chapter': chapter, 'effects': effects})
        if chapters[1]:
            card = {'scenes': [scenes[chapters[1]]]}
            add_chapter_card(card, 0, f'{chapters[1]:03}', week, month)
            calendar_card = card['date_card']
        else:
            commands = routes[1]['presentation']
            assert [op['opcode'] for op in commands] == [56, 67, 69, 56, 13, 56, 74, 12]
            resource = commands[1]['resource']
            draw = commands[2]['operands']
            assert resource == f'data/adv/bin/tc{month:02}{week:02}.bin'
            assert draw == [0, 0, 324, 0, 53, 0, 0, 1024, 128]
            assert [commands[i]['operands'] for i in (0, 3, 4, 5, 7)] == [[0], [3], [600], [4], [30]]
            calendar_card = _date_card_metadata(week, resource, draw, 600, month)
        arrivals.append({'departure': list(prior), 'arrival': [month, week], 'routes': routes,
                         'sections': sections, 'date_card': calendar_card})
    data['arrivals'] = arrivals
    return data


if __name__ == '__main__':
    output = ROOT/'prototype/data/school_year_october_continuation.json'
    output.write_text(json.dumps(build(), indent=2, ensure_ascii=False)+'\n', encoding='utf8', newline='\n')
    for month, week in ARRIVALS:
        (ROOT/f'prototype/assets/school_story/tc{month:02}{week:02}.png').write_bytes(july_date_card(week, month)[1])
    for week, label, chapter, lines in [(3,'three',71,205), (5,'five',76,206)]:
        data = build({chapter:lines}, {(11,week):(None,chapter,None)})
        (ROOT/f'prototype/data/school_year_november_{label}.json').write_text(
            json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf8', newline='\n')
        (ROOT/f'prototype/assets/school_story/tc11{week:02}.png').write_bytes(july_date_card(week,11)[1])
