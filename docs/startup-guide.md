# 启动说明

本文档用于说明本项目的启动方式，并补充飞书接入的配置位置。

## 环境准备

- Python 版本：3.7 ~ 3.12（推荐 3.9）
- 安装依赖：

```bash
pip3 install -r requirements.txt
```

可选依赖（建议安装）：

```bash
pip3 install -r requirements-optional.txt
```

## 配置

复制模板并创建配置文件：

```bash
cp config-template.json config.json
```

在 `config.json` 中填写模型 API Key、通道类型等配置项。

## 启动方式

### 方式一：直接启动

```bash
python3 app.py
```

默认启动 Web 通道，访问：

- http://localhost:9899/chat

### 方式二：使用运行脚本

脚本会引导安装依赖、选择模型与通道并生成 `config.json`：

```bash
./run.sh
```

常用管理命令：

```bash
./run.sh start
./run.sh stop
./run.sh restart
./run.sh status
./run.sh logs
```

### 方式三：Docker

下载 `docker-compose.yml` 并填写环境变量后启动：

```bash
sudo docker compose up -d
```

查看日志：

```bash
sudo docker logs -f chatgpt-on-wechat
```

## 飞书接入配置位置

飞书接入配置写在根目录 `config.json` 中。将 `channel_type` 设置为 `feishu`，并补充以下字段：

```json
{
  "channel_type": "feishu",
  "feishu_app_id": "cli_xxxxx",
  "feishu_app_secret": "your_app_secret",
  "feishu_token": "your_verification_token",
  "feishu_bot_name": "你的机器人名称",
  "feishu_event_mode": "webhook",
  "feishu_port": 9891
}
```

事件接收模式：

- `webhook`：适合生产环境，需要公网 IP 或域名
- `websocket`：适合本地开发，需要安装 `lark-oapi`

更完整的飞书配置说明参考：

- `channel/feishu/README.md`
