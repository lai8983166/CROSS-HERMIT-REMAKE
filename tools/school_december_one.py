"""Export the November week 5 return and the first December school week."""
import json

from tools.school_year_story_export import ROOT, build, july_date_card


def december_one():
    data = build({77: 67, 231: 43}, {(12, 1): (77, None, 231)})
    arrival, = data['arrivals']
    assert [section['effects'] for section in arrival['sections']] == [
        [],
        [{'offset': 3580, 'opcode': 151, 'operands': [9, 0]},
         {'offset': 3592, 'opcode': 91, 'operands': [15, 2]}],
        [{'offset': 898, 'opcode': 151, 'operands': [9, 1]}],
    ]
    return data


if __name__ == '__main__':
    output = ROOT/'prototype/data/school_year_december_one.json'
    output.write_text(json.dumps(december_one(), indent=2, ensure_ascii=False)+'\n',
                      encoding='utf8', newline='\n')
    (ROOT/'prototype/assets/school_story/tc1201.png').write_bytes(july_date_card(1, 12)[1])
