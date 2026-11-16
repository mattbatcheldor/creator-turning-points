# Creator Turning Points

An independent editorial archive by Matthew Batcheldor about moments when creators changed what was possible for creators, platforms or brands.

## Published editions

- Edition 01, Fame first: opens with Jawed Karim’s Me at the Zoo. 2004 to 2025. Fifteen famous moments show that audience attention is easier to document than its commercial effect.

Editions 02 to 07 are in preparation. The Index will open when all seven editions are ready, with 100 cases across the series.

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
