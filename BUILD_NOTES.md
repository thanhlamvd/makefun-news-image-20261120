# Build notes — news-image-20261120 (BUILT, ready for Chrome push + submit)

## Status (07:35, 21/11/2026 Hanoi)

Entry built in the 21/11 daily scan, after the 20 November UTC day ended.
`generate_image.py`, `entry.png`, `main.py` and `README.md` were all
authored fresh in this session (no copies from the 20261119 folder).
Committed on branch main: `aa657552459ed41bdff0abf7a3330620be9eb155`.

## The six verified stories (all reporting dated 20 November 2026)

1. **Europe** — Russian missiles land in Poland: three objects, two
   missiles and a drone, cross into Polish airspace during allied
   drills; NATO calls it a violation. Source: AP, Reuters.
2. **War in Ukraine** — Overnight Russian strikes target bridges in
   Kyiv, killing eight and injuring 28 across nine regions.
   Source: Reuters (Kyiv mayor, prime minister).
3. **Middle East** — Saudi air defences intercept a Houthi ballistic
   missile and two drones aimed at the south; Riyadh was among the
   targets. Source: Reuters, AP.
4. **Iraq** — Federal forces deploy at Jurf al-Sakhar, stronghold of
   Iran-backed Kataib Hezbollah, accused of running an oil-smuggling
   network. Source: Reuters, AP.
5. **Markets** — Stocks slide as the AI sell-off deepens: the S and P
   500 nears correction, down 2 percent for a fifth straight day,
   and the Nikkei falls 4.8 percent. Source: Reuters, AP.
6. **Climate** — The COP31 draft deal drops any call to phase out
   fossil fuels; Pacific nations demand a phase-out.
   Source: The Hindu, CBC News.

Deliberately NOT used: the Shenzhen Trump-Xi-Putin summit and the ICJ
Myanmar genocide ruling — both happened on Thursday 19 November and
were already the lead stories of the 20261119 entry; the brief asks
for 20 November's news. The Houthi strike that damaged Riyadh's PIF
Tower was also 19 November; the 20 November story is the fresh
interception of a missile and two drones.

## Verification (21/11, own tooling only — no kit CLI used)

- `entry.png`: PNG, 1024x1024, 17,554 bytes (limit 1 MiB). Read back
  visually: masthead "THE WORLD IN ONE DAY / FRIDAY, 20 NOVEMBER 2026"
  fully visible, all six cards readable, no text overflow or clipped
  glyphs. A "day in numbers" strip (8 killed in Kyiv, 3 objects over
  Poland, S and P 500 down 2%, Nikkei down 4.8%) fills the foot.
- `python3 main.py` run twice (MAKEFUN_OUTPUT_DIR=/tmp/w1 and
  /tmp/w2): both outputs byte-identical, sha256
  `d08e7739635e188e7c359421445f9e2d1041a3ec5b2c85d8e0a39714f9cc86bb`,
  matching the committed entry.png. (First render sha256
  `60a692c8…` was superseded by a one-line fix to the Kyiv card body:
  dangling "THE MAYOR AND THE PRIME MINISTER SAY." → "OFFICIALS
  SAY."; re-rendered, re-verified, committed as `9849cf1`.)
- `main.py` and `generate_image.py`: Python 3.13 standard library
  only — no network, no clock, no randomness.
- `.makefun/owner.json` verified: wallet
  `BedBMrz1mtuDyj3D8YGBM26xck8tF3puoeL3KVmSaGEy`.

## Bounty (from make.fun API, checked 21/11)

- Slug `news-image-20261120`, "Sum up 20 November's world news in one
  image", $250 prize, top 50 paid, no entry fee. Deadline
  2026-11-22T00:00:00Z = 07:00 Hanoi 22/11/2026. Submission format:
  transcript bundle (not sealed recording). Bounty opened
  2026-11-20T00:00:00Z, so this build is in-window.

## Next step — needs Truong's Chrome

1. Create public repo `makefun-news-image-20261120` under
   thanhlamvd and push HEAD `9849cf1` (3 commits: entry `aa65755`,
   BUILD_NOTES `8b24266`, Kyiv-body fix `9849cf1` — API/git push is
   blocked here, push goes through his Chrome).
2. Submit with the transcript bundle before 07:00 22/11/2026.
