"""Bind six separately owned sources and replay each full parent plus original world loop."""
import contextlib,json,time
from tools import school_retained_world_loop as w
from tools import school_retained_world_loop_analysis as a
from tools import school_retained_world_loop_verification as v
if __name__=='__main__':
 paths=[w.ROOT/'.venv-audit/world-initial-source-rows-v1.json',w.ROOT/'.venv-audit/world-other-source-rows-v1.json']
 for attempt in range(240):
  if all(p.exists() for p in paths):break
  time.sleep(5)
 else:raise RuntimeError('all six complete sources unavailable')
 with open(w.ROOT/'analysis/school-retained-world-loop-proof-v1-20261023.log','x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  rows=json.loads(paths[0].read_bytes())+[r for group in json.loads(paths[1].read_bytes()) for r in group];matrix=w.matrix_header(rows);matrix['source_processes']=3;out=w.ROOT/'analysis/school-retained-world-loop-matrix-v1-20261023.json';assert not out.exists();out.write_text(json.dumps(matrix,indent=2)+chr(10),encoding='utf8',newline=chr(10));raw=out.read_bytes();report=a.analyze(matrix);report['source_matrix_sha256']=w.sha(raw);dest=w.ROOT/'analysis/school-retained-world-loop-source-analysis-v1-20261023.json';assert not dest.exists();dest.write_text(json.dumps(report,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('SIX_SOURCE_MATRIX_AND_ANALYSIS_BOUND',flush=True)
  proof=v.verify_matrix(matrix,jobs=3);proof['source_matrix_sha256']=w.sha(raw);proof['verification_source_sha256']=w.sha((w.ROOT/'tools/school_retained_world_loop_verification.py').read_bytes());out=w.ROOT/'analysis/school-retained-world-loop-proof-v1-20261023.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('SIX_WHOLE_SOURCE_WORLD_PROOFS_COMPLETE',flush=True)
