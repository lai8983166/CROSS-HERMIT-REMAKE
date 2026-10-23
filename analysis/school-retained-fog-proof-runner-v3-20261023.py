"""Five new independent whole cases plus the bound successful full initial-case proof."""
import contextlib,json,re,time
from tools import school_retained_fog_verification as v
if __name__=='__main__':
 matrix=v.ROOT/'analysis/school-retained-fog-matrix-v1-20261023.json';single=v.ROOT/'analysis/school-retained-fog-single-proof-v1-20261023.json';validation=v.ROOT/'analysis/school-retained-fog-validation-v3-20261023.log'
 for attempt in range(360):
  ready=matrix.exists() and single.exists() and validation.exists()
  if ready:
   log=validation.read_text(encoding='utf8')
   if re.search('Ran 32 tests in ',log) and log.rstrip().endswith('OK'):break
  time.sleep(5)
 else:raise RuntimeError('complete source matrix and successful exact initial independent validation unavailable')
 with open(v.ROOT/'analysis/school-retained-fog-proof-v1-20261023.log','x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  raw=matrix.read_bytes();r=v.verify_matrix(json.loads(raw),'analysis/school-retained-fog-independent-v1-20261023','analysis/school-retained-fog-single-proof-v1-20261023.json',3);r['source_matrix_sha256']=v.sha(raw);r['verification_source_sha256']=v.sha((v.ROOT/'tools/school_retained_fog_verification.py').read_bytes());out=v.ROOT/'analysis/school-retained-fog-proof-v1-20261023.json';assert not out.exists();out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('SIX_COMPLETE_INDEPENDENT_CURRENT_FOG_LOOPS_VERIFIED',flush=True)
