# Handoff: Scale of Matter Zoom → GitHub Pages

Paste this whole message into the new chat, and attach scale-zoom-handoff.zip.

---

I'm continuing a project built in another Claude chat: **Scale of Matter Zoom**, an interactive 3D
"zoom to view more" model of physics across scales, written in **Three.js r128** as a single static
`index.html` (HTML + CSS + JS + GLSL, about 2,160 lines). I want to publish it on my personal GitHub page
(GitHub Pages) and keep developing it.

The attached zip contains:
- `index.html` — the full, working app (same as the last published version).
- `CLAUDE.md` — the project brief: goals, working rules, architecture, where everything lives in the file,
  what each level does, the physics models used, and the roadmap. **Read it first.**
- `tools/shot.py` — headless Playwright screenshot check of every level (prints page errors).
- `README.md`, `.gitignore`.

What the app covers now:
- Down the scales: weak-force vertex (W boson) → inside a neutron (quarks, gluon flux tube) → carbon-14
  nucleus → carbon-14 atom (orbitals; "measure an electron" collapse + uncertainty principle) → CO₂
  molecule → a cube of air.
- Carbon in a solid: diamond vs graphite lattice → crystal grains → a cut 1-carat diamond with ray-traced light.
- Light: a pulse through air, crown glass and diamond (real refractive-index formulas, Fresnel reflection,
  angle of incidence, s/p polarization, Brewster angle, real element emission lines from H, Na and Hg,
  probability-amplitude view with phase clock, time slider); the correct Ewald–Oseen picture of light
  entering a material; Feynman's sum over paths with a full two-slit experiment (single photons,
  which-slit marking); the photon as a quantum.
- Controls: rotate, zoom, pan (middle mouse, Shift-drag, two fingers), hideable/resizable panels, works on phones.

How I like to work:
- Physics as accurate as possible; every simplification stated on screen in plain language.
- If my idea is a misconception, build the correct model instead and tell me.
- Keep scale and positions consistent with what's already in the scene.
- Check changes with screenshots before calling them done.

First steps for you:
1. Read `CLAUDE.md`.
2. Help me get it onto GitHub Pages (repo setup, Pages settings, a good README with a screenshot,
   page title/description/preview image). Ask me before picking a license.
3. Then continue the roadmap: zoom outward from the gem to everyday scale, Earth, a star, gravity,
   relativity and astrophysics.
