---
name: wrap
description: Session wrap-up and Obsidian save. Two modes: (1) Add mode — triggered by "add to obsidian", "obsidian save", "옵시디언에 추가", "옵시디언 정리", "obsidian 저장" etc. when saving specific content to Obsidian; (2) Session summary mode — triggered by "/wrap", "세션 정리", "세션 마무리", "wrap up session" etc. Works for all session types: coding, learning, planning, discussion.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - AskUserQuestion
argument-hint: "[content or obsidian-vault-path]"
---

# /wrap — Obsidian Save & Session Summary

## Step 0: Determine Mode

```
$ARGUMENTS present → Mode A: Add content
$ARGUMENTS absent  → Mode B: Session summary
```

## Step 1: Resolve Obsidian Vault Path

Priority order:

1. If `$ARGUMENTS` looks like a file path, use it
2. Read `config.json` in the skill directory — parse `obsidian_vault_path`
   - Use the Read tool to load the file, then parse JSON
3. Fall back to `$OBSIDIAN_VAULT_PATH` environment variable
4. Default: `~/obsidian-vault/claude-sessions/`

Copy `config.example.json` → `config.json` to configure the vault path.

Once resolved, run `mkdir -p <path>` via Bash to ensure the directory exists.

## Step 2: Collect Basic Info

Run via Bash:

- `date "+%y%m%d %H:%M"` — current timestamp
- Mode B only: `git diff --stat`, `git log --oneline -20`, `git diff --name-only` (skip silently if not a git repo)

## Step 3: Write Content

### Common Wrapper Format

All saved content uses this wrapper:

```markdown
## {title}

| Field | Value |
|-------|-------|
| Date | {YYMMDD HH:MM} |
| Project / Topic | {context} |
| Tags | {#tag1 #tag2} |

{mode-specific content}
```

---

### Mode A: Add Content

Write the content from `$ARGUMENTS` as a proper memo or document — not a raw dump, but structured and readable.

- **Title**: extract the core topic from the arguments
- **Tags**: auto-generate based on content
- **Body**: format as a memo/note using lists, tables, or headers as appropriate. Write in Korean.

---

### Mode B: Session Summary

Analyze the **full conversation** from start to finish and write a Korean summary using the structure below:

```markdown
### 세션 흐름

{Narrative of what happened in the session, in chronological order. Include the flow of conversation, exploration, key decision moments, and any blockers. 3–7 sentences.}

### 계획 (only if plan mode was used)

{Core of any plan established — what, why, and in what order. 3–5 lines.}

### 주요 내용

{Auto-selected based on session type — include only what applies:}
- Coding / dev: what was implemented, changed, or fixed
- Learning / analysis: key concepts, insights, knowledge organized
- Planning / discussion: decisions made, open questions

### 이어서 할 것 (omit section if nothing)

- {items to continue in the next session}
```

**Writing rules:**
- All content in **Korean**
- Tags use `#` prefix (e.g. `#리팩토링 #버그수정`)
- Date format: `YYMMDD HH:MM` (e.g. `260211 14:30`)
- Omit sections entirely when empty — never write "없음"
- Include `### 계획` section if plan mode is detected: signs of planning in the conversation, or a related plan file exists under `~/.claude-personal/plans/`

## Step 4: Preview & Confirm

Show the generated content to the user, then ask for confirmation via AskUserQuestion.

- **Save as-is** → proceed to Step 5
- **Request edits** → revise based on feedback, then repeat Step 4
- **Cancel** → skip to Step 6 without saving

## Step 5: Save to Obsidian

Filename format: `YYMMDD.md` (e.g. `260211.md`).

1. Use Glob to check if the file already exists
2. **File exists:**
   - Read existing content
   - **Mode B:** Parse existing `## ` sections for title and tags. If the current summary is a continuation of an existing section (same project, overlapping tags, same topic thread), **merge**: expand date range, update 세션 흐름 / 주요 내용 / 이어서 할 것, use Edit tool. Otherwise, append with `\n\n---\n\n` separator and Write.
   - **Mode A:** Always append with `\n\n---\n\n` separator
3. **File does not exist:** Write as a new file

## Step 6: Done

Output a completion message in this format:

```
📋 저장 완료
   경로: {full file path}
   제목: {one-line title of saved content}
   저장 방식: {새로 추가 | 기존 세션에 병합 | 추가(append)}

세션이 마무리되었습니다. 수고하셨습니다!
💡 컨텍스트 압축을 위해 `/compact` 명령을 실행해주세요.
```

Note: `/compact` is a built-in Claude Code command and cannot be triggered from within a skill. Always prompt the user to run it manually.
