# Enterprise AI Agent Architecture Reference

A collection of architecture patterns (7 facets, 45 patterns) for safely integrating AI agents into enterprises with tens of thousands of employees, diverse existing SaaS, strict permission management, and hierarchical organizations. Built with MkDocs (Material theme) and published on GitHub Pages.

## Quick Start

```bash
uv sync                          # Install dependencies
uv run mkdocs serve              # http://127.0.0.1:8000
uv run mkdocs build --strict     # Production-equivalent build (zero warnings = quality gate)
```

## Documentation Roles

- **[PROJECT.md](PROJECT.md)** — What to build, why, and in what order (specification, plan, full 45-pattern list, Definition of Done).
- **[CLAUDE.md](CLAUDE.md)** — Operational manual for Claude Code (commands, writing conventions, prohibitions).
- **`reference/source-unified-enterprise.md`** — Primary source for all pages (unpublished material).

## Publishing (GitHub Pages)

1. Create a GitHub repository and push (default branch `main`).
2. Update `site_url` / `repo_url` / `repo_name` in `mkdocs.yml` to match your repository.
3. Pushing to `main` triggers `.github/workflows/deploy.yml`, which auto-deploys to GitHub Pages.
4. In repository Settings → Pages → Source, select **GitHub Actions**.

## Structure (7 Facets)

```text
Facet 1 EX Experience & Gateway / Facet 2 GV Control & Governance / Facet 3 ID Identity & Trust (hardest)
Facet 4 RT Runtime & Orchestration / Facet 5 KM Knowledge & Memory / Facet 6 IN Integration & Tools / Facet 7 OB Observability & Audit
```

See [PROJECT.md](PROJECT.md) for the full directory structure and pattern list.
