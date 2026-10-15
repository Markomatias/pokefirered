# Game design — proposed first revision

The Kanto story, gyms, Elite Four, Sevii Islands, Pokédex, abilities, normal moves, held items, leveling and evolution remain. Only National Dex #001–151 may be obtainable, encountered or used by trainers. Preserve unused later-species engine data where removal risks compatibility; keep every route to those species inaccessible in the finished game. Changes below are design proposals awaiting implementation and balance tests, not completed features.

## One action, one weapon

Each Pokémon can equip one gun independently of its held item. Equipping and transferring are initially overworld actions. GUN offers Fire and Reload, with ammunition visible. No gun or no legal target yields an explanation and returns to selection. At zero loaded ammunition, Fire is unavailable; Reload consumes the normal turn and transfers `min(capacity - loaded, reserve)` rounds. Reload with no reserve is unavailable. Cancel spends nothing. Initial capacity limit is 63; database validation rejects higher capacities.

Use finite shared reserve pools by class initially, with shop prices and inventory caps. Loading transfers ammunition; it never duplicates it. Unequipping returns loaded ammunition subject to capacity checks, or leaves the whole operation unchanged. Captured wild Pokémon start without collectible equipment until loot rules are implemented. No infinite ammunition, free healing loop, or automatic free reload. Add scarcity slowly so ordinary Pokémon moves remain useful. Trainer ammunition must obey the same battle rules and finite starting budgets.

## Damage and effects policy

Ordinary ballistic guns are Normal type: Ghost immunity and Rock/Steel resistance apply. Experimental weapons receive a declared existing type; never use TYPE_MYSTERY to bypass the type chart. Normal Pokémon moves retain original STAB. Initial gun attacks have no STAB, preventing same-type guns from becoming obvious replacements for four-move strategies. Immunities and absorb abilities apply, including Flash Fire, Levitate and Wonder Guard where relevant. Protect, Substitute, screens, weather, burn, stages, accuracy/evasion and defensive held items retain their applicable effects. Initial projectiles are non-contact. Soundproof is irrelevant unless a weapon explicitly uses a sound effect mechanic. Test interactions rather than inferring them from animation.

For a damaging shot, use the existing integer damage pipeline with a weapon power/type override and an explicit physical/special selector local to weapon attacks. Conceptual core:

`base = floor(floor((floor(2 * level / 5) + 2) * power * attack / defense) / 50) + 2`

Apply the engine's applicable badge/stat, critical, screen, spread, weather, ability, item, type and random modifiers in its actual order, with gun STAB multiplier fixed to 1. This formula is a design model, not a replacement for the engine's integer rounding order. The implementation milestone must publish exact operation order and fixed-RNG golden results against the real engine. Physical guns use Attack/Defense and burn; energy guns may use Special Attack/Special Defense independently of type, without altering regular moves. Zero-effect immunity produces zero damage, never a minimum-one override. Support weapons use explicit effects instead of this formula.

Attempting a shot spends ammunition only after pre-action incapacitation checks allow execution, before accuracy/immunity/Protect resolution. A miss or blocked shot therefore spends ammunition; an action prevented by sleep/flinch does not. Bursts resolve each projectile separately and stop when the target faints; only fired rounds are spent. Critical chance is normal unless specified; cap burst power and do not grant a free status roll per pellet. Charge/recovery effects spend turns and are canceled/reset consistently on switching and fainting.

Initial vertical slice: M1911, Normal/physical, power 40, accuracy 95, capacity 6, one round/shot, priority 0, normal critical rate, no secondary effect. These numbers are provisional. Test against ordinary moves at levels 5/15/30/50, strong/weak defenses, all type multipliers, burn, crits, screens and doubles before distributing it. All later models need a similar budget; no claimed balance without measured outcomes.

## Twelve database classes

| Class | Named first candidate | Role and cost constraint |
|---|---|---|
| Pistols/revolvers | M1911 | Early reliable single hit; limited magazine |
| Submachine guns | MP5 | Two/three weak hits; ammunition cost per projectile |
| Assault rifles | M4A1 | Midgame balanced option; no universal best weapon |
| Shotguns | SPAS-12 | Finite pellet count; accuracy and reload drawbacks |
| Sniper/marksman | Intervention | Critical specialization; small magazine/recovery |
| Machine guns | M60 (proposed addition) | Sustained burst; reduced priority or recovery |
| Launchers/explosives | RPG-7 (proposed addition) | Low ammunition, accuracy/spread penalties |
| Energy/plasma | Helios (original proposed name) | Special stats; declared elemental type |
| Alien/experimental | Parallax (original proposed name) | Delayed attack with visible warning |
| Elemental | Frostline (original proposed name) | Ice typing; existing immunities/abilities respected |
| Rail/charged | Lodestar (original proposed name) | Charge turn; no free damage on charge |
| Support/utility | Lifeline (original proposed name) | Capped single-use healing charge; finite reserves |

