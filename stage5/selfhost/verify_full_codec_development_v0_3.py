#!/usr/bin/env python3
"""Compact frozen development verification for Stage 5.12 full-codec v0.3.

Four compound success evaluations per valid term preserve all former
status/length/extensional-stream assertions while avoiding duplicate codec runs.
The v0.3 holdout is never opened here.
"""
from __future__ import annotations

import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; SELF=ROOT/'stage5'/'selfhost'; PY=ROOT/'independent'/'python'; GO=ROOT/'reference'/'go'
sys.path.insert(0,str(PY)); sys.setrecursionlimit(max(sys.getrecursionlimit(),40000))
from nex.wire import decode_exact  # noqa
from python_need import NeedLimits, NeedResourceLimitError, evaluate_need_observed  # noqa
from build_foundation import IFZ, app, encode_core, let, lower, nat, v  # noqa
from build_full_codec import PAIR, codec_status, literal_finite_bits, literal_finite_tokens, source_arithmetic  # noqa
from build_full_codec_v0_3 import source_terms_full_codec_v0_3  # noqa
from verify_full_codec_exhaustive import finite_payload, result_matches, stat_value  # noqa

ART=SELF/'full-codec-v0.3.json'; MAN=SELF/'full-codec-development-v0.3.json'
PYL=NeedLimits(max_transitions=5_000_000,max_depth=8_000); GMT=5_000_000; GMD=20_000

def fail(m): raise SystemExit('stage5.12 full codec v0.3 development failed: '+m)

def load_development():
    manifest=json.loads(MAN.read_text())
    if manifest.get('status')!='frozen_before_full_codec_candidate_v0.3': fail('development manifest drifted')
    merged={'valid_terms':[],'decode_errors':[],'encode_errors':[]}
    for rel in manifest['sources']:
        data=json.loads((ROOT/rel).read_text())
        for k in merged: merged[k].extend(data[k])
    if {k:len(v) for k,v in merged.items()} != {'valid_terms':24,'decode_errors':12,'encode_errors':12}: fail('merged counts drifted')
    return merged

def status_is(call, expected):
    _a,_s,_l,eq,_b,_ul,_ub=source_arithmetic()
    return let('r',call,app(eq,codec_status(v('r')),nat(expected)))

def main():
    for cmd in ([sys.executable,str(SELF/'validate_full_codec_contract_v0_3.py')],[sys.executable,str(SELF/'build_full_codec_v0_3.py'),'--check']):
        r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
        if r.returncode: fail(r.stderr.strip() or r.stdout.strip())
    art=json.loads(ART.read_text());
    if art.get('version')!='0.3' or art.get('holdout_status')!='preregistered_unexecuted': fail('candidate identity/status drifted')
    dev=load_development(); src=source_terms_full_codec_v0_3(); dec=src['decodeTerm']; enc=src['encodeTerm']
    wrappers=[]
    for c in dev['valid_terms']:
        cid,bits,tokens=c['id'],c['bits'],c['tokens']; bv=[int(x) for x in bits]
        dc=app(dec,literal_finite_bits(bits)); ec=app(enc,literal_finite_tokens(tokens))
        wrappers += [(f'decode:{cid}',result_matches(dc,tokens,0)),(f'encode:{cid}',result_matches(ec,bv,2)),(f'law1:{cid}',result_matches(app(dec,finite_payload(ec)),tokens,0)),(f'law2:{cid}',result_matches(app(enc,finite_payload(dc)),bv,2))]
    for c in dev['decode_errors']: wrappers.append((f"decode-error:{c['id']}",status_is(app(dec,literal_finite_bits(c['bits'])),c['expected_status'])))
    for c in dev['encode_errors']: wrappers.append((f"encode-error:{c['id']}",status_is(app(enc,literal_finite_tokens(c['tokens'])),c['expected_status'])))
    if len(wrappers)!=120: fail(f'observation count {len(wrappers)} != 120')

    pyres={}; pyref=[]; g_req=[]; maxpt=0; maxpc=''; expected={'kind':'Nat','value':'1'}
    for wid,w in wrappers:
        bits=encode_core(lower(w)); term=decode_exact(bits)
        try:
            obs,st=evaluate_need_observed(term,PYL)
            if obs!=expected: fail(f'{wid}: Python need {obs} != {expected}')
            pyres[wid]=obs
            if st.transitions>maxpt: maxpt,maxpc=st.transitions,wid
        except NeedResourceLimitError as e: pyref.append(f'{wid}: {e}')
        g_req.append({'id':'eval:'+wid,'level':'eval','bits':bits,'max_transitions':GMT,'max_depth':GMD})
    if pyref: fail('Python call-by-need refusals: '+' | '.join(pyref))
    r=subprocess.run(['go','run','./cmd/nexselfhostprobe'],cwd=GO,input=json.dumps(g_req),text=True,capture_output=True)
    if r.returncode: fail('Go probe failed: '+r.stderr.strip())
    rows={x['id']:x for x in json.loads(r.stdout)}; gnref=[]; gcref=[]; matched=0; maxgt=0; maxgc=''
    for wid,_ in wrappers:
        row=rows.get('eval:'+wid)
        if row is None or row.get('static_error'): fail(f'{wid}: Go missing/static error {row}')
        if row.get('need_error'): gnref.append(f"{wid}: {row['need_error']}")
        else:
            if row.get('need_result')!=expected: fail(f'{wid}: Go need mismatch')
            tr=stat_value(row.get('need_stats') or {},'transitions')
            if tr>maxgt: maxgt,maxgc=tr,wid
            if pyres.get(wid)==row.get('need_result'): matched+=1
        if row.get('cbn_error'): gcref.append(f"{wid}: {row['cbn_error']}")
        elif row.get('cbn_result')!=expected: fail(f'{wid}: Go CBN mismatch')
    if gnref: fail('Go call-by-need refusals: '+' | '.join(gnref))
    print('stage5.12 full codec v0.3 development: verified')
    print('development: 24 valid + 12 decode errors + 12 encode errors')
    print('compound forced Nat observations: 120')
    print('Python call-by-need resource refusals: 0'); print('Go call-by-need resource refusals: 0')
    print(f'Go CBN resource refusals: {len(gcref)}'); print(f'Python/Go need values matched: {matched}/120')
    print(f'largest Python need transition count: {maxpt} at {maxpc}'); print(f'largest Go need transition count: {maxgt} at {maxgc}')
    print('round-trip laws: checked on all 24 development valid terms'); print('v0.3 holdout: NOT READ / NOT EXECUTED')
if __name__=='__main__': main()
