---
doc_id: GVS-REG-001
title: GravitySort regulatory and standards register
project: GravitySort
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.8 pipeline): mercury rules, machinery safety standards, water and smelting, with applicability and status; sources checked on 2026-10-25"
---

# GravitySort regulatory and standards register

Which standards and regulations bear on GravitySort, where, and what each needs. The design's main regulatory driver is positive: mercury bans and the Minamata Convention create the need for a mercury-free concentration step. The machinery safety standards are used as design practice for guards and reach distances; no certification is claimed. Not legal advice; anything marked "to assess" needs a qualified reviewer, working with the partner organization, before any product claim. Method: STANDARDS section 23. Mining-area standards are researched here first; no other mining repo in the portfolio has a register yet.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | Minamata Convention on Mercury, Article 7 and Annex C (artisanal and small-scale gold mining) | International (parties) | Parties with ASGM must reduce and where feasible eliminate mercury use; Annex C names whole-ore amalgamation and open burning of amalgam for elimination and calls for national action plans [1] | GravitySort is a concentration step that replaces amalgamation entirely (PR-001) | Design lead | Met by design (GVS-CAL-001 R1 design review) |
| G2 | Colombia, Law 1658 of 2013 (mercury ban in mining from July 2018) | Colombia | Bans mercury in mining [2] | First partner country (decided by Amish on 2026-10-02); the machine uses no mercury | Partner organization | Met by design; the partner's own permits and mining title to assess with the partner |
| G3 | Regulation (EU) 2017/852 on mercury | European Union | Bans mercury exports and mercury use in ASGM amalgamation in the EU [3] | Does not regulate equipment used in Colombia; relevant to EU-funded programmes that would support GravitySort abroad | Project lead | Does not apply (context only) |
| G4 | ISO 12100:2010, safety of machinery, risk assessment and risk reduction | International | General principles for machinery design and the risk assessment method [4] | Used as the method behind the hazard analysis in GVS-RSK-001; no conformity claimed | Design lead | Applies as practice; formal assessment to assess before any field use |
| G5 | ISO 13857:2019, safety distances to prevent hazard zones being reached | International | Reach distances through and over guard openings [5] | Belt, chain and table head guards are perforated sheet; hole size against distance to the pulleys and belts is not yet checked | Design lead | To assess (perforation size and guard distances, before TRL 4) |
| G6 | ISO 14120:2015, guards: general requirements for fixed and movable guards | International | Design and construction of guards [6] | Lid guard with brake interlock, belt and chain guards (PR-012) | Design lead | Applies as practice; met by design review in part (interlocked lid); guard fixings and strength to assess |
| G7 | Regulation (EU) 2023/1230 on machinery | European Union | Essential health and safety requirements and CE marking for machinery placed on the EU market [7] | Only if units were ever sold or supplied in the EU; an open design built by local workshops abroad is not placed on the EU market by the project | Project lead | Does not apply now; to assess if units are ever supplied in the EU |
| G8 | Colombian machinery safety and occupational health rules for mining | Colombia | Workplace safety at mining sites | No Colombian machinery standard identified for this register | Partner organization | To assess with the partner |
| G9 | Water use and discharge permits for mining sites | Colombia (and any partner country) | Abstraction, settling ponds and discharge of process water | GravitySort recirculates about 1.19 m3/h through a settling pond (PR-008) | Partner organization | To assess per site with the partner |
| G10 | Borax (disodium tetraborate decahydrate) hazard classification | European Union CLP (harmonised) | Classified reproductive toxicant, Repr. 1B, H360FD [8] | Borax is used at the smelting step outside the machine; handling advice belongs in the partner's smelting procedure | Partner organization | Applies to the smelting step (outside this design); safety note in GVS-PRC-001 and GVS-RSK-001 |
| G11 | Battery, charger and electrical safety of the motor option | Per country | Lithium packs and the MotionCore module | Covered in the MotionCore repository (shared lab module); the pack is left to the user | MotionCore lead | To assess in MotionCore |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Notes

- The national action plan under the Minamata Convention in the partner country decides which practices miners must stop and by when; GravitySort's role is to give a mercury-free step that works, not to certify compliance.
- No device certification is expected at TRL 3. If units were ever supplied beyond the partner's own trial, G4 to G7 would need a formal assessment.

## Sources

1. Minamata Convention on Mercury, "Guidance document: developing a national action plan to reduce and, where feasible, eliminate mercury use in artisanal and small-scale gold mining," 2017. https://minamataconvention.org/sites/default/files/documents/forms_and_guidance_document/ASGM_guidance_e_2017.pdf (checked 2026-10-25).
2. Mongabay, "Colombia bans the use of mercury in mining," August 2018. https://news.mongabay.com/2018/08/colombia-bans-the-use-of-mercury-in-mining/ (checked 2026-10-25).
3. Regulation (EU) 2017/852 of the European Parliament and of the Council on mercury. https://eur-lex.europa.eu/eli/reg/2017/852/oj/eng (checked 2026-10-25).
4. ISO 12100:2010, Safety of machinery: General principles for design: Risk assessment and risk reduction. https://www.iso.org/standard/51528.html (checked 2026-10-25).
5. ISO 13857:2019, Safety of machinery: Safety distances to prevent hazard zones being reached by upper and lower limbs. https://www.iso.org/standard/69569.html (checked 2026-10-25).
6. ISO 14120:2015, Safety of machinery: Guards: General requirements for the design and construction of fixed and movable guards. https://www.iso.org/standard/59545.html (checked 2026-10-25).
7. Regulation (EU) 2023/1230 of the European Parliament and of the Council on machinery. https://eur-lex.europa.eu/eli/reg/2023/1230/oj (checked 2026-10-25).
8. Instituto Nacional de Seguridad y Salud en el Trabajo (INSST), "Tetraborato disódico, decahidrato," Infocarquim database. https://www.insst.es/agentes-quimicos-infocarquim/sustancias/tetraborato-disodico-decahidrato (checked 2026-10-25).
