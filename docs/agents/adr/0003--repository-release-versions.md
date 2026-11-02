# Version the complete collection with Git tags

Status: implemented

## Problem

The collection has three installation surfaces. Users want a short default installation command and one version for the whole collection. The npm `latest` tag in `skills@latest` identifies the installer, while repository refs identify the skill content. Plugin manifests also carry explicit version strings.

## Decision

Use `npx skills@latest add mel0nyrame/skills` as the default Skills CLI installation command. Keep ordinary development on feature branches and merge reviewed release content into `main`. The default branch supplies current release content; the installer does not automatically select the newest Git tag.

Identify each complete collection release with an immutable `vX.Y.Z` Git tag on its merged `main` commit. Use the corresponding `X.Y.Z` in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` before that release. A tag records the collection's skills, documentation, manifests, and pinned submodule refs together. Individual skills do not have separate release numbers.

Update both manifest versions in the release PR, complete validation and review, merge, then create and push the release tag. Creating a repository or opening a PR does not itself authorize merging or tagging an unmerged feature branch. The first collection version is `0.1.0`; its tag belongs on the merged release commit.

To install a historical release, use an explicit source such as `https://github.com/mel0nyrame/skills/tree/v0.1.0`. Git tags do not dynamically populate installed JSON manifests.

## Alternatives

- Independent versions for each skill multiply release bookkeeping without matching the requested whole-collection distribution.
- A separate npm package would duplicate installation work already provided by the Skills CLI.
- Selecting the newest repository tag implicitly would require different installer behavior or an extra distribution layer. The chosen command resolves the default branch instead.
- Removing plugin versions would not preserve an explicit shared version across the plugin surfaces. Keep the manifest values synchronized with releases.

## Consequences and risks

Keep unreleased work out of `main` and complete tagging promptly after merging a release. A new commit on the default branch changes what an unpinned Skills CLI installation receives, even before a tag exists. Published tags stay fixed; corrections use a new release number.

Before release, verify equal manifest versions, nine discovered bundled skills, excluded external submodules, and the applicable tests. Users update their installed copies separately; repository publication does not silently refresh existing installations.

The source rules are described in [npm package specifiers](https://docs.npmjs.com/cli/v11/using-npm/package-spec/), [Skills CLI repository cloning](https://github.com/vercel-labs/skills/blob/main/src/git.ts), and [Claude plugin version semantics](https://code.claude.com/docs/en/plugins/manifest-reference#version).
