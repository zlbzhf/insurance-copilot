# Expected Output Sketch — Generic Public Institution Pack Source-Backed Update

- Use **Institution Knowledge Organizer** for the selected **public institution pack** when the task is a **source-backed public pack update**.
- Start from a public **source record** with source URL, source type, retrieved date, public-source flag, redistribution mode, and pack ID from `knowledge/registry.json` or the provided source context.
- Preserve the **public/private boundary**: public source summaries may enter `knowledge/institutions/<pack_id>/`; private customer files, agent notes, production exports, and non-public institution material must stay outside the public repo.
- Mark currentness, form requirements, product/service terms, deadlines, and review status with `[verify]` when the official source must be checked again.
- State **No customer data** is included and reject customer-specific facts, private notes, or non-public underwriting guides.
- Treat public service, FAQ, claims, product, or renewal pages as source-backed support only and **not a final claims decision**, underwriting decision, product recommendation, or compliance approval.
- Handoff to **pack maintainer review** before canonical use, and use Professional Review Gate if the material supports a customer-facing or regulated draft.
