# مخيم الشتاء — دقاش، توزر 2026

Winter camp of **فرقة كشافة ومرشدات فوج هيبون** (Hiboun scouts and guides unit, Mahdia region, Tunisian Scouts): brief, photos, visual identity, posters and promotion, in one place.

| | |
| --- | --- |
| **When** | 12 · 13 · 14 ديسمبر 2026 (Saturday → Monday) |
| **Where** | دقاش، توزر — Camping / Espace Badi, Degache oasis |
| **Who** | فتية وفتيات, 12 to 17 years old |
| **Price** | 100 د for members (المنخرطين) · 120 د for non-members (لغير المنخرطين) |
| **Contact** | 22 882 867 |

## Folders

```
01-brief/          the camp information as received, and the corrections applied
02-photos/         campsite photos renamed by content: venue/, tents/, night-and-fire/,
                   graded/ (used in the designs), rejected/, private/ (local only)
03-identity/       the visual identity: brand book, tokens.json, motifs (brick, palms, stars),
                   campaign marks (seal, title lockup), fonts with their licences
04-designs/        exports/ ready to post and print · source/ scripts that rebuild everything
05-promotion/      campaign calendar 24 Nov → 14 Dec, posting checklist, Djerid content ideas
```

Ready to use now: `04-designs/exports/` (feed post, story, A4 PDF, video card, countdown 7 → 1).

## Online versions

- Poster canvas (editable, exports PDF/PNG): https://claude.ai/artifact/HXtLywx8sxpdkWcysJ8byD
- Design system «هوية فوج هيبون»: https://claude.ai/artifact/W88aSm1ZaNbKNpw8j7pDQv

## Still to do

- [ ] Add the official logos (Tunisian Scouts emblem, unit badge) to the poster header once the group confirms it may use them.
- [ ] Decide whether a registration deadline goes on the posts.
- [ ] Collect photo consent before posting any picture of a child from the camp.

## Rebuilding the designs

See `04-designs/source/README.md`. In short: `pip install -r requirements.txt`, `playwright install chromium`, then `python build.py local && python export.py`.

This repository is public. Photos where people can be recognised live in `02-photos/private/`, which is ignored by git and exists only on the group's PC.
