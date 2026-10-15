# Pokémon with Guns — foundation milestone

This milestone establishes the build and design. Gameplay is still the original FireRed. No weapons, acquisition changes, save migrations, or new quests are implemented. The owner authorized Milestone 0 only; wait for explicit approval before beginning Milestone 1. Final design decisions limit obtainable/encountered/trainer species to the original 151, require eventual progression-scaled enemy guns, distinct rarity-appropriate names, and balance that preserves ordinary moves.

Start with [architecture](ARCHITECTURE.md), [game design](DESIGN.md), [milestones](MILESTONES.md), and the [151-species acquisition checklist](pokedex.csv). The owner's supplied brief ends at `- WA` in the sniper list; later catalog entries and any following requirements were not supplied. Preserve that gap rather than inventing requirements.

## Verified development workflow

Checkout inspected: `Markomatias/pokefirered`, commit `037335f4c725d7c9aecdac87066f2002b4bd7e14`, based on pret's FireRed/LeafGreen decompilation. Use this existing isolated checkout. Do not create a worktree unless explicitly requested.

```sh
source /workspace/.setup/env.sh
cd /workspace/pokefirered
make -j5 compare
```

This built `pokefirered.gba` and reported `pokefirered.gba: OK` (SHA-1 `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`). The complete setup script was rerun successfully. Local Debian packages provide ARM binutils, libpng headers/libraries, and zlib headers. `pret/agbcc` is pinned to `da598c1d918402c42c0c0d7128ba14567f3175e9`; it is installed into ignored `tools/agbcc`. Dependency sources and environment activation live outside the project under `/workspace/.setup`. Installation and startup instructions are also saved in the cloud environment draft. No services or secrets are required.

The baseline checksum verifies compilation and asset generation, not gameplay or emulator compatibility. No emulator playthrough, alternate version build, or modern compiler build has been run. After intentional gameplay edits, use `make -j5` and the relevant milestone tests; a vanilla checksum mismatch will then be expected.

Run the planning audit from any directory:

```sh
python3 /workspace/pokefirered/docs/with-guns/audit_plan.py
```

It checks the checklist against repository species, evolution and encounter data, and checks planned acquisition dependencies. It does not execute scripts, verify story gates, or certify that the game is completable.

## Repository discipline

Keep generated ROMs, save files, external commercial ROMs and imported proprietary assets out of commits. Use original project assets or properly licensed new work. No gameplay source, dependency manifest or existing tracked file was changed for environment setup. These planning documents are the first project additions. Review/save the cloud environment draft and publish through environment settings to retain the prepared environment; publication and restoration in a new task have not been tested here.
