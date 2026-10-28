# Portfolio outcome flow

Draft behavioral flow; fields and approval contract remain unresolved.

```mermaid
flowchart LR
  Owner[Owner outcome] --> Goal[Independent goal revision]
  Inventory[Discovered project reference] --> Candidate[Candidate association with basis]
  Goal --> Candidate
  Candidate --> Review{Owner review}
  Review -->|Explicit confirmation| Link[Confirmed relationship]
  Review -->|Insufficient evidence| Pending[Candidate remains visible]
  Link --> History[Traceable portfolio history]
  Pending --> History
```