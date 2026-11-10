"""Validate stored artifacts, not model reasoning. Standard library only."""
from pathlib import Path
import copy, json, subprocess, sys

A=Path(__file__).resolve().parent
ROOT=A.parents[1]
DIMS=['leadership/sponsorship','skills','workflow/process','infrastructure/data','resources/budget','governance/risk','culture/change','operating ownership']
def validate(value, schema, path='$'):
    types={'object':dict,'array':list,'string':str}
    assert isinstance(value,types[schema['type']]),path+' wrong type'
    if isinstance(value,dict):
        assert set(schema.get('required',[])) <= set(value),path+' required keys missing'
        props=schema.get('properties',{})
        if schema.get('additionalProperties') is False:
            assert set(value)<=set(props),path+' extra keys'
        for key,item in value.items():
            if key in props: validate(item,props[key],path+'.'+key)
    elif isinstance(value,list):
        for i,item in enumerate(value):validate(item,schema['items'],f'{path}[{i}]')

def semantics(out):
    text=out['organization_specific_finding']
    for dim in DIMS:
        line=next((v for v in text.splitlines() if v.startswith(dim+':')),None)
        assert line,dim+' missing'
        for label in ['Status:','Strength:','Gap:','Consequence:','Priority:','Action:','Likely owner:','Evidence:','Evidence needed:']:
            assert label in line,dim+' missing '+label
    ownership=next(v for v in text.splitlines() if v.startswith('operating ownership:'))
    if 'Status: UNKNOWN' in ownership:
        assert 'Overall readiness: READY FOR BOUNDED PILOT' not in text,'unknown ownership cannot pass'
        assert any('ownership UNKNOWN' in q for q in out['abstention_or_more_information_needed']),'ownership question missing'
    assert 'Technology/application fit:' in out['application_finding']
    assert 'Conditions to proceed:' in out['recommendation_management_implication']
    assert 'Conditions to pause:' in out['recommendation_management_implication']

def main():
    subprocess.run([sys.executable,str(ROOT/'tools/check_frozen_core.py')],check=True)
    inp=json.loads((ROOT/'core/input_schema.json').read_text())
    schema=json.loads((ROOT/'core/output_schema.json').read_text())
    names=['primary','contrast_high_readiness','contrast_low_readiness']
    cases=[];outputs=[]
    for name in names:
        case=json.loads((A/'cases'/f'{name}.json').read_text());validate(case,inp)
        out=json.loads((A/'responses'/f'{name}_response.json').read_text());validate(out,schema);semantics(out)
        subprocess.run([sys.executable,str(ROOT/'tools/validate_response.py'),str(A/'responses'/f'{name}_response.json')],check=True)
        for fact in case['capabilities_constraints'].splitlines():
            assert fact.split(' ')[0] in out['organization_specific_finding']
        cases.append(case);outputs.append(out);print(name+': schema, coverage and trace checks PASS')
    for key in ['emerging_technology','intended_application','adoption_posture','risk_consequence_context','management_question','time_horizon']:
        assert len({c[key] for c in cases})==1,key+' changed'
    for key in ['general_et_finding','application_finding']:
        assert len({o[key] for o in outputs})==1,key+' changed'
    for out,verdict in zip(outputs,['PARTIALLY READY','READY FOR BOUNDED PILOT','NOT READY']):
        assert 'Overall readiness: '+verdict in out['organization_specific_finding']
    extra=copy.deepcopy(outputs[0]);extra['readiness']={}
    bad=copy.deepcopy(outputs[0]);bad['organization_specific_finding']=bad['organization_specific_finding'].replace('Overall readiness: PARTIALLY READY','Overall readiness: READY FOR BOUNDED PILOT')
    for name,check in [('extra top-level key',lambda:validate(extra,schema)),('ready despite unknown owner',lambda:semantics(bad))]:
        try:check()
        except AssertionError:print('Negative fixture rejected: '+name)
        else:raise AssertionError('Negative fixture accepted: '+name)
    print('LAB 7 VALIDATION PASSED; semantic and real-world verification limits remain.')

if __name__=='__main__':main()
