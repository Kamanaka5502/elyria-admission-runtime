# Release Publication Steps

## Purpose

Use these steps to publish the public buyer-review release in GitHub.

The release should stay bounded: buyer-review runtime candidate, not production deployment approval.

## Release Values

```text
repository: Kamanaka5502/elyria-admission-runtime
tag: v0.8.1-public
title: Elyria Admission Runtime v0.8.1 — Evidence-Gated Consequence Admission Runtime
target branch: main
```

## GitHub UI Steps

1. Open the repository.
2. Go to **Releases**.
3. Click **Draft a new release**.
4. Click **Choose a tag**.
5. Type:

```text
v0.8.1-public
```

6. Select **Create new tag on publish**.
7. Set target branch to:

```text
main
```

8. Use this release title:

```text
Elyria Admission Runtime v0.8.1 — Evidence-Gated Consequence Admission Runtime
```

9. Paste the release description from:

```text
RELEASE_NOTES_V0_8_1_PUBLIC.md
```

10. Publish the release.

## After Publication

Update Issue #6:

```text
[x] Release tag is published
[x] Release title and description use Elyria Admission Runtime
```

Then add the release URL to Issue #6.

## Boundary Check

Before publishing, confirm the release does not claim:

```text
production deployment approval
customer certification
regulatory approval
third-party audit completion
```

Correct release boundary:

```text
A+ bounded buyer-review candidate after verification evidence is recorded.
Production deployment remains subject to customer approval and external review where required.
```
