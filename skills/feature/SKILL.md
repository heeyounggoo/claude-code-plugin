---
name: feature
description: >
  "새 기능 만들어줘", "스킬 추가하고 싶어", "커맨드 만들어줘", "훅 필요해",
  "플러그인 기능 구현해줘", "새 스킬 만들어줘" 등 Claude Code 플러그인 컴포넌트
  (skill/command/hook/agent)를 새로 만들거나 기존 기능을 확장하고 싶을 때 사용.
  아이디어 → 요구사항 정리 → 구현 도구 선택 → 구현 실행까지 전체 과정을 안내한다.
allowed-tools:
  - AskUserQuestion
  - Read
  - Glob
  - Grep
  - Skill
argument-hint: "[기능 아이디어 (선택사항)]"
---

# /feature — 새 기능 구현 워크플로우

Claude Code 플러그인에 새 기능을 추가하는 전체 흐름을 안내한다.
아이디어만 있어도 시작할 수 있고, 대화를 통해 구체화한 뒤 적절한 구현 도구를 선택해 실행한다.

---

## Phase 1: Intent Capture

args가 있으면 그 내용을 아이디어로 사용하고 Phase 2로 이동한다.
args가 없으면 AskUserQuestion으로 질문한다:

> "어떤 기능을 만들고 싶으세요? 아이디어를 자유롭게 설명해주세요."

---

## Phase 2: 기존 스킬 현황 파악

Glob으로 현재 프로젝트의 스킬 목록을 스캔한다:

- `skills/*/SKILL.md`
- `plugins/*/skills/*/SKILL.md`

기존 스킬 이름과 description을 빠르게 읽어 중복 또는 확장 가능한 것이 있는지 확인한다.

---

## Phase 3: Interview (최대 2라운드)

아이디어를 구체화하기 위해 AskUserQuestion으로 질문한다.
**핵심 질문 (1라운드):**

- 언제/어떤 상황에서 이 기능을 사용하게 되나요? (트리거 조건)
- 입력값과 최종 결과(출력)는 무엇인가요?

**보충 질문 (필요 시 2라운드):**

- 기존 스킬과 겹치는 부분이 있나요, 아니면 완전히 새로운 건가요?
- 자동으로 실행되어야 하나요, 아니면 사용자가 직접 호출하나요?

---

## Phase 4: 컴포넌트 타입 분류

인터뷰 내용을 바탕으로 적절한 컴포넌트 타입을 판단한다:

| 특징                                             | 컴포넌트    | 구현 도구                        |
| ------------------------------------------------ | ----------- | -------------------------------- |
| 대화형 워크플로우, 단계별 안내, `/명령어`로 실행 | **Skill**   | `skill-creator:skill-creator`    |
| 인자를 받아 실행하는 슬래시 커맨드               | **Command** | `plugin-dev:command-development` |
| 도구 실행 전후 자동 동작, 검증/차단              | **Hook**    | `plugin-dev:hook-development`    |
| 독립적으로 복잡한 작업을 처리하는 서브에이전트   | **Agent**   | `plugin-dev:agent-development`   |
| 여러 컴포넌트를 묶어 배포하는 패키지             | **Plugin**  | `plugin-dev:create-plugin`       |

---

## Phase 5: 추천 제시 및 선택

분석 결과를 바탕으로 추천 구현 도구와 이유를 설명한 뒤, AskUserQuestion으로 선택을 받는다.

추천 예시:

```
이 기능은 사용자가 직접 호출해서 단계별로 안내받는 형태이므로 Skill이 적합합니다.
skill-creator를 사용하면 description 작성, 테스트, 개선까지 체계적으로 도와줍니다.
```

선택지:

1. 추천 도구 (이유 포함, 첫 번째로 배치)
2. 대안 도구 (있다면)
3. 직접 구현 (스킬 도구 없이 바로 작성)

---

## Phase 6: 구현 실행

선택된 도구에 따라 실행한다:

- **skill-creator** → `Skill` 도구로 `skill-creator:skill-creator` 호출
- **plugin-dev:\*-development** → `Skill` 도구로 해당 스킬 호출
- **직접 구현** → 인터뷰 내용을 바탕으로 SKILL.md 직접 작성

### 직접 구현 시 파일 경로

```
skills/{name}/SKILL.md           # 메인 플러그인 스킬
plugins/{plugin}/skills/{name}/SKILL.md  # 서브 플러그인 스킬
```

---

## 주의사항

- Interview는 최대 2라운드로 제한한다 — 너무 많은 질문은 흐름을 끊는다
- 기존 스킬과 중복이 확인되면 새로 만들기 전에 먼저 알린다
- 추천에는 항상 이유를 함께 설명한다 ("왜 이 도구가 적합한지")
- args로 아이디어가 충분히 전달된 경우 Phase 1~3을 압축할 수 있다
