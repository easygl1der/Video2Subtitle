# 🎬 video2subs - 最简单使用指南

## 一句话说明

**将视频自动转成字幕文件，完全离线，一行命令搞定！**

---

## 📦 第一步：安装（只需一次）

```bash
# 1. 克隆项目
git clone https://github.com/easygl1der/Video2Subtitle.git
cd Video2Subtitle

# 2. 安装Python包
pip install -e .

# 3. 安装torch（AI引擎）
pip install torch
```

**系统要求**：
- Python 3.10 或更高
- FFmpeg（视频处理工具）
  - Ubuntu: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: 从 https://ffmpeg.org 下载

---

## 🚀 第二步：使用（超级简单）

### 最基本用法

```bash
# 只需一行命令！
python3 -m video2subs.cli transcribe 你的视频.mp4
```

就这样！程序会自动：
1. ✅ 提取音频
2. ✅ 识别语音
3. ✅ 生成3个字幕文件在 `output/` 文件夹

---

## 📁 生成的文件

转写完成后，在 `output/` 文件夹会看到：

### 1️⃣ output.srt（字幕文件）
```srt
1
00:00:00,000 --> 00:00:05,000
大家好，欢迎观看本期视频。
```
→ 可以直接导入视频编辑软件或播放器使用

### 2️⃣ output.json（详细数据）
```json
{
  "segments": [
    {
      "index": 1,
      "start": 0.0,
      "end": 5.0,
      "text": "大家好，欢迎观看本期视频。",
      "char_len": 13,
      "word_len": 13
    }
  ]
}
```
→ 可以用于程序处理

### 3️⃣ output.txt（纯文本）
```
大家好，欢迎观看本期视频。
```
→ 方便阅读和复制

---

## 💡 进阶用法

### 指定中文视频

```bash
python3 -m video2subs.cli transcribe 视频.mp4 --language zh
```

### 自定义输出位置

```bash
python3 -m video2subs.cli transcribe 视频.mp4 --output ./我的字幕
```

### 使用更准确的模型（更慢但更准）

```bash
python3 -m video2subs.cli transcribe 视频.mp4 --model small
```

模型对比：
- `tiny` - 最快，准确度较低（75MB）
- `base` - **推荐**，速度快准确度好（145MB）⭐
- `small` - 更准确，稍慢（465MB）
- `medium` - 很准确，较慢（1.5GB）
- `large-v3` - 最准确，最慢（3GB）

### GPU加速（如果有NVIDIA显卡）

```bash
python3 -m video2subs.cli transcribe 视频.mp4 --device cuda
```

---

## 🌐 从网上下载视频并转写

```bash
# 支持YouTube等网站
python3 -m video2subs.cli transcribe "https://www.youtube.com/watch?v=xxxxx"

# 或者直接的视频链接
python3 -m video2subs.cli transcribe "https://example.com/video.mp4"
```

---

## 📺 完整例子演示

我刚才运行的实际例子：

```bash
# 命令
python3 -m video2subs.cli transcribe tests/assets/sample_audio.wav \
  --model tiny \
  --output ./demo_output \
  --name demo

# 结果
✓ Transcription completed successfully!
Generated 1 subtitle segments

Output files:
  • SRT: demo_output/demo.srt
  • JSON: demo_output/demo.json
  • TXT: demo_output/demo.txt
```

**生成的字幕内容**：

`demo.srt` 文件：
```srt
1
00:00:00,000 --> 00:00:05,000
Thank you.
```

`demo.json` 文件：
```json
{
  "segments": [
    {
      "index": 1,
      "start": 0.0,
      "end": 5.0,
      "text": "Thank you.",
      "char_len": 10,
      "word_len": 2
    }
  ]
}
```

---

## ❓ 常见问题

### Q1: 第一次运行很慢？
**A:** 正常！首次使用会自动下载模型（约145MB），以后就快了。

### Q2: 报错"FFmpeg not found"？
**A:** 需要安装FFmpeg：
- Ubuntu: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

### Q3: 识别不准确？
**A:** 尝试：
1. 指定语言：`--language zh`（中文）或 `--language en`（英文）
2. 用更大的模型：`--model small` 或 `--model medium`

### Q4: 想要更快的速度？
**A:** 如果有NVIDIA显卡，用GPU：`--device cuda`

---

## 🎯 使用场景

✅ **视频字幕制作** - 自动为视频生成字幕  
✅ **会议记录** - 把录音转成文字  
✅ **课程笔记** - 将讲课视频转成文本  
✅ **内容转录** - 提取视频中的文字内容  

---

## 🆘 需要帮助？

查看完整文档：`README.md`  
快速入门：`QUICKSTART.md`  
提交问题：https://github.com/easygl1der/Video2Subtitle/issues

---

## 🎉 总结

**3步搞定**：
1. 安装项目
2. 运行 `python3 -m video2subs.cli transcribe 你的视频.mp4`
3. 在 `output/` 文件夹找到字幕文件

就是这么简单！🚀
