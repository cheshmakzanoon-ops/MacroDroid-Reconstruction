from pathlib import Path
import hashlib,json,shutil,datetime
base=Path('/dev/shm/ink-indicator-fixed-sampling-01')
output=base/'checkpoints/01-incomplete-runtime-draft'
output.mkdir(parents=True,exist_ok=False)
inputs=[]
for folder in ('source','parent-inputs','evidence/draft-00-before-slot-isolation'):
 inputs += [p for p in (base/folder).rglob('*') if p.is_file()]
inputs += [base/p for p in ('bootstrap_source.py','source-input-binding.json','rewrite_record_stage.py','freeze_draft_01.py')]
rows=[]
for path in sorted(inputs):
 name=path.relative_to(base).as_posix()
 data=path.read_bytes()
 target=output/name
 target.parent.mkdir(parents=True,exist_ok=True)
 target.write_bytes(data)
 target.chmod(path.stat().st_mode & 0o777)
 rows.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'mode':oct(path.stat().st_mode & 0o777)})
text='''# Incomplete fixed indicator runtime draft — inactive checkpoint\n\nThis checkpoint preserves authored work before its first host validation. It is not runnable acceptance tooling, is not an activated workflow, and reports no Android execution, measured pixel result, parity credit, or source-method recovery. The independent prefix/experiment verifier, complete CLI integration, host controls, runtime file manifest, and workflow are still being completed. Calls to not-yet-implemented functions in this draft are pending work, not executed successes.\n\nThe frozen design is `fccc817be37d821a781348a8870c227ff5471fcdc72d71f38a81bc062c7a3eec`, published at commit `39250fac022aee5551f36782bafd72cabbc33718`, under `work-in-progress/indicator-fixed-sampling/01-bounded-design`. All sixteen parent declarations remain pinned to `6331410cfd2391389270564803623079e8355ad8`.\n\nRoot approved three explicit implementation deltas: (1) exact AAPT2 6,135,688 bytes / `6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745` as a read-only, 60-second `dump badging` dependency; (2) eight separately queued fixed-index slots bounded at 900 seconds apiece, in separate owned directories, preserving the unchanged parent's 3,600-second queue limit and one global 7,200-second deadline, aborting the remaining schedule after a failure; and (3) lossless streamed gzip records containing a four-byte row-major pixel index and two four-byte RGBA tuples, with dimensions/count/hashes and an independent decode/recount. No frame choice, settling, masks, tolerance or additional comparison credit is introduced.\n\nAll 40 planned post-input observations and 92 predetermined comparisons remain required. The two APK identities, condition A then B, O/C/C/O order, single observed NEXT selector, 2-second post-input wait and 1-second completion-to-next-start gap are unchanged. The initial draft is retained separately under `evidence/draft-00-before-slot-isolation`.\n\nThis checkpoint is immutable. Further implementation and its actual failed/passed checks will be frozen as a separate successor. No application source, APK, existing recorder or existing comparison policy has been edited.\n'''
(output/'README.md').write_text(text)
rows.append({'path':'README.md','bytes':len(text.encode()),'sha256':hashlib.sha256(text.encode()).hexdigest(),'mode':'0o644'})
result={'schema':1,'status':'INCOMPLETE_INACTIVE_RUNTIME_DRAFT','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'android_executed':False,'host_tests_executed':False,'workflow_activated':False,'active_application_changed':False,'new_parity_credit':0,'design_checkpoint_sha256':'fccc817be37d821a781348a8870c227ff5471fcdc72d71f38a81bc062c7a3eec','files':rows}
(output/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
for row in rows:
 p=output/row['path']; data=p.read_bytes()
 assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
cp=(output/'checkpoint.json').read_bytes()
print(json.dumps({'path':str(output/'checkpoint.json'),'bytes':len(cp),'sha256':hashlib.sha256(cp).hexdigest(),'files':len(rows),'payload_bytes':sum(row['bytes'] for row in rows),'status':result['status']},indent=2))
