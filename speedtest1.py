from fastapi import FastAPI, Request
import speedtest
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

async def perform_download_test():
    loop = asyncio.get_event_loop()
    st = await loop.run_in_executor(None, speedtest.Speedtest)
    await loop.run_in_executor(None, st.get_best_server)

    download_speed = await loop.run_in_executor(None, lambda: st.download() / 1_000_000)  # Convert to Mbps
    return download_speed

async def perform_upload_test():
    loop = asyncio.get_event_loop()
    st = await loop.run_in_executor(None, speedtest.Speedtest)
    await loop.run_in_executor(None, st.get_best_server)

    upload_speed = await loop.run_in_executor(None, lambda: st.upload() / 1_000_000)  # Convert to Mbps
    return upload_speed

@app.get("/")
async def root(req: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": req}
    )

@app.get("/speed")
async def speed():
    download_speed = await perform_download_test()
    upload_speed = await perform_upload_test()
    return {
        "download_speed": f"{download_speed:.2f} Mbps",
        "upload_speed": f"{upload_speed:.2f} Mbps"
    }
