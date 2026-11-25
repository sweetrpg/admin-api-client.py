# AGENTS.md

This file provides guidance to Claude Code, Codex, GitHub Copilot, and other coding agents
working in this repository.

## About This Project

`admin-api-client.py` is the Python client SDK for `admin-api` (`sweetrpg/admin-api`): fetches
active banner messages and maintenance-mode records for a set of scopes (`platform`,
`service:<name>`). It's the Python sibling of `admin-api-client.swift`, extracted so that
Flask-based frontends (`assets-web`, `initiative-web`, `shelf-web`, `shared-web`) don't each
hand-roll their own copy of the same fetch/cache/fail-open logic.

Unlike a domain API client SDK, this package bakes in caching (90s TTL), a 2s request timeout,
and fail-open behavior on every error path - every consumer must behave identically for this
cross-cutting concern, so it isn't left to each app to re-derive.

## Committing Code

[Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <description>`.

## Branches and Workflow

Git-flow (see `docs/git-flow.md` in `sweetrpg/platform`): `develop` is the integration branch,
`master` reflects the latest release. Feature/fix branches off `develop`, PR back into `develop`.

## Running Checks Locally

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and task running
(`pyproject.toml` + committed `uv.lock`):

```bash
uv sync --group test   # create .venv and install deps
uv run pytest          # run tests
uv lock --upgrade      # update dependencies
```

`uv` is the required Python tool on this platform; do not use `pip`/`tox` directly.

## Platform Conventions and Decisions

This repo is a submodule of `sweetrpg/platform`. Platform-wide conventions and Architecture
Decision Records live there:

- checked out inside the platform tree: `../../../docs/README.md` (convention index) and
  `../../../docs/adr/README.md` (platform ADRs, `PADR-*`)
- standalone or module-only checkout:
  <https://github.com/sweetrpg/platform/tree/master/docs> and
  <https://github.com/sweetrpg/platform/tree/master/docs/adr>

Accepted `PADR-*` records are binding constraints. Read the ADR index before proposing a
structural change; if a task needs to contradict an accepted record, stop and say so -
propose a superseding ADR rather than working around it. This repo's own service-local
decisions are `ADR-*` and belong in `docs/adr/` here.

Before implementing any feature, complete the
[feature work checkpoint](https://github.com/sweetrpg/platform/blob/master/docs/openspec.md#feature-work-checkpoint)
and record the answers in the issue or PR.
