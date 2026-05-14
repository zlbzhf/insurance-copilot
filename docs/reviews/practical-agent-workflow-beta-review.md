# Practical Agent Workflow Beta Review

## Purpose

Check whether the project moved from architecture-first knowledge governance toward a practical insurance-agent assistant comparable in workflow discipline to `claude-for-legal`.

## Plan Checklist

- [x] Task 1: Practitioner-first workflow surface created and README front-loaded with job-style workflows.
- [x] Task 2: Practice profile gate strengthened with Quick Start / Full Setup cold-start path.
- [x] Task 3: CRM-lite private workspace templates added and validator updated.
- [x] Task 4: Daily Agent Workbench reference/template/example/eval added.
- [x] Task 5: Client Plan Draft reference/template/example/eval added.
- [x] Task 6: Chinese Talk Tracks and Referral Ask reference/template/example/eval added.
- [x] Task 7: Renewal/lapse operational cadence and cookbook added.
- [x] Task 8: Synthetic end-to-end family protection demo added.
- [x] Task 9: Validators and quality gates updated to prevent regression.
- [x] Task 10: Reflection document created.

## What Improved vs claude-for-legal Gap

- The front door now starts with named practitioner workflows instead of standards/schema language.
- Cold-start is now a gate, not merely a recommendation.
- Daily operating work, client plan drafting, Chinese customer messages, referrals, and CRM-lite private workspace are now first-class assets.
- The repo still remains Hermes-first and avoids Claude plugin artifacts.
- Review gates remain explicit: licensed/compliance review, no automatic sending, no CRM/calendar writes, no policy/claim/application side effects.

## What Remains Weaker

- No real read-only connectors are implemented yet; only contracts/templates and local-file patterns exist.
- Public AIA/友邦 pack is still structurally ready but not content-rich with real public source-backed product/service pages.
- Scheduled agents remain cookbook-level, not deployed cron jobs.
- No UI/web app exists; Hermes prompt usage remains the interface.
- Static evals check expected fixtures, not live model behavior.

## Non-goals Preserved

- No real customer data.
- No real insurer data ingestion.
- No automated external side effects.
- No Claude plugin metadata.

## Next Phase Recommendation

Build a small read-only local-file connector slice: renewal register reader + customer profile reader + policy summary reader. Then run a synthetic daily workbench from those files. After that, consider a minimal public AIA pack using only official public sources with the ingestion gateway.
