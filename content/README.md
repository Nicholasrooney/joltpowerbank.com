# Editing the testimonial and logo conveyors

**Testimonials**: edit `testimonials.json`. Each entry:

```json
{ "quote": "What they said, in their words.", "name": "Mary Byrne", "venue": "The Harbour Bar · Dún Laoghaire" }
```

Delete the `"placeholder": true` entries once you have real quotes. Only use quotes you have permission to publish.

**Logos**: drop venue logo files (`.svg`, `.png`, `.jpg`, `.webp`) into `assets/logos/`. Name the file after the venue (e.g. `the-harbour-bar.png`); that name becomes the alt text. Every file in the folder goes on the conveyor; with none, placeholder tiles show.

Then run `python build.py` from the repo folder to regenerate the pages.
