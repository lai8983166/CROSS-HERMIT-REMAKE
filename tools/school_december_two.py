"""Export Chapter309's decision, its two separate joins and the December 2 school."""
import json
from tools.school_sortie_week_story_export import ROOT, join_data, july_date_card
from tools.school_year_story_export import build


def december_two():
    data = build({309:142}, {(12,2):(309,None,None)})
    scene, = data['scenes']
    assert scene['effects'] == [
        {'offset':0x73e,'opcode':144,'operands':[20]},
        {'offset':0x746,'opcode':144,'operands':[21]},
        {'offset':0xc54,'opcode':144,'operands':[19]},
    ]
    assert [s['effects'] for s in data['arrivals'][0]['sections'][1:]] == [
        [{'offset':3640,'opcode':151,'operands':[11,0]}, {'offset':3652,'opcode':91,'operands':[13,2]}],
        [{'offset':1564,'opcode':151,'operands':[11,1]}]]
    members = [101,3,9,5,8,6,1,16,17,13,14,15,11,18,32,2,7,28,110,115,118,116,107]
    data['joins'] = [join_data({},20,None,members+[20]),join_data({},21,None,members+[20,21]),
                     join_data({},19,None,members+[19])]
    return data


if __name__ == '__main__':
    output = ROOT/'prototype/data/school_year_december_two.json'
    output.write_text(json.dumps(december_two(),indent=2,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')
    (ROOT/'prototype/assets/school_story/tc1202.png').write_bytes(july_date_card(2,12)[1])
