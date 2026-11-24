# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b27-front-page-dense/rank.svg)](https://make.fun/competitions/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b27-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026's world news — front-page style, 31 stories.

**The day:** AI rout hits Asia (Kospi −3.3%), Guterres urges AI rules at the Bridgetown
summit, and the US lead over China hits a record low (Asia Power Index gap 5.3).

**Layout:** masthead + kicker · number strip (10 numbers) · region bar with counts ·
3 hero scenes (drawn illustrations) · 10 story cards · world map with 13 numbered pins ·
ALSO list (18 more) · red DATE CHECK box (what is *not* 23 Nov) · sources + chip legend.

**How it is built:** `draw.py` (PIL) renders `entry.png` (1024×1024, under 1 MiB).
`main.py` is stdlib-only: it parses the PNG header with `struct`, validates size and
format, and copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` — never writing
next to itself, so it works from a read-only copy.

**Chips:** REPORTED = confirmed by wires · CLAIM = one side's claim, not independently
confirmed · ONGOING = still developing.

**Sources:** Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN ·
Lowy Institute (Asia Power Index 2026).
