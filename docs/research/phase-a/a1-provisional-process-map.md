# A1 — Provisional current-state maps

These maps are **research reconstructions from one sports secretary's account**, not validated by guard observation. Detailed A2 maps will follow role and exception clarification.

## A. Key and item access

```mermaid
flowchart TD
  A[Student wants equipment] --> B[Approach security guard]
  B --> C[Give ID card and declare intended items]
  C --> D[Guard records student, items, issue time and signature]
  D --> E[Guard releases sports-room key]
  E --> F[Student self-selects items]
  F --> G[Equipment used; informal sharing possible]
  G --> H[Student places items back and returns key]
  H --> I[Guard records claimed return time and signature]
  I --> J[Guard returns ID card]
```

**Verification gaps:** no check that declared items match actual removal; no individual item-to-borrower continuity when equipment changes hands; no confirmed physical return or condition inspection.

## B. Reported damage and maintenance

```mermaid
flowchart TD
  A[Equipment damaged or unusable] --> B[Damage may remain unreported]
  B --> C[Later student requests replacement or complains]
  C --> D[Sports secretary investigates]
  D --> E{Repairable?}
  E -->|Yes| F[External shop repair; cost route as applicable]
  E -->|No| G[Replacement/purchase process]
  F --> H[Return to sports room]
  G --> H
```

**Caution:** Some incidents may instead be directly reported; precise branch frequency unknown. No formal quarantine/inspection state confirmed.

## C. Reported procurement

```mermaid
flowchart TD
  A[Equipment requirement identified] --> B[Secretary checks current stock informally]
  B --> C[Obtain vendor quote or quotes]
  C --> D{Value below INR 10,000?}
  D -->|Yes| E[Secretary purchases, pays and seeks reimbursement]
  D -->|No| F[Three quotes, choose lowest, hostel office direct payment]
  E --> G[Receive equipment; paper bill in office]
  F --> G
  G --> H[Put equipment into sports room]
```

**Verification needed:** threshold interpretation, approval rules, invoice processing, asset recording, elapsed time and exceptional procurement cases.
