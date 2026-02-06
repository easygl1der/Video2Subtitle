# video2subs - 离线视频转字幕工具

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个完全离线的视频转字幕工具，支持本地文件和在线视频链接，提供 CLI 和 HTTP API 接口。

## ✨ 特性

- 🔒 **完全离线**：使用 faster-whisper 本地模型，无需任何云服务 API
- 🎯 **多种输入**：支持本地视频/音频文件、直链 URL、YouTube 等视频网站
- 📝 **多格式输出**：自动生成 SRT、JSON、TXT 三种格式字幕
- ⚡ **性能优化**：支持 CPU 和 CUDA GPU 加速
- 🛠️ **双接口**：提供命令行工具和 HTTP API 服务
- 🌍 **多语言支持**：支持中文、英文、日语等多种语言识别
- 🔌 **可扩展设计**：预留接口可添加其他 ASR 服务提供商

## 📦 安装

### 系统依赖

1. **FFmpeg**（必需）

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# 下载: https://ffmpeg.org/download.html
# 并添加到 PATH 环境变量
```

2. **Python 3.10+**

### 安装项目

```bash
# 克隆仓库
git clone https://github.com/yourusername/video2subs.git
cd video2subs

# 安装（推荐使用虚拟环境）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 基础安装
pip install -e .

# 开发安装（包含测试工具）
pip install -e ".[dev]"
```

### 验证安装

```bash
# 检查安装
video2subs --version

# 查看系统信息
video2subs info

# 列出可用模型
video2subs models
```

## 🚀 快速开始

### CLI 使用

#### 基础用法

```bash
# 转写本地视频文件
video2subs transcribe ./video.mp4

# 指定输出目录
video2subs transcribe ./video.mp4 --output ./subtitles

# 指定语言和模型
video2subs transcribe ./video.mp4 --language zh --model small
```

#### 高级用法

```bash
# 使用 GPU 加速（需要 NVIDIA GPU + CUDA）
video2subs transcribe ./video.mp4 --device cuda --model medium

# 启用 VAD（语音活动检测）过滤静音
video2subs transcribe ./video.mp4 --vad

# 从 URL 下载并转写
video2subs transcribe "https://example.com/video.mp4"

# YouTube 视频（需要 yt-dlp）
video2subs transcribe "https://www.youtube.com/watch?v=xxxxx"

# 自定义输出文件名
video2subs transcribe ./video.mp4 --name my_subtitle
```

#### 完整参数说明

```bash
video2subs transcribe [SOURCE] [OPTIONS]

参数:
  SOURCE                  视频/音频文件路径或 URL

选项:
  -o, --output PATH       输出目录（默认: ./output）
  -n, --name TEXT         输出文件基础名（默认: output）
  -m, --model MODEL       Whisper 模型（默认: base）
                          可选: tiny, base, small, medium, large-v2, large-v3
  -l, --language CODE     语言代码（如: en, zh, ja）不指定则自动检测
  -d, --device DEVICE     设备: auto, cpu, cuda（默认: auto）
  --vad                   启用语音活动检测
  --no-ytdlp             禁用 yt-dlp 下载器
  --no-cleanup           保留临时文件
  -v, --verbose          详细日志输出
  --help                 显示帮助信息
```

### HTTP API 使用

#### 启动服务器

```bash
# 使用默认配置启动（端口 8000）
python -m video2subs.server

# 或使用 uvicorn
uvicorn video2subs.server:app --host 0.0.0.0 --port 8000
```

#### API 端点

**1. 转写 URL 视频**

```bash
curl -X POST "http://localhost:8000/transcribe/url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/video.mp4",
    "model": "base",
    "language": "zh"
  }'
```

**2. 上传文件转写**

```bash
curl -X POST "http://localhost:8000/transcribe/file" \
  -F "file=@video.mp4" \
  -F "model=base" \
  -F "language=zh"
```

**3. 转写并下载字幕文件**

```bash
# 下载 SRT 格式
curl -X POST "http://localhost:8000/transcribe/file/download" \
  -F "file=@video.mp4" \
  -F "format=srt" \
  -o output.srt

# 下载 JSON 格式
curl -X POST "http://localhost:8000/transcribe/file/download" \
  -F "file=@video.mp4" \
  -F "format=json" \
  -o output.json
```

**4. 查看可用模型**

```bash
curl http://localhost:8000/models
```

#### API 文档

启动服务器后，访问自动生成的 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📄 输出格式

### SRT 格式示例

```srt
1
00:00:00,000 --> 00:00:02,500
大家好，欢迎观看本期视频。

