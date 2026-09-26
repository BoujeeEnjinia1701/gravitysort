---
doc_id: GVS-PRB-001
title: GravitySort problem statement
project: GravitySort
doc_type: Problem statement
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, out of scope, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update. Cost and power constraints from GVS-CAL-001; water pumping gap; partner screening criterion and borax smelting step adopted for TRL 3 under Amish's 2026-09-25 instruction (GVS-DDR-001), open for his review
---

# GravitySort problem statement

Artisanal and small-scale gold miners use mercury to catch fine gold because it is cheap, needs no power and works well enough, and the mercury ends up in their bodies, their homes and their rivers. Mercury-free gravity equipment exists, but the machines that catch fine gold (centrifugal concentrators and shaking tables) are costly and mostly imported, and cheap sluices lose much of the fine gold. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## The problem

Artisanal and small-scale gold mining (ASGM) is the largest source of human-made mercury emissions to air, at about 838 t in 2015, or 37.7 % of the global total ([US EPA summary of the UNEP Global Mercury Assessment 2018](https://www.epa.gov/international-cooperation/mercury-emissions-global-context)). UNEP estimates that 10 to 15 million people work in the sector, including 4 to 5 million women and children ([UNEP Global Mercury Partnership](https://www.unep.org/globalmercurypartnership/what-we-do/artisanal-and-small-scale-gold-mining-asgm)).

Mercury is used because it solves a real processing problem. Much of the gold in milled ore is fine (below about 0.1 mm), and fine gold is hard to hold on a sluice. Miners add mercury, which wets gold and forms an amalgam that is easy to collect, then burn off the mercury over an open fire to leave sponge gold. The two worst practices are whole-ore amalgamation, where mercury is mixed with all of the ore rather than a small concentrate, and open burning of amalgam. Both are named for elimination in Annex C of the Minamata Convention on Mercury ([Minamata Convention guidance on national action plans](https://minamataconvention.org/sites/default/files/documents/forms_and_guidance_document/ASGM_guidance_e_2017.pdf)).

Mercury is also not as good as it looks. In Colombian processing centers where whole ore is amalgamated in small ball mills, gold recovery is typically about 30 %, and a study of simple gravity and flotation equipment built from local materials found that concentration can be more profitable when recovery is higher than that ([Veiga et al., *Journal of Cleaner Production* 205, 2018](https://doi.org/10.1016/j.jclepro.2018.09.039)). The obstacle is less the physics than access: gravity equipment that catches fine gold is "generally more expensive" and "requires some experience to operate" ([US EPA, ASGM without mercury](https://www.epa.gov/international-cooperation/artisanal-and-small-scale-gold-mining-without-mercury)).

GravitySort addresses the equipment gap: an open, garage-buildable centrifugal concentrator and small shaking table, powered by pedals or a small electric motor, that together make a clean concentrate small enough to smelt directly with borax, so no mercury is needed at any step.

## Users and context

Table 1. Intended users. Proposed for review; the real list must come from co-design sessions.

| User | Need | Context |
| --- | --- | --- |
| Small mining group (3 to 10 people) | Recover more of the gold in the ore they already mine, without mercury, at a cost they can recover in weeks | Hard-rock or alluvial pits; ore milled by hammer mill or ball mill to below about 1 to 2 mm |
| Processing center (entable, plant) operator | Replace whole-ore amalgamation with a concentrate step to meet new rules and keep customers | Mills ore for many miners on a fee basis; has mains or generator power |
| Women processors | A safer role than panning with mercury at home or at the river | Often handle panning, washing and amalgam burning today |
| Local workshop or welder | Build, repair and sell the machine with local tools and materials | Welding set, drill press, hand tools; no lathe in many cases |
| NGO, cooperative or extension officer | Demonstrate mercury-free processing with miners and measure recovery | Programmes under national ASGM action plans; planetGOLD and similar |

### Operating environment

- **Feed:** ore milled to below 2 mm, as a slurry of about 25 to 35 % solids by mass; gold grades from about 1 to 20 g/t; heavy minerals such as magnetite, pyrite and hematite in the feed.
- **Sites:** remote pits and camps, often in tropical forest or savanna, sometimes at altitude; dust, mud, rain and heat (15 to 40 °C).
- **Water:** often scarce or silt-laden; recirculation through a settling pond is good practice and increasingly required.
- **Power:** frequently none, or a small generator shared with the mill.
- **Security:** gold concentrate is valuable and theft is a real concern, so concentrate must be easy to lock away.
- **Supply chain:** steel tube, sheet metal, bicycle parts, bearings, V-belts, HDPE drums and hoses are sold in most mining towns; specialist parts are not.

## Constraints

- Garage-buildable prototype, about $350 USD in parts. The TRL 3 BOM is $465, over this and over the $450 recommended at TRL 2, which is awaiting Amish (GVS-CAL-001, GVS-DDR-001).
- No mercury in any step, and no chemicals beyond water and, at the smelting step outside this machine, borax flux.
- Built with welding, drilling and hand tools; parts that normally need a lathe (bowl, spindle) must have a no-lathe route.
- Runs without grid power: pedal drive as the baseline, with an optional motor through MotionCore on a pack of the user's choice. The water supply (about 1.19 m3/h from the settling pond) still needs a pump, which the design does not yet provide (GVS-DDR-001 item 12).
- Carried to site in parts by two people and assembled with hand tools.

## Out of scope

- Milling and crushing (a separate machine; GravitySort starts from milled ore).
- Cyanide leaching, flotation and any chemical processing.
- Smelting equipment. Direct smelting with borax is the recommended final step (adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review) and the concentrate is sized for it, but the furnace is not part of this design.
- Tailings dams and water treatment beyond a settling pond.
- Legal status, licensing and the gold trade. These decide whether any equipment is adopted and must be covered by the partner organization.

## Prior work

- **Commercial centrifugal concentrators** (Knelson, Falcon and similar) use a spinning riffled bowl, often fluidized with water, to hold dense particles at tens of times gravity. They are effective on fine gold but costly, and small units run batch cycles of about 0.5 to 2 h ([US EPA](https://www.epa.gov/international-cooperation/artisanal-and-small-scale-gold-mining-without-mercury)).
- **Shaking tables** give high-grade concentrates but are "relatively expensive and require some experience to operate" ([US EPA](https://www.epa.gov/international-cooperation/artisanal-and-small-scale-gold-mining-without-mercury)).
- **CICAN project, Colombia.** A chain mill, shaking table and flotation cell were built from junkyard and workshop materials for micro-miners processing under 2 t per day, with capital costs of US$2,600 to US$10,500 ([Veiga et al., 2018](https://doi.org/10.1016/j.jclepro.2018.09.039)). GravitySort aims below the bottom of that range for the concentration step alone.
- **Direct smelting with borax (Benguet method).** Small-scale miners in Benguet, Philippines, smelt gravity concentrates with borax instead of amalgamating them; the Benguet federation reports that its 15,000 members use the method ([Pure Earth](https://www.pureearth.org/filipino-gold-miners-borax-revolution/); [Appel and Na-Oy, *Journal of Health and Pollution*, 2012](https://www.journalhealthpollution.org/doi/full/10.5696/2156-9614-2.3.5)). The method needs a small, clean concentrate; the US EPA cites about 50 to 100 g ([US EPA](https://www.epa.gov/international-cooperation/artisanal-and-small-scale-gold-mining-without-mercury)).
- **planetGOLD** runs mercury-free ASGM programmes, including equipment and finance, in many countries ([planetGOLD](https://www.planetgold.org/about)).

The gap GravitySort targets is an open design that combines the fine-gold capture of a centrifuge with the upgrading of a table, at a parts cost a small group can afford, and that runs on pedal power.

## Open questions

- [ ] What gold particle size distribution do partner sites actually have, and how much of the gold is locked in sulfides that no gravity method will recover?
- [ ] Is pedal power acceptable for a full shift, or will users treat the motor as the default?
- [ ] How much water is available per site, and is recirculation practical?
- [ ] Which country's national action plan and partner offers the best first field site? The screening criterion adopted for TRL 3 (GVS-DDR-001 item 8a) is a country with a mercury ban in force, such as Colombia, or a Minamata action plan with a planetGOLD programme; the partner itself is proposed, awaiting Amish.
- [ ] How do sites without power pump about 1.2 m3/h of water from the settling pond to the header tank?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
