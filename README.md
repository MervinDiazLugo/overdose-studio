# Overdose Studio Buenos Aires — website

Static site for GitHub Pages. No build step.

English is the main version at each path; the Spanish copy lives in an `es/` folder beside it
(`es/`, `fugitive-show/es/`, `fugitive-show/presskit/es/`). Change both when editing a page.

- `index.html` — studio home (games, team, about, contact)
- `team.json` — team members; add one object per collaborator:
  `{"name": "...", "role": {"en": "...", "es": "..."}, "photo": "assets/team/name.jpg", "pixel": true, "links": {"Portfolio": "https://..."}}`
  (`pixel` draws the photo with hard pixels, for pixel-art portraits)
- `fugitive-show/` — The Fugitive Show page and presskit (copied from the game repo's `press/sitio`)
- `assets/` — logo, favicon, team photos

## Preview locally

```
python -m http.server 8000
```

Open http://localhost:8000 (opening the file directly blocks loading `team.json`).

## Publish

Push to `main` of the GitHub repo, then Settings → Pages → Deploy from branch → `main` / root.
