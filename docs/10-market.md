---
doc_id: GVS-MKT-001
title: GravitySort market and viability
project: GravitySort
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.8 pipeline): segments, cited equipment prices checked on 2026-10-25, estimated unit cost from the BOM and the open route"
---

# GravitySort market and viability

GravitySort is for small mining groups and processing centers that need a mercury-free step that catches fine gold, at a fraction of the price of imported centrifuges and shaking tables, which cost from about US$1,000 for small imported units to US$12,000 to US$22,000 for branded ones. An open design matters because the machine must be built, repaired and adapted in mining towns, where imported equipment is costly to buy and hard to fix. Prices and benchmarks are cited with the date they were checked. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Small mining groups processing about 1 to 2 t of milled ore a day | Groups of 3 to 10 miners in Colombia (first partner country), Peru, Ghana and the Philippines | iCON i150 centrifugal concentrator, 2 t/h: US$11,900 to US$13,500 listed [1]; Gemeni shaking table range: US$22,000 listed [2]; Gemini GT60 table about US$8,000 in Guyana in 2013 [3] | 594 in parts (BOM, excluding MotionCore); plus 335 for the optional MotionCore kit and motor | Centrifuge and table in one pedal-driven machine for about a twentieth of the branded price; no power needed; repairable locally |
| Processing centers (entables) replacing whole-ore amalgamation | Fee-based mills in Colombia and Peru with mains or generator power | Small imported centrifugal units: US$400 (10 to 20 kg/h) to US$2,800 (Falcon-type clone, 50 to 70 kg/h); 3 x 6 ft shaking table US$1,200 (100 to 150 kg/h), 2024 tiers [4] | 594 plus 335 (motor option) | A concentrate step that meets mercury bans, sized for about 200 kg/h, with the motor option |
| NGOs, cooperatives and extension programmes | Programmes under national ASGM action plans; planetGOLD and similar | Equipment from workshop materials in the CICAN project, Colombia: US$2,600 to US$10,500 capital for under 2 t/day [5]; a centrifuge for under US$6,000 in Canada [6] | 594 | Open documentation, build plan and BOM so programmes can build and teach locally |
| Mining education and exploration | Technical colleges; field sampling of heavy minerals | Laboratory tables and centrifuges (prices as above) | 594 | A teaching machine whose every part is drawn and explained |

## Viability, first order

On the 5 g/t reference ore, one shift of 1.55 t carries about 7.75 g of gold (GVS-CAL-001). If GravitySort recovers about 60 % overall, as assumed in GVS-CAL-001, against about 30 % for whole-ore amalgamation in Colombian processing centers [5], the extra gold is about 2.3 g per shift. At the 2025 average gold price of US$3,431/oz [7] (about US$110/g) that is about US$250 per shift, so the parts cost of about US$594 would be recovered in a few shifts. This is an illustration only: the recovery is an assumption until tested (PR-004, TRL 4), real grades range from about 1 to 20 g/t, and miners receive less than the world price.

## Open route

- **Who builds it.** A welder or small metal shop in a mining town builds the frame, guards and table; bicycle parts, bearings, V-belts and HDPE drums are bought locally; the liner is cast in a printed mold by a resin or 3D printing shop. The build plan GVS-BLD-001 and the drawings GVS-DWG-001 to 121 cover every part.
- **How it spreads.** Through the partner cooperative and its programme (the first candidate was decided by Amish on 2026-10-02: a miners' cooperative introduced through the Alliance for Responsible Mining in Medellin), NGOs working under national action plans, and technical colleges. The Helpful Engineering network can connect builders.
- **What keeps it open.** Hardware under CERN-OHL-S-2.0 and software under MIT (`REUSE.toml`); every derivative stays open. No commercial channel is planned at TRL 3; any sale of units would need the regulatory steps in GVS-REG-001 (G4 to G7).

## Sources

1. 911 Metallurgist, "i150 iCON concentrator," product page listing US$13,500 and US$11,900, 2 t/h, 2 mm feed, 10 to 30 L/min water, 1.5 kW. https://www.911metallurgist.com/equipment/i150-icon-concentrator/ (checked 2026-10-25).
2. 911 Metallurgist, "Original GEMENI Table," product page listing US$22,000 (was US$25,000); GT60 up to 30 kg/h, GT250 up to 115 kg/h, GT1000 up to 0.5 t/h. https://www.911metallurgist.com/equipment/?p=19066 (checked 2026-10-25).
3. Stabroek News, "Moving from mercury," 15 November 2013. https://stabroeknews.com/2013/11/15/business/moving-mercury-3/print (checked 2026-10-25).
4. Alibaba.com SmartBuy, "How to choose a gold separator machine for small scale mining," price tiers as of 2024. https://smartbuy.alibaba.com/buyingguides/gold-separator-machine-small-scale (checked 2026-10-25).
5. Veiga, M. M., et al. *Journal of Cleaner Production* 205 (2018) (title as in the DOI record). https://doi.org/10.1016/j.jclepro.2018.09.039 (as cited in GVS-PRB-001).
6. Veiga, M. M., and A. J. Gunson. "Gravity Concentration in Artisanal Gold Mining." *Minerals* 10, no. 11 (2020): 1026. https://doi.org/10.3390/min10111026 (checked 2026-10-25).
7. World Gold Council, "Gold Demand Trends: Full Year 2025." https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-full-year-2025 (as cited in the README).
