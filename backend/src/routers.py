import aiofiles
from aiofiles import os
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from src.utils import yolo_processing, yt_download_tmp

router = APIRouter()


# Yolo video processing
@router.post("/video/yolo", tags=["Video"])
async def yolo(file: UploadFile = File(...)):
    if not (file.filename.endswith(".mp4") or file.filename.endswith(".MP4")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="There was an error with the file extension"
        )

    try:
        async with aiofiles.tempfile.NamedTemporaryFile("wb", delete=False) as temp:
            try:
                contents = await file.read()
                await temp.write(contents)
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="There was an error uploading the file"
                )
            finally:
                await file.close()

        res = await yolo_processing(temp.name)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="There was an error processing the file"
        )
    finally:
        await os.remove(temp.name)

    return res


@router.post("/video/yt/yolo", tags=["Video"])
async def yolo_yt(yt_url: str):
    try:
        temp_video = await yt_download_tmp(yt_url)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="There was an error downloading the file from YouTube"
        )

    try:
        res = await yolo_processing(temp_video)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="There was an error processing the file"
        )
    finally:
        await aiofiles.os.remove(temp_video)

    return res
