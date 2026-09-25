# GravitySort

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mining · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $350 USD · **Difficulty:** 4 of 5

A mercury-free gravity concentrator for small-scale gold miners: a pedal- or motor-driven centrifugal bowl and shaking table combination that recovers fine gold without amalgamation.

## Concept rationale

If a local workshop can build a concentrator that matches mercury on recovery and cost, miners have an economic reason to stop using mercury, not only a legal one.

## Burning platform

Artisanal gold mining is the largest source of mercury pollution worldwide, and the Minamata Convention asks countries to reduce and where possible eliminate its use.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. Mining is a Design Molecule research area with no open project yet, and mercury in small-scale gold mining is its most urgent human problem.

## Problem

Artisanal and small-scale gold mining uses mercury to capture fine gold because it is cheap and works, poisoning miners, families and rivers. Mercury-free equipment exists but is costly and often recovers less fine gold.

## Concept

A mercury-free gravity concentrator for small-scale gold miners: a pedal- or motor-driven centrifugal bowl and shaking table combination that recovers fine gold without amalgamation.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Centrifugal concentrator bowl with riffle rings
- Drive: pedal crank or 250 W motor via MotionCore
- Water supply and flow control
- Small shaking table deck
- Frame and splash guard
- Concentrate collection tray

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Rotating machinery and water: guard the bowl drive, limit speed and keep hands clear when running.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Gap-filling areas set.
