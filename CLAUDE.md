# CLAUDE.md

Operational manual for Claude Code. **What to build** is in `PROJECT.md`; this document defines **how to work**. Before starting any page, always read the corresponding section in the primary source (`reference/source-unified-enterprise.md`).

---

## Repository Overview

An MkDocs (Material theme) documentation site. Edit `docs/`, auto-publish to GitHub Pages. Content: enterprise AI agent architecture patterns (7 facets, 45 patterns). Only `docs/` is published. `reference/` is writing material — **do not edit or publish**.

Core thesis: not "making AI smarter" but "safely onboarding a new execution entity into the enterprise's ID, permissions, responsibilities, processes, auditing, and organizational structure." Maintain this perspective throughout every page.

## Environment Setup

```bash
uv sync
```

## Common Commands

```bash
uv run mkdocs serve              # Local preview (http://127.0.0.1:8000, hot reload)
uv run mkdocs build --strict     # Production-equivalent build. Treats link breaks & nav mismatches as errors
uv run python scripts/build_machine_index.py  # Regenerate machine-readable JSON indexes
```

**Always pass `mkdocs build --strict` before committing.** Zero warnings is the quality gate.

## Writing Workflow (1 pattern = 1 work unit)

1. Pick a target ID (e.g., `ID-2`) from the pattern list in `PROJECT.md`.
2. **Read the primary source**: the corresponding section in `reference/source-unified-enterprise.md`.
3. Open the target file (e.g., `docs/patterns/id-identity/id2-identity-federation-obo.md`).
4. Fill all sections of the common schema, following the source's intent (see conventions below).
5. Update frontmatter: fill `description` with one sentence, change `status: draft` → `status: done`.
6. Add **relative links** to dependent/related patterns in `## Related Patterns`.
7. Pass `mkdocs build --strict`.
8. 1 pattern = 1 commit (keep granularity small).

## Writing Conventions

### Tone & Style
- Japanese pages: use 常体 (だ・である). Concise, technical. Keep sentences short.
- English pages (`.en.md`): professional, accessible, active voice where possible.
- No subjective superiority claims or exaggeration. Present tradeoffs neutrally.
- Do not add facts or proper nouns not in the source. If adding, cite explicitly and avoid definitive assertions.

### Structure (Pattern Pages)
- Headings follow the 8 sections in `PROJECT.md` §4.1 — **fixed order, fixed names**. Do not add or remove sections.
- Each section is primarily prose. Bullet lists are limited to element enumeration (technologies, SaaS, etc.) and each item should be brief.
- "When to Use / When Not to Use" should present paired conditions.
- "Pitfalls & Selection Tips" should describe concrete anti-patterns (e.g., "using a single all-powerful service account to call every SaaS").

### Frontmatter
```yaml
---
title: "ID-2 Identity Federation & On-Behalf-Of (OBO Delegation)"
description: "Calls downstream SaaS using delegation tokens scoped to the requester's own permissions, faithfully propagating authorization."
status: done
---
```

### Cross-Links
- Same facet: `[ID-4 Permission Mirror](id4-permission-mirror-least-of.md)`
- Different facet: `[KM-1 Access-Controlled RAG](../km-knowledge/km1-access-controlled-rag.md)`
- Link targets use **file paths (with .md)**. `--strict` validates paths.

### Diagrams & Tables (Material Features)
- Flows, structures, state transitions, and **authorization sequences** use mermaid. Sequence/flow diagrams are especially recommended for ID-2 (OBO/Token Exchange), ID-6 (PDP/PEP), RT-7 (Saga), RT-10 (Event-Driven):
  ````markdown
  ```mermaid
  sequenceDiagram
    participant U as User
    participant GW as Agent Gateway
    participant SF as Salesforce
    U->>GW: Request (ID Token)
    GW->>GW: Token Exchange (RFC 8693) → OBO Token
    GW->>SF: API call with user's own permissions
  ```
  ````
- Comparisons (OBO vs. SA, Central Lake vs. Mesh, etc.) use Markdown tables.
- Supplements and warnings use admonitions: `!!! note` / `!!! warning` / `!!! tip`. Critical security warnings use `!!! danger`.
- Alternatives use `=== "Tab Name"` (pymdownx.tabbed).

## Navigation (nav) Handling

- When adding or renaming pages, update `nav` in `mkdocs.yml` manually.
- After modifying pattern/decision/department pages, run **`uv run python scripts/build_machine_index.py`** to regenerate `docs/_machine/*.json`.
- After nav changes, check `git diff mkdocs.yml` to ensure no unintended differences.

## Deploy

- Pushing to `main` triggers `.github/workflows/deploy.yml`, which deploys to GitHub Pages.
- First time only: in GitHub repository Settings → Pages → Source, select **GitHub Actions**.
- Update `site_url` / `repo_url` / `repo_name` in `mkdocs.yml` to match the actual repository.

## Prohibited Actions (Including Enterprise-Specific Cautions)

- Editing or publishing `reference/` (primary source / unpublished material).
- Altering the common schema sections (order, names, or count).
- Leaving mismatches between nav and frontmatter `title`.
- Committing with `mkdocs build --strict` warnings remaining.
- Fabricating content not in the source, or making definitive claims about specific vendor product superiority.
- **Writing design examples that cross the workforce/customer boundary** (violates ID-1 principle — maintain two-face separation).
- **Writing anything that reads as "security is enforced via prompts"** (violates ID-7 principle — safety guarantees belong on the execution platform side).
- Using real company system names, real data, or real personal information in examples (use fictitious examples).
- Committing `site/` (build artifacts) — already in `.gitignore`.

## Completion Checklist (Per Page)

- [ ] Reflects the corresponding section of the primary source
- [ ] All sections have content with no TODOs remaining
- [ ] `title` matches nav, `description` filled, `status: done`
- [ ] Internal links are valid (`mkdocs build --strict` has no warnings)
- [ ] mermaid diagrams are present where needed (especially authorization, Saga, event-driven flows)
- [ ] Does not violate the principles of workforce/customer separation, least-privilege composition, or platform-side defense
