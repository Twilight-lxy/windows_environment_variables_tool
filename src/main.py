#!/usr/bin/env python3
"""
环境变量管理器启动脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from env_gui import main
    from admin_utils import is_admin
    
    if __name__ == "__main__":
        print("启动环境变量管理器...")
        print(f"当前权限状态: {'管理员' if is_admin() else '普通用户'}")
        
        if not is_admin():
            print("提示: 以普通用户身份运行，部分功能(系统环境变量)将受限")
            print("可以在GUI中点击'权限状态'按钮以管理员权限重新启动")
        
        main()
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所需的依赖包:")
    print("pip install pyyaml tqdm")
    input("按Enter键退出...")
    sys.exit(1)
except Exception as e:
    print(f"启动失败: {e}")
    input("按Enter键退出...")
    sys.exit(1)
