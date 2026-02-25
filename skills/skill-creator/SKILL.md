---
name: skill-creator
description: Create new skills, modify and improve existing skills for Claude Code. Use when users want to create a skill from scratch, update or optimize an existing skill, or ask about skill structure and best practices. Make sure to use this skill whenever the user mentions "스킬 생성", "skill 생성", "스킬 만들어", "skill 만들어", "새 스킬", "스킬 작성", or wants to turn a workflow into a reusable skill, even if they don't explicitly say "skill".
Do NOT use for API service code generation, form generation, or general code generation unrelated to skill creation.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

## Core Process

The process of creating a skill follows this loop:

1. Capture the user's intent
2. Interview for details and research context
3. Draft the SKILL.md
4. Create test prompts and validate
5. Iterate based on feedback
6. Optimize the description for triggering accuracy

## Step 1: Capture Intent

Start by understanding the user's intent. If the current conversation already contains a workflow the user wants to capture (e.g., "turn this into a skill"), extract answers from the conversation history first.

Ask these questions (skip any already answered):

1. What should this skill enable Claude to do?
2. When should this skill trigger? (user phrases/contexts)
3. What's the expected output format?
4. Where should the skill live? (project `.claude/skills/` or global `~/.claude/skills/`)

## Step 2: Interview and Research

Proactively ask about:
- Edge cases and input/output formats
- Example files or scenarios
- Success criteria
- Dependencies (MCP servers, CLI tools, etc.)

Check available MCPs and existing project patterns for context. Come prepared to reduce burden on the user.

## Step 3: Write the SKILL.md

### Folder Structure

```
skill-name/                    # kebab-case required
├── SKILL.md                   # required (exact casing)
│   ├── YAML frontmatter       # name + description required
│   └── Markdown instructions
└── Bundled Resources          # optional
    ├── scripts/               # executable code
    ├── references/            # docs loaded as needed
    └── assets/                # templates, icons, fonts
```

### YAML Frontmatter

```yaml
---
name: skill-name               # kebab-case, must match folder name
description: |                  # required, under 1024 chars
  What the skill does + when to use it.
  Include trigger phrases and negative triggers.
  Use when user says "X", "Y", or "Z".
  Do NOT use for [unrelated things].
---
```

Optional frontmatter fields: `license`, `allowed-tools`, `compatibility`, `metadata` (author, version, category, tags).

### Frontmatter Rules

- name: **kebab-case only** (no spaces, underscores, or uppercase)
- File must be named exactly `SKILL.md` (not SKILL.MD, skill.md)
- No XML tags (`< >`) in frontmatter
- Do not use `claude` or `anthropic` as skill names (reserved)
- Frontmatter delimiters `---` are required

### Description Writing

The description is the primary triggering mechanism. It determines whether Claude invokes the skill. Write it "pushy" to prevent undertriggering.

**Good example:**
```yaml
description: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff". Make sure to use this skill whenever the user mentions Figma designs, even if they don't explicitly ask for documentation.
```

**Bad examples:**
```yaml
description: Helps with projects.                    # too vague
description: Creates documentation systems.           # no trigger context
```

Include both positive triggers and negative triggers ("Do NOT use for ...") to prevent over-triggering.

### Progressive Disclosure (3-Level Loading)

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - Loaded when skill triggers (keep under 500 lines)
3. **Bundled resources** - Loaded as needed (unlimited size)

Key patterns:
- Keep SKILL.md under 500 lines; if approaching the limit, add hierarchy with pointers
- Reference files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

### Body Structure

```markdown
# Skill Name

## Instructions
### Step 1: [First Major Step]
Specific, actionable description.

### Step 2: [Second Major Step]
...

## Examples
**Example 1:** [common scenario]
Input: "user request"
Output: what gets produced

## Troubleshooting
**Error:** [Common error message]
**Cause:** [Why it happens]
**Solution:** [How to fix]
```

### Writing Style

- Use imperative form in instructions
- Explain **why** things are important rather than heavy-handed MUSTs and NEVERs
- Generalize instructions (don't overfit to specific examples)
- Write a draft, then review with fresh eyes and improve
- Include examples to clarify expected behavior

### Design Patterns

Choose the appropriate pattern for the skill:

1. **Sequential Workflow** - Step-by-step execution with dependencies and validation between steps
2. **Multi-MCP Coordination** - Orchestrating multiple MCP servers in phases
3. **Iterative Refinement** - Draft, quality check, improve loop
4. **Context-aware Tool Selection** - Decision tree for selecting the right tool per situation
5. **Domain-specific Intelligence** - Embedding specialized domain knowledge and rules

### Domain Organization

When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file.

## Step 4: Test and Validate

After writing the draft:

1. Come up with 2-3 realistic test prompts (things a real user would say)
2. Share them with the user for confirmation
3. Run the skill against each test prompt
4. Evaluate results together with the user

### Test Checklist

Before finalizing:
- [ ] Triggers on clear, relevant requests
- [ ] Triggers on different phrasings of the same intent
- [ ] Does NOT trigger on unrelated topics
- [ ] Produces expected output format
- [ ] Instructions are followed correctly

## Step 5: Iterate and Improve

Based on feedback:

1. **Generalize from feedback** - Don't overfit to test examples; the skill will be used across many different prompts
2. **Keep the prompt lean** - Remove instructions that aren't pulling their weight
3. **Explain the why** - Transmit understanding of why each instruction matters
4. **Bundle repeated patterns** - If test runs all produce similar helper scripts, put them in `scripts/`

Repeat the test-evaluate-improve loop until:
- The user is happy with the results
- No more meaningful improvements can be made

## Step 6: Description Optimization (Optional)

For fine-tuning trigger accuracy:

1. Generate 20 eval queries (8-10 should-trigger, 8-10 should-not-trigger)
2. Queries should be realistic and specific (include file paths, personal context, abbreviations, typos)
3. Should-not-trigger queries should be near-misses (shared keywords but different intent)
4. Test triggering and adjust description iteratively

## Troubleshooting

- **Skill not triggering**: Add more specific trigger phrases to description, make it "pushier"
- **Over-triggering**: Add negative triggers ("Do NOT use for ...")
- **Instructions not followed**: Move critical instructions to the top, keep them concise, explain why they matter
- **SKILL.md too long**: Extract details into `references/` files, keep SKILL.md under 500 lines
- **MCP connection failures**: Verify MCP server connection and authentication status
