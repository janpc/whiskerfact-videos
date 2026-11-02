# wifi_bands — precision check (2026-11-03)

Sources:
- ASUS: https://asus.com/support/FAQ/1044838
- Linksys: https://support.linksys.com/kb/article/129
- TP-Link: https://www.tp-link.com/it/support/faq/499/
- UChicago Data Science Institute: https://datascience.uchicago.edu/insights/practical-steps-for-improving-your-wi-fi/
- UT Austin (Evans group, IEEE ICC 2011): https://users.ece.utexas.edu/~bevans/papers/2011/microwave/index.html
- Britannica, microwave oven: https://www.britannica.com/topic/microwave-oven
- West Texas A&M (C. Baird): https://www.wtamu.edu/~cbaird/sq/2014/10/15/why-are-the-microwaves-in-a-microwave-oven-tuned-to-water/
- Britannica, hertz: https://www.britannica.com/science/hertz
- Analog Devices glossary: https://www.analog.com/en/resources/glossary/ghz

| # | Script sentence | Source 1 (quote) | Source 2 (quote) | Match |
|---|---|---|---|---|
| 1 | Gigahertz means the radio wave wiggles billions of times per second. | Britannica (hertz): "one hertz is one cycle per second." | Analog Devices: "GHz, short for gigahertz, is a unit of frequency equal to one billion hertz." | yes ("wiggles" = cycles; "billions" for 2.4–5 GHz) |
| 2 | Up close, five gigahertz usually moves more data every second, so big downloads and video calls fly. | ASUS: "2.4GHz can reach further than 5GHz, but the speed is slower than 5GHz." | UChicago DSI: "5 GHZ is good for speed while 2.4 GHz is good for coverage" (higher frequencies can carry more data). | yes ("can", "usually": Linksys notes the band alone does not set max speed) |
| 3 | Higher-frequency waves fade faster, and they have a harder time getting through walls and furniture. | TP-Link: waves "attenuate much faster at higher frequencies." | UChicago DSI: "Lower frequencies are better at penetrating through stuff (walls, furniture, or people)"; ASUS: 5 GHz "harder for it to pass through obstacles". | yes |
| 4 | Two point four usually reaches farther, often all the way to the back bedroom. | Linksys: "The 5 GHz band has a shorter range compared to a 2.4 GHz band." | TP-Link: "the 2.4GHz frequency is able to reach farther than the 5GHz frequency." | yes ("back bedroom" is an illustration) |
| 5 | In most setups, two point four has just three channels that don't overlap. | ASUS: "there are actually only three channels that do not overlap and interfere with each other." | Linksys table: "Three non-overlapping channels" (2.4 GHz). TP-Link: "only three of them non-overlapping". | yes |
| 6 | Five gigahertz has many more of those lanes, often around twenty, depending on your country and router. | Linksys table: "23 non-overlapping channels" (5 GHz). | TP-Link: "5GHz has 23 non-overlapping channels." | yes ("often around twenty", hedged: count varies by country/DFS, as reviewer noted) |
| 7 | Your microwave oven runs at about two point four five gigahertz. | Britannica: "Microwave ovens generate radiation at a frequency of about 2,450 megahertz" | WTAMU (Baird): spectrum peaks "that spanned from 2.40 to 2.50 GHz"; 2.45 GHz "allocated by the FCC". | yes ("about") |
| 8 | Right inside the two point four band. | WTAMU: oven output spans 2.40–2.50 GHz. | UT Austin: microwave ovens are a source of interference for WLANs "operating in the 2.4 GHz band". | yes |
| 9 | The oven's radio noise can make nearby Wi-Fi stutter. | UT Austin: "microwave ovens emit interference that can either prevent an access point from transmitting or cause a dramatic increase in bit errors at the receiver." | UChicago DSI: "microwaves and old, cordless phones can also use that 2.4 GHz band" and interfere with Wi-Fi. | yes ("can") |
| 10 | Bluetooth and old cordless phones share that band too. | Linksys: 2.4 GHz is used by "Bluetooth devices, cordless phones, microwave ovens". | ASUS: "other 2.4GHz devices that are using Bluetooth or wireless connection such as microwaves"; UChicago: "old, cordless phones". | yes |
| 11 | Final score: five gigahertz wins, two to one. | Scoring of the three rounds above (speed 5, range 2.4, crowding 5). | — (tally, not a fact) | yes |
| 12 | My take? Use both: five near the router, two point four for the far rooms. | Opinion ("my take"), follows rows 2–4. UChicago author: 2.4 GHz worked better from the bedroom because 5 GHz "can't make it through the walls". | ASUS: 2.4 reaches further, 5 is faster. | yes (opinion, consistent) |
| 13 | Best plot twist in tech. | Opinion (PERSONALITY.md "his own take"), not a claim. | — | yes |

On-screen titles/labels follow the same wording (e.g. "3 non-overlapping", "20+ channels", "~2.45 GHz").
| 14 | Next time your stream freezes on two point four while the popcorn pops, check the microwave. | Follows rows 7–9 (UT Austin, UChicago). | Limited to 2.4 GHz after review. | yes |

## Independent review
- Round 1 (separate agent, script + URLs only): 5 points (5 GHz channel count by region/DFS; "three" non-overlapping is region-dependent; closing line overgeneralised to 5 GHz; range not guaranteed; speed cause-and-effect). All fixed with hedged wording above; "professional opinion" changed to "my take"; hook says "classic" band (6 GHz exists).
- Round 2: "No open points." Optional tweak ("two point four band") applied.
