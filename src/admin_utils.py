"""
管理员权限检测和获取工具
"""
import ctypes
import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def is_admin():
    """检测当前进程是否具有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(script_path=None):
    """以管理员权限运行当前脚本或指定脚本"""
    if script_path is None:
        script_path = sys.argv[0]
    
    try:
        if is_admin():
            return True
        else:
            # 构建命令行参数
            params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
            
            # 使用ShellExecute以管理员权限重新启动
            result = ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                f'"{script_path}" {params}', 
                None, 
                1
            )
            # 如果ShellExecuteW返回值大于32，表示成功
            return result > 32
    except Exception as e:
        print(f"获取管理员权限失败: {e}")
        return False

def get_current_user():
    """获取当前用户信息"""
    try:
        result = subprocess.run(
            ["whoami"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except:
        return "未知用户"

def get_system_info():
    """获取系统信息"""
    info = {}
    
    # 获取用户信息
    info['user'] = get_current_user()
    
    # 检查管理员权限
    info['is_admin'] = is_admin()
    
    # 获取Python版本和路径
    info['python_version'] = sys.version
    info['python_executable'] = sys.executable
    
    # 获取操作系统信息
    try:
        import platform
        info['os_name'] = platform.system()
        info['os_version'] = platform.version()
        info['architecture'] = platform.architecture()[0]
    except:
        info['os_name'] = "Windows"
        info['os_version'] = "未知版本"
        info['architecture'] = "未知架构"
    
    return info

class AdminDialog:
    """管理员权限对话框"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result = False
        
    def show_admin_dialog(self):
        """显示管理员权限信息对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("管理员权限状态")
        dialog.geometry("400x600")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # 获取系统信息
        sys_info = get_system_info()
        
        # 标题
        title_frame = tk.Frame(dialog, bg='#f0f0f0')
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="系统运行状态", 
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0'
        )
        title_label.pack()
        
        # 管理员权限状态
        admin_frame = tk.Frame(dialog)
        admin_frame.pack(fill=tk.X, padx=10, pady=5)
        
        admin_status = "是" if sys_info['is_admin'] else "否"
        admin_color = "#006600" if sys_info['is_admin'] else "#cc0000"
        
        tk.Label(admin_frame, text="管理员权限:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        admin_label = tk.Label(
            admin_frame, 
            text=admin_status, 
            font=('Arial', 10, 'bold'),
            fg=admin_color
        )
        admin_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 权限说明
        if not sys_info['is_admin']:
            warning_frame = tk.Frame(dialog, bg='#fff2e6')
            warning_frame.pack(fill=tk.X, padx=10, pady=5)
            
            warning_text = tk.Text(
                warning_frame, 
                height=3, 
                wrap=tk.WORD,
                bg='#fff2e6',
                font=('Arial', 9)
            )
            warning_text.pack(fill=tk.X, padx=5, pady=5)
            warning_text.insert('1.0', 
                "⚠️ 警告: 当前未以管理员权限运行\n"
                "• 无法修改系统环境变量\n"
                "• 部分功能可能受限")
            warning_text.config(state=tk.DISABLED)
        
        # 系统信息
        info_frame = tk.LabelFrame(dialog, text="系统信息", font=('Arial', 10, 'bold'))
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        info_text = tk.Text(info_frame, wrap=tk.WORD, font=('Consolas', 9))
        info_scrollbar = tk.Scrollbar(info_frame, orient=tk.VERTICAL, command=info_text.yview)
        info_text.configure(yscrollcommand=info_scrollbar.set)
        
        info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 填充系统信息
        info_content = f"""当前用户: {sys_info['user']}
管理员权限: {'是' if sys_info['is_admin'] else '否'}

操作系统: {sys_info['os_name']} {sys_info['os_version']}
系统架构: {sys_info['architecture']}

Python版本: {sys_info['python_version'].split()[0]}
Python路径: {sys_info['python_executable']}

运行状态:
• 用户环境变量: ✓ 可读写
• 系统环境变量: {'✓ 可读写' if sys_info['is_admin'] else '✗ 只读 (需要管理员权限)'}
"""
        
        info_text.insert('1.0', info_content)
        info_text.config(state=tk.DISABLED)
        
        # 按钮框架
        button_frame = tk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 如果不是管理员，显示获取权限按钮
        if not sys_info['is_admin']:
            def restart_as_admin():
                if messagebox.askyesno(
                    "确认", 
                    "程序将以管理员权限重新启动。\n当前的未保存更改可能会丢失。\n\n是否继续？"
                ):
                    dialog.destroy()
                    self.result = True
                    # 以管理员权限重新启动
                    if run_as_admin():
                        # 如果重启成功，退出当前程序
                        self.parent.quit()
                    else:
                        # 如果重启失败，显示错误信息
                        messagebox.showerror("错误", "无法以管理员权限启动程序")
            
            admin_btn = tk.Button(
                button_frame, 
                text="以管理员权限重新启动", 
                command=restart_as_admin,
                bg='#ff6600',
                fg='white',
                font=('Arial', 10, 'bold'),
                relief=tk.RAISED,
                bd=2
            )
            admin_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 刷新按钮
        def refresh_info():
            dialog.destroy()
            self.show_admin_dialog()
        
        tk.Button(
            button_frame, 
            text="刷新", 
            command=refresh_info
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 关闭按钮
        tk.Button(
            button_frame, 
            text="关闭", 
            command=dialog.destroy
        ).pack(side=tk.RIGHT)
        
        # 等待对话框关闭
        dialog.wait_window()
        return self.result

def show_admin_status(parent_window):
    """显示管理员状态对话框"""
    dialog = AdminDialog(parent_window)
    return dialog.show_admin_dialog()
