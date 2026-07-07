# ShrimpSend Integration Skill

## Description

ShrimpSend AI设备集成技能。允许AI代理像一台设备一样通过ShrimpSend向其他设备发送文件、文本和剪贴板内容。支持登录、注册设备、列出设备、发送文本和剪贴板内容。

## When to Use

- 当用户说"发送文件到手机"、"通过ShrimpSend发送"、"给手机发消息"、"ShrimpSend"
- 当需要跨设备传输文件、文本或剪贴板内容
- 当需要测试ShrimpSend集成功能
- 当需要从AI代理向手机、平板、电脑发送内容

## Capabilities

- **设备注册**：AI代理作为虚拟设备注册到ShrimpSend
- **文本发送**：向目标设备发送文本消息
- **剪贴板发送**：向目标设备发送剪贴板内容
- **设备列表**：列出所有可用设备
- **文件发送**：发送文件（需要服务器支持）

## Setup

### Prerequisites

1. ShrimpSend账号（https://xiachuan.net）
2. Python 3.8+
3. requests库

### Installation

1. 确保AI客户端库已安装在 `/workspace/projects/shrimpsend/ai-client/`
2. 安装依赖：
   ```bash
   pip install requests
   ```

## Usage

### Quick Start

```bash
# 进入AI客户端目录
cd /workspace/projects/shrimpsend/ai-client

# 登录ShrimpSend
python -m shrimpsend_ai.cli login --server https://api.xiachuan.net --email your@email.com --password yourpassword

# 注册为AI设备
python -m shrimpsend_ai.cli register --name "Omnibot AI Agent" --type AI_AGENT

# 列出所有设备
python -m shrimpsend_ai.cli list-devices

# 发送文本消息
python -m shrimpsend_ai.cli send-text --device "Xiaomi Mi 10 Pro" --text "Hello from AI!"

# 发送剪贴板内容
python -m shrimpsend_ai.cli send-clipboard --device "Xiaomi Mi 10 Pro" --content "Clipboard content" --type "text/plain"
```

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `login` | 登录ShrimpSend | `login --server https://api.xiachuan.net --email user@pass.com --password pass` |
| `register` | 注册AI设备 | `register --name "AI Agent" --type AI_AGENT` |
| `list-devices` | 列出所有设备 | `list-devices` |
| `send-text` | 发送文本消息 | `send-text --device "Phone" --text "Hello"` |
| `send-clipboard` | 发送剪贴板内容 | `send-clipboard --device "Phone" --content "text" --type "text/plain"` |
| `logout` | 登出 | `logout` |

### Python API

```python
from shrimpsend_ai import ShrimpSendClient

# 创建客户端
client = ShrimpSendClient(
    server="https://api.xiachuan.net",
    config_dir="~/.shrimpsend-ai"
)

# 登录
client.login("email", "password", device_id="ai-001")

# 发送文本
client.send_text(target_device="Xiaomi Mi 10 Pro", text="Hello!")

# 发送剪贴板
client.send_clipboard(target_device="Xiaomi Mi 10 Pro", content="text", content_type="text/plain")
```

## Configuration

### Server Addresses

- **国内版**: `https://api.xiachuan.net`
- **国际版**: `https://api.shrimpsend.com`

### Device Types

- `AI_AGENT`: AI代理设备
- `android`: Android设备
- `ios`: iOS设备
- `web`: Web客户端

## Security

- JWT Token存储在 `~/.shrimpsend-ai/auth.json`
- 配置信息存储在 `~/.shrimpsend-ai/config.json`
- 不要在日志中暴露Token

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Login failed | 检查服务器地址、邮箱、密码 |
| Device not found | 确保目标设备在线 |
| Send failed | 检查token是否过期，重新登录 |
| 401 Unauthorized | Token过期，重新登录 |

## Examples

### Example 1: Send message to phone

```bash
cd /workspace/projects/shrimpsend/ai-client
python -m shrimpsend_ai.cli login --server https://api.xiachuan.net --email user@pass.com --password pass
python -m shrimpsend_ai.cli send-text --device "My Phone" --text "Hello from AI!"
```

### Example 2: Send clipboard content

```bash
python -m shrimpsend_ai.cli send-clipboard --device "My Phone" --content "Copied text" --type "text/plain"
```

## Integration with Omnibot

### Method 1: Direct CLI

```bash
# From Omnibot terminal
cd /workspace/projects/shrimpsend/ai-client
python -m shrimpsend_ai.cli send-text --device "My Phone" --text "Message from Omnibot"
```

### Method 2: Python Script

```python
# In Omnibot Python script
import sys
sys.path.insert(0, '/workspace/projects/shrimpsend/ai-client')

from shrimpsend_ai import ShrimpSendClient

client = ShrimpSendClient.from_config()
client.send_text(target_device="My Phone", text="Hello from Omnibot!")
```

## Architecture

```
shrimpsend-integration/
├── SKILL.md                 # 本文件
├── scripts/                 # 辅助脚本
│   └── shrimpsend_cli.sh   # CLI包装脚本
└── examples/                # 示例代码
    └── basic_usage.py
```

## Version

- **Version**: 1.0.0
- **Author**: Omnibot AI Agent
- **License**: AGPL-3.0-or-later

## Support

- **GitHub**: https://github.com/lantianhcgp/shrimpsend
- **Branch**: feature/ai-device-integration
- **Documentation**: See ai-client/README.md