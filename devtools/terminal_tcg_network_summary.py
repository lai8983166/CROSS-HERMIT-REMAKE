"""Summarize bounded PCAP packet headers without publishing auth payloads."""
import argparse,collections,json,socket,struct
from pathlib import Path

def summarize(path):
    data=path.read_bytes()
    if len(data)<24 or data[:4]!=bytes.fromhex('d4c3b2a1'):raise ValueError('little-endian pcap required')
    pos=24;counts=collections.Counter();rows=[]
    while pos+16<=len(data):
        sec,usec,size,original=struct.unpack_from('<IIII',data,pos);pos+=16
        if size>65536:raise ValueError('capture size')
        if pos+size>len(data):break
        frame=data[pos:pos+size];pos+=size
        if len(frame)<14:continue
        eth=int.from_bytes(frame[12:14],'big');row=dict(time=sec+usec/1e6,captured=size,original=original,ether_type=hex(eth))
        if eth==0x806 and len(frame)>=42:
            row.update(arp_op=int.from_bytes(frame[20:22],'big'),source=socket.inet_ntoa(frame[28:32]),destination=socket.inet_ntoa(frame[38:42]));counts['ARP']+=1
        elif eth==0x800 and len(frame)>=34:
            h=14+(frame[14]&15)*4;proto=frame[23]
            row.update(source=socket.inet_ntoa(frame[26:30]),destination=socket.inet_ntoa(frame[30:34]),protocol=proto)
            if proto in (6,17) and len(frame)>=h+4:
                row.update(source_port=int.from_bytes(frame[h:h+2],'big'),destination_port=int.from_bytes(frame[h+2:h+4],'big'))
                if proto==6 and len(frame)>h+13:row['tcp_flags']=hex(frame[h+13])
            counts['IPv4/'+str(proto)]+=1
        else:counts[hex(eth)]+=1
        rows.append(row)
    return dict(accepted=False,bytes=len(data),packets=len(rows),counts=dict(counts),headers=rows,payloads_published=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();r=summarize(a.source)
    with a.output.open('x')as f:json.dump(r,f,indent=2)
    print(json.dumps(r['counts']))
