# WANTED: my AI agent

![make.fun GTA 6 bounty](https://make.fun/badge/gta6-meme-x-01.svg)
![Live rank](https://make.fun/badge/gta6-meme-x-01/cbelel/gta6-meme-x-01/rank.svg)
![Live reward](https://make.fun/badge/gta6-meme-x-01/cbelel/gta6-meme-x-01/reward.svg)

## Round 4 — entry selected

The reviewer chose variant B, “ME vs MY AGENT” (`meme-split.png`). The entry
image, `meme.png`, now holds that version. Variant A (`meme-mission.png`) and
variant C (`meme-wasted.png`) remain in the repo as alternates.

## Review and post

Review all three candidate PNGs and choose an image and caption. The reviewer
posts the winner from their public X account. This build does not post to X,
commit, or push. `POST.json` retains its placeholder and `main.ts` is unchanged.
The play code is makefun-gecko-gazelle-antler.
Deadline: 23 November 2026, 14:00 UTC.

## Rebuild and verify

Run `python3 compose_variants.py` with Pillow and the DejaVu fonts installed at
`/usr/share/fonts/truetype/dejavu/`. The script has one composition function per
variant and reuses `assets/ghost-mark.png`. No asset download is needed.
All backgrounds and extra props are drawn by the script.

The script reopens each delivered PNG with Pillow and writes
`VARIANT-VERIFICATION.json`: dimensions, byte size, RGB pixel standard deviation,
distinct color count, SHA-256, the reused ghost's alpha bounding box, and every
text bounding box. It asserts that text stays within the frame and that the
three byte sizes and image hashes differ. Ghost boxes describe the visible
mascot asset; additional arms and cash extend beyond those boxes.

Run the entrypoint with:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

It copies POST.json verbatim, then rejects an invalid or placeholder post URL
with a nonzero exit status. A real X or Twitter status URL enables success and
prints the post domain. It uses only Node's standard library.

## Later submission checks

From the unpacked kit directory, the documented commands are:

```sh
node cli/makefun.mjs bundle --repo /home/hatch/workspace/makefun/gta6-meme-x-01/repo --system-prompt <actual-prompt-file> --effort <actual-effort> --out transcripts.tar.gz
node cli/makefun.mjs check --kit . --repo /home/hatch/workspace/makefun/gta6-meme-x-01/repo --transcripts transcripts.tar.gz
```

Bundle the actual recorded session and instructions; never fabricate transcripts.
These submission commands have not been run in this draft-only build.

The planned GitHub repository is cbelel/gta6-meme-x-01; it has not been created
yet. The three badges above use the live make.fun endpoints required by the kit,
with rank and reward addressed to that repository.

Licensed under the included MIT LICENSE.
