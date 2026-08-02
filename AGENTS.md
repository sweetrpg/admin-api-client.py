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

```bash
pip install -r requirements/tests.txt
tox
```
