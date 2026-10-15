# Delivery milestones and acceptance gates

The owner authorized Milestone 0 only. Wait for explicit owner approval before beginning Milestone 1. After approval, complete one milestone, verify it and report results before broadening scope. Do not implement the entire game in one task. Foundation work below is completed; all gameplay milestones are pending.

| Milestone | Deliverable | Required evidence before completion |
|---|---|---|
| 0 — foundation | Existing checkout, reproducible tools, architecture/design and acquisition plan | FireRed baseline checksum matches; setup rerun passes; checklist audit passes. Completed here; no gameplay tests claimed. |
| 1 — persistence spike | One weapon definition, accessors, inventory schema, new-game/migration strategy, no battle use | Target size/offset assertions; get/set checksum round trips; vanilla import to zero equipment; unsupported version rejection; save/reload and slot recovery; no item/move changes. |
| 2 — equipment lifecycle | Equip/unequip UI and weapon display | Save/reload, PC deposit/withdraw/reorder/box swap, party reorder, faint/revive, level/evolution, daycare deposit/return, hatch, release, full inventory/full PC; distinct creatures with matching identities; no lost/duplicated weapon or ammunition. |
| 3 — playable vertical slice | M1911, dedicated readable GUN command, Fire/Reload; one controlled acquisition point | Emulator test in wild/trainer/doubles: exactly one action, correct speed order, cancel/no gun/no ammunition, misses, blocked actions, KO, switch and battle exit. Screenshot review at 240 × 160. Publish exact damage/rounding with fixed RNG tests and conservation of ammunition. |
| 4 — battle interaction coverage | Progression-scaled trainer loadouts, AI and special battle guards | Ability/type/status/screens/Substitute/Protect/critical matrix; recharge/charge and forced action rules; special controllers unchanged; compatible behavior or clear guard for link/trade modes. Ordinary four-move/held-item regressions tested. |
| 5 — definitive Kanto | 151-only roster across wild/trainers/gifts/trades/eggs/evolution, combined encounters, trade alternatives, starters/fossils/Hitmons/Eevee, stones, Mew and legend rematches | Checklist linked to changed scripts/flags; fresh-save path to all 151; test each initial starter, each fossil and each Hitmon choice, full party/PC rewards, reload midquest, all stone budgets and story gates. Source audit alone cannot pass this milestone. |
| 6 — weapon catalog | All twelve classes with individually named weapons and progression | Per-entry database validation; acquisition/price/ammo balance; charging, pellets, multihits and finite support effects measured; ordinary moves remain viable. Recover missing catalog text before promising exact full catalog. |
| 7 — release candidate | Story/postgame polish and distribution package | Full fresh-save Kanto/Sevii playthrough, 151 owned in one save, save stress/recovery, no softlocks, resource budgets, emulator/hardware compatibility, legal patch distribution and clean repository without ROM/save binaries. |

## Functional test recording

Every result must record commit, ROM hash, emulator/version (or hardware), starting save/scenario, inputs, expected/observed outcomes and pass/fail. Keep test saves local and out of commits. Mark unrun, skipped and failed separately. For deterministic battle tests record RNG seed, stats, type, ability, held item, weather/screens and expected damage/ammunition. Test one side effect at a time, then representative combinations.

Automate pure database validation and deterministic engine tests where practical. Exercise actual persistence, battle controller and script paths; a desktop reimplementation of a formula is insufficient. The repository's checksum comparison is a baseline regression check only. Once gameplay changes begin, successful ROM compilation plus emulator functional checks become the minimum gate. A release gate requires an actual complete save-file acquisition run.

Recommended next task, only after explicit owner approval: milestone 1, beginning with raw/copy/access auditing and measured target layouts. If the candidate filler or save block is not safe, revise the schema before adding any equipment or command UI. No migration or compatibility guarantee exists yet.
