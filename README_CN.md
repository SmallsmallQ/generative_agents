# 生成式智能体系统 (Generative Agents)

这是一个基于大语言模型的生成式智能体模拟系统，可以创建具有自主行为、记忆和社交能力的虚拟智能体。

## 系统架构

- **前端服务器**: Django + Phaser.js 游戏引擎
- **后端服务器**: Python 智能体逻辑处理
- **智能体**: 具有记忆、规划和社交能力的虚拟角色

## 环境要求

- Python 3.9+
- Conda 环境管理器
- 现代浏览器 (Chrome, Firefox, Safari)

## 安装步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd generative_agents
```

### 2. 创建Conda环境
```bash
conda create -n generative_agents python=3.9
conda activate generative_agents
```

### 3. 安装依赖
```bash
# 安装前端依赖
cd environment/frontend_server
pip install -r requirements.txt

# 安装后端依赖
cd ../../reverie/backend_server
pip install -r ../../requirements.txt
```

## 启动系统

### 方法一：自动启动脚本

创建一个启动脚本 `start_system.sh`：

```bash
#!/bin/bash
# 激活conda环境
source ~/anaconda3/etc/profile.d/conda.sh
conda activate generative_agents

# 启动前端服务器
cd environment/frontend_server
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000 &
FRONTEND_PID=$!

# 等待前端启动
sleep 3

# 创建必要的通信文件
echo '{"step": 0}' > temp_storage/curr_step.json

# 启动后端服务器
cd ../../reverie/backend_server
python reverie.py &
BACKEND_PID=$!

echo "系统已启动！"
echo "前端服务器: http://localhost:8000"
echo "前端PID: $FRONTEND_PID"
echo "后端PID: $BACKEND_PID"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
wait
```

### 方法二：手动启动

#### 1. 启动前端服务器
```bash
# 激活环境
conda activate generative_agents

# 进入前端目录
cd environment/frontend_server

# 收集静态文件
python manage.py collectstatic --noinput

# 启动Django服务器
python manage.py runserver 0.0.0.0:8000
```

#### 2. 启动后端服务器
```bash
# 新开一个终端窗口
conda activate generative_agents

# 进入后端目录
cd reverie/backend_server

# 启动后端服务器
python reverie.py
```

#### 3. 创建通信文件
```bash
# 在前端目录下创建必要的通信文件
cd environment/frontend_server
echo '{"step": 0}' > temp_storage/curr_step.json
```

## 访问系统

1. 打开浏览器访问: `http://localhost:8000`
2. 点击 "simulator_home" 进入智能体模拟界面
3. 你将看到三个智能体：Klaus Mueller、Isabella Rodriguez、Maria Lopez

## 调试指南

### 常见问题及解决方案

#### 1. 前端显示 "Please start the backend first"
**原因**: 缺少后端通信文件
**解决**: 
```bash
cd environment/frontend_server
echo '{"step": 0}' > temp_storage/curr_step.json
```

#### 2. 静态文件加载失败
**原因**: 静态文件未收集
**解决**:
```bash
cd environment/frontend_server
python manage.py collectstatic --noinput
```

#### 3. 后端服务器无法启动
**原因**: 缺少必要的配置文件或依赖
**解决**:
```bash
# 检查Python环境
conda activate generative_agents
python --version

# 检查依赖
pip list | grep django
pip list | grep openai
```

#### 4. 智能体不移动
**原因**: 后端服务器未正确响应前端请求
**解决**:
1. 检查后端服务器是否在运行
2. 检查 `temp_storage/curr_step.json` 文件是否存在
3. 查看浏览器控制台是否有JavaScript错误

### 调试命令

#### 检查服务器状态
```bash
# 检查前端服务器
curl -I http://localhost:8000

# 检查后端进程
ps aux | grep "python reverie.py"
ps aux | grep "manage.py runserver"
```

#### 查看日志
```bash
# 前端日志在终端输出
# 后端日志在终端输出

# 检查Django日志
tail -f environment/frontend_server/logs/django.log
```

#### 重置系统
```bash
# 停止所有服务
pkill -f "python reverie.py"
pkill -f "manage.py runserver"

# 清理临时文件
rm -f environment/frontend_server/temp_storage/curr_step.json

# 重新启动
```

## 系统功能

### 智能体能力
- **记忆系统**: 长期记忆、短期记忆、空间记忆
- **规划能力**: 日常计划、任务分解
- **社交互动**: 对话、关系建立
- **环境感知**: 空间导航、对象交互

### 界面功能
- **实时模拟**: 智能体行为实时显示
- **状态查看**: 查看智能体当前状态和记忆
- **交互控制**: 暂停/播放模拟
- **详细视图**: 查看智能体的详细状态信息

## 开发调试

### 修改智能体行为
1. 编辑 `reverie/backend_server/persona/` 目录下的文件
2. 修改 `prompt_template/` 中的提示模板
3. 重启后端服务器

### 修改前端界面
1. 编辑 `environment/frontend_server/templates/` 中的HTML模板
2. 修改 `static_dirs/css/style.css` 样式文件
3. 刷新浏览器页面

### 添加新的智能体
1. 在 `storage/` 目录下创建新的智能体数据
2. 修改前端模板以显示新智能体
3. 更新后端配置

## 故障排除

### 性能问题
- 确保有足够的内存（建议8GB+）
- 检查CPU使用率
- 考虑减少同时运行的智能体数量

### 网络问题
- 检查防火墙设置
- 确保端口8000未被占用
- 检查网络连接

### 数据问题
- 检查 `storage/` 目录下的数据文件
- 验证JSON文件格式
- 确保文件权限正确

## 技术支持

如果遇到问题，请检查：
1. Python版本是否为3.9+
2. 所有依赖是否正确安装
3. 端口8000是否可用
4. 文件权限是否正确

## 许可证

请查看项目根目录的LICENSE文件了解详细信息。
