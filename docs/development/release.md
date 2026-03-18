# Release Process

This page documents the release workflow for the SDK.

## High Level Steps

- Add at most one release label to the pull request that targets `main`:
  - `release:major`
  - `release:minor`
  - `release:patch`
- Open or update the pull request and let the `Release Preview` workflow compute the next version.
- Merge the pull request into `main`.
- Let the `Release On Merge` workflow validate the merged code, bump the versioned files, create the `vX.Y.Z` tag, and push it.
- Let the tag-triggered documentation workflow deploy versioned docs and then call the reusable publish and GitHub release workflows.

If no release label is present, the workflow defaults to a patch release.

## Workflow Details

- Pull requests to `main` run `Release Preview`, which resolves the release label and shows the version that would be published after merge.
- Merged pull requests to `main` run `Release On Merge`, which reruns the release checks with `uv sync --dev --locked`, `uv run invoke test.run`, `uv run invoke qa.all`, and `uv run invoke docs.build` before creating the release commit and tag.
- Tag pushes matching `v*` keep using the existing documentation workflow to deploy docs, publish the package to PyPI, and create the GitHub release.

## Label Rules

- Use exactly one release label per pull request.
- If more than one release label is applied, the preview workflow fails.
- The supported labels are `release:major`, `release:minor`, and `release:patch`.

## Prerequisites

- Configure PyPI Trusted Publishing for this repository and the reusable publish workflow.
- Protect `main` so pull requests are required before merge.
- Keep the CI workflow required on pull requests so the release workflow only runs for reviewed, green changes.
