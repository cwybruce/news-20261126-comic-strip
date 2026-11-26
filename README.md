# news-20261126-comic-strip

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/cwybruce/news-20261126-comic-strip/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/cwybruce/news-20261126-comic-strip/reward.svg)](https://make.fun/bounty/news-image-20261126)

The day in four frames: the world news of Thursday 26 November 2026 as a newspaper comic strip — a rocket and Mercury for Pakistan's first astronaut flying to Tiangong and BepiColombo's arrival at Mercury, jets over an air base for Ukraine's strike and Kim Jong Un's nuclear call, a gavel and factory for the US judge blocking the birthright citizenship order and the new tariff plans, and a chess board for the Gukesh vs Sindarov Game 2 draw, with a ticker of the day's other headlines below.

## Run it

```sh
python3 main.py
```

This copies the pre-rendered image `entry.png` to `/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR/entry.png` when set). The comic strip was drawn at build time by `draw_comic.py` (Pillow + DejaVu fonts); `main.py` itself is a pure-stdlib copier, so it needs no third-party packages, runs with no network, and is fully deterministic.

Built with [make.fun](https://make.fun/?ref=d5a50dzy) — enter the bounty [here](https://make.fun/bounty/news-image-20261126).
