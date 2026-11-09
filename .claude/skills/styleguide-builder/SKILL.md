---
name: styleguide-builder
description: 사용자가 제공한 한국어 저자 코퍼스로 문체 가이드를 만들거나 갱신할 때 사용한다.
---

# styleguide-builder 진입점

본체: `/workspace/tools/slop-rewrite/.claude/skills/styleguide-builder/SKILL.md`
설치 루트: `/workspace/tools/slop-rewrite`
고정 소스: `byungjunjang/slop-rewrite@b6d301120cfa0ceec90b80907f6110995dcc7395`

현재 프로젝트의 작업 규칙을 먼저 확인하고, 위 본체를 읽어 실행한다. 본체의 프로젝트 루트는 설치 루트이고 모든 상대 명령은 설치 루트에서 실행한다. 프로젝트 원문은 절대 경로로 전달한다. 기존 원문과 코드·설정을 자동 교정하지 않는다.

다람탐정의 대사·소설 검토 기본값은 `가이드 없음`이다. 업무·블로그 가이드를 인물 말투에 적용하지 않는다. 로컬 취향은 설치 루트의 `taste/`에 있으며, 이 프로젝트에서는 [운용 설정](../../../docs/writing/SLOP_REWRITE.md)을 함께 읽는다. `검토`와 `윤문`을 구분하고, 게임 반영은 원본 보존·대사 판정 검증 절차를 따른다.
