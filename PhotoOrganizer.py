import os
import re
import logging
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS
from tqdm import tqdm

def get_exif_date(file_path: Path) -> datetime:
    """从EXIF元数据中提取拍摄日期"""
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    if tag_name == "DateTimeOriginal":
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except (UnidentifiedImageError, AttributeError, ValueError):
        pass
    return None

def organize_photos_with_metadata():
    """自动整理当前路径照片/视频到「已整理」目录"""
    # 初始化日志系统
    logging.basicConfig(
        filename='photo_organizer.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s'
    )
    
    # 配置路径
    source_dir = Path.cwd()
    target_dir = source_dir / "已整理"
    target_dir.mkdir(parents=True, exist_ok=True)

    # 支持的文件类型
    media_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi']
    date_pattern = re.compile(r'(20\d{2})[-/]?(\d{2})[-/]?\d{2}')

    # 获取文件列表并初始化进度条
    files = [f for f in source_dir.glob('*') if f.is_file() and f.suffix.lower() in media_extensions]
    
    with tqdm(total=len(files), desc="整理进度", unit="文件") as pbar:
        for file_path in files:
            try:
                filename = file_path.name
                file_ext = file_path.suffix.lower()

                # 优先从EXIF获取日期
                date_taken = get_exif_date(file_path)
                if date_taken:
                    year, month = date_taken.strftime("%Y"), date_taken.strftime("%m")
                else:
                    # 次选文件名日期匹配
                    match = date_pattern.search(filename)
                    if match:
                        year, month = match.group(1), match.group(2)
                    else:
                        # 最后使用修改时间
                        mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        year, month = mod_time.strftime("%Y"), mod_time.strftime("%m")

                # 构建目标路径
                year_folder = f"{year}年"
                month_folder = f"{month.zfill(2)}月"
                dest_dir = target_dir / year_folder / month_folder
                dest_dir.mkdir(parents=True, exist_ok=True)

                # 处理文件名冲突
                dest_path = dest_dir / filename
                if dest_path.exists():
                    counter = 1
                    while dest_path.exists():
                        new_name = f"{file_path.stem}_{counter}{file_ext}"
                        dest_path = dest_dir / new_name
                        counter += 1

                # 移动文件
                shutil.move(str(file_path), str(dest_path))
                logging.info(f"移动成功: {filename} -> {dest_path.relative_to(target_dir)}")

            except Exception as e:
                logging.error(f"移动失败: {filename} - {str(e)}", exc_info=True)
            
            pbar.update(1)

if __name__ == "__main__":
    try:
        organize_photos_with_metadata()
        print("\n整理完成！日志已保存到 photo_organizer.log")
    except KeyboardInterrupt:
        print("\n操作已取消")
