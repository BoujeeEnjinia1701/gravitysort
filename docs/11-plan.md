---
doc_id: GVS-PLN-001
title: GravitySort project plan
project: GravitySort
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.8 pipeline): workstreams, resources, stage gates P0 to P6 (P4 to P6 on hold), next steps, decisions requested and the reference list"
---

# GravitySort project plan

GravitySort is at stage P3 (design outputs, TRL 3): the constructable design, its D3 model of every concept option, drawings, priced BOM, build plan and pipeline documents exist on paper. The next gate, P4 (verification, TRL 4), is on hold under the portfolio cap; before it Amish is asked to confirm the concept (option A recommended, GVS-DEC-001 O1) and to decide the containment band (O2). Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept and STEM | Design lead | GVS-STM-001, GVS-OPT-001, GVS-DDR-004 | Done at P3; STEM check open: nine rows need tests or datasheets, two need Amish's decisions (O2, O3) |
| Requirements and traceability | Design lead | GVS-URS-001, GVS-PRS-001, GVS-RTM-001 | Done at P3; to revise after co-design |
| Calculations | Design lead | GVS-CAL-001 v0.9 | Done at P3 |
| CAD and drawings | Design lead | `cad/src/model.py` (D3, options A to C), STEP, GVS-DWG-001 to 121 | Done at P3 |
| Build plan and BOM | Design lead | GVS-BLD-001, `bom/bom.csv` | Done at P3 |
| Regulatory, risk and market | Project lead | GVS-REG-001, GVS-RSK-001, GVS-MKT-001 | First issue; items to assess with the partner |
| Partner and co-design | Project lead (Amish) | Agreement with the first candidate cooperative; co-design sessions | Not started (outreach is Amish's action) |
| Renders and media | Coordinator | Options picture, product renders, cards (Blender on Amish's Mac) | Scenes ready; renders pending |
| Prototype build and lab tests (P4) | Workshop partner and design lead | Prototype, test plans and reports | On hold (TRL cap 3) |
| Field trial (P5) | Partner organization | Trial with the cooperative | On hold |

## Resources needed

Table 2. Resources (estimates, to assess with the partner before P4).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Prototype parts | One machine to the BOM | n/a | 594 (BOM estimate) plus 335 if the MotionCore option is built |
| Workshop time (welder, fitter) | Frame, guards, table, assembly | To assess with the workshop | To assess |
| PU casting trial | Liner cast in the printed mold | To assess | To assess |
| Spiked or characterized test ore and assays | Recovery test of PR-004 | To assess | To assess |
| Partner co-design sessions | Validated user requirements | To assess | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Met (2026-10-25, retrofitted under kit 1.8) |
| P1 Definition | URS, PRS draft, RSK with hazard analysis, MKT, REG complete | Met (2026-10-25) |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR, STEM check closed where a calculation can close it | Met on paper; concept selection awaiting Amish (GVS-DDR-004) |
| P3 Design outputs | Model, STEP, drawings, priced BOM, BLD, DEC, design FMEA, traceability complete | Met (TRL 3 since 2026-09-25; D3 model of every option 2026-10-25) |
| P4 Verification | Prototype, lab test plans and reports (recovery, table ratio, pedal power, containment impact test) | On hold (TRL cap 3) |
| P5 Validation | Field trial with the partner, human factors | On hold |
| P6 Commercialization | Only with a named deployment partner | On hold |

## Next steps and decision requested

1. **Decision O1 (concept selection, GVS-DDR-004):** confirm option A, the current design, as the concept carried forward (recommended), or choose B or C.
2. **Decision O2 (containment):** keep the 6 mm tub with an impact test before any spin test (recommended), or fit a steel band now, which takes the mass over PR-011 (GVS-DEC-001).
3. **Decisions O3 to O5:** tank sway near the table frequency (raise the brace node and take a saving, recommended), spindle supports (tap test at TRL 4), fluidization flow (sweep it in the TRL 4 test).
4. Amish's outreach to the first candidate partner (decided 2026-10-02), so that co-design can test the user requirements.
5. Coordinator renders `media/options.png` and the product renders on Amish's Mac.
6. When the TRL cap lifts: the P4 tests in Table 3, starting with the containment impact test and the recovery test.

## References

Every source cited in this repository's documents, Chicago style.

- Alibaba.com SmartBuy. "How to Choose a Gold Separator Machine for Small Scale Mining." Accessed October 25, 2026. https://smartbuy.alibaba.com/buyingguides/gold-separator-machine-small-scale.
- Appel, Peter W. U., and Leoncio Na-Oy. "The Borax Method of Gold Extraction for Small-Scale Miners." *Journal of Health and Pollution* 2, no. 3 (2012). https://www.journalhealthpollution.org/doi/full/10.5696/2156-9614-2.3.5.
- Caballero Espejo, Jorge, et al. "Deforestation and Forest Degradation Due to Gold Mining in the Peruvian Amazon: A 34-Year Perspective." *Remote Sensing* 10, no. 12 (2018): 1903. https://www.mdpi.com/2072-4292/10/12/1903.
- Canadian Mining Journal. "GOLD: Extend the Bowl Life of Falcon Gravity Concentrators." September 2, 2014. https://canadianminingjournal.com/news/gold-extend-the-bowl-life-of-falcon-gravity-concentrators.
- DIG Corporation. "3/4 in MPT Drip Filter with Stainless Steel Screen (120 Mesh), P13-120." Cheapsprinklers.com. Accessed October 25, 2026. https://cheapsprinklers.com/products/dig-120-mesh-flush-valve-stainless-steel-screen-filter-3-4-p13-120.
- European Union. Regulation (EU) 2017/852 on Mercury. https://eur-lex.europa.eu/eli/reg/2017/852/oj/eng.
- European Union. Regulation (EU) 2023/1230 on Machinery. https://eur-lex.europa.eu/eli/reg/2023/1230/oj.
- GBC Ghana. "GWCL Attributes Water Supply Challenges to Galamsey Activities." 2024. https://www.gbcghanaonline.com/general-news/gwcl-attributes-water-supply-challenges-to-galamsey-activities/2024/.
- INSST. "Tetraborato disódico, decahidrato." Infocarquim. Accessed October 25, 2026. https://www.insst.es/agentes-quimicos-infocarquim/sustancias/tetraborato-disodico-decahidrato.
- International Organization for Standardization. ISO 12100:2010, ISO 13857:2019 and ISO 14120:2015. https://www.iso.org/standard/51528.html; https://www.iso.org/standard/69569.html; https://www.iso.org/standard/59545.html.
- Minamata Convention on Mercury. "Guidance Document: Developing a National Action Plan to Reduce and, Where Feasible, Eliminate Mercury Use in Artisanal and Small-Scale Gold Mining." 2017. https://minamataconvention.org/sites/default/files/documents/forms_and_guidance_document/ASGM_guidance_e_2017.pdf.
- Mitchell, C. J., T. Bide, C. Odhiambo, M. Nyakinye, J. C. Rushton, C. Kresse, and M. Pearson. "Neoarchean Gold Grain Size and Artisanal Mining in Migori, Kenya: Review of Current Recovery Methods." *Earth Science, Systems and Society* 6 (2026): esss2025-005. https://doi.org/10.1144/esss2025-005.
- Mongabay. "Colombia Bans the Use of Mercury in Mining." August 2018. https://news.mongabay.com/2018/08/colombia-bans-the-use-of-mercury-in-mining/.
- NRDC. "The Minamata Convention: What It Means for Artisanal and Small-Scale Gold Mining." https://www.nrdc.org/bio/susan-egan-keane/minamata-convention-what-it-means-artisanal-and-small-scale-gold-mining.
- planetGOLD. "About." https://www.planetgold.org/about.
- Poling, C. W., and J. F. Hamilton. "Fine Gold Recovery of Selected Sluicebox Configurations." University of British Columbia pilot-scale study (gravel sampled July 22, 1985). Yukon Geological Survey library. https://emrlibrary.gov.yk.ca/emrlibrary/ygs/mining_technology/fine_gold_recovery_sluiceboxes.pdf.
- Pure Earth. "Filipino Gold Miners' Borax Revolution." https://www.pureearth.org/filipino-gold-miners-borax-revolution/.
- "Risk Factors of Malaria Transmission in Mining Workers in Muara Enim, South Sumatra, Indonesia." *Scientific Reports* (2023). https://pmc.ncbi.nlm.nih.gov/articles/PMC10484942.
- "Epidemiological and Entomological Studies of a Malaria Outbreak among French Armed Forces Deployed at Illegal Gold Mining Sites Reveal New Aspects of the Disease's Transmission in French Guiana." https://pmc.ncbi.nlm.nih.gov/articles/PMC4722744.
- Stabroek News. "Moving from Mercury." November 15, 2013. https://stabroeknews.com/2013/11/15/business/moving-mercury-3/print.
- UNEP Global Mercury Partnership. "Artisanal and Small-Scale Gold Mining (ASGM)." https://www.unep.org/globalmercurypartnership/what-we-do/artisanal-and-small-scale-gold-mining-asgm.
- US EPA. "Artisanal and Small-Scale Gold Mining Without Mercury." https://www.epa.gov/international-cooperation/artisanal-and-small-scale-gold-mining-without-mercury.
- US EPA. "Mercury Emissions: The Global Context." https://www.epa.gov/international-cooperation/mercury-emissions-global-context.
- Veiga, Marcello M., et al. *Journal of Cleaner Production* 205 (2018). https://doi.org/10.1016/j.jclepro.2018.09.039.
- Veiga, Marcello M., and A. J. Gunson. "Gravity Concentration in Artisanal Gold Mining." *Minerals* 10, no. 11 (2020): 1026. https://doi.org/10.3390/min10111026.
- World Gold Council. "Gold Demand Trends: Full Year 2025." https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-full-year-2025.
- World Health Organization. "Arsenic." Fact sheet. https://www.who.int/news-room/fact-sheets/detail/arsenic.
- 911 Metallurgist. "i150 iCON Concentrator" and "Original GEMENI Table." Accessed October 25, 2026. https://www.911metallurgist.com/equipment/i150-icon-concentrator/; https://www.911metallurgist.com/equipment/?p=19066.
