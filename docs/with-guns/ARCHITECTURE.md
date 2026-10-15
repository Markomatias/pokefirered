# Architecture and constraints

## Source map

| Concern | Actual entry points | Implication |
|---|---|---|
| Build | `Makefile`, `config.mk`, `make_tools.mk`, `.github/workflows/build.yml` | Default FIRERED, revision 0, MODERN=0. One source tree selects both versions; no codebase merge needed. |
| Persistent Pokémon | `include/pokemon.h`, `src/pokemon.c` | Box records contain identity, checksum and four shuffled/encrypted 12-byte substructures. Use Get/SetMonData and Get/SetBoxMonData paths. |
| Party/PC | `include/pokemon_storage_system.h`, `src/pokemon_storage_system.c`, `src/party_menu.c` | Six party members; 14 boxes × 30 slots. Equipment belongs to the creature, not a party position. |
| Save | `include/global.h`, `include/save.h`, `src/save.c`, `src/load_save.c` | Two rotating 14-sector save slots with checksums and recovery; do not bypass save routines. |
| Command selection | `src/battle_controller_player.c`, `src/battle_controllers.c`, `include/constants/battle.h` | Four hardcoded choices map to move, item, switch and run. Controller payloads and return values need review. |
| Battle execution | `src/battle_main.c`, `src/battle_script_commands.c`, `src/battle_util.c`, `data/battle_scripts_1.s` | Selection, action order, status checks, effects and battle script execution are separate concerns. |
| Damage | `CalculateBaseDamage` in `src/pokemon.c`; type/effect commands in `src/battle_script_commands.c` | Gen III type-based physical/special categories; do not introduce a global modern damage split. |
| Acquisition | `src/data/wild_encounters.json`, `src/data/pokemon/evolution.h`, `data/maps/*/scripts.inc`, `include/constants/flags.h`, `include/constants/vars.h` | Generated encounter headers are not the authoring source. Version selection, quest flags and script rewards all affect reachability. |
| Other lifecycle | `src/daycare.c`, `src/trade.c`, `src/trade_scene.c`, `src/evolution_scene.c`, `src/pokemon.c` | Breeding, copies, trades and evolution need explicit equipment policy. |

## Save layout investigation

The declared layouts give BoxPokemon = 80 bytes and party Pokemon = 100 bytes; each encrypted substructure is 12 bytes. Confirm these sizes with target-compiler assertions when implementing. Adding bytes to a substructure expands every boxed record and changes serialization, checksums, PC capacity requirements and link payload assumptions.

`PokemonSubstruct0` has a named `u16 filler` after friendship. The initial source search found no `substruct0->filler` access. This is a candidate, not a demonstrated safe extension. Proposed encoding: bits 0–7 weapon ID (0 = none), bits 8–13 loaded ammunition (0–63), bits 14–15 schema tag. Tag 0 represents legacy/no equipment; tag 1 is the first weapon schema. Invalid tag/ID/capacity combinations normalize to no weapon, with diagnostics in development builds. Do not read this field directly from encrypted records. Initializing, checksum recomputation and copies must follow the existing accessors. Audit raw/assembly accesses before adopting it.

This preserves ordinary held items and all four moves. Reserve ammunition and ownership counts are global inventory, not extra bytes in each Pokémon. Per-Pokémon equipment follows PC moves automatically only if all paths preserve the full boxed record; this still requires testing. Never key persistent equipment by party index, personality alone, or OT ID alone.

SaveBlock1 is documented as 0x3D68 bytes, SaveBlock2 as 0xF24. Sector payload is 3968 bytes. SaveBlock1 uses four sectors (capacity 15872, declared size 15720); SaveBlock2 uses one (capacity 3968, declared size 3876). Neither slack budget supports a naive 420-entry equipment side table. PC storage spans nine sectors. Existing static assertions in `src/save.c` enforce sector capacity.

`SaveBlock1.unused_348C[400]` is a second candidate with only its declaration found in the initial C/assembly reference search. A proposed inventory layout needs 8 header bytes (magic/version/length), 256 one-byte unequipped weapon counts and 24 bytes for twelve u16 reserve-ammo pools: 288 bytes; leave 112 untouched. This is a budget proposal, not permission to overwrite the block. Audit all save consumers, quest log/new-game/erase paths and external formats first; preserve offsets and existing sector checksum/recovery behavior. Disable new features if format validation fails. Migration must explicitly distinguish a fresh save, a vanilla save and a future/unsupported hack save.

New games initialize everything. A vanilla-save import must treat candidate fields as untrusted and never interpret arbitrary filler as a valid owned gun. Prefer a one-time opt-in import with a backed-up save and zero equipment; reject unsupported formats cleanly. Recovery from one damaged save slot must restore inventory and creature state together. Do not advertise cross-version downgrade support.

## Integration boundaries

Introduce a weapon data table, equipment accessors, inventory API, battle action adapter and equipment UI in separate modules. Database IDs are stable after release; changing display order must not change IDs. Weapon IDs are independent of species/move/item IDs. No gun may occupy a normal move slot or held-item slot. Battle-only state holds targets, charge/recovery and pending ammunition debits; persist loaded ammunition back to the correct party record at defined action boundaries.

A dedicated GUN command is preferred. Prototype a readable three-row command layout at 240 × 160, retaining FIGHT/BAG/POKéMON/RUN. If that fails, present a submenu mockup for owner approval before substituting it. Cancel and no-equipment messages return to selection without spending a turn. A confirmed attack or reload spends exactly one action. Safari battles, tutorials and scripted catching demos retain their special controllers. Link battles/trades require an explicit compatibility gate until a matching hack protocol exists; never silently send weapon data to vanilla games.

Audit AI evaluation, speed/priority, paralysis/sleep/freeze/confusion/flinch, forced moves, double-battle targeting, Pursuit and action cancellation before enabling weapons broadly. Battle state must not leak into a later Pokémon after switching or fainting. Eggs hatch unequipped; releasing an equipped Pokémon requires confirmation and an atomic return to inventory (or cancellation when full). Trade compatibility and daycare transfers are milestone gates, not assumed working behavior.

## Resource and verification limits

GBA memory, ROM capacity, VRAM, sprite limits, text widths and ARM toolchain behavior constrain every new subsystem. Measure ELF/map section sizes and worst-case battle allocations at each milestone. Original ROM padding is not proof that all addresses can safely grow. The current environment validates compilation/checksum only; emulator and hardware functional tests remain outstanding. Existing CI builds several ROM variants and modern GCC; those were inspected, not run here.
