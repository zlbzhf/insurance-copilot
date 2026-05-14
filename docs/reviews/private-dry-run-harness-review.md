# Private Dry-Run Deployment Harness Review

## Scope Reviewed

This review covers the `Private Dry-Run Deployment Harness` slice:

```text
scripts/private_dry_run.py
tests/test_private_dry_run.py
docs/private-dry-run-harness.md
examples/private-dry-run/
evals/cases/private-dry-run-harness.json
evals/expected/private-dry-run-harness.md
scripts/validate_repo.py
.github/workflows/validate.yml
```

## Planned Review Focus

Independent blocker review should check:

- symlink/path traversal;
- source workspace mutation;
- output contamination and hardlink aliases;
- child-command failure handling;
- no live cron creation;
- fixture privacy;
- documentation mismatch.

## Self-Check Before Independent Review

- The harness rejects symlinked workspace roots.
- The harness rejects output inside the workspace.
- The harness rejects output samefile/hardlink aliases to workspace source files when the output path already exists.
- Existing non-empty output directories require `--force`.
- Generated artifacts are outside the source workspace.
- Readiness blockers are captured as diagnostics and return exit `1`, not treated as broken CLI config.
- Child command configuration errors return fail-loud exit `2`.
- The harness writes `live_cron_created: false` and does not create Hermes cron jobs.
- Tests assert source workspace hashes remain unchanged.

## Independent Review Result

Automated subagent review attempt timed out after 600 seconds. A manual blocker-focused review was completed against the staged diff using the checklist above.

Result:

```json
{
  "passed": true,
  "security_concerns": [],
  "logic_errors": [],
  "suggestions": [
    "Manifest self-checksum is explicitly marked self-referential-not-recorded while all other artifacts include verifiable SHA-256 checksums."
  ],
  "summary": "No remaining blocker found in symlink/path traversal, output contamination/hardlink aliases, source workspace mutation, child-command failure handling, fixture privacy, or live-cron side effects."
}
```

## Post-Review Fix

The initial manifest inventory attempted to include a checksum for `manifest.json` itself, which is self-referential and cannot be stable once embedded in the file. The harness now writes every non-manifest artifact checksum and records the manifest artifact as:

```json
{
  "sha256": "self-referential-not-recorded",
  "checksum_recorded": false
}
```

Tests verify non-manifest artifact hashes against file bytes and verify the manifest self-reference marker.
