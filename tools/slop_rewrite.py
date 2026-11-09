#!/usr/bin/env python3
"""설치한 한국어 윤문 검사기를 호출한다. 원문 쓰기·외부 전송 기능은 없다."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('file',nargs='?')
    p.add_argument('--guide',default='없음')
    p.add_argument('--genre',choices=['줄글','개조식','공통'])
    p.add_argument('--orig')
    p.add_argument('--record')
    for mode in ('hint','prompt','bundle','status'):
        p.add_argument('--'+mode,action='store_true')
    args=p.parse_args()
    config=json.loads((ROOT/'tools/slop-rewrite.json').read_text())
    source=Path(config['installation_root'])
    runner=source/'.claude/skills/slop-rewrite/scripts/check_all.py'
    if not runner.is_file():
        p.error('본체가 없습니다. docs/writing/SLOP_REWRITE.md의 설치 절차를 실행하세요.')
    result=subprocess.run(['git','rev-parse','HEAD'],cwd=source,capture_output=True,text=True,check=True)
    actual=result.stdout.strip()
    if actual!=config['source_commit']:
        p.error('고정 소스와 설치본 버전이 다릅니다. 설정과 변경 내역을 먼저 확인하세요.')
    if args.status:
        print(json.dumps(dict(source_commit=actual,installation_root=str(source),runner_exists=True,private_taste_exists=(source/'taste/writing-taste.md').is_file()),ensure_ascii=False,indent=2))
        return 0
    if not args.file:p.error('검사할 원문 파일이 필요합니다.')
    command=[sys.executable,'-X','utf8',str(runner),'--guide',args.guide]
    if args.genre:command+=['--genre',args.genre]
    for key in ('hint','prompt','bundle'):
        if getattr(args,key):command.append('--'+key)
    for key in ('orig','record'):
        value=getattr(args,key)
        if value:command+=['--'+key,str(Path(value).resolve())]
    command.append(str(Path(args.file).resolve()))
    return subprocess.run(command,cwd=source).returncode

if __name__=='__main__':raise SystemExit(main())
