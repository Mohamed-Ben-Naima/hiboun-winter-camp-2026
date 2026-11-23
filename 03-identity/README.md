# 03 · Identity — هوية فوج هيبون

The visual identity of **فرقة كشافة ومرشدات فوج هيبون** (Hiboun scouts and guides unit, Mahdia region, Tunisian Scouts), built first for the **Winter Camp in Degache, Tozeur — 12, 13 and 14 December 2026**. Use it for every poster, story, reel, video card and document of the camp, and as the base for the group's next events.

Arabic first, French second. Everything here was made for right-to-left layouts.

## The idea: «ليالي الجريد» (Djerid nights)

A cold, starry desert night, and a warm place inside it. Every piece is built from five things the Djerid is known for:

| Motif | Where it comes from | How we use it |
| --- | --- | --- |
| **The arch** (البورطال) | The vaulted passages and doors of Ouled el-Hadef, Tozeur's old quarter, and the palm-wood arch at the camp gate in Degache | The one window every photo is shown through: top corners round to half the width, bottom square, a 20px brick frame and a thin cream rule inside |
| **Brick relief** (الطوب) | Tozeur's yellow fired bricks laid proud and recessed to draw diamonds, chevrons and bands; the kilns are fired with palm fronds | `brick-tile.svg` fills the arch frame; `brick-frieze.svg` (raised diamonds) closes the bottom edge of every format with an amber rule above it |
| **The date palm** (النخلة) | The Djerid literally means "palm fronds"; Degache's oasis lives from Deglet Nour dates | Moonlit silhouettes at the edges (palm-silhouette, 55%), and the palm with three ember dates inside the seal |
| **Stars and crescent** | Clear winter nights; days around 17–19°C, nights near 7°C | The star field over the top of the ground, amber sparkle stars, the amber crescent in the header |
| **The seal** (شارة المخيم) | The scout camp badge | A round ember badge: «مخيم الشتاء» on the top ring, «دقاش · توزر · 2026» on the bottom ring. Goes on every piece, tilted −8° to −10°, overlapping the arch's top corner |

## Voice and copy

- Warm, short, inviting; speak to the scout and reassure the parent. No exclamation marks in a row, no emoji on posters.
- Always «فتية وفتيات» and «كشافة ومرشدات» (the unit includes girls).
- Tunisian month names: جانفي، فيفري، مارس، أفريل، ماي، جوان، جويلية، أوت، سبتمبر، أكتوبر، نوفمبر، ديسمبر. Western digits (12، 2026).
- Dates: «12 · 13 · 14 ديسمبر» on one line, the year and weekdays underneath («2026 · من السبت إلى الإثنين»).
- Prices: «100 د» for members (المنخرطين), «120 د» for non-members (لغير المنخرطين). Correct spelling: المنخرطين (ط, not ض).
- Phone numbers are set inside `dir="ltr"` and grouped 2-3-3: **22 882 867**. In a right-to-left line without it the groups come out reversed.
- Tagline bank (Aref Ruqaa, one per piece): «بين النخيل والنجوم» (current) · «دفء الواحة في ليل الشتاء» · «نار، نخيل ونجوم» · «ليلة في الجريد».

## Colour

Two themes. **Night** is the campaign look; **Day** is the same system on salt cream for documents, certificates and cheap print runs (no dark flood of ink).

| Token | Night | Day | Use |
| --- | --- | --- | --- |
| `surface` | #141833 | #F6EBD7 | Ground |
| `surface-raised` / `sky-glow` | #1A2150 / #2A3470 | #FFF8EC / #EADCC0 | Radial sky glow, centred above the arch |
| `ink` | #F6EBD7 | #141833 | Title and text |
| `ink-muted` | #D9CBB0 | #5A4A3A | Detail lines |
| `accent-text` | #F2B544 | #8A5209 | Tagline, icons |
| `amber` (دقلة النور) | #F2B544 | | Member price sticker, moon, sparkles, frieze rule |
| `ember` (جمر) | #E2552D | | Seal, title shadow, phone disc |
| `brick` / `brick-light` / `brick-mortar` | #C98E4E / #E9C48A / #7A4A22 | | Only inside the brick motifs |
| `cream` (ملح الشط) | #F6EBD7 | | Call pill, arch rule |

Contrast rules: body text 4.5:1 or better on its ground in both themes (every `ink*` and `accent-text` pair passes). Cream on ember is 3.2:1, so it is only for 19px bold or larger (seal ring, big labels); smaller text on red uses `ember-deep`. Never put text directly on a photo without the night gradient (bottom 46% of the arch, night at 95% → 0).

## Typography

Four Google Fonts families, all free (OFL):

- **Lalezar** (`display`) — the title. Two to four words, line-height 1, always with the ember offset shadow.
- **Aref Ruqaa** (`script`) — the tagline only. Short, amber, under the title.
- **Alexandria** (`sans`) — every fact: dates, place, ages, prices, phone. Weights 400–900.
- **Reem Kufi** (`kufi`) — kicker lines and the seal ring. Its square Kufic geometry rhymes with the brick walls.

