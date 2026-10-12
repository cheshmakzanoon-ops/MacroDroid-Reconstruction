#!/usr/bin/env python3
"""Freeze the complete small indicator dossier without copying its APK/ZIP inputs."""
from pathlib import Path
import gzip
import hashlib
import io
import json
import stat
import tarfile

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'checkpoints/01-source-and-ordering-dossier'


def row(p, relative):
    data = p.read_bytes()
    return {'path': relative, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'mode': stat.S_IMODE(p.stat().st_mode)}


def main():
    DEST.mkdir(parents=True, exist_ok=False)
    expected = {
        '03-invoked-method-and-full-frame-review': 'SCOPED_SOURCE_AND_RAW_FRAME_OBSERVATIONS_VERIFIED',
        '06-source-derived-ordering-witness': 'SOURCE_DERIVED_ORDERING_WITNESS_RECORDED',
        '07-later-incomplete-run-five-screen-observations': 'LATER_INCOMPLETE_RUN_FIVE_SCREEN_OBSERVATIONS_VERIFIED',
        '08-prior-normal-scale-failure-context': 'PRIOR_ALL_SCALES_ONE_FAILURE_CONTEXT_VERIFIED',
    }
    for path, status in expected.items():
        assert json.loads((ROOT/'reports'/path/'result.json').read_text())['status'] == status
    assert json.loads((ROOT/'study01-command.json').read_text())['returncode'] == 1
    for n in ('03','06','07','08'):
        assert json.loads((ROOT/('study'+n+'-command.json')).read_text())['returncode'] == 0
    source_files = sorted([*ROOT.glob('*.py'), *ROOT.glob('*.md')])
    sources = []
    for p in source_files:
        assert p.is_file() and not p.is_symlink()
        q = DEST/p.name
        q.write_bytes(p.read_bytes())
        q.chmod(stat.S_IMODE(p.stat().st_mode))
        assert q.read_bytes() == p.read_bytes()
        sources.append(row(q,p.name))
    evidence = sorted([p for p in (ROOT/'reports').rglob('*') if p.is_file()] +
                      list(ROOT.glob('study*-command.json')) + list(ROOT.glob('study*-stdout.log')) +
                      list(ROOT.glob('study*-stderr.log')))
    assert all(not p.is_symlink() for p in evidence)
    inventory = [row(p,p.relative_to(ROOT).as_posix()) for p in evidence]
    archive = DEST/'evidence.tar.gz'
    with archive.open('wb') as raw:
        with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as compressed:
            with tarfile.open(mode='w',fileobj=compressed,format=tarfile.PAX_FORMAT) as tar:
                for p, info in zip(evidence,inventory):
                    data = p.read_bytes()
                    assert hashlib.sha256(data).hexdigest() == info['sha256']
                    member = tarfile.TarInfo(info['path'])
                    member.size = len(data)
                    member.mode = info['mode']
                    member.mtime = 0
                    tar.addfile(member,io.BytesIO(data))
    with tarfile.open(archive,'r:gz') as tar:
        members = tar.getmembers()
        assert [m.name for m in members] == [r['path'] for r in inventory]
        for member, info in zip(members,inventory):
            assert member.isfile() and member.mode == info['mode']
            data = tar.extractfile(member).read()
            assert len(data) == info['bytes'] and hashlib.sha256(data).hexdigest() == info['sha256']
    compact = []
    for p in evidence:
        rel = p.relative_to(ROOT)
        if p.name in ('result.json','failure.json','failure-observation.json','commands.json',
                      'closed-failure-provenance.json','five-pixel-observations.json',
                      'whole-class-and-invoked-method-results.json') or rel.parts[0].startswith('study'):
            q = DEST/'review-evidence'/rel
            q.parent.mkdir(parents=True,exist_ok=True)
            q.write_bytes(p.read_bytes())
            q.chmod(stat.S_IMODE(p.stat().st_mode))
            compact.append(row(q,q.relative_to(DEST).as_posix()))
    checkpoint = {
        'schema':1,
        'scope':'Bounded read-only indicator source/pixel dossier; retained-fraction hypothesis and Android proposal only',
        'source_files':sources,
        'review_evidence_files':compact,
        'evidence_archive':row(archive,archive.name),
        'evidence_member_count':len(inventory),
        'evidence_members':inventory,
        'historical_broad_class_gate_still_failed':True,
        'original_source_class_comparisons_equal':26,
        'candidate_source_whole_class_comparisons_equal':25,
        'candidate_q77_t_method_unchanged_and_only_q77_B_registered_change':True,
        'historical_eighteen_class_two_apk_comparisons_equal':36,
        'earlier_within_apk_pairs_zero':12,
        'earlier_cross_apk_pairs_five_pixels':16,
        'later_five_available_screen_pairs_zero':5,
        'same_apk_cross_run_pixel_counts':{'original':31,'candidate':34},
        'normal_scale_run_uses_older_candidate_and_remains_failed':True,
        'source_derived_traces_are_not_dex_or_android_execution':True,
        'cause_proven':False,'android_proposal_executed':False,
        'active_source_policy_registry_or_apk_modified':False,
    }
    cp = DEST/'checkpoint.json'
    cp.write_text(json.dumps(checkpoint,indent=2)+'\n')
    for p, info in zip(evidence,inventory):
        assert row(p,p.relative_to(ROOT).as_posix()) == info
    print(json.dumps({'checkpoint':str(cp),'checkpoint_bytes':cp.stat().st_size,
                      'checkpoint_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
                      'source_files':len(sources),'compact_files':len(compact),
                      'evidence_members':len(inventory),'archive':checkpoint['evidence_archive']},sort_keys=True))


if __name__ == '__main__':
    main()
