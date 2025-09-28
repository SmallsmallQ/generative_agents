# CloseAI API 配置说明

本文档说明如何为 Generative Agents 项目配置 CloseAI API。

## 配置步骤

### 1. 已创建的配置文件

项目已经为您配置好了以下文件：

- `reverie/backend_server/utils.py` - 包含 CloseAI API 配置
- `reverie/backend_server/test_api_config.py` - API 连接测试脚本

### 2. API 配置详情

在 `utils.py` 文件中已配置：

```python
# CloseAI API Configuration
openai_api_key = "sk-K5StjduntFAmeSy9RaQZrnL1rXLLFWU31T515VFjYonON6m4"
openai_api_base = "https://api.openai-proxy.org/v1"
```

### 3. 验证配置

运行测试脚本验证配置是否正确：

```bash
cd reverie/backend_server
python test_api_config.py
```

如果看到 "🎉 Configuration is working correctly!" 消息，说明配置成功。

### 4. 安装依赖

如果还未安装依赖，请运行：

```bash
pip install -r requirements.txt
```

### 5. 关于 CloseAI 平台

- **API 地址**: https://api.openai-proxy.org
- **兼容性**: 完全兼容 OpenAI API
- **支持模型**: gpt-3.5-turbo, gpt-4 等
- **特殊支持**: 自动协议转换，支持 Response 接口

### 6. 使用注意事项

1. **API 限流**: 平台有限流机制，请勿高频调用余额查询接口
2. **模型选择**: 建议使用 gpt-3.5-turbo 以控制成本
3. **错误处理**: 如遇到 API 超时，项目会自动重试
4. **成本控制**: 运行仿真可能产生一定费用，建议定期检查使用情况

### 7. 运行仿真

配置完成后，您可以按照 README.md 中的说明运行 Generative Agents 仿真：

1. 启动后端服务器：
```bash
cd reverie/backend_server
python reverie.py
```

2. 启动前端服务器：
```bash
cd environment/frontend_server
python manage.py runserver
```

### 8. 故障排除

如果遇到问题：

1. 检查 API key 是否正确
2. 确认网络连接正常
3. 运行 `python test_api_config.py` 进行诊断
4. 查看控制台错误消息

## API 密钥管理

**重要提醒**：
- 请勿将 API 密钥提交到公共代码仓库
- 建议将 `utils.py` 添加到 `.gitignore` 文件中
- 如需更换 API 密钥，请修改 `utils.py` 文件中的 `openai_api_key` 值