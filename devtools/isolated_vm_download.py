"""Bounded range download of the already selected official Windows ISO on F:."""
import concurrent.futures
import hashlib
import json
import time
import requests
from devtools.isolated_windows_vm import WORKER,MEDIA,MEDIA_BYTES,require_owned_root


def main():
    require_owned_root()
    if MEDIA.exists():raise ValueError('complete media already present')
    source=json.loads((WORKER/'media-source.json').read_bytes());url=source['url']
    if not url.startswith('https://software-static.download.prss.microsoft.com/')or source['expected_bytes']!=MEDIA_BYTES:
        raise ValueError('fixed Microsoft source required')
    partial=MEDIA.with_suffix('.iso.partial');progress=WORKER/'download-progress.json'
    chunk=1024*1024
    if progress.exists():state=json.loads(progress.read_bytes())
    else:
        prefix=partial.stat().st_size
        if not 0<=prefix<MEDIA_BYTES:raise ValueError('invalid completed sequential prefix')
        state=dict(url=url,total=MEDIA_BYTES,prefix=prefix,completed=[],chunk_bytes=chunk)
    if state['url']!=url or state['total']!=MEDIA_BYTES or state['chunk_bytes']!=chunk:raise ValueError('same ranged download identity')
    starts=range(state['prefix'],MEDIA_BYTES,chunk)
    completed=set(state['completed']);pending=[a for a in starts if a not in completed]
    def fetch(a):
        b=min(a+chunk,MEDIA_BYTES)-1
        for attempt in range(3):
            try:
                began=time.monotonic()
                with requests.get(url,headers={'Range':f'bytes={a}-{b}'},stream=True,timeout=(20,30))as r:
                    if r.status_code!=206 or r.headers.get('Content-Range')!=f'bytes {a}-{b}/{MEDIA_BYTES}':
                        raise ValueError('exact bounded HTTP Content-Range required')
                    parts=[];size=0
                    for part in r.iter_content(16*1024):
                        size+=len(part)
                        if size>b-a+1 or time.monotonic()-began>180:raise ValueError('bounded range size/time')
                        parts.append(part)
                    if size!=b-a+1:raise ValueError('truncated range')
                    return a,b''.join(parts)
            except (requests.RequestException,ValueError):
                if attempt==2:raise
        raise RuntimeError('unreachable')
    with partial.open('r+b')as stream,concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:
        futures={};todo=iter(pending)
        for _ in range(8):
            a=next(todo,None)
            if a is not None:futures[pool.submit(fetch,a)]=a
        while futures:
            done,_=concurrent.futures.wait(futures,return_when=concurrent.futures.FIRST_COMPLETED)
            for future in done:
                del futures[future];a,data=future.result();stream.seek(a);stream.write(data);stream.flush()
                completed.add(a);state['completed']=sorted(completed)
                state['completed_bytes']=state['prefix']+sum(min(chunk,MEDIA_BYTES-x)for x in completed)
                temporary=progress.with_suffix('.json.tmp');temporary.write_text(json.dumps(state),encoding='utf8');temporary.replace(progress)
                if len(completed)%32==0 or state['completed_bytes']==MEDIA_BYTES:
                    print(json.dumps(dict(completed_bytes=state['completed_bytes'],total=MEDIA_BYTES)),flush=True)
                a=next(todo,None)
                if a is not None:futures[pool.submit(fetch,a)]=a
    if completed!=set(starts)or partial.stat().st_size!=MEDIA_BYTES:raise ValueError('all ranges must be complete')
    h=hashlib.sha256()
    with partial.open('rb')as stream:
        for b in iter(lambda:stream.read(1024*1024),b''):h.update(b)
    source.update(bytes=MEDIA_BYTES,sha256=h.hexdigest(),download_complete=True)
    (WORKER/'media-source.json').write_text(json.dumps(source,indent=2),encoding='utf8')
    partial.rename(MEDIA);print(json.dumps(dict(download_complete=True,sha256=h.hexdigest())),flush=True)


if __name__=='__main__':main()
