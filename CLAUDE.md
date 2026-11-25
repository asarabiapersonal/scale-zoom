# Scale of Matter Zoom — project brief for Claude Code

A single-page, zoomable 3D model of physics across scales, written in plain JavaScript with Three.js r128.
You zoom (log scale) from a W boson vertex inside a neutron, out through the nucleus, the carbon-14 atom,
CO₂ and air, into a diamond/graphite crystal, grains and a cut gem, and into a light pulse
travelling through air, glass and diamond. The owner (Adam) wants it **as physically accurate as possible**,
with every simplification stated on screen. Future direction: zoom outward to everyday scale, then
Earth, a star, gravity, relativity and astrophysics.

Published copy (claude.ai artifact): https://claude.ai/artifact/S9ZZEW7xBZtnWYZh6Jjr8z
That copy matches `index.html` here (artifact version 1795134294-fc4d, 19 Nov 2026).

## Publishing
Live at https://asarabiapersonal.github.io/scale-zoom/ (repo `asarabiapersonal/scale-zoom`, GPL-3.0), served by
GitHub Pages from `main`, folder `/`. **Every push to `main` republishes the live site**, so run `tools/shot.py`
first. `tools/preview.py` regenerates `assets/preview.png` (Open Graph image) and `assets/screenshot.png` (README).
The claude.ai artifact above is the older copy from before the astro branch.

## Files
- `index.html` — the whole app (~2,480 lines: HTML, CSS, JS, GLSL in one file). Three.js r128 from cdnjs.
  Earth and Moon maps load from the three.js r128 examples on jsDelivr; plain colors stay if they fail.
- `tools/shot.py` — headless Playwright screenshot run over every level; prints page errors.
- Open `index.html` directly in a browser, or serve the folder (`python -m http.server`).

## Working rules (keep these)
1. **Physics first.** Use real constants and published models. Cite the model in a code comment.
   If the user's idea is a misconception, build the correct model, keep theirs only as a labelled
   "this is NOT what happens" toggle if useful, and say so plainly in the reply. (Done before for
   "photons absorbed and re-emitted atom by atom" → Ewald–Oseen model, and "uncertainty = when vs where"
   → position vs momentum.)
2. **State every simplification** in the level's panel text (`fl`/`pl` notes) or a status line.
3. **Keep scale and position consistent** with existing objects when adding to a level.
4. Plain language in all on-screen text; no jargon without a one-line explanation.
5. After each change: syntax check, screenshot the affected level(s), look at the images, fix overlaps.
   Syntax check: `node -e "const s=require('fs').readFileSync('index.html','utf8');new Function(s.match(/<script>([\s\S]*)<\/script>/)[1])"`
6. Make a backup copy before big edits (`index.vNN.html` was the habit; git is better now).
7. Every `localStorage` access stays inside try/catch.

## Architecture
- **Zoom variable** `z` = log10(view height in metres); `zT` is the target it eases to. Scene units are
  **femtometres** (1 fm = 1e-15 m). Constants: `A0` = Bohr radius in fm (52917.7), `NM` = 1e6 fm.
- **Four branches**, each with its own scene, draw function and label container. `setBranch(b)` switches;
  `zLo()/zHi()` give each branch's zoom range.
  | branch | levels | draw fn | scene |
  |---|---|---|---|
  | `main` | 0 Nucleus, 1 Neutron, 2 Weak vertex, 3 Atom, 4 Molecule, 5 Air | `draw(dt)` | `scene` (+ `volScene` raymarch) |
  | `mat`  | 6 Crystal, 7 Grains, 8 Gem | `drawMat(dt)` | `matScene` |
  | `pho`  | 9 Light pulse, 13 Sum over paths, 12 At the surface, 10 Light in the lattice, 11 Photon quantum | `drawPho(dt)` | `phoScene` |
  | `astro` | 14 In your fingers, 15 Earth, 16 Earth and Moon, 17 The Sun, 18 Inner planets | `drawAstro(dt)` | `astroScene` (**units: metres**) |
- `LEVEL_Z[n]` = default zoom for level n. The ladder (`.rung[data-level=n]`) sets branch + `zT`.
  Inside a draw function, `setLevel(n)` is chosen from `z` (and for pho, pan position and flags).
- **Panel text**: `LEVELS[n]` (main) / `matLevel(n)` / `phoLevel(n)` return `{k,h,p[],eq[],f[],fl,pl,hint,...flags}`.
  `setLevel` builds the left panel from that object; flags like `orb`, `surf`, `paths` add control blocks,
  wired up near the end of `setLevel`.
- **Demo button**: `DEMO[n] = [label, fn]`.
- **Labels**: `mkLabel` (main), `mkLabelM` (mat), `mkLabelP` (pho); positioned each frame with
  `place(el, worldPos, alpha, dxPx, dyPx)`.
- **Raymarched volumes** (QCD vacuum, W field, atomic orbitals, CO₂ orbitals) render to a half-res target
  (`volRT`) and are composited. Orbitals use Clementi–Raimondi Z_eff (1s 5.67, 2s 3.22, 2p 3.14).
