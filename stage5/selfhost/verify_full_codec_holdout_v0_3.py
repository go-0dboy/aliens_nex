#!/usr/bin/env python3
"""Guarded one-shot preregistered holdout verifier for full-codec v0.3."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SELF=ROOT/'stage5'/'selfhost'; PY=ROOT/'independent'/'python'; GO=ROOT/'reference'/'go'
sys.path.insert(0,str(PY)); sys.setrecursionlimit(max(sys.getrecursionlimit(),40000))
from nex.wire import decode_exact  # noqa
from python_need import NeedLimits, NeedResourceLimitError, evaluate_need_observed  # noqa
from build_foundation import app, encode_core, let, lower, nat, v  # noqa
from build_full_codec import codec_status, literal_finite_bits, literal_finite_tokens, source_arithmetic  # noqa
from build_full_codec_v0_3 import source_terms_full_codec_v0_3  # noqa
from verify_full_codec_exhaustive import finite_payload, result_matches, stat_value  # noqa
ART=SELF/'full-codec-v0.3.json'; CON=SELF/'full-codec-contract-v0.3.json'; DEV=SELF/'full-codec-development-v0.3.json'; HOLD=SELF/'full-codec-holdout-v0.3.json'; PRE=SELF/'full-codec-preholdout-result-v0.3.json'
PYL=NeedLimits(max_transitions=5_000_000,max_depth=8_000)
def fail(m): raise SystemExit('stage5.12 full codec v0.3 holdout failed: '+m)
def blob(p):
    r=subprocess.run(['git','hash-object',str(p.relative_to(ROOT))],cwd=ROOT,text=True,capture_output=True)
    if r.returncode: fail('cannot hash '+str(p))
    return r.stdout.strip()
def status_is(call,e):
    _a,_s,_l,eq,_b,_ul,_ub=source_arithmetic(); return let('r',call,app(eq,codec_status(v('r')),nat(e)))
def main():
    for cmd in ([sys.executable,str(SELF/'validate_full_codec_contract_v0_3.py')],[sys.executable,str(SELF/'build_full_codec_v0_3.py'),'--check']):
        r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
        if r.returncode: fail(r.stderr.strip() or r.stdout.strip())
    if not PRE.exists(): fail('frozen pre-holdout result missing')
    pre=json.loads(PRE.read_text())
    if pre.get('schema')!='nex-selfhost-full-codec-preholdout-result' or pre.get('version')!='0.3' or pre.get('status')!='development_and_exhaustive_passed_candidate_frozen': fail('pre-holdout result invalid')
    if not pre.get('pre_holdout_historical_regression',{}).get('passed'): fail('historical regression not green')
    frozen=pre.get('frozen_git_blobs',{})
    for p,k in ((ART,'candidate_artifact'),(CON,'contract'),(DEV,'development_manifest'),(HOLD,'holdout_workload')):
        if blob(p)!=frozen.get(k): fail(f'{p.name}: frozen Git blob mismatch')
    h=json.loads(HOLD.read_text())
    if h.get('status')!='preregistered_unexecuted' or (len(h['valid_terms']),len(h['decode_errors']),len(h['encode_errors']))!=(7,3,3): fail('holdout drifted')
    src=source_terms_full_codec_v0_3(); dec=src['decodeTerm']; enc=src['encodeTerm']; wrappers=[]
    for c in h['valid_terms']:
        cid,bits,toks=c['id'],c['bits'],c['tokens']; bv=[int(x) for x in bits]; dc=app(dec,literal_finite_bits(bits)); ec=app(enc,literal_finite_tokens(toks))
        wrappers += [(f'decode:{cid}',result_matches(dc,toks,0)),(f'encode:{cid}',result_matches(ec,bv,2)),(f'law1:{cid}',result_matches(app(dec,finite_payload(ec)),toks,0)),(f'law2:{cid}',result_matches(app(enc,finite_payload(dc)),bv,2))]
    for c in h['decode_errors']: wrappers.append((f"decode-error:{c['id']}",status_is(app(dec,literal_finite_bits(c['bits'])),c['expected_status'])))
    for c in h['encode_errors']: wrappers.append((f"encode-error:{c['id']}",status_is(app(enc,literal_finite_tokens(c['tokens'])),c['expected_status'])))
    if len(wrappers)!=34: fail('holdout observation count drifted')
    expected={'kind':'Nat','value':'1'}; py={}; pref=[]; req=[]; maxpt=0; maxpc=''
    for wid,w in wrappers:
        bits=encode_core(lower(w)); term=decode_exact(bits)
        try:
            obs,st=evaluate_need_observed(term,PYL)
            if obs!=expected: fail(wid+': Python need mismatch')
            py[wid]=obs
            if st.transitions>maxpt: maxpt,maxpc=st.transitions,wid
        except NeedResourceLimitError as e: pref.append(f'{wid}: {e}')
        req.append({'id':'eval:'+wid,'level':'eval','bits':bits,'max_transitions':5_000_000,'max_depth':20_000})
    if pref: fail('Python call-by-need refusals: '+' | '.join(pref))
    r=subprocess.run(['go','run','./cmd/nexselfhostprobe'],cwd=GO,input=json.dumps(req),text=True,capture_output=True)
    if r.returncode: fail('Go probe failed: '+r.stderr.strip())
    rows={x['id']:x for x in json.loads(r.stdout)}; gn=[]; gc=[]; matched=0; maxgt=0; maxgc=''
    for wid,_ in wrappers:
        row=rows.get('eval:'+wid)
        if row is None or row.get('static_error'): fail(wid+': Go static/missing')
        if row.get('need_error'): gn.append(f"{wid}: {row['need_error']}")
        else:
            if row.get('need_result')!=expected: fail(wid+': Go need mismatch')
            tr=stat_value(row.get('need_stats') or {},'transitions')
            if tr>maxgt: maxgt,maxgc=tr,wid
            if py.get(wid)==row.get('need_result'): matched+=1
        if row.get('cbn_error'): gc.append(f"{wid}: {row['cbn_error']}")
        elif row.get('cbn_result')!=expected: fail(wid+': Go CBN mismatch')
    if gn: fail('Go call-by-need refusals: '+' | '.join(gn))
    print('stage5.12 full codec v0.3 preregistered holdout: passed')
    print(f'candidate Git blob: {blob(ART)}'); print(f'contract Git blob: {blob(CON)}'); print(f'development manifest Git blob: {blob(DEV)}'); print(f'holdout Git blob: {blob(HOLD)}')
    print('holdout: 7 valid + 3 decode errors + 3 encode errors'); print('compound forced Nat observations: 34')
    print('Python call-by-need resource refusals: 0'); print('Go call-by-need resource refusals: 0'); print(f'Go CBN resource refusals: {len(gc)}'); print(f'Python/Go need values matched: {matched}/34')
    print(f'largest Python need transition count: {maxpt} at {maxpc}'); print(f'largest Go need transition count: {maxgt} at {maxgc}'); print('round-trip laws: checked on all 7 holdout valid terms')
if __name__=='__main__': main()
