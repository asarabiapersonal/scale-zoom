"""Make the social preview images (Open Graph / README) from index.html.
Usage:  python tools/preview.py      (writes assets/preview.png 1200x630 and assets/screenshot.png 1280x800)
Needs the same setup as tools/shot.py.
"""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from shot import ROOT, make_test_copy

async def main():
    test = make_test_copy()
    (ROOT / "assets").mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--no-sandbox"])
        # README screenshot: the full interface on the atom level
        pg = await b.new_page(viewport={"width": 1280, "height": 800})
        await pg.goto(test.as_uri()); await pg.wait_for_timeout(3000)
        await pg.screenshot(path=str(ROOT / "assets/screenshot.png"))
        await pg.close()
        # Link preview: 1200x630, panels hidden (H hides both side panels)
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        await pg.goto(test.as_uri()); await pg.wait_for_timeout(3000)
        await pg.keyboard.press("h"); await pg.wait_for_timeout(800)
        await pg.screenshot(path=str(ROOT / "assets/preview.png"))
        await b.close()

asyncio.run(main())
