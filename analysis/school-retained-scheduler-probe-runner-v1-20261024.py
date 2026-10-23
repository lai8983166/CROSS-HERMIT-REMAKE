import contextlib,json,gzip
from tools import school_retained_scheduler as w
if __name__=='__main__':
 with open(w.ROOT/'analysis/school-retained-scheduler-probe-v1-20261024.log','x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  built=w.build_group('scheduler-probe-v1-20261024','initial');c=w.produce_one(built,'initial',76);out=w.ROOT/'analysis/school-retained-scheduler-single-v1-20261024.json.gz';assert not out.exists();out.write_bytes(gzip.compress(json.dumps(c,separators=(',',':')).encode(),mtime=0));print('SOURCE_COMPLETE',c['scheduler']['frontier'],flush=True)
