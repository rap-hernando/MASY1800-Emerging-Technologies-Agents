"""Validate saved artifacts and prompt construction; does not execute an LLM."""
from pathlib import Path
import copy
import hashlib
import json
import os
import subprocess
import sys
class ValidationError(ValueError):
 pass

class ContractValidator:
 """Validate every keyword used by these two frozen schemas; fail on new ones.

 Not a general JSON Schema implementation. The frozen contracts use objects,
 arrays, strings, required, properties, items and additionalProperties only.
 """
 def __init__(self,schema):
  self.schema=schema
  self.check_schema(schema)
 def check_schema(self,schema):
  supported={'$schema','title','description','type','required','properties','items','additionalProperties'}
  if set(schema)-supported: raise ValueError('Unsupported schema keywords: '+str(set(schema)-supported))
  if schema.get('type') not in {'object','array','string'}: raise ValueError('Unsupported schema type')
  for sub in schema.get('properties',{}).values():self.check_schema(sub)
  if 'items' in schema:self.check_schema(schema['items'])
 def validate(self,data):self.visit(data,self.schema,'$')
 def visit(self,data,schema,path):
  kind=schema['type'];expected={'object':dict,'array':list,'string':str}[kind]
  if not isinstance(data,expected):raise ValidationError(path+' must be '+kind)
  if kind=='object':
   for key in schema.get('required',[]):
    if key not in data:raise ValidationError(path+' missing '+key)
   props=schema.get('properties',{})
   if schema.get('additionalProperties') is False and set(data)-set(props):raise ValidationError(path+' has extra fields')
   for key,value in data.items():
    if key in props:self.visit(value,props[key],path+'.'+key)
  elif kind=='array' and 'items' in schema:
   for i,value in enumerate(data):self.visit(value,schema['items'],path+'['+str(i)+']')

ROOT=Path(__file__).resolve().parents[3]
AGENT=ROOT/'agents/diffusion_agent'
os.environ['PYTHONUTF8']='1'
def run(*args):
 result=subprocess.run([sys.executable,*args],cwd=ROOT,text=True,encoding='utf-8',capture_output=True,check=True)
 return result.stdout.strip()
print(run('tools/check_frozen_core.py'))
iv=ContractValidator(json.loads((ROOT/'core/input_schema.json').read_text(encoding='utf-8')))
ov=ContractValidator(json.loads((ROOT/'core/output_schema.json').read_text(encoding='utf-8')))
meta=json.loads((AGENT/'agent_metadata.json').read_text(encoding='utf-8'))
specialist=(AGENT/'specialist_instructions.md').read_text(encoding='utf-8')
ledger=json.loads((AGENT/'sources/source_ledger.json').read_text(encoding='utf-8'))
assert json.loads(specialist.split('```json\n',1)[1].split('\n```',1)[0])==ledger['sources']
print('PASS: embedded evidence capsule matches source ledger')
cases=sorted((AGENT/'cases').glob('*.json'))
assert len(cases)==5
last=None
for case in cases:
 iv.validate(json.loads(case.read_text(encoding='utf-8')))
 response=AGENT/'responses'/f'{case.stem}_response.json'
 data=json.loads(response.read_text(encoding='utf-8'));ov.validate(data);assert data['agent']==meta
 basic=run('tools/validate_response.py',str(response))
 packet=ROOT/'work'/f'diffusion_agent_{case.stem}_prompt.txt'
 run('tools/build_prompt.py','--agent','agents/diffusion_agent','--case',str(case),'--out',str(packet))
 content=packet.read_text(encoding='utf-8'); assert specialist in content
 assert json.dumps(json.loads(case.read_text(encoding='utf-8')),indent=2) in content
 print(f'PASS: {case.stem}: input/full output schema, {basic}, packet construction; packet SHA256={hashlib.sha256(packet.read_bytes()).hexdigest()}')
 last=data
for name, mutate in [('extra top-level field',lambda x:x.update(extra='invalid')),('missing evidence denominator note field',lambda x:x['evidence'][0].pop('notes'))]:
 bad=copy.deepcopy(last);mutate(bad)
 try:ov.validate(bad)
 except ValidationError:print('PASS: full schema rejects '+name)
 else:raise AssertionError('invalid response accepted: '+name)
print('COMPLETE: 5 cases, 5 saved examples and 5 prompt packets validated. No LLM was invoked; semantic/factual quality requires human review and fresh model runs.')
