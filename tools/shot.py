"""Headless screenshot check for index.html.
Usage:  python tools/shot.py            (writes shots/*.png, prints page errors)
Needs:  pip install playwright && python -m playwright install chromium
        npm i three@0.128.0   (so the page can load three.js offline; see LOCAL_THREE below)
The page loads three.js r128 from cdnjs. For offline runs this script serves a copy with the
CDN URL swapped for node_modules/three/build/three.min.js.
"""
import asyncio, pathlib, re, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CDN = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
LOCAL_THREE = "node_modules/three/build/three.min.js"

def make_test_copy():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    if (ROOT / LOCAL_THREE).exists():
        src = src.replace(CDN, LOCAL_THREE)
    out = ROOT / "test.html"
    out.write_text(src, encoding="utf-8")
    return out

async def main():
    test = make_test_copy()
    (ROOT / "shots").mkdir(exist_ok=True)
    async with async_playwright() as p:
        # SwiftShader gives WebGL without a GPU; drop these args on a machine with a GPU
        b = await p.chromium.launch(args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--no-sandbox"])
        pg = await b.new_page(viewport={"width": 1280, "height": 800})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(test.as_uri()); await pg.wait_for_timeout(2500)
        await pg.screenshot(path=str(ROOT / "shots/atom.png"))
        # visit every rung on the scale ladder
        for lv in [0, 1, 2, 4, 5, 6, 7, 8, 9, 13, 12, 10, 11]:
            await pg.click(f'.rung[data-level="{lv}"]'); await pg.wait_for_timeout(3500)
            await pg.screenshot(path=str(ROOT / f"shots/level{lv:02d}.png"))
        print("page errors:", errs or "none")
        await b.close()
        sys.exit(1 if errs else 0)

if __name__ == "__main__":
    asyncio.run(main())
