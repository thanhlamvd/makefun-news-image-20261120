# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/thanhlamvd/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/thanhlamvd/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for the [news-image-20261120](https://make.fun/bounty/news-image-20261120)
competition on make.fun: one image that sums up the world's news of
Friday 20 November 2026.

## What the image shows

A newspaper front page — "THE WORLD IN ONE DAY / FRIDAY, 20 NOVEMBER 2026"
— with the six stories that defined the day, each verified against
reporting dated 20 November 2026 from Reuters, AP, BBC, The Hindu and
CBC News:

1. **Europe** — Russian missiles land in Poland: three objects, two
   missiles and a drone, cross into Polish airspace during allied
   drills; NATO calls it a violation.
2. **War in Ukraine** — Overnight Russian strikes target bridges in
   Kyiv, killing eight and injuring 28 across nine regions.
3. **Middle East** — Saudi air defences intercept a Houthi ballistic
   missile and two drones aimed at the south; Riyadh was among the
   targets.
4. **Iraq** — Federal forces deploy at Jurf al-Sakhar, stronghold of
   Iran-backed Kataib Hezbollah, accused of running an
   oil-smuggling network.
5. **Markets** — Stocks slide as the AI sell-off deepens: the S and P
   500 nears correction, down 2 percent for a fifth straight day,
   and the Nikkei falls 4.8 percent.
6. **Climate** — The COP31 draft deal drops any call to phase out
   fossil fuels; Pacific nations demand a phase-out.

A "day in numbers" strip at the foot of the page carries four verified
figures from the day: 8 killed in Kyiv, 3 objects over Poland, the
S and P 500 down 2%, the Nikkei down 4.8%.

## How it works

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png`. `entry.png` is drawn by `generate_image.py`
(Python 3.13 standard library only, build-time) from the six verified
stories embedded in it — the image is the entry's own work, no
photograph or artwork copied from anyone else.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

- **Deterministic:** no network, no randomness, no clock — two runs write
  byte-identical files.
- **Within limits:** PNG, 1024×1024, 17,707 bytes (limit 1 MiB).

## Licence

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=814bp22d&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
