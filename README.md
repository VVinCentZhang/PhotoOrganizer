# PhotoOrganizer
## 将视频和照片按照年份和月份整理归纳
---
1. 将PhotoOrganizer.py文件放在需要整理的文件夹
2. 使用命令提示符或终端进入所在文件夹(可在当前文件夹的路径栏直接输入```cmd```)
3. 在命令提示符或终端中输入
   ```python
   python PhotoOrganizer.py
   ```
   并按回车健
4. 脚本会自动从EXIF元数据中提取拍摄日期或读取文件名中的日期，并自动整理当前路径照片/视频到「已整理」目录中的对应年/月文件夹中
---
+ 需安装依赖
  ```python
  pip install pillow tqdm
  ```
