# news-image-20261119-0xdemon

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/DemonDeployer/news-image-20261119-0xdemon/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/DemonDeployer/news-image-20261119-0xdemon/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up Thursday 19 November 2026's world news: the first-ever Trump–Xi–Putin trilateral summit in Shenzhen, GTA VI launching worldwide after 13 years, Iran widening the Gulf war to Kuwait and Bahrain, a third Ukrainian strike on the Crimean Bridge, the ICJ ruling Myanmar committed genocide against the Rohingya, and Anthropic's record $81.3B IPO — six verified stories, dated and labelled, in a single front-page composition. The footer ticker adds the Van Gogh record sale and the COP31 talks in Antalya.

`main.py` renders `entry.png` (1024×1024, Pillow only, no network) from the six stories fixed in the script, so the image is byte-identical on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Sources (19 November 2026)

- Trump–Xi–Putin trilateral summit, Shenzhen — BBC News / CBS News / Japan Times (via One Turn); Dawn; NDTV
- GTA VI launch — USA Today, Le Monde, BusinessWorld
- Iran attacks on Kuwait and Bahrain; Strait of Hormuz — The Wall Street Journal (via Hansen Intel Report); IEA
- Third strike on the Crimean Bridge — AP News (via Hansen Intel Report); BBC
- ICJ: Myanmar committed genocide against the Rohingya — Reuters; The Guardian; Al Jazeera
- Anthropic $81.3B IPO — Inshorts; News Media House
- Van Gogh $190.4M record; COP31 Antalya — Horizon

---

<sub>Entered on [make.fun](https://make.fun/?ref=qamf9tkx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
