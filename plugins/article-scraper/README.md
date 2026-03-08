# article-scraper

범용 아티클 스크래퍼 미니 플러그인. URL 하나로 단건·목록 페이지를 자동 스크랩하여 번역·요약 후 Obsidian에 저장한다.

## 설치

### 옵션 A: 메인 플러그인에 포함 (권장)

메인 플러그인(`claude-code-plugin`) 설치 시 함께 포함된다.

```bash
git clone https://github.com/heeyounggoo/claude-code-plugin ~/dev/claude-code-plugin
mkdir -p ~/.claude/plugins
ln -s ~/dev/claude-code-plugin ~/.claude/plugins/claude-code-plugin
```

`~/.claude/settings.json`에 추가:

```json
{
  "plugins": ["~/.claude/plugins/claude-code-plugin"]
}
```

### 옵션 B: 이 플러그인만 단독 설치

```bash
git clone https://github.com/heeyounggoo/claude-code-plugin ~/dev/claude-code-plugin
claude --plugin-dir ~/dev/claude-code-plugin/plugins/article-scraper
```

## 초기 설정

처음 사용 전 저장 경로를 설정한다.

```
/scrape:config
```

`vault_path`(Obsidian 볼트 경로)와 `output_dir`(저장 폴더명)을 입력하면 `.claude/scrape.local.md`에 저장된다.

설정을 건너뛰면 `$OBSIDIAN_VAULT_PATH` 환경변수 → `~/obsidian-vault/Articles/` 순으로 기본값을 사용한다.

## 사용법

```
/scrape <URL>
```

- **단건 아티클**: 본문 추출 → 번역/요약 → Obsidian 저장
- **목록 페이지**: 아티클 URL 추출 → 3개씩 병렬 처리 → 페이지네이션 자동 순회

## 저장 포맷

```markdown
---
title: 제목
date: 260308
tags: [tag1, tag2]
source: https://...
---

(번역된 본문)

## 정리

**주제**: ...
**중요한 점**:

- ...
```
