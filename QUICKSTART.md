# video2subs 快速开始指南

## 5分钟上手

### 1. 克隆项目

```bash
git clone https://github.com/easygl1der/Video2Subtitle.git
cd Video2Subtitle
```

### 2. 安装依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装项目
pip install -e .
```

### 3. 安装系统依赖

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
下载 FFmpeg: https://ffmpeg.org/download.html  
并添加到 PATH 环境变量

### 4. 验证安装

```bash
# 检查版本
python3 -m video2subs.cli --version

# 查看可用模型
python3 -m video2subs.cli models

# 查看系统信息
python3 -m video2subs.cli info
```

## 第一次转写

### 使用测试音频

项目已包含测试音频文件：

```bash
# 转写测试音频（使用最小模型快速测试）
python3 -m video2subs.cli transcribe tests/assets/sample_audio.wav \
  --model tiny \
  --output ./my_output

# 查看生成的文件
ls my_output/
# output.srt  output.json  output.txt
```

### 使用自己的视频

```bash
# 基础转写
python3 -m video2subs.cli transcribe ./your_video.mp4

# 指定语言和模型
python3 -m video2subs.cli transcribe ./your_video.mp4 \
  --language zh \
  --model base \
  --output ./subtitles

# 使用GPU加速（需要NVIDIA GPU + CUDA）
python3 -m video2subs.cli transcribe ./your_video.mp4 \
  --device cuda \
  --model small
```

## 使用HTTP API

### 启动服务器

```bash
# 启动服务器（默认端口8000）
python3 -m video2subs.server

# 或使用uvicorn
uvicorn video2subs.server:app --host 0.0.0.0 --port 8000
```

### 访问API文档

在浏览器中打开：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API 测试

```bash
# 上传文件转写
curl -X POST "http://localhost:8000/transcribe/file" \
  -F "file=@your_video.mp4" \
  -F "model=base" \
  -F "language=zh"

# 下载SRT字幕
curl -X POST "http://localhost:8000/transcribe/file/download" \
  -F "file=@your_video.mp4" \
  -F "format=srt" \
  -o output.srt
```

## Python API 使用

创建文件 `my_script.py`:

```python
from video2subs import transcribe_video

# 转写视频
result = transcribe_video(
    source="./video.mp4",
    output_dir="./output",
    model="base",
    language="zh"
)

# 打印结果
print(f"生成了 {len(result.segments)} 个字幕段落")

# 遍历前3个段落
for seg in result.segments[:3]:
    print(f"[{seg.start:.2f}s - {seg.end:.2f}s] {seg.text}")
```

运行：
```bash
python3 my_script.py
```

## 常用命令

### 查看帮助

```bash
# 总体帮助
python3 -m video2subs.cli --help

# 转写命令帮助
python3 -m video2subs.cli transcribe --help
```

### 清理缓存

```bash
# 清理临时文件
python3 -m video2subs.cli cleanup

# 清理所有缓存（包括模型）
python3 -m video2subs.cli cleanup --all
```

## 模型下载说明

首次使用某个模型时，会自动从 Hugging Face 下载：

- **tiny**: ~75 MB
- **base**: ~145 MB（推荐）
- **small**: ~465 MB
- **medium**: ~1.5 GB
- **large-v2/v3**: ~3 GB

模型默认缓存在 `~/.cache/video2subs/models/`

## 性能参考

**Intel i7 CPU + base模型:**
- 1分钟视频 ≈ 12秒处理时间

**NVIDIA RTX 3080 + base模型:**
- 1分钟视频 ≈ 2秒处理时间

## 故障排查

### FFmpeg未找到
```bash
# 验证FFmpeg安装
ffmpeg -version

# 如果未安装，参考上面的安装说明
```

### Python版本过低
```bash
# 检查Python版本（需要3.10+）
python3 --version

# 如果版本过低，请升级Python
```

### 模型下载慢
```bash
# 配置Hugging Face镜像（中国用户）
export HF_ENDPOINT=https://hf-mirror.com

# 或手动下载模型到
# ~/.cache/huggingface/hub/
```

### GPU不可用
```bash
# 检查CUDA是否可用
python3 -c "import torch; print(torch.cuda.is_available())"

# 如果False，使用CPU模式
python3 -m video2subs.cli transcribe video.mp4 --device cpu
```

## 更多示例

查看 `examples/` 目录：
- `basic_usage.py` - Python API示例
- `api_client.py` - HTTP API客户端示例

## 获取帮助

- GitHub Issues: https://github.com/easygl1der/Video2Subtitle/issues
- 完整文档: 查看 README.md

---

**祝使用愉快！** 🎉
