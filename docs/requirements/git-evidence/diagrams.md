# Revision observations are not achievement

```mermaid
flowchart LR
  Repo[Authorized repository observation] --> Revision[Revision and activity evidence]
  Artifacts[Existing verification artifacts] --> Verification[Attributed test build or release result]
  Revision --> Report[Qualified evidence report]
  Verification --> Report
  Missing[No available verification artifact] --> Unknown[Unknown verification]
  Unknown --> Report
  Report --> Assessment[Criterion-specific assessment not activity-only success]
```