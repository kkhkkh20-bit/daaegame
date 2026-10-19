#!/usr/bin/env python3
"""Read-only exact-preimage guard. Never copies files, mutates git, or skips a mismatch."""
import argparse
import hashlib
import json
from pathlib import Path

def git_blob(path):
    data=path.read_bytes();return hashlib.sha1(('blob %d\0'%len(data)).encode()+data).hexdigest()

def verify(root,manifest,after=False):
    problems=[]
    reserved=manifest.get('reserved_manifest_path')
    if not after and reserved and (root/reserved).exists():
        problems.append(dict(path=reserved,reason='ADDED_PATH_ALREADY_EXISTS'))
    if any(path not in manifest['preimages'] for path in manifest.get('modifications', {})):
        problems.append(dict(reason='MODIFICATION_WITHOUT_PREIMAGE'))
    for path,expected in manifest['preimages'].items():
        if after:expected=manifest.get('modifications', {}).get(path, {}).get('after', expected)
        file=root/path
        actual=git_blob(file) if file.is_file() else None
        if actual!=expected:problems.append(dict(path=path,expected=expected,actual=actual,reason='PREIMAGE_MISMATCH'))
    for path,expected in manifest['additions'].items():
        file=root/path
        if not after and file.exists():problems.append(dict(path=path,reason='ADDED_PATH_ALREADY_EXISTS'))
        if after and (not file.is_file() or git_blob(file)!=expected):problems.append(dict(path=path,reason='ADDED_PAYLOAD_MISMATCH'))
    return problems

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,required=True,help='experiments/renpy-ch1 root');parser.add_argument('--after-addition',action='store_true');parser.add_argument('--manifest',type=Path,default=Path(__file__).with_name('placement-contract-preimages.json'));args=parser.parse_args()
    manifest=json.loads(args.manifest.read_text());problems=verify(args.root,manifest,args.after_addition)
    print(json.dumps(dict(base=manifest['baseline_commit'],mode='after' if args.after_addition else 'before',passed=not problems,problems=problems),indent=2))
    return 1 if problems else 0
if __name__=='__main__':raise SystemExit(main())
