"""Read-only closure of fixed graphics/input model and build evidence; never runs native."""
from __future__ import annotations
import argparse,gzip,json
from pathlib import Path
from devtools.terminal_graphics_platform import base,need
from devtools import terminal_graphics_native as graphics,terminal_input_native as inputs

ROOT=base.ROOT

def load(path):
    raw=(ROOT/path).read_bytes();return json.loads(gzip.decompress(raw) if path.endswith('.gz') else raw)

def verify(pin):
    need(base.identity(ROOT/pin['path'])==pin,'fixed evidence bytes '+pin['path'])

def prove():
    parent_path='.venv-audit/terminal-window-destruction-build-v2-20261114/native-window-case-v2-host.json.gz'
    need(base.sha((ROOT/parent_path).read_bytes())=='00f48951f7781697207bcfab046cd62b1f69325942ef3eefb436505a791e35c5','fixed previous native success')
    parent=load(parent_path)
    for pin in parent['implementation_pins']:verify(pin)
    models=[]
    for path,sha in [('.venv-audit/terminal-graphics-model-v6-20261114.json.gz','60f4ab083519c29fbe0907a413e92a42429affafc61b2a1ccc8f69e8b459241f'),('.venv-audit/terminal-input-model-v2-20261114.json.gz','35177f9713b4b94c0ec76cc2392a3bde0cbc411320b65847e59b79922404b26b')]:
        need(base.sha((ROOT/path).read_bytes())==sha,'fixed successful model');r=load(path)
        need(r['reached'] and not r['native_executed'] and not r['desktop_used'] and not r['ready_for_native'] and not r['formal_acceptance'],'model scope unchanged')
        for pin in r['implementation']:verify(pin)
        need(all(r['cleanup']['status'][k]==0 for k in r['cleanup']['zero_fields']),'final model resource zeros')
        need(r['seconds']<=90 and len((ROOT/path).read_bytes())<8*1024*1024,'explicit model budget')
        models.append(dict(source=base.identity(ROOT/path),seconds=r['seconds'],original_instruction_hooks=sum(x['count']for x in r['instruction_sites']),original_instruction_sites=len(r['instruction_sites']),API=len(r['API_calls']),callbacks=len(r['callbacks']),request_response_pairs=sum(x['direction']=='request'for x in r['native_trace']),cleanup_zero_fields=r['cleanup']['zero_fields'],published_GAME=r.get('published_GAME',0),natural_WinMain_return=False))
    builds=[]
    for generator,path in [(graphics,'.venv-audit/terminal-graphics-owner-build-v3-20261114/static-report.json'),(inputs,'.venv-audit/terminal-input-owner-build-v2-20261114/static-report.json')]:
        r=load(path)
        for key in ('generator','include','parent_generator','parent_include','generated_source','helper'):verify(r[key])
        need(base.sha(generator.source().encode())==r['generated_source']['sha256'],'exact retained generated C++ source')
        need(not r['native_executed'] and not r['desktop_used'],'build only')
        generator.self_check();builds.append(dict(report=base.identity(ROOT/path),helper=r['helper'],source=r['generated_source'],native_executed=False))
    review_paths=['analysis/terminal-graphics-platform-independent-review-v1-20261114.json','analysis/terminal-input-platform-independent-review-v1-20261114.json','analysis/terminal-graphics-desktop-preflight-v1-20261114.json']
    for path in review_paths:
        r=load(path)
        for pin in r.get('implementation',r.get('evidence',[])):verify(pin)
    need(load(review_paths[0])['accepted_for_offline_component_review'] and load(review_paths[1])['accepted_within_model_scope'],'independent component review')
    desktop=load(review_paths[2]);need(desktop['tests']==dict(run=32,failures=0,errors=0),'32 offline restoration regressions')
    return dict(schema_version=1,kind='same_MAIN_graphics_input_original_GAME_publication_offline_readiness',baseline_commit='44a9884d680c8c6a28810f888fa68959b755d3a0',bounded_offline_component_passed=True,ready_for_native=False,actual_native_runs=0,desktop_reads=0,desktop_writes=0,screenshots=0,global_input_sent=False,actual_GAME_publication=False,symbolic_original_GAME_store_executed=True,wait_return=False,first_result_consumption=False,formal_acceptance=False,formal_progress='2/8',generator=base.identity(Path(__file__)),previous_native_success=base.identity(ROOT/parent_path),prior_native_implementation_pins_exact=len(parent['implementation_pins']),models=models,builds=builds,reviews=[base.identity(ROOT/p)for p in review_paths],desktop_tests=desktop['tests'],input_tamper_rejections=len(load(review_paths[1])['tamper_rejections']),graphics_rejections=10,main_review=['Original fixed calls and source bytes, current MAIN identity, callbacks, native reference failure handling and deferred GDI retirement reviewed independently from native author.','Parent recovery context checked before every write; closed native admission, original foreground lifetime guard, gamma actual readback and no-op failure coverage retained.','Native input original GUID/dataformat relocation, full instance qualification, real HRESULT/ULONG, Unacquire/Release/window lifetime and mandatory actual cursor restore gate reviewed.'],limitations=['Model values are symbolic; old caps are declared model inputs, no current GPU/glyph/input/desktop observation.','Locked texture readback does not yet prove Unlock/relock persistence.','Graphics model extra DLL references are not a faithful Windows module reference model.','Pending WinMain stack is hashed only and abandoned after supplemental destructors; published GAME global cannot be resumed after cleanup.','Native runner still needs authenticated release receipts, process watchdog, asset cwd and D3D-to-display gamma mapping before new desktop authorization.','LastInput tick is not a complete generation proof; native original input and desktop gamma restoration remain unqualified.','No complete independent replay, two fresh native cases, scene worker wait or result consumption.'])

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=(ROOT/a.out).resolve()
    need(out.is_relative_to(ROOT/'analysis') and not out.exists(),'fresh F small report')
    r=prove();raw=(json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode();need(len(raw)<262144,'bounded small closure report');out.write_bytes(raw);print(json.dumps(base.identity(out)))