Scale on a 1080px-wide poster: title 188 · tagline 56 · org 30 · info value 36 · info label 21 · phone 46 · price 48 · kicker 22. On A4 print the same layout is scaled by 0.735 with nothing below 12px.

## Layout: the poster anatomy

Top to bottom, the same order in every format:

1. **Header** — kicker «الكشافة التونسية · جهة المهدية», then the org line; the crescent on the opposite side. Official logos (Tunisian Scouts emblem, unit badge) go in this band once the group confirms it may use them.
2. **The arch** with the hero photo, the seal overlapping its top corner, palm silhouettes behind it at both edges.
3. **Title** overlapping the bottom of the arch by about a quarter of its height, tagline underneath.
4. **Info row** — three equal cells between two hairlines: when (calendar icon), where (pin), who (people). Icon in accent-text, value in info-value, detail in info-label.
5. **Action** — the cream call pill (ember phone disc, «للتسجيل والاستفسار», the number) and the two price stickers (amber filled for members, amber outline for non-members, tilted −6° / +5°).
6. **Brick frieze** across the full bottom edge with a 3px amber rule on top.

| Format | Size | Margins / safe zone |
| --- | --- | --- |
| Feed post (Facebook, Instagram) | 1080 × 1350 | 64px sides |
| Story, WhatsApp status, reel cover | 1080 × 1920 | Keep text between y 150 and y 1700 (top and bottom bars cover the rest) |
| Print | A4, 794 × 1123 px at 96 dpi | 72px design units (≈ 53px) sides; nothing under 12px |
| Video title / end card | 1920 × 1080 | Arch on the left, text block on the right from x 900 |
| Countdown story | 1080 × 1920 | Number of days is the only thing that changes |

## Photography

- Warm and real: the camp's own tents, palm-frond shelters, the fire, the well, lights at night. Grade warm (+4% red, −5% blue), +6% contrast, light grain.
- Phone and WhatsApp photos are small (720px): upscale once with Lanczos, sharpen lightly and add fine grain so the JPEG blocks disappear. Show them inside the arch, not full-bleed, except on the countdown where a night photo sits under a strong night gradient.
- Use only photos of the real place. A desert-quad photo with mountains in the camp's album is not Tozeur scenery: leave it out.
- Children: no identifiable faces of minors without that child's photo consent (the group's own rule). Prefer backs, hands, silhouettes around the fire, tents and landscapes. Do not reuse group photos of other units.

## Video and motion

- Vertical 9:16 first (reels, TikTok, WhatsApp status), 16:9 only for the after-movie and YouTube.
- The hook in the first 1.5 seconds: fire crackling close up, a palm-frond tent at golden hour, or the stars. Then the facts.
- Moves that belong to this identity: the **arch reveal** (the arch mask opens from a thin vertical slit to full width), the **brick wipe** (the frieze rises from the bottom to clear the frame), the **title rise** (Lalezar title slides up 40px while its ember shadow lands 120ms later), slow push-ins on photos. 8–12 frames per cut on beats; nothing spins or bounces.
- Burned-in Arabic subtitles: Alexandria 800, cream, on a night box at 60%, bottom third, max two lines.
- Sound: the place itself (fire, wind in the palms, night insects), the group singing, or music the group has the rights to.
- Always end on the Video-Card (1920 × 1080) or the story artboard for 2–3 seconds with the phone number.
- Shot list for Degache: the gate arch, palm canopy from below, dates hanging, brick walls in Tozeur, the well at night, the fire circle from above (no faces), tents under string lights, sunrise over Chott el-Djerid (the largest salt depression in North Africa, close to Degache), flamingos on the chott if seen.

## Campaign rollout and content ideas

The calendar, posting checklist and the Djerid reference sheet live in `05-promotion/campaign-plan.md`.

## Reusing the identity for the next events

Keep the core: night or day ground, cream type, Lalezar title with ember shadow, the seal shape, the info row, the call pill, the bottom frieze. Swap the regional skin: the photo, the arch shape (for Mahdia events use the Skifa el-Kahla gate), the frieze pattern and the seal ring text. Summer events can move the accent from ember to sea blue, keeping amber.

These tokens also serve as the winter seasonal theme of the group's web platform (Manara).

## Files in this folder

- `tokens.json` — colours (two themes), type, spacing, radius, shadows. The same file as the online design system.
- `motifs/` — `brick-tile.svg`, `brick-frieze.svg`, `palm-a.svg`, `palm-b.svg`, `palm-light.svg`, `stars.svg`, `stars-tall.svg`, `grain.png`. Drawn by `04-designs/source/make_motifs.py`.
- `campaign/` — the seal (1600px) and the title lockup, transparent PNGs for video overlays, stickers and print.
- `fonts/` — Lalezar, Aref Ruqaa, Alexandria and Reem Kufi with their SIL Open Font Licence files (`OFL-*.txt`): free to use, embed and share, not to sell on their own.

Online: the design system with live component previews is at https://claude.ai/artifact/W88aSm1ZaNbKNpw8j7pDQv and the poster canvas at https://claude.ai/artifact/HXtLywx8sxpdkWcysJ8byD.
