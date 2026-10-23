import contextlib,json,time,unittest
from tools import school_retained_scheduler_verification as v
if __name__=='__main__':
 matrix=v.ROOT/'analysis/school-retained-scheduler-matrix-v1-20261024.json';single=v.ROOT/'analysis/school-retained-scheduler-single-proof-v1-20261024.json';log=v.ROOT/'analysis/school-retained-scheduler-validation-v1-20261024.log';n=unittest.defaultTestLoader.loadTestsFromName('tools.tests.test_school_retained_scheduler').countTestCases()
 for i in range(720):
  txt=log.read_text(encoding='utf8') if log.exists() else ''
  if 'FAILED (' in txt:raise RuntimeError('new validation failed; formal proof not launched')
  if matrix.exists() and single.exists() and ('Ran '+str(n)+' tests in ') in txt and txt.rstrip().endswith('OK'):break
  time.sleep(5)
 else:raise RuntimeError('complete source matrix and whole initial validation unavailable')
 with open(v.ROOT/'analysis/school-retained-scheduler-proof-v1-20261024.log','x',encoding='utf8',buffering=1) as stream,contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):
  raw=matrix.read_bytes();r=v.verify_matrix(json.loads(raw),'analysis/school-retained-scheduler-independent-v1-20261024','analysis/school-retained-scheduler-single-proof-v1-20261024.json',3);r['source_matrix_sha256']=v.sha(raw);r['verification_source_sha256']=v.sha((v.ROOT/'tools/school_retained_scheduler_verification.py').read_bytes());out=v.ROOT/'analysis/school-retained-scheduler-proof-v1-20261024.json';assert not out.exists();out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('SIX_COMPLETE_INDEPENDENT_ORIGINAL_SCHEDULER_DISPATCHES_VERIFIED',flush=True)
