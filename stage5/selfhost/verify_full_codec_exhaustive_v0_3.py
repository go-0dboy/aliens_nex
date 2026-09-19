#!/usr/bin/env python3
"""Frozen 27-Term bounded-exhaustive verification for full-codec v0.3."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SELF=ROOT/'stage5'/'selfhost'; PY=ROOT/'independent'/'python'; GO=ROOT/'reference'/'go'
sys.path.insert(0,str(PY)); sys.setrecursionlimit(max(sys.getrecursionlimit(),40000))
from nex.wire import decode_exact, encode_term  # noqa
from python_need import NeedLimits, NeedResourceLimitError, evaluate_need_observed  # noqa
from build_foundation import app, encode_core, lower  # noqa
from build_full_codec import literal_finite_bits, literal_finite_tokens  # noqa
from build_full_codec_v0_3 import source_terms_full_codec_v0_3  # noqa
from validate_full_codec_contract import encode_ast, exhaustive_terms, tokens_of  # noqa
from verify_full_codec_exhaustive import finite_payload, result_matches, stat_value  # noqa
ART=SELF/'full-codec-v0.3.json'; CON=SELF/'full-codec-contract-v0.3.json'; PYL=NeedLimits(max_transitions=5_000_000,max_depth=8_000)
def fail(m): raise SystemExit('stage5.12 bounded exhaustive full-codec v0.3 failed: '+m)
def main():
    a=json.loads(ART.read_text()); c=json.loads(CON.read_text()); frozen=c['bounded_exhaustive_class']
    if a.get('version')!='0.3' or a.get('holdout_status')!='preregistered_unexecuted': fail('candidate identity/holdout drifted')
    if frozen.get('maximum_ast_nodes')!=3 or frozen.get('expected_term_count')!=27: fail('bounded class drifted')
    terms=[t for n in range(1,4) for t in exhaustive_terms(n)]
    if len(terms)!=27: fail('generated term count drifted')
    cases=[]; controls=[]
    for i,ast in enumerate(terms):
        cid=f'term-{i:02d}'; bits=encode_ast(ast); toks=list(tokens_of(ast))
        if encode_term(decode_exact(bits))!=bits: fail(cid+': Direct Python mismatch')
        cases.append((cid,bits,toks)); controls.append({'id':cid,'bits':bits})
    r=subprocess.run(['go','run','./cmd/nextermcontrol'],cwd=GO,input=json.dumps(controls),text=True,capture_output=True)
    if r.returncode: fail('Direct Go control failed: '+r.stderr.strip())
    gr={x['id']:x for x in json.loads(r.stdout)}
    for cid,bits,toks in cases:
        row=gr.get(cid)
        if row is None or row.get('error') or row.get('reencoded')!=bits or row.get('tokens')!=[str(x) for x in toks]: fail(cid+': Direct Go mismatch')
    src=source_terms_full_codec_v0_3(); dec=src['decodeTerm']; enc=src['encodeTerm']; wrappers=[]
    for cid,bits,toks in cases:
        bv=[int(x) for x in bits]; dc=app(dec,literal_finite_bits(bits)); ec=app(enc,literal_finite_tokens(toks))
        wrappers += [(f'decode:{cid}',result_matches(dc,toks,0)),(f'encode:{cid}',result_matches(ec,bv,2)),(f'law1:{cid}',result_matches(app(dec,finite_payload(ec)),toks,0)),(f'law2:{cid}',result_matches(app(enc,finite_payload(dc)),bv,2))]
    expected={'kind':'Nat','value':'1'}; py={}; pyref=[]; req=[]; maxpt=0; maxpc=''
    for wid,w in wrappers:
        bits=encode_core(lower(w)); term=decode_exact(bits)
        try:
            obs,st=evaluate_need_observed(term,PYL)
            if obs!=expected: fail(wid+': Python need mismatch')
            py[wid]=obs
            if st.transitions>maxpt: maxpt,maxpc=st.transitions,wid
        except NeedResourceLimitError as e: pyref.append(f'{wid}: {e}')
        req.append({'id':'eval:'+wid,'level':'eval','bits':bits,'max_transitions':5_000_000,'max_depth':20_000})
    if pyref: fail('Python need refusals: '+' | '.join(pyref))
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
    if gn: fail('Go need refusals: '+' | '.join(gn))
    print('stage5.12 bounded exhaustive full codec v0.3: verified'); print('complete frozen Term class: 27/27')
    print('Direct Python canonical round trips: 27/27'); print('Direct Go canonical round trips/token projections: 27/27')
    print(f'NEX-on-Python/Go forced law observations: {matched}/108'); print('Python call-by-need resource refusals: 0'); print('Go call-by-need resource refusals: 0')
    print(f'Go CBN resource refusals: {len(gc)}'); print(f'largest Python need transition count: {maxpt} at {maxpc}'); print(f'largest Go need transition count: {maxgt} at {maxgc}')
    print('v0.3 holdout: NOT READ / NOT EXECUTED')
if __name__=='__main__': main()