2
00:00:02,500 --> 00:00:05,000
今天我们要介绍的是字幕生成工具。
```

### JSON 格式示例

```json
{
  "segments": [
    {
      "index": 1,
      "start": 0.0,
      "end": 2.5,
      "text": "大家好，欢迎观看本期视频。",
      "char_len": 13,
      "word_len": 13
    },
    {
      "index": 2,
      "start": 2.5,
      "end": 5.0,
      "text": "今天我们要介绍的是字幕生成工具。",
      "char_len": 17,
      "word_len": 17
    }
  ],
  "metadata": {
    "total_segments": 2,
    "total_duration": 5.0,
    "total_chars": 30
  }
}
```

### TXT 格式示例

```
大家好，欢迎观看本期视频。
今天我们要介绍的是字幕生成工具。
```

## 🎯 模型选择指南

| 模型 | 大小 | 速度 | 准确度 | 显存需求 | 推荐场景 |
|------|------|------|--------|----------|----------|
| tiny | ~75 MB | 最快 | 较低 | ~1 GB | 快速测试、实时预览 |
| base | ~145 MB | 快 | 中等 | ~1 GB | **日常使用（推荐）** |
| small | ~465 MB | 中等 | 良好 | ~2 GB | 平衡性能与质量 |
| medium | ~1.5 GB | 较慢 | 很好 | ~5 GB | 高质量字幕 |
| large-v2 | ~3 GB | 慢 | 最佳 | ~10 GB | 专业级质量 |
| large-v3 | ~3 GB | 慢 | 最佳 | ~10 GB | 最新最佳模型 |

### 性能参考

**CPU (Intel i7-10700K):**
- tiny: ~10x 实时速度
- base: ~5x 实时速度
- small: ~2x 实时速度

**GPU (NVIDIA RTX 3080):**
- tiny: ~50x 实时速度
- base: ~30x 实时速度
- small: ~15x 实时速度
- medium: ~8x 实时速度

## 🔧 配置

### 环境变量

```bash
# 自定义缓存目录
export VIDEO2SUBS_CACHE_DIR=~/.cache/video2subs

# 自定义模型存储目录
export VIDEO2SUBS_MODEL_DIR=~/.cache/video2subs/models

# 自定义临时文件目录
export VIDEO2SUBS_TEMP_DIR=/tmp/video2subs
```

### Python API 使用

```python
from video2subs import transcribe_video

# 基础使用
result = transcribe_video(
    source="./video.mp4",
    output_dir="./output",
    model="base",
    language="zh"
)

# 访问结果
print(f"生成了 {len(result.segments)} 个字幕段落")
print(f"输出文件: {result.output_files}")

# 遍历字幕段落
for segment in result.segments:
    print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
```

## 🧪 测试

```bash
# 运行所有单元测试
pytest tests/

# 运行特定测试
pytest tests/test_exporters.py

# 详细输出
pytest tests/ -v

# 集成测试（需要下载模型，较慢）
pytest tests/test_integration.py -m integration
```

## 🐛 常见问题

### 1. FFmpeg 未安装或找不到

**错误**: `FFmpeg is not installed or not in PATH`

**解决**: 安装 FFmpeg 并确保在 PATH 中：
```bash
# 验证安装
ffmpeg -version
```

### 2. CUDA 相关错误

**错误**: `CUDA out of memory` 或 GPU 相关错误

**解决**:
- 使用更小的模型（如 `tiny` 或 `base`）
- 切换到 CPU 模式：`--device cpu`
- 关闭其他占用 GPU 的程序

### 3. 模型下载缓慢

**原因**: 模型从 Hugging Face 下载

**解决**:
- 使用国内镜像（如配置 HF_ENDPOINT）
- 或手动下载模型到 `~/.cache/huggingface/hub/`

### 4. YouTube 下载失败

**错误**: yt-dlp 相关错误

**解决**:
```bash
# 更新 yt-dlp
pip install --upgrade yt-dlp

# 或禁用 yt-dlp 使用直链下载
video2subs transcribe URL --no-ytdlp
```

### 5. 字幕时间戳不准确

**原因**: 语音节奏、VAD 设置等

**解决**:
- 尝试启用 VAD：`--vad`
- 使用更大的模型提高识别准确度
- 检查原始音频质量

### 6. 识别语言错误

**解决**: 明确指定语言代码
```bash
# 中文
video2subs transcribe video.mp4 --language zh

# 英文
video2subs transcribe video.mp4 --language en

# 日语
video2subs transcribe video.mp4 --language ja
```

## 📚 参考资料

本项目借鉴和参考了以下优秀开源项目：

- [jianchang512/stt](https://github.com/jianchang512/stt) - 离线音视频转字幕工具
- [jianchang512/pyvideotrans](https://github.com/jianchang512/pyvideotrans) - 视频翻译配音工具
- [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) - C++ Whisper 实现
- [OpenAI Whisper](https://github.com/openai/whisper) - 原始 Whisper 模型
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - 高性能 Whisper 实现

## 🔮 后续计划

- [ ] 添加词级时间戳支持（word-level timestamps）
- [ ] 集成更多 ASR 引擎（可选云服务）
- [ ] 支持实时转写（流式输入）
- [ ] 添加字幕后处理（标点优化、断句优化）
- [ ] Web UI 界面
- [ ] Docker 镜像支持
- [ ] 批量处理模式

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发设置

```bash
# 克隆仓库
git clone https://github.com/yourusername/video2subs.git
cd video2subs

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 代码格式化
black src/ tests/

# 代码检查
ruff check src/ tests/
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## ⚠️ 免责声明

1. **遵守法律法规**：使用本工具下载视频时，请遵守相关网站的服务条款和当地法律法规
2. **版权尊重**：请勿用于侵犯他人版权的行为
3. **离线优先**：本项目默认完全离线运行，不会向任何第三方服务发送数据
4. **模型许可**：Whisper 模型遵循其原始许可证，使用前请了解相关限制

## 💡 支持

- GitHub Issues: [提交问题](https://github.com/yourusername/video2subs/issues)
- Discussions: [讨论区](https://github.com/yourusername/video2subs/discussions)

## 🌟 Star History

如果这个项目对你有帮助，欢迎 Star ⭐️

---

**Made with ❤️ for the open source community**
