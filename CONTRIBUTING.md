# 贡献指南

感谢你对 video2subs 项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告问题

如果你发现了 bug 或有功能建议：

1. 检查 [Issues](https://github.com/yourusername/video2subs/issues) 确保问题未被报告
2. 创建新 Issue，包含：
   - 清晰的标题和描述
   - 重现步骤（如果是 bug）
   - 预期行为和实际行为
   - 环境信息（操作系统、Python 版本等）
   - 相关日志或截图

### 提交代码

1. **Fork 项目**

```bash
# 克隆你的 fork
git clone https://github.com/yourusername/video2subs.git
cd video2subs
```

2. **创建分支**

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

3. **开发环境设置**

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"
```

4. **编写代码**

- 遵循项目代码风格
- 添加必要的测试
- 更新文档（如果需要）

5. **运行测试**

```bash
# 运行所有测试
pytest tests/

# 代码格式化
black src/ tests/

# 代码检查
ruff check src/ tests/
```

6. **提交更改**

```bash
git add .
git commit -m "feat: add new feature"  # 或 "fix: fix bug"
```

提交信息格式：
- `feat:` 新功能
- `fix:` bug 修复
- `docs:` 文档更新
- `test:` 测试相关
- `refactor:` 代码重构
- `perf:` 性能优化
- `chore:` 其他修改

7. **推送并创建 PR**

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

### 代码规范

- **Python 版本**: 支持 Python 3.10+
- **代码风格**: 使用 Black 格式化，每行最多 100 字符
- **类型提示**: 尽可能使用类型注解
- **文档字符串**: 使用 Google 风格的 docstring
- **测试**: 新功能必须包含测试

### 测试指南

```bash
# 运行特定测试
pytest tests/test_exporters.py

# 查看覆盖率
pytest --cov=video2subs tests/

# 详细输出
pytest -v tests/
```

### 文档贡献

文档改进同样重要！

- README.md: 主要文档
- API 文档: 代码中的 docstring
- 示例: examples/ 目录

## 行为准则

- 尊重所有贡献者
- 使用友好、专业的语言
- 接受建设性批评
- 专注于对项目最有利的事情

## 需要帮助？

- 查看 [Issues](https://github.com/yourusername/video2subs/issues) 中标记为 `good first issue` 的问题
- 在 [Discussions](https://github.com/yourusername/video2subs/discussions) 提问
- 查看现有代码和测试作为参考

## 许可

提交代码即表示你同意将贡献以 MIT 许可证开源。

感谢你的贡献！ 🎉
