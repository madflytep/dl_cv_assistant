import tempfile
import uuid
import zipfile
from io import BytesIO
from os import path

import aiofiles
from aiofiles import os
from fastapi.responses import StreamingResponse
from pytube import YouTube

from src.yolo import predict_video


async def yolo_processing(file_path: str):
    temp_video = path.join(tempfile.gettempdir(), f"{uuid.uuid1()!s}.webm")
    async with aiofiles.tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_csv:
        await predict_video(file_path, temp_video, temp_csv)

    zip_result = zipfiles(temp_video, temp_csv.name)
    await os.remove(temp_video)
    await os.remove(temp_csv.name)

    return zip_result


def zipfiles(f_video: str, f_csv: str):
    zip_io = BytesIO()
    with zipfile.ZipFile(zip_io, mode="w", compression=zipfile.ZIP_DEFLATED) as temp_zip:
        temp_zip.write(f_video, "video.webm")
        temp_zip.write(f_csv, "data.csv")

    return StreamingResponse(
        iter([zip_io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": "attachment; filename=result.zip"},
    )


async def yt_download_tmp(yt_url: str) -> str:
    yt = YouTube(yt_url)
    video_buffer = BytesIO()
    yt.streams.filter(file_extension="mp4").get_highest_resolution().stream_to_buffer(video_buffer)
    async with aiofiles.tempfile.NamedTemporaryFile("wb", delete=False) as temp:
        await temp.write(video_buffer.getbuffer())

    return temp.name
