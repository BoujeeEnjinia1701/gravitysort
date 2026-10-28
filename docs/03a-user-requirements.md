---
doc_id: GVS-URS-001
title: GravitySort user requirements
project: GravitySort
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.8 pipeline): user needs drawn from the users and stakeholders in GVS-PRB-001 Tables 1 to 3 and from the decisions in GVS-DEC-001; proposed for review with the co-design partner"
---

# GravitySort user requirements

What the people who would use, build and support GravitySort need, written from their side. Product requirements that meet these needs are in GVS-PRS-001 (`03-requirements.md`) and the links are in the traceability matrix GVS-RTM-001 (`03b-traceability.md`). Method: STANDARDS section 22. None of these needs has yet been confirmed by the users themselves: they are drawn from the problem statement, the cited literature and Amish's decisions, and are proposals for the first co-design sessions with the partner in Colombia (GVS-DEC-001, 2026-10-02).

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Regulatory | No mercury | We can recover our gold without mercury at any step, so we can sell to buyers and meet the law where mercury is banned | High | Small mining group; NGO or extension officer; regulators (PRB Tables 2 and 3) |
| UR-002 | Performance | Daily ore | It keeps up with the ore our group mills in a working day, about 1.5 t | High | Small mining group; processing center operator (PRB Table 2) |
| UR-003 | Performance | Fine gold | It catches the fine gold that our sluices and pans lose, so we earn more from the same ore | High | Small mining group (PRB Table 2) |
| UR-004 | Performance | Smeltable concentrate | The final concentrate is small and clean enough (about 100 g a day) to smelt with borax ourselves | High | Small mining group; women processors (PRB Table 2) |
| UR-005 | Usability | No grid power | It runs where there is no power, by human effort that a crew can share over a shift | High | Small mining group at remote pits (PRB Table 2) |
| UR-006 | Usability | Motor where power exists | Where we have a battery or generator, a small motor can run it instead of the pedals | Medium | Processing center operator (PRB Table 2) |
| UR-007 | Environment and durability | Little and dirty water | It works with the little water we have, recirculated from a settling pond and carrying silt | High | Small mining group; regulators (PRB Tables 2 and 3) |
| UR-008 | Cost | Affordable | A small group can afford the parts and earn them back in weeks | High | Small mining group; NGO or cooperative (PRB Tables 2 and 3) |
| UR-009 | Deployment and assembly | Local build and repair | A welder in our mining town can build and repair it with the tools they have, without a lathe | High | Local workshop or welder (PRB Table 2) |
| UR-010 | Logistics | Carried to site | Two people can carry it to the pit in loads and put it together with hand tools | Medium | Small mining group (PRB Table 2) |
| UR-011 | Safety | Safe to run | The spinning and moving parts are guarded, it stops quickly, it cannot run dangerously fast unnoticed, and it does not tip over | High | Every operator; NGO duty of care (PRB Tables 2 and 3) |
| UR-012 | Usability | Quick, secure clean-up | We can take out the concentrate quickly without tools and lock it away from theft | High | Small mining group; women processors (PRB Table 2) |
| UR-013 | Maintenance | Wear parts on site | The parts that wear can be replaced at the site and last a season | Medium | Local workshop; small mining group (PRB Table 2) |
| UR-014 | Usability | Bowl speed and settings shown | The operator can see and set how hard the machine is working without instruments | Medium | Small mining group; NGO measuring recovery (PRB Table 2) |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.

## Notes

- UR-002 follows the restatement of R2 by Amish on 2026-10-02 (200 kg/h of feed time, about 1.55 t per eight-hour shift; GVS-DEC-001).
- UR-010 follows the restatement of R11 by Amish on 2026-10-01 (100 kg in all, every load 30 kg or less; GVS-DDR-003, A1).
- UR-011 includes the tipping criterion decided by Amish on 2026-10-03 (a 10 degree slope in any direction with a full tank; GVS-DEC-001).
- The value-engineering target behind UR-008 is USD 455 in parts (`project.yaml`), a hypothetical control target, not a limit (Amish, 2026-10-01).
