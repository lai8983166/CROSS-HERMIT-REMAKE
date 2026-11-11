"""Recover current bounded compatibility evidence into a fresh F directory."""
import argparse,gzip,hashlib,json,zipfile
from pathlib import Path
from devtools.terminal_tcg_compat_verify import verify

def main(a):
    root=Path(__file__).resolve().parents[1]
    raw=a.index.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=a.sha256:raise ValueError('index identity')
    index=json.loads(raw);out=a.output.resolve()
    if not str(out).replace('\\','/').lower().startswith(('f:/','/mnt/f/')):raise ValueError('F-backed output only')
    def read(row):
        data=(root/row['path']).read_bytes()
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('artifact identity')
        return data
    read(index['capsule']);compressed=read(index['compressed'])
    stream=gzip.decompress(compressed);original=index['raw_original']
    if len(stream)!=original['bytes'] or hashlib.sha256(stream).hexdigest()!=original['sha256']:raise ValueError('stream identity')
    out.mkdir(exist_ok=False)
    with zipfile.ZipFile(root/index['capsule']['path'])as z:
        rows=json.loads(z.read('index.json'))['entries']
        for row in rows:
            prefix='raw/tcg-compat-restore-v4/'
            if not row['member'].startswith(prefix):continue
            name=row['member'][len(prefix):]
            if Path(name).name!=name:raise ValueError('nonlocal capsule member')
            data=z.read(row['member'])
            if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('member identity')
            (out/name).write_bytes(data)
    (out/'checkpoint.bin').write_bytes(stream)
    report_hash=hashlib.sha256((out/'report.json').read_bytes()).hexdigest()
    result=verify(out,report_hash)
    (out/'recovery-check.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(dict(recovered=True,verified=result['bounded_compatibility_restore_passed'],output=str(out))))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('index',type=Path);p.add_argument('sha256');p.add_argument('output',type=Path)
    main(p.parse_args())
