# 🪟 Windows 系统安装和使用指南

## 你遇到的错误

```
ModuleNotFoundError: No module named 'video2subs'
```

**原因**：项目还没有安装，Python找不到这个模块。

---

## ✅ 完整安装步骤（Windows）

### 第1步：安装系统依赖

#### 1.1 检查Python版本（必须3.10+）

打开 **命令提示符**（CMD）或 **PowerShell**：

```cmd
python --version
```

或

```cmd
python3 --version
```

**要求**：Python 3.10 或更高版本

如果版本太低，从这里下载最新版：https://www.python.org/downloads/

---

#### 1.2 安装FFmpeg（必需）

**方法1：使用Chocolatey（推荐）**

如果已安装Chocolatey包管理器：
```cmd
choco install ffmpeg
```

**方法2：手动安装**

1. 下载FFmpeg：https://www.gyan.dev/ffmpeg/builds/
   - 选择 `ffmpeg-release-essentials.zip`
   
2. 解压到：`C:\ffmpeg\`

3. 添加到PATH环境变量：
   - 右键"此电脑" → 属性 → 高级系统设置
   - 环境变量 → 系统变量 → Path → 编辑
   - 新建 → 输入：`C:\ffmpeg\bin`
   - 确定保存

4. 验证安装（重启CMD）：
```cmd
ffmpeg -version
```

---

### 第2步：安装项目

#### 2.1 进入项目目录

```cmd
cd D:\桌面\Video2Subtitle
```

#### 2.2 创建虚拟环境（推荐但可选）

```cmd
python -m venv venv
venv\Scripts\activate
```

**注意**：激活虚拟环境后，命令提示符前面会显示 `(venv)`

#### 2.3 安装项目依赖

```cmd
pip install -e .
```

这会安装所有需要的包，包括：
- faster-whisper（语音识别引擎）
- ffmpeg-python（视频处理）
- fastapi（API服务）
- 等等...

**可能需要几分钟，请耐心等待！**

#### 2.4 安装PyTorch（AI引擎）

**CPU版本**（适合没有NVIDIA显卡的电脑）：
```cmd
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**GPU版本**（如果有NVIDIA显卡，速度更快）：
```cmd
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

### 第3步：验证安装

```cmd
python -m video2subs.cli --version
```

应该显示：
```
video2subs, version 0.1.0
```

如果看到版本号，说明安装成功！✅

---

## 🚀 开始使用

### 基本用法

```cmd
# 转写视频（假设视频在当前目录）
python -m video2subs.cli transcribe "2026-02-07 02-12-41_20260207_02140721.mp4"
```

**注意**：
- Windows上文件名如果有空格，需要加引号
- 首次运行会自动下载模型（约145MB），需要联网

### 指定输出目录

```cmd
python -m video2subs.cli transcribe "你的视频.mp4" --output "D:\字幕输出"
```

### 指定中文语言

```cmd
python -m video2subs.cli transcribe "你的视频.mp4" --language zh
```

### 使用更准确的模型

```cmd
python -m video2subs.cli transcribe "你的视频.mp4" --model small --language zh
```

---

## 🎯 完整示例

假设你的视频文件是：`2026-02-07 02-12-41_20260207_02140721.mp4`

### 最简单的命令

```cmd
python -m video2subs.cli transcribe "2026-02-07 02-12-41_20260207_02140721.mp4"
```

### 推荐命令（中文视频，好的模型）

```cmd
python -m video2subs.cli transcribe "2026-02-07 02-12-41_20260207_02140721.mp4" ^
  --language zh ^
  --model base ^
  --output ".\字幕输出"
```

**注意**：Windows CMD中，多行命令用 `^` 连接。PowerShell用 `` ` ``。

---

## 📁 输出文件位置

默认在 `.\output\` 文件夹，包含3个文件：
- `output.srt` - 字幕文件
- `output.json` - JSON格式
- `output.txt` - 纯文本

---

## ❌ 常见问题解决

### 问题1：`ModuleNotFoundError: No module named 'video2subs'`

**解决**：
```cmd
cd D:\桌面\Video2Subtitle
pip install -e .
```

### 问题2：`pip: command not found`

**解决**：
- 重新安装Python，安装时勾选"Add Python to PATH"
- 或手动添加Python到PATH环境变量

### 问题3：`ffmpeg: command not found`

**解决**：
1. 确认FFmpeg已安装
2. 添加到PATH环境变量
3. 重启CMD窗口

### 问题4：下载模型很慢

**解决**：使用国内镜像
```cmd
set HF_ENDPOINT=https://hf-mirror.com
python -m video2subs.cli transcribe "你的视频.mp4"
```

### 问题5：中文路径报错

**解决**：
- 使用英文路径
- 或用引号包裹路径：`"D:\桌面\Video2Subtitle"`

### 问题6：`No module named 'torch'`

**解决**：
```cmd
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

---

## 🔍 检查清单

安装遇到问题？按顺序检查：

- [ ] Python版本 ≥ 3.10
  ```cmd
  python --version
  ```

- [ ] FFmpeg已安装
  ```cmd
  ffmpeg -version
  ```

- [ ] 在正确的项目目录
  ```cmd
  cd D:\桌面\Video2Subtitle
  dir
  ```
  应该能看到 `pyproject.toml` 文件

- [ ] 已安装项目
  ```cmd
  pip install -e .
  ```

- [ ] 已安装PyTorch
  ```cmd
  pip install torch --index-url https://download.pytorch.org/whl/cpu
  ```

- [ ] 验证安装
  ```cmd
  python -m video2subs.cli --version
  ```

---

## 💡 快捷命令（复制粘贴）

### 完整安装流程

```cmd
REM 1. 进入项目目录
cd D:\桌面\Video2Subtitle

REM 2. 安装项目
pip install -e .

REM 3. 安装PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cpu

REM 4. 验证
python -m video2subs.cli --version

REM 5. 转写视频
python -m video2subs.cli transcribe "你的视频.mp4" --language zh
```

---

## 🎓 PowerShell用户

如果使用PowerShell而不是CMD：

```powershell
# 安装
cd D:\桌面\Video2Subtitle
pip install -e .
pip install torch --index-url https://download.pytorch.org/whl/cpu

# 使用
python -m video2subs.cli transcribe "你的视频.mp4" `
  --language zh `
  --model base `
  --output ".\字幕输出"
```

**注意**：PowerShell多行用 `` ` `` 而不是 `^`

---

## 📞 还是不行？

1. 查看完整错误信息
2. 在GitHub提Issue：https://github.com/easygl1der/Video2Subtitle/issues
3. 提供以下信息：
   - Windows版本
   - Python版本
   - 完整错误日志
   - 执行的命令

---

## ✅ 成功标志

当你看到这样的输出，说明成功了：

```
============================================================
Starting video-to-subtitles transcription
============================================================

[Step 1/4] Getting media file...
[Step 2/4] Extracting audio...
[Step 3/4] Running ASR transcription...
[Step 4/4] Exporting subtitles...

✓ Transcription completed successfully!

Generated 10 subtitle segments

Output files:
  • SRT: output\output.srt
  • JSON: output\output.json
  • TXT: output\output.txt
```

---

**祝使用顺利！** 🎉
