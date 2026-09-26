# GravitySort

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mining · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $455 USD · **Difficulty:** 4 of 5

A mercury-free gravity concentrator for small-scale gold miners: a pedal- or motor-driven centrifugal bowl and shaking table combination that recovers fine gold without amalgamation.

![GravitySort concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement GVS-DWG-001 (PDF)](cad/drawings/GVS-DWG-001.pdf) · [Sizing note GVS-CAL-001](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Miners use mercury because it catches fine gold cheaply, not because they want to. If a local workshop can build a machine that catches as much gold as mercury, or more, at a price a small group can pay back in weeks, miners gain an economic reason to stop, not only a legal one. GravitySort pairs the two gravity methods that each solve half the problem: a fluidized centrifugal bowl holds fine gold from a steady stream of milled ore, and a small shaking table cleans the bowl's concentrate down to a few tens of grams that can be smelted directly with borax. One pedal or motor drive runs both.

It is open and garage-buildable because commercial centrifuges and tables are imported, costly and hard to repair at a mine site. The frame is welded tube, the drive is bicycle parts and V-belts, the tub and tank are HDPE drums, and the bowl liner is cast in a printed mold, so a welder in a mining town can build, repair and adapt it, and anyone can check how it works.

## Burning platform

Artisanal and small-scale gold mining is the largest human source of mercury emissions to air: about 838 t in 2015, 37.7 % of the global total ([US EPA summary of the UNEP Global Mercury Assessment 2018](https://www.epa.gov/international-cooperation/mercury-emissions-global-context)). UNEP estimates that 10 to 15 million people work in the sector, including 4 to 5 million women and children, and that it produces about 12 to 15 % of the world's gold ([UNEP Global Mercury Partnership](https://www.unep.org/globalmercurypartnership/what-we-do/artisanal-and-small-scale-gold-mining-asgm)).

The pressure is rising. Gold averaged a record US$3,431/oz in 2025, up 44 % on the year ([World Gold Council](https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-full-year-2025)), which raises the incentive to mine and the value of every gram lost. Yet whole-ore amalgamation in Colombian processing centers typically recovers only about 30 % of the gold ([Veiga et al., 2018](https://doi.org/10.1016/j.jclepro.2018.09.039)), so better gravity equipment can pay for itself as well as remove mercury.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Artisanal and small-scale gold mining | Mercury-free primary concentration and clean-up for groups processing about 1 to 2 t of ore per day |
| Ore processing centers (entables) | Replace whole-ore amalgamation with a concentrate step, as national action plans require |
| Responsible gold supply chains | Refiners, traders and jewelers sourcing traceable mercury-free gold from certified small mines |
| Development and extension programmes | Demonstration unit for NGOs, cooperatives and government extension officers |
| Mining education | Teaching gravity separation in technical colleges and mining schools |
| Mineral exploration | Concentrating heavy minerals from stream sediment and trench samples in the field |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| Ghana | Illegal small-scale mining (galamsey) has silted rivers; Ghana Water reported raw water turbidity of about 14,000 NTU at one plant designed for 2,000 NTU ([GBC Ghana](https://www.gbcghanaonline.com/general-news/gwcl-attributes-water-supply-challenges-to-galamsey-activities/2024/)) |
| Peru | Gold mining cleared 95,751 ha of forest in the southeastern Peruvian Amazon from 1985 to 2017 ([Caballero Espejo et al., *Remote Sensing*, 2018](https://www.mdpi.com/2072-4292/10/12/1903)); Madre de Dios miners rely on mercury |
| Colombia | Mercury use in mining has been banned since July 2018 under Law 1658 of 2013 ([Mongabay](https://news.mongabay.com/2018/08/colombia-bans-the-use-of-mercury-in-mining/)), so miners need working alternatives |
| Philippines | In Benguet, the regional miners' federation reports all 15,000 members smelt gravity concentrates with borax instead of mercury ([Pure Earth](https://www.pureearth.org/filipino-gold-miners-borax-revolution/)), a model GravitySort's clean concentrate is designed to feed |
| European Union | Mercury exports and amalgamation in small-scale gold mining are prohibited ([Regulation (EU) 2017/852](https://eur-lex.europa.eu/eli/reg/2017/852/oj/eng)); EU buyers and programmes need mercury-free equipment to support abroad |

## What sparked the idea

The starting point was a single phrase in the Minamata Convention on Mercury, the treaty signed in Minamata, Japan, in October 2013. Its annex on artisanal and small-scale gold mining asks countries to eliminate the worst practices in the sector, including whole-ore amalgamation, in which mercury is mixed with all of the milled ore rather than with a small concentrate ([NRDC summary of the convention](https://www.nrdc.org/bio/susan-egan-keane/minamata-convention-what-it-means-artisanal-and-small-scale-gold-mining)). Ending that practice without ending the miners' income means putting a concentration step in front of the gold: something that turns tonnes of ore into a handful of heavy concentrate. GravitySort is that step, sized so the concentrate is small enough to smelt directly with borax and no mercury is needed at all.

## Problem

Artisanal and small-scale gold mining uses mercury to capture fine gold because it is cheap and works, poisoning miners, families and rivers. Mercury-free equipment exists but is costly and often recovers less fine gold. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

Problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

A welded steel frame carries a fluidized centrifugal bowl (220 mm lip, about 60 G at 730 rpm) that takes about 200 kg/h of ore milled below 2 mm, with a hopper screen above it and a water header tank beside it. A pedal crank, or a 250 W motor through the lab's MotionCore module, turns the bowl through a jackshaft, bevel gearbox and V-belt; a bicycle disc brake stops it, and the lid opens only with the brake set. At the end of the day the same drive runs a 1,000 x 450 mm shaking table that cleans about 5.3 kg of bowl concentrate down to about 100 g for direct smelting with borax. The TRL 3 sizing note gives 48 W at the pedals, 1.19 m3/h of mostly recirculated water and about 1.55 t of ore per shift; about 60 % overall recovery on free-gold ore is assumed, compared with about 30 % for whole-ore amalgamation. The frame is 25 x 25 x 1.5 mm steel tube, and the machine weighs about 77 kg in six loads. The parts cost is $455, within the $455 budget. All figures are estimates, not measurements.

Sizing note: [docs/04-calcs/01-sizing.md](docs/04-calcs/01-sizing.md) · Decisions: [GVS-DDR-001](docs/decisions/0001-trl2-review-decisions.md), [GVS-DDR-002](docs/decisions/0002-recommendations-accepted.md) · Drawing: [GVS-DWG-001](cad/drawings/GVS-DWG-001.pdf) · Model: [cad/src/model.py](cad/src/model.py)

Full design precis: [docs/02-concept.md](docs/02-concept.md) · Requirements: [docs/03-requirements.md](docs/03-requirements.md)

## Key components

- Welded steel base frame
- Feed hopper with 2 mm screen
- Centrifugal bowl with riffle rings and a cast polyurethane liner
- Fluidization water jacket and rotary union
- Spindle, bearings, splash tub and lid guard
- Bicycle disc brake with a parking latch and lid interlock, and a bicycle computer as the bowl speed display
- Drive: pedal crank, or a 250 W motor via MotionCore, through a jackshaft, bevel gearbox and V-belts, with guards
- Water header tank, valve and flow meter
- Small shaking table with head motion and a lockable concentrate tray

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Rotating machinery and water: the bowl spins at up to 850 rpm and coasts for about 20 s after the drive stops. Never run without the lid guard and belt and chain guards, keep hands, hair and loose clothing clear, and apply and park the brake before opening the lid. A rider can push the bowl past its 900 rpm limit; the bowl is designed with a large burst margin at that speed, but watch the speed display. Never use GravitySort with mercury or on untested mercury-contaminated tailings. Fence settling ponds. Concentrates can contain arsenic and lead minerals; wash hands after handling. Smelting, done outside this machine, reaches over 1,000 °C and needs a proper furnace and protective equipment. The motor option adds lithium cells; follow the MotionCore safety section. See [docs/02-concept.md](docs/02-concept.md#safety).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (GVS-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `GVS-PRC-001/v1.0`.

## Credits

Designed by Amish Chadha. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for roles. To cite this design, use [CITATION.cff](CITATION.cff) (GitHub shows it as "Cite this repository").

AI assistance (Claude) was used to accelerate concept renders, prototype documentation and first-pass sizing calculations. Design direction and all decisions are Amish Chadha's, recorded in this repository's decision records (`docs/decisions/`).

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
