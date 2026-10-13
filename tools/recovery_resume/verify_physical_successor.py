#!/usr/bin/env python3
"""Scan restored active source and apply only the checksum-selected lookup overlay."""
import argparse
import json
import shutil
import sys
from pathlib import Path


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,required=True)
    parser.add_argument('--project',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    repo,project,output=args.repository.resolve(),args.project.resolve(),args.output.resolve()
    if project.is_relative_to(repo) or output.is_relative_to(project):
        raise ValueError('Use independent owned output directories')
    sys.path.insert(0,str(repo/'tools/day_trigger_acceptance'))
    import inputs
    pins=inputs.load_pins()
    for f in (repo/'project').rglob('*'):
        if f.is_file():
            if f.is_symlink():raise ValueError('Symlink input')
            target=project/f.relative_to(repo/'project');target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,target)
    actual=inputs.scan_inputs(project)
    expected=inputs.validate_snapshot(inputs.read_json(project/'reports/release-input-snapshot.json'))
    inputs.compare_inputs(actual,expected)
    if {k:actual[k] for k in ('files','snapshot_sha256')}!=pins['numeric_future_snapshot']:
        raise ValueError('Current promoted source is not the pinned numeric parent')
    if inputs.byte_identity(inputs.encoded(actual))!=pins['numeric_future_manifest']:
        raise ValueError('Physical numeric manifest bytes differ')
    before=actual
    selected=output/'selected/project';selected.mkdir(parents=True,exist_ok=False)
    for role,specification in pins['lookup_capsules'].items():inputs.checked_capsule(repo,specification)
    for row,selection in zip(pins['lookup_source_changes'],pins['lookup_payload_resolutions']):
        inputs.require(row['path']==selection['path'],'Role ordering mismatch')
        f=inputs.checked_identity(repo/pins['lookup_capsules'][selection['capsule']]['path'],selection['source'],row['candidate'])
        target=selected/row['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,target)
    inputs.apply_changes(project,selected.parent,pins['lookup_source_changes'])
    after=inputs.scan_inputs(project);future=inputs.derive(before,pins['lookup_source_changes']);inputs.compare_inputs(after,future)
    inputs.require({k:after[k] for k in ('files','snapshot_sha256')}==pins['future_snapshot'],'Physical combined identity mismatch')
    inputs.require(inputs.byte_identity(inputs.encoded(after))==pins['future_manifest'],'Physical combined manifest mismatch')
    (output/'before-inputs.json').write_bytes(inputs.encoded(before));(output/'after-inputs.json').write_bytes(inputs.encoded(after))
    (project/'reports/release-input-snapshot.json').write_bytes(inputs.encoded(after))
    result={'status':'PHYSICAL_NUMERIC_TO_LOOKUP_REPORT_SUCCESSOR_VERIFIED','before':{k:before[k] for k in ('files','snapshot_sha256')},
            'after':{k:after[k] for k in ('files','snapshot_sha256')},'selected_source_paths':21,'android_runtime_executed':False,
            'full_runtime_1_to_1_established':False}
    (output/'physical-source.json').write_bytes(inputs.encoded(result)+b'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
