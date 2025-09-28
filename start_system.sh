#!/bin/bash

echo "=== 生成式智能体系统启动脚本 ==="
echo ""

# 检查conda是否安装
if ! command -v conda &> /dev/null; then
    echo "错误: 未找到conda，请先安装Anaconda或Miniconda"
    exit 1
fi

# 激活conda环境
echo "正在激活conda环境..."
source ~/anaconda3/etc/profile.d/conda.sh
conda activate generative_agents

if [ $? -ne 0 ]; then
    echo "错误: 无法激活generative_agents环境，请先创建环境"
    echo "运行: conda create -n generative_agents python=3.9"
    exit 1
fi

echo "环境激活成功！"
echo ""

# 进入项目目录
cd "$(dirname "$0")"

# 启动前端服务器
echo "正在启动前端服务器..."
cd environment/frontend_server

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput > /dev/null 2>&1

# 创建必要的通信文件
echo '{"step": 0}' > temp_storage/curr_step.json

# 启动Django服务器
echo "启动Django服务器在端口8000..."
python manage.py runserver 0.0.0.0:8000 &
FRONTEND_PID=$!

# 等待前端启动
sleep 3

# 启动后端服务器
echo "正在启动后端服务器..."
cd ../../reverie/backend_server
python reverie.py &
BACKEND_PID=$!

echo ""
echo "=== 系统启动完成！ ==="
echo "前端服务器: http://localhost:8000"
echo "前端进程ID: $FRONTEND_PID"
echo "后端进程ID: $BACKEND_PID"
echo ""
echo "请在浏览器中访问: http://localhost:8000"
echo "点击 'simulator_home' 进入智能体模拟界面"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 等待用户中断
trap 'echo ""; echo "正在停止服务..."; kill $FRONTEND_PID $BACKEND_PID 2>/dev/null; echo "服务已停止"; exit 0' INT

# 保持脚本运行
wait
