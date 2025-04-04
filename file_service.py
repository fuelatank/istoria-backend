from fastapi import UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
from datetime import datetime

# 设置音频文件存储目录
UPLOAD_DIR = "audio_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

async def upload_audio(file: UploadFile = File(...)):
    try:
        # 生成唯一文件名（使用时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_{timestamp}.wav"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # 保存上传的文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "status": "success",
            "message": "文件上传成功",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def download_audio(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        file_path,
        media_type="audio/wav",
        filename=filename
    )

# 获取最新上传的音频文件
@app.get("/latest")
async def get_latest_audio():
    try:
        files = os.listdir(UPLOAD_DIR)
        if not files:
            raise HTTPException(status_code=404, detail="没有可用的音频文件")
        
        # 按修改时间排序，获取最新文件
        latest_file = max(
            files,
            key=lambda x: os.path.getmtime(os.path.join(UPLOAD_DIR, x))
        )
        
        return FileResponse(
            os.path.join(UPLOAD_DIR, latest_file),
            media_type="audio/wav",
            filename=latest_file
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取所有音频文件列表
@app.get("/list")
async def list_audio_files():
    try:
        files = os.listdir(UPLOAD_DIR)
        return {
            "files": files,
            "count": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 删除指定音频文件
@app.delete("/delete/{filename}")
async def delete_audio(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    try:
        os.remove(file_path)
        return {"status": "success", "message": f"文件 {filename} 已删除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



