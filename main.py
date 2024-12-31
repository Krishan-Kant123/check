from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)

@app.get("/")
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://wallpaper.mob.org/best/1/")
        content = await page.content()
        await browser.close()

        list = []
        soup = BeautifulSoup(content, "html.parser")
        gallery = soup.find("div", class_="image-gallery__items")
        if gallery:
            img_tags = gallery.find_all("img", class_="image-gallery-image__image")
            for img in img_tags:
                img_src = img.get("src") or img.get("data-src")
                if img_src:
                    list.append(img_src)
        return list
