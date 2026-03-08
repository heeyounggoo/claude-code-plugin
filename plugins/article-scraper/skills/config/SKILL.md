---
name: config
description: scrape 스킬 설정 관리. vault_path, output_dir 확인 및 업데이트.
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
---

# /scrape:config — scrape 설정 관리

scrape 스킬의 저장 경로 설정을 확인하고 업데이트한다.

## 1단계: 설정 파일 읽기

`.claude/scrape.local.md` 파일을 Read로 읽는다.

- 파일이 없으면 기본값을 표시한다:
  - `vault_path`: `~/obsidian-vault`
  - `output_dir`: `Articles`

현재 설정을 사용자에게 출력한다:

```
현재 설정:
  vault_path: {현재값 또는 "미설정 (기본값: ~/obsidian-vault)"}
  output_dir: {현재값 또는 "미설정 (기본값: Articles)"}
```

## 2단계: 설정 입력

AskUserQuestion으로 사용자에게 아래를 묻는다:

```
어떻게 변경하시겠어요?
1. vault_path 변경
2. output_dir 변경
3. 둘 다 변경
4. 취소
```

선택에 따라 해당 값을 AskUserQuestion으로 입력받는다.

취소 선택 시 종료 메시지 출력 후 종료.

## 3단계: 설정 파일 저장

`.claude/scrape.local.md`를 Write로 아래 포맷으로 저장한다.

기존 파일이 있으면 해당 값만 업데이트하고 나머지는 보존한다.

```markdown
---
vault_path: {입력값}
output_dir: {입력값}
---
```

## 4단계: 완료 메시지

```
설정이 저장되었습니다.
  vault_path: {저장된 값}
  output_dir: {저장된 값}
  파일: .claude/scrape.local.md

/scrape <URL> 명령으로 아티클 스크랩을 시작하세요.
```
