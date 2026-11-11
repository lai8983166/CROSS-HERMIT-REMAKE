"""Materialize one retained current stream to a fresh F-backed verification dir.

No VM startup. Retired full streams fail explicitly; old source dirs stay frozen.
"""
import argparse,gzip,hashlib,json
from pathlib import Path


def materialize(root,case,output):
    root=root.resolve();output=output.resolve()
    if not(str(output).lower().startswith('f:')or str(output).startswith('/mnt/f/')):
        raise ValueError('fresh F-backed output required')
    worker=root/'.venv-audit/native-worker'
    index=json.loads((root/'analysis/terminal-wait-tcg-checkpoint-streams-v1-20261111.json').read_bytes())
    rows=[r for r in index['streams']if Path(r['path']).parent.name==case]
    if len(rows)!=1 or rows[0]['retired_without_full_stream_recovery']:raise ValueError('unknown or retired full stream')
    row=rows[0];source=worker/case
    if (root/row['path']).is_file():stream=(root/row['path']).read_bytes()
    else:
        compressed=root/row['compressed_path']
        if hashlib.sha256(compressed.read_bytes()).hexdigest()!=row['compressed_sha256']:raise ValueError('compressed identity')
        with gzip.open(compressed,'rb')as f:stream=f.read(row['bytes']+1)
    if len(stream)!=row['bytes']or hashlib.sha256(stream).hexdigest()!=row['sha256']:raise ValueError('stream identity/size')
    report=(source/'report.json').read_bytes();r=json.loads(report);payloads={}
    for item in r['files']:
        name=Path(item['path']).name
        raw=stream if name=='checkpoint.bin'else(source/name).read_bytes()
        if len(raw)!=item['bytes']or hashlib.sha256(raw).hexdigest()!=item['sha256']:raise ValueError('artifact identity '+name)
        payloads[name]=raw
    output.mkdir(exist_ok=False)
    for name,raw in payloads.items():(output/name).write_bytes(raw)
    (output/'report.json').write_bytes(report)
    return hashlib.sha256(report).hexdigest()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('case');p.add_argument('output',type=Path)
    a=p.parse_args();print(materialize(Path(__file__).resolve().parents[1],a.case,a.output))
