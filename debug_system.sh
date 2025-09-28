#!/bin/bash

echo "=== 生成式智能体系统调试工具 ==="
echo ""

# 检查conda环境
echo "1. 检查conda环境..."
if command -v conda &> /dev/null; then
    echo "✓ Conda已安装"
    conda info --envs | grep generative_agents > /dev/null
    if [ $? -eq 0 ]; then
        echo "✓ generative_agents环境存在"
    else
        echo "✗ generative_agents环境不存在"
        echo "请运行: conda create -n generative_agents python=3.9"
        exit 1
    fi
else
    echo "✗ Conda未安装"
    exit 1
fi

# 激活环境
source ~/anaconda3/etc/profile.d/conda.sh
conda activate generative_agents

# 检查Python版本
echo ""
echo "2. 检查Python版本..."
python --version

# 检查依赖
echo ""
echo "3. 检查关键依赖..."
python -c "import django; print('✓ Django版本:', django.get_version())" 2>/dev/null || echo "✗ Django未安装"
python -c "import openai; print('✓ OpenAI版本:', openai.__version__)" 2>/dev/null || echo "✗ OpenAI未安装"

# 检查端口占用
echo ""
echo "4. 检查端口8000..."
if lsof -i :8000 > /dev/null 2>&1; then
    echo "✗ 端口8000已被占用"
    echo "占用进程:"
    lsof -i :8000
    echo ""
    echo "是否要停止占用进程? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        pkill -f "manage.py runserver"
        pkill -f "python reverie.py"
        echo "已停止相关进程"
    fi
else
    echo "✓ 端口8000可用"
fi

# 检查文件结构
echo ""
echo "5. 检查项目文件结构..."
if [ -d "environment/frontend_server" ]; then
    echo "✓ 前端目录存在"
else
    echo "✗ 前端目录不存在"
fi

if [ -d "reverie/backend_server" ]; then
    echo "✓ 后端目录存在"
else
    echo "✗ 后端目录不存在"
fi

# 检查通信文件
echo ""
echo "6. 检查通信文件..."
if [ -f "environment/frontend_server/temp_storage/curr_step.json" ]; then
    echo "✓ curr_step.json存在"
else
    echo "✗ curr_step.json不存在，正在创建..."
    echo '{"step": 0}' > environment/frontend_server/temp_storage/curr_step.json
    echo "✓ 已创建curr_step.json"
fi

# 检查静态文件
echo ""
echo "7. 检查静态文件..."
if [ -d "environment/frontend_server/static_root" ]; then
    echo "✓ 静态文件已收集"
else
    echo "✗ 静态文件未收集，正在收集..."
    cd environment/frontend_server
    python manage.py collectstatic --noinput
    echo "✓ 静态文件收集完成"
    cd ../..
fi

# 测试服务器连接
echo ""
echo "8. 测试服务器连接..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200"; then
    echo "✓ 前端服务器正在运行"
else
    echo "✗ 前端服务器未运行"
fi

# 检查后端进程
echo ""
echo "9. 检查后端进程..."
if pgrep -f "python reverie.py" > /dev/null; then
    echo "✓ 后端服务器正在运行"
else
    echo "✗ 后端服务器未运行"
fi

echo ""
echo "=== 调试完成 ==="
echo ""
echo "如果所有检查都通过，请运行: ./start_system.sh"
echo "如果仍有问题，请查看README_CN.md中的故障排除部分"
