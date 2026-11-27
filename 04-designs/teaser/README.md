# Teaser «من البحر… لوين؟»

A "guess where" teaser for the winter camp. It asks the question that poster v2's tagline answers: «من البحر… لوين؟» → «من البحر… إلى النخيل».

Ready-to-post files are in `../exports/teaser/`:

| File | What it is | Use it for |
| --- | --- | --- |
| `WinterCamp-Teaser-Reel-9x16.mp4` | 15.5 s Reel with its own sound, loops | Instagram/Facebook Reel, TikTok, WhatsApp status |
| `WinterCamp-Teaser-Reel-9x16-silent.mp4` | the same, no sound | when you add a trending song inside Instagram |
| `WinterCamp-Reveal-Reel-9x16.mp4` | 17 s: the same clues, then the stamp «دقاش · توزر», prices and phone | the answer, about two days later |
| `WinterCamp-Reveal-Reel-9x16-silent.mp4` | the same, no sound | as above |
| `WinterCamp-Teaser-Carousel-1…6-4x5.jpg` | the story as six swipeable slides (2160 × 2700) | a feed carousel; slide 1 also works alone |
| `WinterCamp-Teaser-Story-Quiz-9x16.jpg` | «وين مخيمنا هالشتاء؟» with an empty band for the Quiz sticker | Instagram story |

## The story, second by second

| Time | Scene |
| --- | --- |
| 0.0 | Mahdia at night: the lighthouse turning, a fishing boat, the moon. «من البحر...» is on screen from the first frame. |
| 0.5 | «لوين؟» slams in; the screen shakes and a boom hits. «كان يا مكان… في شتاء 2026». |
| 2.1 | The camera tilts down from the sea to a storybook map heading south: beach, Sahel olive groves, steppe, dunes, an oasis with brick houses and water channels. The scout trail (trail-sign arrows, sea blue → amber) draws itself. «نتبعو إشارات الطريق… 4 تلميحات». A «؟» pin drops on the oasis. |
| 4.75 | A page from the scout logbook «كرّاس الرحلة». Four polaroids land one by one, from vague to obvious: palms (a real photo of the camp's palm grove) → «دقلة… اسمها النور» → «طوب يرسم أشكال» → «شطّ ملح… والسراب يلعب». |
| 11.15 | Teaser: «عرفتوها؟ اكتبوها في الكومنتار» with an arrow toward the comment button, a clock ticking. Reveal: the stamp «دقاش · توزر» lands on the pile, then «من البحر… إلى النخيل». |
| 13.1 | End card: logos, «مخيم الشتاء», dates, «الحكاية قريب تبدا…» (teaser) or place, prices and phone (reveal). The last half second fades back into the first frame, so the Reel loops without a seam. |

Why this shape: Instagram ranks Reels on how much of the video people watch and how often they send it to friends, and a question in the first second followed by "4 clues" gives a reason to stay to the end. The comment question gives a reason to type, the scrapbook look is trending, and the loop makes many viewers watch twice.

## Sound

The sound is original, synthesised in `source/sound.py`, so there is no licence problem, even on a business account that has no access to popular music. It has:

- waves at Mahdia;
- a boom on «لوين؟»;
- wind and footsteps while the map scrolls;
- a darbouka rhythm in 6/8 with an oud-like plucked melody in the Hijaz mode, one phrase per clue;
- a riser, then a clock ticking under the question;
- the waves again at the end so the loop flows.

To use a trending song instead, post the `-silent` version and pick the song in Instagram. The clues land every 1.6 s, so a track with a beat around 112 BPM fits them.

## Rebuilding

From `source/`, after `pip install -r requirements.txt` and `playwright install chromium`:

```
python make_teaser.py        # writes _build/teaser.html, the animated page
python render.py check       # key frames as JPGs in _build/check/
python render.py             # both Reels into ../exports/teaser/
python make_stills.py        # carousel + quiz story
```

- To change a word, edit `make_teaser.py` (the HTML at the bottom, and `CLUES` for the captions).
- To change timing, edit `teaser.js`; `sound.py` uses the same times.
- To change the look, edit `teaser.css`.
- Every frame is drawn from its time alone (`seek(t, variant)`), so any one frame can be checked or re-rendered.
