from pathlib import Path
import datetime
import gzip
import hashlib
import json
import os
import shutil
import stat
import subprocess

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
COMMIT = 'dbbb89cf4ca65edd3d2c2b96151dadf41aaec514'
PREFIX = 'docs/verification/storage-cleanup/20261012-validation-duplicates-assessment'
OUT = ROOT / 'transfer-validation-assessment' / 'placeholder-retirement'
NAMES = ('transfer-validation', 'overlay-bootstrap-validation')
TARGETS = tuple(ROOT / name for name in NAMES)
INVENTORY_SHA = '4a3ee9bdc09451080da9e0a2acd021126a86b33c15ba4f84c1681b715db773b0'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def write(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2) + '\n')

def under_target(text):
    text = text.removesuffix(' (deleted)')
    return any(text == str(path) or text.startswith(str(path) + '/') for path in TARGETS)

def process_guard():
    physical_self = os.readlink('/proc/self')
    assert physical_self.isdigit()
    ancestry = set()
    ancestor = physical_self
    while ancestor.isdigit() and ancestor != '0' and ancestor not in ancestry:
        ancestry.add(ancestor)
        try:
            status_text = (Path('/proc') / ancestor / 'status').read_text()
        except FileNotFoundError:
            break
        ancestor = next(line.split()[1] for line in status_text.splitlines() if line.startswith('PPid:'))
    matches = []
    unreadable = []
    readable = []
    scanned = 0
    for proc in Path('/proc').iterdir():
        if not proc.name.isdigit() or proc.name in ancestry:
            continue
        scanned += 1
        try:
            cwd = os.readlink(proc / 'cwd')
            if under_target(cwd):
                matches.append({'physical_pid': proc.name, 'kind': 'cwd'})
        except (FileNotFoundError, ProcessLookupError):
            pass
        except PermissionError:
            unreadable.append({'physical_pid': proc.name, 'kind': 'cwd'})
        try:
            comm = (proc / 'comm').read_text().strip()
            raw_argv = (proc / 'cmdline').read_bytes()
            argv = raw_argv.split(b'\0')
            readable.append(dict(physical_pid=proc.name, comm=comm, argv_bytes=len(raw_argv),
                                 argv_sha256=hashlib.sha256(raw_argv).hexdigest(),
                                 argv_first_basename=os.path.basename(os.fsdecode(argv[0])) if argv and argv[0] else ''))
            if any(str(path).encode() in item for path in TARGETS for item in argv):
                matches.append({'physical_pid': proc.name, 'kind': 'argv'})
        except (FileNotFoundError, ProcessLookupError):
            pass
        except PermissionError:
            unreadable.append({'physical_pid': proc.name, 'kind': 'argv'})
        try:
            for fd in (proc / 'fd').iterdir():
                try:
                    target = os.readlink(fd)
                    if under_target(target):
                        matches.append({'physical_pid': proc.name, 'kind': 'fd', 'fd': fd.name})
                except (FileNotFoundError, ProcessLookupError):
                    pass
        except (FileNotFoundError, ProcessLookupError):
            pass
        except PermissionError:
            unreadable.append({'physical_pid': proc.name, 'kind': 'fd'})
    result = dict(physical_self_pid=physical_self, python_namespace_pid=os.getpid(),
                  reviewer_physical_ancestry=sorted(ancestry, key=int),
                  process_count=scanned, matching_users=matches, unreadable=unreadable,
                  readable_comm_and_argv_inventory=readable,
                  cwd_fd_checks_passed=False if unreadable else True,
                  cwd_fd_permission_restrictions_not_bypassed=True,
                  approved_criterion='Closed owner-confirmed duplicates plus readable physical comm/argv and exact durable bytes; cwd/fd unavailability is explicit.')
    assert not matches and not any(item['kind'] == 'argv' for item in unreadable), result
    return result

OUT.mkdir(parents=True, exist_ok=False)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert subprocess.run(['git','merge-base','--is-ancestor',COMMIT,'origin/main'],cwd=REPO).returncode==0
for name in ('checkpoint.json','assessment.json','inventory.json.gz','assess_transfer_validation_duplicates.py'):
 assert git('show',COMMIT+':'+PREFIX+'/'+name)==(REPO/PREFIX/name).read_bytes()
compressed=(REPO/PREFIX/'inventory.json.gz').read_bytes()
assert hashlib.sha256(compressed).hexdigest()==INVENTORY_SHA
summary=json.loads((REPO/PREFIX/'assessment.json').read_text());raw=gzip.decompress(compressed)
assert len(raw)==summary['inventory_bytes'] and hashlib.sha256(raw).hexdigest()==summary['inventory_sha256']
rows=json.loads(raw);assert len(rows)==60809 and all(row['removal_candidate'] and row['kind']=='file' for row in rows)
assert all(Path(row['path']).parts[0] in NAMES and '..' not in Path(row['path']).parts for row in rows)
old_retained=json.loads((ROOT/'transfer-validation-assessment/retirement/retained-before.json').read_text())
retained_before={name:{'bytes':Path(name).stat().st_size,'sha256':sha(Path(name))} for name in old_retained}
assert retained_before==old_retained
write('retained-before.json',retained_before)
owners={'root':{'no_target_users':True,'active_paths':['/tmp/macrodroid-widget-plugin-combined-qmngc23u','combined-recovery/reports/05-full-acceptance'],'new_workspace_writes_paused':True},
 'build_environment':{'no_target_users':True,'all_local_subprocesses_closed':True,'new_workspace_writes_paused':True},
 'recover_touch_action':{'no_target_users':True,'active_paths':['widget-art-probe','video-monitor-recovery','/tmp/macrodroid-video-host-23wavrcl'],'new_workspace_writes_paused':True},
 'repository_transfer':{'owner_of_closed_validation_materializations':True,'no_other_target_users':True}}
