# python3 fastapi 实现的简易网盘，支持流媒体播放

## 已完成

- [x] 文件列表
- [x] 文件上传
- [x] 文件下载
- [x] 流媒体播放
- [x] 下载链接临时密码
- [x] 流媒体播放临时密码
- [x] docker image
- [x] 流媒体网页播放

## 图片

![home](readme_assets/home.png)
![upload](readme_assets/upload.png)
![login](readme_assets/login.png)

## 使用

```yaml
version: "2"

services:
  yunpan:
    image: ghcr.io/dreamhunter2333/yunpan:latest
    container_name: yunpan
    environment:
      - root_path=/data
      - password=admin
      - secret=admin
    volumes:
      - ../data:/data
    ports:
      - "8000:8000"
```

## 开发

```bash
cp .env.example .env
python3 -m venv ./venv
./venv/bin/python3 -m pip install -r requirements.txt
./venv/bin/python3 -m uvicorn main:app
```

```bash
cd front
yarn
yarn serve
```