- **Camera**: orbit angles `theta`, `phi`; `pan` vector (middle-drag, Shift-drag, two-finger drag; `0`
  or double middle-click / double-tap recenters). Zoom eases `z → zT`.
- **Test hook**: `window.__zoom` (`zto(z)`, `tset(t,speed)`, `elem(e)`, `wrong()`, `astro(lv)`, `asCut(on)`, `asWalk(sec)`,
  `_as` = the astro state, `_cam` = the camera) for automated checks.
- Side panels hide/resize; layout in `localStorage['scaleZoom.panels']`; surface close-up toggle in
  `localStorage['scaleZoom.surface']`.

## Photon branch details (most recent work)
- **Light pulse (9)**: lanes air / crown glass (BK7, Sellmeier) / diamond (Sellmeier, Peter 1923), air via
  Peck & Reeder. Pulse envelope at c/n_g, crests at c/n. Fresnel r,t for s and p at any angle (`phAngles`),
  Snell refraction, Brewster button, lanes spread as angle grows (`phLayout`). Real emitters (H, Na, Hg,
  NIST lines), several at once side by side (`PH.elems`, `toggleElem`). Probability-amplitude view
  (helix, |ψ|², phase clock, detection). Time slider + speed. `PH` holds state; `LANES` the lanes.
- **At the surface (12)**: Ewald–Oseen extinction / Feynman Vol I ch. 31 — electrons sway in phase with the
  field, each wavelet travels at c and lags a quarter cycle, the sum cancels the original wave and builds the
  slow one. Contrast toggle for the wrong absorb/re-emit idea. Placed at true scale just below the lowest
  lane (`sfPlace`), aligned with the lanes' surface. `SF` holds state.
- **Sum over paths (13)**: Feynman QED arrows. One-bend paths through the mid-plane; chain ordered by height
  (Cornu spiral, "nearest neighbours") or by arrival. Opening slider, detector height. **Two-slit mode**:
  slit separation/width, close either slit, "mark which slit" (adds |A|² instead of A), photons sent one at a
  time along their possible paths and landing per |A₁+A₂|², fixed photon list per setting so the time slider
  scrubs both ways. `PP` holds state.
- Wave packets and close-up stay visible until z ≈ −7.9 (a few nm view).

## Atom (3) — latest addition
"Measure one electron": a 2p_y electron's cloud collapses at a spot sampled from |ψ|² (r⁴e^(−Zr/a₀), cos²θ);
packet of width Δx then spreads with Δv = ħ/(2mΔx) (free flight, phase-space sampling), then settles back.
Presets: pin down where (Δx = 3 pm) / how fast (Δx = 160 pm). `MQ` holds state; `updateMeasure`, `mqLabels`.
Known nit: after a sharp measurement the spreading points are faint against the bright cloud.

## Astro branch (14–18) — zooming outward
- Joined to the gem: in `draw()`, the `mat` branch switches to `astro` when z > −1.45 while zooming out, and back
  when z < −1.6 while zooming in. The astro scene redraws the gem (sharing the `GEM` geometry) at its origin.
- Scene units are metres. World frame: ecliptic, +y = ecliptic north, longitude L along (cos L, 0, −sin L).
  The gem is at the origin; Earth's center `AS.CE` lies straight below Greenwich (51.48° N). Near the ground the
  camera's "up" is the local vertical (`AS.Qloc`), blended to ecliptic north between z 7.6 and 8.8 (`AS.Q`).
- Camera target follows the zoom path gem → person → Earth center → Sun (`tgtA` in `drawAstro`); `AS.focus='sun'`
  (rung 17) blends it to the Sun. Between z 3.4 and 7 the view is pulled to look straight down on Greenwich.
- Physics: start date 20 March 2026 12:00 UTC (equinox). Planets from JPL/Standish mean elements (`PLAN`, `kepPos`),
  Moon from the main lunar-theory terms (`moonPos`), Earth tilted 23.44° and turned so it is midday at Greenwich
  (spin then frozen). ISS: 420 km, 51.64°, orbit apex over Greenwich. Sun: limb darkening, cutaway with core
  (< 0.25 R), radiative zone (to 0.713 R), convection zone; "Follow the energy out" draws a random walk.
- Field view: Newtonian g arrows in the screen plane, log length (`astroArrows`). Demos: drop the gem
  (real-time free fall), run time (×300 / ×100,000 / ×2,000,000 by level), energy walk.
- Simplifications are listed in `ASIMPL` (shown on every astro level).

## Roadmap / open items
1. **Relativity and astrophysics** (next): general relativity (Mercury's 43″/century, light bending at the Sun,
   GPS clock rates, curvature), then stars, the galaxy and beyond. Extends the `astro` branch above z ≈ 12.
2. Optional refactor into ES modules (one per branch) once under git; keep behaviour identical and
   re-run `tools/shot.py` on every level before/after.
3. Small polish: label crowding at 80° incidence with all three lanes; brighten measurement points; at 800 px
   height the lowest ladder rungs sit under the panel's resize grip until scrolled.
