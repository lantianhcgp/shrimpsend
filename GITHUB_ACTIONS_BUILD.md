# GitHub Actions 构建指南

## ✅ 构建状态

**Workflow**: Build Android APK  
**分支**: feature/ai-device-integration  
**状态**: ⏳ 已排队 (queued)  
**创建时间**: 2026-07-07 12:41:58 (北京时间)

## 🔗 查看构建状态

### 方法1: 直接访问GitHub Actions页面
- **Actions页面**: https://github.com/lantianhcgp/shrimpsend/actions
- **当前Workflow**: https://github.com/lantianhcgp/shrimpsend/actions/workflows/build-android.yml

### 方法2: 使用GitHub API
```bash
curl -s https://api.github.com/repos/lantianhcgp/shrimpsend/actions/runs | jq '.workflow_runs[0] | {status, conclusion}'
```

## ⏱️ 构建流程

### 1. 触发构建
- ✅ 代码推送到 `feature/ai-device-integration` 分支
- ✅ GitHub Actions 自动触发构建

### 2. 构建步骤
1. ** Checkout 代码** - 下载最新代码
2. **Setup Java** - 安装 Java 17
3. **Setup Flutter** - 安装 Flutter 3.24.3
4. **Get dependencies** - 获取 Flutter 依赖
5. **Build APK** - 构建 Android APK
6. **Upload APK** - 上传 APK 到 Artifacts

### 3. 预计时间
- **总时间**: 约 10-15 分钟
- **当前状态**: 已排队，等待运行

## 📥 下载 APK

### 构建成功后
1. 访问 Actions 页面: https://github.com/lantianhcgp/shrimpsend/actions
2. 点击最新的构建运行
3. 在 "Artifacts" 部分下载 `shrimpsend-apk`

### 直接下载链接 (构建成功后)
- **APK文件**: https://github.com/lantianhcgp/shrimpsend/suites/下载链接

## 🔧 故障排除

### 如果构建失败
1. 查看构建日志
2. 检查错误信息
3. 常见问题:
   - Flutter 版本不兼容
   - 依赖冲突
   - Android SDK 问题

### 手动触发构建
1. 访问 Actions 页面
2. 选择 "Build Android APK" workflow
3. 点击 "Run workflow"

## 📱 安装 APK

### 安装步骤
1. 下载 APK 文件
2. 在 Android 设备上安装
3. 允许安装未知来源应用
4. 打开 ShrimpSend 应用

### 首次使用
1. 登录 ShrimpSend 账号
2. 注册为 AI 设备
3. 开始发送文件和内容

## 📊 构建日志

### 查看详细日志
1. 访问 Actions 页面
2. 点击构建运行
3. 查看各个步骤的详细日志

### 常见构建日志位置
- **Flutter 构建日志**: `flutter build apk --release`
- **依赖解析**: `flutter pub get`
- **Java 编译**: Gradle 构建日志

## 🎯 下一步

### 构建成功后
1. ✅ 下载 APK 文件
2. ✅ 安装到 Android 设备
3. ✅ 测试 AI 设备集成功能
4. ✅ 发送文件和内容到其他设备

### 测试功能
```bash
# 使用 Python 客户端
python -m shrimpsend_ai.cli login --server https://xiachuan.net --email your@email.com --password yourpassword
python -m shrimpsend_ai.cli register --name "Omnibot AI Agent"
python -m shrimpsend_ai.cli send-text --device "My Phone" --text "Hello from AI!"
```

## 📞 支持

- **GitHub仓库**: https://github.com/lantianhcgp/shrimpsend
- **Actions页面**: https://github.com/lantianhcgp/shrimpsend/actions
- **Issues**: https://github.com/lantianhcgp/shrimpsend/issues

---

**构建开始时间**: 2026-07-07 12:41:58 (北京时间)  
**预计完成时间**: 2026-07-07 12:55:00 (北京时间)  
**状态**: ⏳ **构建中**