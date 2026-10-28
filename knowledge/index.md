---
okf_version: "0.2"
---

# Siddhi Knowledge

Durable engineering knowledge about Siddhi, in [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).
It is independent of requirements, OpenSpec changes, and code: those link here, never the reverse.
Rules for this bundle are in `profile.json`; `python3 scripts/verify_knowledge.py` enforces them.

Extracted concepts are draft: they preserve intended architecture and reusable
rationale, not proof of implementation or human verification. Read each concept's
proposal and uncertainty qualifications before applying it.

# Sections

* [Product](product/) - Vision, scope, and the phased roadmap
* [Architecture](architecture/) - HTTP/application boundaries, source ingestion, analysis, persistence, and security
* [Concepts](concepts/) - Domain ideas that the rest of the knowledge builds on
* [Decisions](decisions/) - Durable architectural decisions (ADRs)
* [Practices](practices/) - How we build and verify Siddhi
* [Runbooks](runbooks/) - What to do when something goes wrong
* [Technologies](technologies/) - Format directions, compatibility limits, and upstream contract uncertainty