The brief supplies ordinary names through a partial sniper list; preserve those as the requested catalog, without promising all models in the vertical slice. Later class candidates above are suggestions, not recovered missing text. Every collectible entry needs a real display name, stable ID, class, type, stat category, power/effect, accuracy, targeting, ammo pool, capacity/cost, priority, critical policy, charge/recovery, acquisition gate and price. Use newly authored visuals/audio; references to names do not authorize copying another game's assets.

## Definitive Kanto acquisition plan

`pokedex.csv` enumerates all 151 species, baseline source evidence, proposed route, progression, choice dependency and implementation/testing status. Evolution rows inherit the acquisition and progression constraints of their parent. Proposed additions retain believable habitats and existing slots: first budget rare/common slot changes and record resulting encounter rates. Do not concatenate version tables or replace every encounter. LeafGreen-only evidence in the checklist is a planning lead, not evidence that FireRed can currently catch it.

Keep the first starter choice. After becoming Champion, Oak awards the two missing starter species through separately tracked rewards; full-party/full-PC refusal must not consume rewards. Cinnabar's postgame fossil researcher provides the unchosen fossil via a quest, with ordinary revival retained. After the Dojo victory, a post-Champion rematch awards the unchosen Hitmon. Celadon's postgame breeder supplies two additional Eevee, once each, enabling all three stone evolutions without breeding or cartridge access. Ensure renewable/budgeted evolution stones, particularly enough Moon Stones for the full checklist.

Replace the four Kanto trade-only evolutions with level 37 evolution. Later-generation trade-item evolutions fall outside the final roster and must be inaccessible. Keep their unused underlying data only for engine safety. Audit every evolution branch from a Kanto species that could produce a later species, including friendship and trade-item methods. Preserve original trade routes only if their compatibility is verified; they are never required for #001–151.

Mew quest proposal: Champion + National Dex + completed Sevii Rocket/Ruby/Sapphire story; three research clues in existing Kanto/Sevii locations lead to a new encounter area. Set the proper fateful-encounter bit: `IsBattlerModernFatefulEncounter` gates Mew obedience in this engine. Failed capture/fainting should permit a documented rematch after another Hall of Fame clear, and saving during the quest must preserve progress. No external event item. Mewtwo retains Cerulean Cave's existing gates. Retain legendary difficulty; add recovery/rematch paths for lost one-time legends so a single save cannot become permanently incomplete.

## Final owner decisions and progression

These decisions supersede conflicting language in the initial brief. The deliverable now is Milestone 0 only, on a separate documentation branch and pull request. Milestone 1 requires explicit owner approval.

The 151-only rule applies to wild encounters, trainer parties, gifts, prizes, NPC trades, starters, eggs, evolution, postgame and event/scripted battles. Non-Kanto babies and later evolutions must never become obtainable; breeding must yield an allowed Kanto form or be disallowed with a clear message. Do not delete species constants or renumber save identities. Add a final-roster audit spanning data and scripts, then verify actual gameplay gates. Existing non-Kanto content remains untouched in Milestone 0; policy is not yet implemented. Imported saves with out-of-roster Pokémon require a clearly documented migration/rejection policy before release.

All enemy trainer groups eventually use firearms: ordinary trainers, Team Rocket, rival, Gym Leaders and Elite Four. Early trainers receive low-power weapons and small finite ammunition budgets; midgame trainers add balanced rifles and limited specialist weapons; late leaders and Elite Four use stronger tactical combinations with explicit counters. Unarmed trainers may remain where appropriate. No hidden unlimited ammunition or special free actions. The AI must compare gun damage, ordinary moves, status, switching and reloading; type immunity must discourage wasting shots. Give each boss a documented loadout and benchmark difficulty against an ordinary-move team as well as a gun-equipped team. No trainer loadouts change in this milestone.

Every collectible firearm has a distinct name. Common, uncommon and rare weapons primarily use iconic Call of Duty names from the supplied catalog. Epic, legendary and mythic discoveries primarily draw on famous Halo, DOOM, GoldenEye and Fallout weapons; possible named candidates include the Halo Plasma Rifle, DOOM BFG 9000, GoldenEye Golden Gun and Fallout Fat Man. These are naming/design references only, with original project artwork and sound. The class table's unsupplied names remain provisional and must be reconciled with the completed catalog before content implementation. Rarity never grants automatic kills or immunity bypass: even the Golden Gun needs a bounded power/effect and scarce ammunition. Assign stable unique IDs and unique full names, then design readable short labels for the GBA interface.

Balance gates: report expected damage per turn (including reload/charge/recovery), burst variance, damage per ammunition cost, status utility and availability against accessible normal moves at each story tier. Test physical/special attackers, frail/tanky defenders, all immunity/resistance patterns and representative abilities/items. Track whether gun use crowds out ordinary moves in boss/wild battles. Adjust power, accuracy, ammunition, price and recovery before adding more models. Do not declare a firearm balanced based solely on its listed power or rarity.