write('owner-confirmations.json',owners)
write('process-guard-before.json',process_guard())
actual=set()
for target in TARGETS:
 assert target.is_dir() and not target.is_symlink()
 for directory,dirs,files in os.walk(target,followlinks=False):
  assert not any((Path(directory)/name).is_symlink() for name in dirs)
  for name in files:
   p=Path(directory)/name;assert p.is_file() and not p.is_symlink();actual.add(p.relative_to(ROOT).as_posix())
assert actual=={row['path'] for row in rows}
write('process-guard-immediate.json',process_guard())
disk_before=shutil.disk_usage(ROOT)._asdict()
write('pre-retirement.json',dict(status='AUTHORIZED_EXACT_DUPLICATE_PLACEHOLDER_RETIREMENT',commit=COMMIT,
 exact_roots=list(NAMES),files=len(rows),inventory_compressed_sha256=INVENTORY_SHA,
 explicit_cwd_fd_unavailable=True,all_four_owners_confirmed_no_users=True,short_write_barrier=True,disk=disk_before,
 source_payloads_remain_in_verified_git_archives=True))
changed=[]
for index,row in enumerate(sorted(rows,key=lambda row:(-row['bytes'],row['path']))):
 p=ROOT/row['path'];before=p.lstat()
 assert stat.S_ISREG(before.st_mode) and before.st_size==row['bytes'] and oct(stat.S_IMODE(before.st_mode))==row['mode'],row['path']
 before_hash=sha(p);assert before_hash==row['sha256'],row['path']
 assert p.lstat().st_ino==before.st_ino and p.lstat().st_size==before.st_size
 temporary=p.with_name('.retiring-'+str(os.getpid())+'-'+str(index))
 descriptor=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL,stat.S_IMODE(before.st_mode))
 try:
  os.fchmod(descriptor,stat.S_IMODE(before.st_mode));os.fsync(descriptor)
 finally:
  os.close(descriptor)
 os.replace(temporary,p)
 after=p.lstat();assert stat.S_ISREG(after.st_mode) and after.st_size==0 and after.st_blocks==0,row['path']
 changed.append(dict(path=row['path'],original_sha256=before_hash,
  before={'bytes':before.st_size,'allocated_bytes':before.st_blocks*512,'device':before.st_dev,'inode':before.st_ino,'mtime_ns':before.st_mtime_ns,'mode':oct(stat.S_IMODE(before.st_mode))},
  after={'bytes':after.st_size,'allocated_bytes':after.st_blocks*512,'device':after.st_dev,'inode':after.st_ino,'mtime_ns':after.st_mtime_ns,'mode':oct(stat.S_IMODE(after.st_mode))},
  placeholder_sha256=hashlib.sha256(b'').hexdigest()))
 if index%2000==0:
  write('progress.json',dict(files_replaced=len(changed),original_payload_bytes_replaced=sum(x['before']['bytes'] for x in changed),free_bytes=shutil.disk_usage(ROOT).free))
  print(json.dumps({'replaced':len(changed),'payload_bytes':sum(x['before']['bytes'] for x in changed),'free_bytes':shutil.disk_usage(ROOT).free}),flush=True)
assert len(changed)==60809
for row in changed:
 p=ROOT/row['path'];metadata=p.lstat();assert stat.S_ISREG(metadata.st_mode) and metadata.st_size==0 and metadata.st_blocks==0,row['path']
retained_after={name:{'bytes':Path(name).stat().st_size,'sha256':sha(Path(name))} for name in retained_before}
write('retained-after.json',retained_after);assert retained_after==retained_before
all_metadata=(json.dumps(changed,sort_keys=True,separators=(',',':'))+'\n').encode()
with (OUT/'full-before-after.json.gz').open('wb') as f:
 with gzip.GzipFile(fileobj=f,mode='wb',mtime=0,filename='') as z:z.write(all_metadata)
disk_after=shutil.disk_usage(ROOT)._asdict()
receipt=dict(status='EXACT_CLOSED_VALIDATION_PAYLOADS_RETIRED_TO_ZERO_BYTE_PLACEHOLDERS',started_utc=started,
 finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),verified_assessment_commit=COMMIT,exact_roots=list(NAMES),
 files=60809,original_logical_bytes_replaced=sum(row['before']['bytes'] for row in changed),original_allocated_bytes_replaced=sum(row['before']['allocated_bytes'] for row in changed),
 full_before_after_metadata_bytes=len(all_metadata),full_before_after_metadata_sha256=hashlib.sha256(all_metadata).hexdigest(),
 all_original_payloads_verified_against_durable_inventory_before_atomic_replacement=True,all_current_target_files_zero_length_and_zero_blocks=True,
 paths_deliberately_retained=True,no_claim_of_directory_removal=True,protected_source_and_evidence_files_rehashed=len(retained_before),protected_hashes_unchanged=True,
 cwd_fd_checks_unavailable_not_passed=True,readable_physical_process_guards_passed=2,all_four_owner_confirmations=True,
 permission_or_infrastructure_changes=False,original_archives_or_active_source_or_generated_acceptance_caches_modified=False,
 disk_before=disk_before,disk_after=disk_after,free_space_delta_bytes=disk_after['free']-disk_before['free'],disk_delta_observational_due_to_active_private_acceptance=True)
write('receipt.json',receipt);print(json.dumps(receipt),flush=True)
