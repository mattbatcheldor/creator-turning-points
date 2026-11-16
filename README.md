# Creator Turning Points

An independent editorial archive by Matthew Batcheldor about moments when creators changed what was possible for creators, platforms or brands.

## Published editions

- Edition 01, Fame first: opens with Jawed Karim’s Me at the Zoo. 2004 to 2025. Fifteen famous moments show that audience attention is easier to document than its commercial effect.

- Edition 02, Proof first: opens with Marques Brownlee’s Humane Ai Pin review. 2014 to 2024. The numbers are clearer than the attribution. Thirteen Sales trend cases, one survey and one livestream record show why a measured change still needs a baseline.

- Edition 03, Money first: opens with YouTube’s first partners. 2007 to 2024. The money moved from platforms to fans, then back again.

- Edition 04, Platform first: opens with Twitch Plays Pokémon. 2002 to 2021. Creators show platforms what their formats are for.

- Edition 05, Failure first: opens with the Adpocalypse. 2016 to 2025. Most of the creator economy’s rules were written after a failure.

- Edition 06, Brand first: opens with MrBeast’s Feastables. 2011 to 2024. The creators who lasted owned something besides the audience.

- Edition 07, Edge first: opens with Li Ziqi. 2014 to 2022. The edge invented formats the centre later copied.

- The Index: all 100 cases, six lessons across the editions and the creators who appear more than once.

Editions 03 to 07 and The Index were published from Claude’s drafts on 16 November 2026 without the media verification step. Their cases show platform tiles until credited stills and screening films are added. See NOT_VERIFIED.md.

## Build and check

```sh
python3 src/build.py
python3 src/audit.py
```

Publish the generated files from the main branch and repository root using GitHub Pages. The root index.html is Edition 01. The edition-01/ address forwards to it.

## Working together

GitHub main is the published source of truth. Claude drafts the next edition’s case JSON and page template. ChatGPT verifies its sources and media, adds credited 800 by 450 WebP thumbnails and four screening selections, builds and audits the edition, then integrates it. Import only the new edition’s files. Shared engine, styling and scripts are integrated in GitHub to avoid overwriting published work.

Each edition uses src/campaigns-NN.json, src/page-template-NN.html and assets/edition-NN/. Before drafting, use the current main branch and check earlier editions and both sister archives for repeated stories. Mark unverified evidence and substituted media explicitly.

## Companion archives

- [Brand Turning Points](https://mattbatcheldor.github.io/brand-turning-points/)
- [Partnership Turning Points](https://mattbatcheldor.github.io/partnership-turning-points/)

See AUDIT.md and NOT_VERIFIED.md for verification limits. Images retain their owners’ credits.
