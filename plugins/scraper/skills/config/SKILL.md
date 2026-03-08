---
name: config
description: Scraper 플러그인의 vault_path 설정을 조회하거나 변경. "볼트 경로 설정", "obsidian 경로 변경", "scraper 설정", "/config" 등을 요청하면 이 스킬을 사용.
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
argument-hint: "[설정항목] [값]"
---

# /config — Scraper 플러그인 설정

`~/.claude/scraper.local.md`를 읽고 설정을 조회하거나 수정한다.

---

## 1단계: 현재 설정 읽기

Read로 `~/.claude/scraper.local.md`를 읽는다.

파일이 없거나 읽기 실패 시 기본값을 사용한다:
- `vault_path`: `~/obsidian-vault`

`$OBSIDIAN_VAULT_PATH` 환경변수 존재 여부도 Bash로 확인한다:
```bash
echo $OBSIDIAN_VAULT_PATH
```

---

## 2단계: 현재 설정 출력

아래 형식으로 현재 설정을 출력한다:

```
현재 Scraper 설정

vault_path: {값}
환경변수 $OBSIDIAN_VAULT_PATH: {설정됨: {값} | 미설정}

* 환경변수가 설정된 경우 환경변수가 우선 적용됩니다.
```

---

## 3단계: 수정할 항목 선택

`$ARGUMENTS`가 있으면 그 값을 바로 사용한다 (예: `vault_path ~/my-vault`).

없으면 AskUserQuestion으로 확인한다:

```
어떤 설정을 변경할까요?
options:
  - vault_path: Obsidian 볼트 경로 변경
  - cancel: 취소
```

---

## 4단계: 값 입력

`vault_path` 선택 시 AskUserQuestion으로 새 경로를 입력받는다:

```
새 Obsidian 볼트 경로를 입력해주세요.
(예: ~/Documents/obsidian, /Users/me/vault)
현재 값: {현재값}
```

---

## 5단계: 저장

`~/.claude/scraper.local.md`에 Write로 저장한다.

파일 포맷:
```markdown
---
vault_path: {새 경로}
---
```

---

## 6단계: 완료 메시지

```
✅ 설정이 저장되었습니다
   vault_path: {새 경로}
   파일: ~/.claude/scraper.local.md
```
