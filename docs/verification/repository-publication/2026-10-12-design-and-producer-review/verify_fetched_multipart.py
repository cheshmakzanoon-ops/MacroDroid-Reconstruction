"""Stream immutable multipart containers from fetched Git blobs without assembly."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess


def check(condition, message):
    if not condition:
        raise ValueError(message)


def safe_path(value):
    check(isinstance(value, str), "path must be a string")
    path = PurePosixPath(value)
    check(not path.is_absolute() and ".." not in path.parts and path.as_posix() == value,
          "noncanonical repository path")
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--git-dir", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--manifest", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    check(re.fullmatch(r"[0-9a-f]{40}", args.commit) is not None, "invalid commit")
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    git = ["git", "--git-dir=" + str(args.git_dir), "--literal-pathspecs"]
    subprocess.run(git + ["cat-file", "-e", args.commit + "^{commit}"], check=True)

    def tree_entry(path):
        raw = subprocess.check_output(git + ["ls-tree", "-z", args.commit, "--", path])
        rows = raw.split(b"\0")
        check(len(rows) == 2 and rows[-1] == b"", "expected exactly one tree entry")
        metadata, actual_path = rows[0].split(b"\t", 1)
        mode, kind, oid = metadata.decode().split(" ")
        check(actual_path.decode() == path and mode == "100644" and kind == "blob",
              "unexpected tree path, mode, or object kind")
        return oid

    results = []
    for name in args.manifest:
        name = safe_path(name)
        manifest_oid = tree_entry(name)
        raw = subprocess.check_output(git + ["cat-file", "blob", manifest_oid])
        manifest = json.loads(raw)
        check(manifest["format"] == "macrodroid-multipart-artifact" and
              type(manifest["format_version"]) is int and manifest["format_version"] == 1,
              "unsupported multipart manifest")
        check(type(manifest["size_bytes"]) is int and manifest["size_bytes"] > 0,
              "invalid container size")
        check(re.fullmatch(r"[0-9a-f]{64}", manifest["sha256"]) is not None,
              "invalid container digest")
        check(isinstance(manifest["parts"], list) and manifest["parts"], "empty part list")
        container_hash = hashlib.sha256()
        total, seen, parts = 0, set(), []
        for part in manifest["parts"]:
            path = safe_path(part["path"])
            check(path not in seen, "duplicate part path")
            seen.add(path)
            check(type(part["size_bytes"]) is int and part["size_bytes"] > 0,
                  "invalid part size")
            oid = tree_entry(path)
            check(oid == part["git_blob_sha1"], "manifest/tree object mismatch")
            sha256 = hashlib.sha256()
            git_sha1 = hashlib.sha1(b"blob " + str(part["size_bytes"]).encode() + b"\0")
            size = 0
            process = subprocess.Popen(git + ["cat-file", "blob", oid], stdout=subprocess.PIPE)
            with process.stdout:
                while True:
                    chunk = process.stdout.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    sha256.update(chunk)
                    git_sha1.update(chunk)
                    container_hash.update(chunk)
            check(process.wait() == 0, "Git blob reader failed")
            check(size == part["size_bytes"] and sha256.hexdigest() == part["sha256"] and
                  git_sha1.hexdigest() == oid, "fetched part byte identity differs")
            parts.append(dict(path=path, bytes=size, sha256=sha256.hexdigest(),
                              git_blob_sha1=oid, mode="100644", verified=True))
            total += size
        check(total == manifest["size_bytes"] and container_hash.hexdigest() == manifest["sha256"],
              "fetched concatenation identity differs")
        results.append(dict(manifest_path=name, manifest_git_blob_sha1=manifest_oid,
                            manifest_sha256=hashlib.sha256(raw).hexdigest(),
                            bytes=total, sha256=container_hash.hexdigest(), parts=parts,
                            exact_container_identity_verified=True))
    result = dict(schema=1, status="FETCHED_MULTIPART_CONTAINER_IDENTITIES_VERIFIED",
                  started_utc=started,
                  completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  commit=args.commit, git_directory=str(args.git_dir),
                  executed_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  assembled_container_written=False, application_or_runtime_retested=False,
                  containers=results)
    with args.output.open("x", encoding="utf-8") as out:
        out.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(status=result["status"], commit=args.commit,
                         containers=len(results), bytes=sum(row["bytes"] for row in results),
                         output=str(args.output))))


if __name__ == "__main__":
    main()
