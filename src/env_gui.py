import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime
from env_utils import get_all_env_list, set_env_to_system, delete_env_vars
from yaml_utils import save_env_to_yaml, get_env_from_yaml
from admin_utils import is_admin, show_admin_status, get_current_user
import threading
import os
import base64
import tempfile

# 硬编码的图标数据（base64编码）
ICON_DATA = """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"""

class EnvironmentVariableGUI:
    def __init__(self, root):
        self.root = root
        
        # 检查管理员权限并设置标题
        self.is_admin = is_admin()
        admin_suffix = " [管理员]" if self.is_admin else " [普通用户]"
        self.root.title(f"环境变量管理器{admin_suffix}")
        self.root.geometry("1200x800")

        self.root.iconphoto(True, tk.PhotoImage(data=ICON_DATA))

        # 环境变量数据
        self.env_data = []          # 当前编辑的数据
        self.system_env_data = []   # 系统实际数据
        self.filtered_data = []
        
        # 差异状态字典 - 用于跟踪每个变量的状态
        self.diff_status = {}  # {(name, scope): 'added'|'removed'|'modified'|'same'}
        
        # 创建界面
        self.create_widgets()
        
        # 配置差异颜色
        self.configure_diff_colors()
        
        # 绑定事件
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Double-1>', self.on_tree_double_click)
        
    def configure_diff_colors(self):
        """配置差异显示的颜色"""
        # 创建标签用于不同的差异状态
        self.tree.tag_configure('added', background='#e6ffe6', foreground='#006600')      # 浅绿色 - 新增
        self.tree.tag_configure('removed', background='#ffe6e6', foreground='#cc0000')    # 浅红色 - 删除
        self.tree.tag_configure('modified', background='#fff2e6', foreground='#cc6600')   # 浅橙色 - 修改
        self.tree.tag_configure('same', background='#ffffff', foreground='#000000')       # 白色 - 相同
        
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建顶部按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 左侧功能按钮组
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side=tk.LEFT)
        
        # 环境变量读取按钮
        ttk.Button(left_buttons, text="读取当前环境变量", command=self.load_and_compare_env_vars).pack(side=tk.LEFT, padx=(0, 15))
        
        # 选中变量操作组
        selected_group = ttk.Frame(left_buttons)
        selected_group.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(selected_group, text="写入选中变量", command=self.write_selected_env).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(selected_group, text="变更选中变量", command=self.modify_selected_env).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(selected_group, text="删除选中变量", command=self.delete_selected_env).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(selected_group, text="应用所有修改", command=self.apply_all_changes).pack(side=tk.LEFT, padx=(0, 0))
        
        # 备份操作组
        backup_group = ttk.Frame(left_buttons)
        backup_group.pack(side=tk.LEFT)
        
        ttk.Button(backup_group, text="备份环境变量", command=self.backup_env_vars).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(backup_group, text="导入备份", command=self.import_backup).pack(side=tk.LEFT)
        
        # 管理员权限状态和按钮
        admin_frame = ttk.Frame(button_frame)
        admin_frame.pack(side=tk.RIGHT)
        
        # 显示权限状态
        admin_text = "管理员" if self.is_admin else "普通用户"
        admin_color = "#006600" if self.is_admin else "#cc6600"
        
        self.admin_label = tk.Label(
            admin_frame, 
            text=f"权限: {admin_text}", 
            fg=admin_color,
            font=('Arial', 9, 'bold')
        )
        self.admin_label.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(admin_frame, text="权限状态", command=self.show_admin_status).pack(side=tk.LEFT)
        
        # 搜索框架
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_tree)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # 差异状态图例
        legend_frame = ttk.Frame(search_frame)
        legend_frame.pack(side=tk.RIGHT)
        
        ttk.Label(legend_frame, text="图例:", font=('Arial', 8)).pack(side=tk.LEFT, padx=(10, 5))
        
        # 创建小色块来显示图例
        added_label = tk.Label(legend_frame, text=" 新增 ", bg='#e6ffe6', fg='#006600', font=('Arial', 8))
        added_label.pack(side=tk.LEFT, padx=2)
        
        modified_label = tk.Label(legend_frame, text=" 修改 ", bg='#fff2e6', fg='#cc6600', font=('Arial', 8))
        modified_label.pack(side=tk.LEFT, padx=2)
        
        removed_label = tk.Label(legend_frame, text=" 删除 ", bg='#ffe6e6', fg='#cc0000', font=('Arial', 8))
        removed_label.pack(side=tk.LEFT, padx=2)
        
        # 创建主要内容框架
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧树形控件框架
        tree_frame = ttk.Frame(content_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 创建树形控件
        self.tree = ttk.Treeview(tree_frame, columns=('value', 'kind', 'scope'), show='tree headings')
        self.tree.heading('#0', text='变量名')
        self.tree.heading('value', text='值')
        self.tree.heading('kind', text='类型')
        self.tree.heading('scope', text='作用域')
        
        # 设置列宽
        self.tree.column('#0', width=200)
        self.tree.column('value', width=300)
        self.tree.column('kind', width=100)
        self.tree.column('scope', width=100)
        
        # 添加滚动条
        tree_scrollbar_v = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scrollbar_h = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scrollbar_v.set, xscrollcommand=tree_scrollbar_h.set)
        
        # 布局树形控件和滚动条
        self.tree.grid(row=0, column=0, sticky='nsew')
        tree_scrollbar_v.grid(row=0, column=1, sticky='ns')
        tree_scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # 右侧编辑框架
        edit_frame = ttk.LabelFrame(content_frame, text="编辑环境变量")
        edit_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        edit_frame.configure(width=400)
        edit_frame.pack_propagate(False)
        
        # 变量名输入
        ttk.Label(edit_frame, text="变量名:").pack(anchor=tk.W, padx=5, pady=(5, 0))
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(edit_frame, textvariable=self.name_var, width=50)
        self.name_entry.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # 变量值输入
        ttk.Label(edit_frame, text="变量值:").pack(anchor=tk.W, padx=5)
        self.value_text = tk.Text(edit_frame, height=10, width=50)
        self.value_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # 值的滚动条
        value_scrollbar = ttk.Scrollbar(edit_frame, orient=tk.VERTICAL, command=self.value_text.yview)
        self.value_text.configure(yscrollcommand=value_scrollbar.set)
        
        # 变量类型
        ttk.Label(edit_frame, text="类型:").pack(anchor=tk.W, padx=5)
        self.kind_var = tk.StringVar()
        kind_combo = ttk.Combobox(edit_frame, textvariable=self.kind_var, values=['String', 'ExpandString'], state='readonly')
        kind_combo.pack(fill=tk.X, padx=5, pady=(0, 5))
        kind_combo.set('String')
        
        # 作用域
        ttk.Label(edit_frame, text="作用域:").pack(anchor=tk.W, padx=5)
        self.scope_var = tk.StringVar()
        scope_combo = ttk.Combobox(edit_frame, textvariable=self.scope_var, values=['User', 'Machine'], state='readonly')
        scope_combo.pack(fill=tk.X, padx=5, pady=(0, 5))
        scope_combo.set('User')

        # 分号分隔值显示框架
        separator_frame = ttk.LabelFrame(edit_frame, text="分号分隔的值")
        separator_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 分隔值列表
        self.separator_listbox = tk.Listbox(separator_frame, height=8)
        self.separator_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 分隔值滚动条
        sep_scrollbar = ttk.Scrollbar(separator_frame, orient=tk.VERTICAL, command=self.separator_listbox.yview)
        sep_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.separator_listbox.configure(yscrollcommand=sep_scrollbar.set)
        
        # 分隔值操作按钮
        sep_button_frame = ttk.Frame(edit_frame)
        sep_button_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        ttk.Button(sep_button_frame, text="添加项", command=self.add_separator_item).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(sep_button_frame, text="删除项", command=self.delete_separator_item).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(sep_button_frame, text="编辑项", command=self.edit_separator_item).pack(side=tk.LEFT)
        
        # 编辑操作按钮
        edit_button_frame = ttk.Frame(edit_frame)
        edit_button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(edit_button_frame, text="保存修改", command=self.save_changes).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(edit_button_frame, text="取消", command=self.cancel_edit).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(edit_button_frame, text="新建空白模板", command=self.new_variable).pack(side=tk.LEFT)
        
        # 状态栏
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 用户信息标签
        user_info = get_current_user()
        self.user_label = ttk.Label(status_frame, text=f"用户: {user_info}", relief=tk.SUNKEN, anchor=tk.E)
        self.user_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 绑定文本变化事件
        self.value_text.bind('<KeyRelease>', self.on_value_text_change)
        
        # 添加右键菜单显示差异详情
        self.create_context_menu()
        
    def create_context_menu(self):
        """创建右键上下文菜单"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="查看差异详情", command=self.show_diff_details)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="恢复系统值", command=self.restore_system_value)
        
        # 绑定右键事件
        self.tree.bind("<Button-3>", self.show_context_menu)  # Windows右键
        self.tree.bind("<Control-Button-1>", self.show_context_menu)  # Mac右键
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        # 选择点击的项
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            
            # 检查是否是环境变量项
            parent = self.tree.parent(item)
            if parent:  # 有父节点，说明是具体的环境变量
                try:
                    self.context_menu.tk_popup(event.x_root, event.y_root)
                finally:
                    self.context_menu.grab_release()
    
    def show_diff_details(self):
        """显示选中变量的差异详情"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        parent = self.tree.parent(item)
        if not parent:  # 不是具体的环境变量
            return
        
        name = self.tree.item(item, 'text')
        values = self.tree.item(item, 'values')
        if len(values) < 3:
            return
        
        current_value, current_kind, scope = values[0], values[1], values[2]
        key = (name, scope)
        diff_status = self.diff_status.get(key, 'same')
        
        # 创建差异详情对话框
        dialog = tk.Toplevel(self.root)
        dialog.title(f"差异详情 - {name}")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 状态显示
        status_frame = ttk.Frame(dialog)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        status_colors = {
            'added': ('#e6ffe6', '#006600', '新增到系统'),
            'removed': ('#ffe6e6', '#cc0000', '从系统删除'),
            'modified': ('#fff2e6', '#cc6600', '与系统不同'),
            'same': ('#ffffff', '#000000', '与系统相同')
        }
        
        bg_color, fg_color, status_text = status_colors.get(diff_status, ('#ffffff', '#000000', '未知状态'))
        
        status_label = tk.Label(status_frame, text=f"状态: {status_text}", 
                               bg=bg_color, fg=fg_color, font=('Arial', 10, 'bold'))
        status_label.pack(fill=tk.X, pady=5)
        
        # 当前值
        ttk.Label(dialog, text="当前值:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=(5, 0))
        current_text = tk.Text(dialog, height=8, wrap=tk.WORD)
        current_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        current_text.insert('1.0', current_value)
        current_text.config(state=tk.DISABLED)
        
        # 系统值（如果存在差异）
        if diff_status in ['modified', 'removed']:
            # 查找系统中的值
            system_value = None
            system_kind = None
            for env in self.system_env_data:
                if env[0] == name and env[3] == scope:
                    system_value = env[1]
                    system_kind = env[2]
                    break
            
            if system_value is not None:
                ttk.Label(dialog, text="系统值:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=(5, 0))
                system_text = tk.Text(dialog, height=8, wrap=tk.WORD)
                system_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                system_text.insert('1.0', system_value)
                system_text.config(state=tk.DISABLED)
        
        # 关闭按钮
        ttk.Button(dialog, text="关闭", command=dialog.destroy).pack(pady=10)
    
    def restore_system_value(self):
        """恢复选中变量为系统值"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        parent = self.tree.parent(item)
        if not parent:  # 不是具体的环境变量
            return
        
        name = self.tree.item(item, 'text')
        values = self.tree.item(item, 'values')
        if len(values) < 3:
            return
        
        scope = values[2]
        key = (name, scope)
        
        # 查找系统中的值
        for env in self.system_env_data:
            if env[0] == name and env[3] == scope:
                system_name, system_value, system_kind, system_scope = env
                
                # 更新当前数据
                for i, current_env in enumerate(self.env_data):
                    if current_env[0] == name and current_env[3] == scope:
                        self.env_data[i] = [system_name, system_value, system_kind, system_scope]
                        break
                
                # 更新编辑器显示
                self.load_env_to_editor(system_name, system_value, system_kind, system_scope)
                
                # 重新计算差异
                if self.system_env_data:
                    self.update_diff_status(self.system_env_data)
                
                self.status_var.set(f"已恢复 {name} 为系统值")
                return
        
        messagebox.showinfo("提示", f"未找到变量 {name} 在系统中的值")
        
    def show_admin_status(self):
        """显示管理员权限状态"""
        show_admin_status(self.root)
        
    def on_value_text_change(self, event=None):
        """当值文本改变时更新分号分隔列表"""
        value = self.value_text.get('1.0', tk.END).strip()
        self.update_separator_list(value)
        
    def update_separator_list(self, value):
        """更新分号分隔的值列表"""
        self.separator_listbox.delete(0, tk.END)
        if value and ';' in value:
            items = [item.strip() for item in value.split(';') if item.strip()]
            for item in items:
                self.separator_listbox.insert(tk.END, item)
    
    def add_separator_item(self):
        """添加分号分隔项"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加项")
        dialog.geometry("400x100")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="请输入要添加的项:").pack(pady=5)
        
        entry = ttk.Entry(dialog, width=50)
        entry.pack(pady=5)
        entry.focus()
        
        def add_item():
            item = entry.get().strip()
            if item:
                current_value = self.value_text.get('1.0', tk.END).strip()
                if current_value:
                    if not current_value.endswith(';'):
                        current_value += ';'
                    new_value = current_value + item
                else:
                    new_value = item
                
                self.value_text.delete('1.0', tk.END)
                self.value_text.insert('1.0', new_value)
                self.update_separator_list(new_value)
                dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="添加", command=add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        entry.bind('<Return>', lambda e: add_item())
    
    def delete_separator_item(self):
        """删除选中的分号分隔项"""
        selection = self.separator_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的项")
            return
        
        current_value = self.value_text.get('1.0', tk.END).strip()
        items = [item.strip() for item in current_value.split(';') if item.strip()]
        
        # 删除选中的项
        for index in reversed(selection):
            if index < len(items):
                items.pop(index)
        
        # 更新值
        new_value = ';'.join(items)
        self.value_text.delete('1.0', tk.END)
        self.value_text.insert('1.0', new_value)
        self.update_separator_list(new_value)
    
    def edit_separator_item(self):
        """编辑选中的分号分隔项"""
        selection = self.separator_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要编辑的项")
            return
        
        index = selection[0]
        current_value = self.value_text.get('1.0', tk.END).strip()
        items = [item.strip() for item in current_value.split(';') if item.strip()]
        
        if index >= len(items):
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑项")
        dialog.geometry("400x100")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="请编辑项内容:").pack(pady=5)
        
        entry = ttk.Entry(dialog, width=50)
        entry.pack(pady=5)
        entry.insert(0, items[index])
        entry.focus()
        entry.select_range(0, tk.END)
        
        def save_item():
            new_item = entry.get().strip()
            if new_item:
                items[index] = new_item
                new_value = ';'.join(items)
                self.value_text.delete('1.0', tk.END)
                self.value_text.insert('1.0', new_value)
                self.update_separator_list(new_value)
                dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="保存", command=save_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        entry.bind('<Return>', lambda e: save_item())
        
    def compare_with_system(self):
        """比较当前数据与系统实际数据的差异"""
        def compare_worker():
            try:
                self.root.after(0, lambda: self.status_var.set("正在获取系统环境变量..."))
                self.root.after(0, lambda: self.root.config(cursor="wait"))
                
                # 获取系统实际数据
                system_data = get_all_env_list()
                
                # 在主线程中更新差异状态
                self.root.after(0, lambda: self.update_diff_status(system_data))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"比较失败: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("比较失败"))
            finally:
                self.root.after(0, lambda: self.root.config(cursor=""))
        
        # 启动后台线程
        thread = threading.Thread(target=compare_worker, daemon=True)
        thread.start()
    
    def update_diff_status(self, system_data):
        """更新差异状态并重新渲染树形控件"""
        try:
            self.system_env_data = system_data
            self.diff_status = {}
            
            # 创建系统数据的查找字典
            system_dict = {}
            for env in system_data:
                name, value, kind, scope = env
                key = (name, scope)
                system_dict[key] = (value, kind)
            
            # 创建当前数据的查找字典
            current_dict = {}
            for env in self.env_data:
                name, value, kind, scope = env
                key = (name, scope)
                current_dict[key] = (value, kind)
            
            # 检查当前数据中的变量状态
            for env in self.env_data:
                name, value, kind, scope = env
                key = (name, scope)
                
                if key not in system_dict:
                    # 系统中不存在，标记为新增
                    self.diff_status[key] = 'added'
                else:
                    system_value, system_kind = system_dict[key]
                    if value != system_value or kind != system_kind:
                        # 值或类型不同，标记为修改
                        self.diff_status[key] = 'modified'
                    else:
                        # 完全相同
                        self.diff_status[key] = 'same'
            
            # 检查系统中存在但当前数据中不存在的变量（已删除）
            for env in system_data:
                name, value, kind, scope = env
                key = (name, scope)
                if key not in current_dict:
                    # 添加到当前数据中，但标记为删除状态
                    self.env_data.append([name, value, kind, scope])
                    self.diff_status[key] = 'removed'
            
            # 更新过滤数据并重新渲染
            self.filtered_data = self.env_data.copy()
            self.populate_tree()
            
            # 统计差异
            added_count = sum(1 for status in self.diff_status.values() if status == 'added')
            modified_count = sum(1 for status in self.diff_status.values() if status == 'modified')
            removed_count = sum(1 for status in self.diff_status.values() if status == 'removed')
            same_count = sum(1 for status in self.diff_status.values() if status == 'same')
            
            self.status_var.set(f"差异对比完成 - 新增:{added_count}, 修改:{modified_count}, 删除:{removed_count}, 相同:{same_count}")
            
        except Exception as e:
            messagebox.showerror("错误", f"更新差异状态失败: {str(e)}")
            self.status_var.set("差异对比失败")
        
    def load_env_vars(self):
        """在后台线程中读取环境变量"""
        def load_worker():
            try:
                self.status_var.set("正在读取环境变量...")
                self.root.config(cursor="wait")
                
                # 在后台线程中获取环境变量
                env_data = get_all_env_list()
                
                # 在主线程中更新界面
                self.root.after(0, lambda: self.update_tree_data(env_data))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"读取环境变量失败: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("就绪"))
                self.root.after(0, lambda: self.root.config(cursor=""))
        
        # 启动后台线程
        thread = threading.Thread(target=load_worker, daemon=True)
        thread.start()
    
    def update_tree_data(self, env_data):
        """更新树形控件数据"""
        try:
            self.env_data = env_data
            self.system_env_data = env_data.copy()  # 保存为系统基准数据
            self.filtered_data = env_data.copy()
            
            # 初始化差异状态 - 全部标记为相同
            self.diff_status = {}
            for env in env_data:
                name, value, kind, scope = env
                key = (name, scope)
                self.diff_status[key] = 'same'
            
            self.populate_tree()
            self.status_var.set(f"已加载 {len(env_data)} 个环境变量")
        except Exception as e:
            messagebox.showerror("错误", f"更新界面失败: {str(e)}")
        finally:
            self.root.config(cursor="")
            
    def populate_tree(self):
        """填充树形控件并应用差异颜色"""
        # 清空现有内容
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 按作用域分组
        user_vars = []
        machine_vars = []
        
        for env in self.filtered_data:
            name, value, kind, scope = env
            if scope.lower() == 'user':
                user_vars.append(env)
            else:
                machine_vars.append(env)
        
        # 添加用户变量
        if user_vars:
            user_root = self.tree.insert('', 'end', text='用户变量', values=('', '', 'User'))
            for env in user_vars:
                name, value, kind, scope = env
                key = (name, scope)
                
                # 获取差异状态
                diff_status = self.diff_status.get(key, 'same')
                
                # 根据差异状态应用标签
                item = self.tree.insert(user_root, 'end', text=name, values=(value, kind, scope), tags=(diff_status,))
        
        # 添加系统变量
        if machine_vars:
            machine_root = self.tree.insert('', 'end', text='系统变量', values=('', '', 'Machine'))
            for env in machine_vars:
                name, value, kind, scope = env
                key = (name, scope)
                
                # 获取差异状态
                diff_status = self.diff_status.get(key, 'same')
                
                # 根据差异状态应用标签
                item = self.tree.insert(machine_root, 'end', text=name, values=(value, kind, scope), tags=(diff_status,))
        
        # 展开所有节点
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
    
    def filter_tree(self, *args):
        """过滤树形控件内容"""
        search_text = self.search_var.get().lower()
        if not search_text:
            self.filtered_data = self.env_data.copy()
        else:
            self.filtered_data = []
            for env in self.env_data:
                name, value, kind, scope = env
                if (search_text in name.lower() or 
                    search_text in value.lower() or 
                    search_text in scope.lower()):
                    self.filtered_data.append(env)
        
        self.populate_tree()
    
    def on_tree_select(self, event):
        """树形控件选择事件"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            # 检查是否是环境变量项（而不是分组项）
            parent = self.tree.parent(item)
            if parent:  # 有父节点，说明是具体的环境变量
                name = self.tree.item(item, 'text')
                values = self.tree.item(item, 'values')
                if len(values) >= 3:
                    value, kind, scope = values[0], values[1], values[2]
                    self.load_env_to_editor(name, value, kind, scope)
    
    def on_tree_double_click(self, event):
        """树形控件双击事件"""
        self.on_tree_select(event)
    
    def load_env_to_editor(self, name, value, kind, scope):
        """将环境变量加载到编辑器"""
        self.name_var.set(name)
        self.value_text.delete('1.0', tk.END)
        self.value_text.insert('1.0', value)
        self.kind_var.set(kind)
        self.scope_var.set(scope)
        self.update_separator_list(value)
    
    def save_changes(self):
        """保存编辑的更改"""
        name = self.name_var.get().strip()
        value = self.value_text.get('1.0', tk.END).strip()
        kind = self.kind_var.get()
        scope = self.scope_var.get()
        
        if not name:
            messagebox.showwarning("警告", "变量名不能为空")
            return
        
        # 查找现有变量并更新，或添加新变量
        found = False
        for i, env in enumerate(self.env_data):
            if env[0] == name and env[3] == scope:
                self.env_data[i] = [name, value, kind, scope]
                found = True
                break
        
        if not found:
            self.env_data.append([name, value, kind, scope])
        
        self.filtered_data = self.env_data.copy()
        
        # 自动更新差异状态
        if self.system_env_data:
            # 如果有系统数据，重新计算差异
            self.update_diff_status(self.system_env_data)
            self.status_var.set(f"已更新变量: {name} - 差异已重新计算")
        else:
            # 如果没有系统数据，只是重新填充树
            self.populate_tree()
            self.status_var.set(f"已更新变量: {name} - 请点击'读取当前环境变量'获取完整状态")
    
    def cancel_edit(self):
        """取消编辑"""
        self.name_var.set("")
        self.value_text.delete('1.0', tk.END)
        self.kind_var.set("String")
        self.scope_var.set("User")
        self.separator_listbox.delete(0, tk.END)
    
    def new_variable(self):
        """新建变量"""
        self.cancel_edit()
        self.status_var.set("新建变量模式")
    
    def get_selected_env_vars(self):
        """获取选中的环境变量"""
        selection = self.tree.selection()
        selected_vars = []
        
        for item in selection:
            parent = self.tree.parent(item)
            if parent:  # 有父节点，说明是具体的环境变量
                name = self.tree.item(item, 'text')
                values = self.tree.item(item, 'values')
                if len(values) >= 3:
                    value, kind, scope = values[0], values[1], values[2]
                    selected_vars.append([name, value, kind, scope])
        
        return selected_vars
    
    def write_selected_env(self):
        """写入选中的环境变量"""
        selected_vars = self.get_selected_env_vars()
        if not selected_vars:
            messagebox.showwarning("警告", "请先选择要写入的环境变量")
            return
        
        # 检查差异状态是否匹配（写入操作适用于新增和修改状态）
        if self.diff_status:
            valid_vars = []
            invalid_vars = []
            
            for env in selected_vars:
                name, value, kind, scope = env
                key = (name, scope)
                diff_status = self.diff_status.get(key, 'same')
                
                if diff_status in ['added', 'modified']:
                    valid_vars.append(env)
                else:
                    invalid_vars.append((name, scope, diff_status))
            
            if invalid_vars:
                invalid_list = "\n".join([f"- {name} ({scope}): {status}" for name, scope, status in invalid_vars])
                messagebox.showwarning(
                    "状态验证失败", 
                    f"以下变量状态不匹配，写入操作只能应用于新增或修改状态的变量：\n\n{invalid_list}"
                )
                return
            
            if not valid_vars:
                messagebox.showwarning("警告", "没有可写入的变量")
                return
            
            # 使用验证后的变量列表
            selected_vars = valid_vars
        else:
            # 如果没有差异状态，提示用户先进行比较
            if not messagebox.askyesno(
                "未进行差异比较", 
                "尚未进行差异状态分析，无法验证变量状态。\n"
                "建议先点击'读取当前环境变量'。\n\n"
                "是否继续写入所有选中的变量？"
            ):
                return
        
        # 检查是否有系统变量且没有管理员权限
        has_machine_vars = any(env[3].lower() == 'machine' for env in selected_vars)
        if has_machine_vars and not self.is_admin:
            if messagebox.askyesno(
                "权限不足", 
                f"选中的变量包含 {sum(1 for env in selected_vars if env[3].lower() == 'machine')} 个系统变量，"
                "需要管理员权限才能写入。\n\n是否查看权限状态？"
            ):
                self.show_admin_status()
            return
        
        if messagebox.askyesno("确认", f"确定要写入 {len(selected_vars)} 个环境变量到系统吗？\n注意：系统变量需要管理员权限"):
            def write_worker():
                try:
                    self.root.after(0, lambda: self.status_var.set("正在写入环境变量..."))
                    self.root.after(0, lambda: self.root.config(cursor="wait"))
                    
                    set_env_to_system(selected_vars)
                    
                    self.root.after(0, lambda: messagebox.showinfo("成功", f"已写入 {len(selected_vars)} 个环境变量"))
                    self.root.after(0, lambda: self.status_var.set("写入完成"))
                    
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("错误", f"写入失败: {str(e)}"))
                    self.root.after(0, lambda: self.status_var.set("就绪"))
                finally:
                    self.root.after(0, lambda: self.root.config(cursor=""))
            
            thread = threading.Thread(target=write_worker, daemon=True)
            thread.start()
    
    def modify_selected_env(self):
        """变更选中的环境变量 - 仅允许修改状态的变量"""
        selected_vars = self.get_selected_env_vars()
        if not selected_vars:
            messagebox.showwarning("警告", "请先选择要变更的环境变量")
            return
        
        # 检查是否已进行差异比较
        if not self.diff_status:
            messagebox.showwarning("警告", "请先点击'读取当前环境变量'进行状态分析")
            return
        
        # 验证选中变量的状态
        valid_vars = []
        invalid_vars = []
        
        for env in selected_vars:
            name, value, kind, scope = env
            key = (name, scope)
            diff_status = self.diff_status.get(key, 'same')
            
            if diff_status in ['added', 'modified']:
                valid_vars.append(env)
            else:
                invalid_vars.append((name, scope, diff_status))
        
        if invalid_vars:
            invalid_list = "\n".join([f"- {name} ({scope}): {status}" for name, scope, status in invalid_vars])
            messagebox.showwarning(
                "状态验证失败", 
                f"以下变量状态不匹配，变更操作只能应用于新增或修改状态的变量：\n\n{invalid_list}"
            )
            return
        
        if not valid_vars:
            messagebox.showwarning("警告", "没有可变更的变量")
            return
        
        # 检查是否有系统变量且没有管理员权限
        has_machine_vars = any(env[3].lower() == 'machine' for env in valid_vars)
        if has_machine_vars and not self.is_admin:
            if messagebox.askyesno(
                "权限不足", 
                f"选中的变量包含 {sum(1 for env in valid_vars if env[3].lower() == 'machine')} 个系统变量，"
                "需要管理员权限才能变更。\n\n是否查看权限状态？"
            ):
                self.show_admin_status()
            return
        
        if messagebox.askyesno("确认", f"确定要变更 {len(valid_vars)} 个环境变量到系统吗？"):
            def modify_worker():
                try:
                    self.root.after(0, lambda: self.status_var.set("正在变更环境变量..."))
                    self.root.after(0, lambda: self.root.config(cursor="wait"))
                    
                    set_env_to_system(valid_vars)
                    
                    self.root.after(0, lambda: messagebox.showinfo("成功", f"已变更 {len(valid_vars)} 个环境变量"))
                    self.root.after(0, lambda: self.status_var.set("变更完成"))
                    
                    # 重新加载并比较
                    self.root.after(1000, self.load_and_compare_env_vars)
                    
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("错误", f"变更失败: {str(e)}"))
                    self.root.after(0, lambda: self.status_var.set("就绪"))
                finally:
                    self.root.after(0, lambda: self.root.config(cursor=""))
            
            thread = threading.Thread(target=modify_worker, daemon=True)
            thread.start()
    
    def delete_selected_env(self):
        """删除选中的环境变量"""
        selected_vars = self.get_selected_env_vars()
        if not selected_vars:
            messagebox.showwarning("警告", "请先选择要删除的环境变量")
            return
        
        # 检查差异状态是否匹配（删除操作只能应用于存在于系统中的变量）
        if self.diff_status:
            valid_vars = []
            invalid_vars = []
            
            for env in selected_vars:
                name, value, kind, scope = env
                key = (name, scope)
                diff_status = self.diff_status.get(key, 'same')
                
                # 删除操作适用于 same、modified、removed 状态，但不适用于 added 状态
                if diff_status in ['same', 'modified', 'removed']:
                    valid_vars.append(env)
                else:
                    invalid_vars.append((name, scope, diff_status))
            
            if invalid_vars:
                invalid_list = "\n".join([f"- {name} ({scope}): {status}" for name, scope, status in invalid_vars])
                messagebox.showwarning(
                    "状态验证失败", 
                    f"以下变量状态不匹配，删除操作只能应用于系统中已存在的变量：\n\n{invalid_list}"
                )
                return
            
            if not valid_vars:
                messagebox.showwarning("警告", "没有可删除的变量")
                return
            
            # 使用验证后的变量列表
            selected_vars = valid_vars
        else:
            # 如果没有差异状态，提示用户先进行比较
            if not messagebox.askyesno(
                "未进行差异比较", 
                "尚未进行差异状态分析，无法验证变量状态。\n"
                "建议先点击'读取当前环境变量'。\n\n"
                "是否继续删除所有选中的变量？"
            ):
                return
        
        # 检查是否有系统变量且没有管理员权限
        has_machine_vars = any(env[3].lower() == 'machine' for env in selected_vars)
        if has_machine_vars and not self.is_admin:
            if messagebox.askyesno(
                "权限不足", 
                f"选中的变量包含 {sum(1 for env in selected_vars if env[3].lower() == 'machine')} 个系统变量，"
                "需要管理员权限才能删除。\n\n是否查看权限状态？"
            ):
                self.show_admin_status()
            return
        
        if messagebox.askyesno("确认", f"确定要从系统中删除 {len(selected_vars)} 个环境变量吗？\n此操作不可恢复！"):
            def delete_worker():
                try:
                    self.root.after(0, lambda: self.status_var.set("正在删除环境变量..."))
                    self.root.after(0, lambda: self.root.config(cursor="wait"))
                    
                    deleted_count = delete_env_vars(selected_vars)
                    
                    self.root.after(0, lambda: messagebox.showinfo("完成", f"已删除 {deleted_count} 个环境变量"))
                    self.root.after(0, lambda: self.status_var.set("删除完成"))
                    
                    # 重新加载环境变量
                    self.root.after(1000, self.load_env_vars)
                    
                    # 如果有系统数据，触发差异比较
                    if hasattr(self, 'system_env_data') and self.system_env_data:
                        self.root.after(1500, lambda: self.compare_with_system())
                    
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("错误", f"删除失败: {str(e)}"))
                    self.root.after(0, lambda: self.status_var.set("就绪"))
                finally:
                    self.root.after(0, lambda: self.root.config(cursor=""))
            
            thread = threading.Thread(target=delete_worker, daemon=True)
            thread.start()
    
    def apply_all_changes(self):
        """应用所有修改的变量到系统"""
        if not self.diff_status:
            messagebox.showwarning("警告", "请先读取当前环境变量并比较差异")
            return
        
        # 筛选出所有有变化的变量
        changed_vars = []
        for env in self.env_data:
            name, value, kind, scope = env
            key = (name, scope)
            diff_status = self.diff_status.get(key, 'same')
            
            if diff_status in ['added', 'modified']:
                changed_vars.append(env)
        
        if not changed_vars:
            messagebox.showinfo("提示", "没有需要应用的修改")
            return
        
        # 检查是否有系统变量且没有管理员权限
        has_machine_vars = any(env[3].lower() == 'machine' for env in changed_vars)
        if has_machine_vars and not self.is_admin:
            machine_count = sum(1 for env in changed_vars if env[3].lower() == 'machine')
            if messagebox.askyesno(
                "权限不足", 
                f"待应用的变量包含 {machine_count} 个系统变量，"
                "需要管理员权限才能应用。\n\n是否查看权限状态？"
            ):
                self.show_admin_status()
            return
        
        # 统计变更类型
        added_count = sum(1 for env in changed_vars 
                         if self.diff_status.get((env[0], env[3]), 'same') == 'added')
        modified_count = sum(1 for env in changed_vars 
                           if self.diff_status.get((env[0], env[3]), 'same') == 'modified')
        
        confirm_msg = f"确定要应用所有修改到系统吗？\n\n新增: {added_count} 个\n修改: {modified_count} 个\n总计: {len(changed_vars)} 个环境变量"
        
        if messagebox.askyesno("确认应用所有修改", confirm_msg):
            def apply_worker():
                try:
                    self.root.after(0, lambda: self.status_var.set("正在应用所有修改..."))
                    self.root.after(0, lambda: self.root.config(cursor="wait"))
                    
                    set_env_to_system(changed_vars)
                    
                    self.root.after(0, lambda: messagebox.showinfo(
                        "成功", 
                        f"已应用所有修改到系统\n新增: {added_count} 个\n修改: {modified_count} 个"
                    ))
                    self.root.after(0, lambda: self.status_var.set("应用完成"))
                    
                    # 重新加载并比较
                    self.root.after(1000, self.load_and_compare_env_vars)
                    
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("错误", f"应用修改失败: {str(e)}"))
                    self.root.after(0, lambda: self.status_var.set("就绪"))
                finally:
                    self.root.after(0, lambda: self.root.config(cursor=""))
            
            thread = threading.Thread(target=apply_worker, daemon=True)
            thread.start()
    
    def backup_env_vars(self):
        """备份当前环境变量"""
        if not self.env_data:
            messagebox.showwarning("警告", "没有环境变量数据可备份")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(
            title="保存备份文件",
            defaultextension=".yaml",
            initialfile=f"env_backup_{timestamp}.yaml",
            filetypes=[
                ("YAML files", "*.yaml"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    # 保存为JSON格式
                    backup_data = {
                        'timestamp': datetime.now().isoformat(),
                        'count': len(self.env_data),
                        'variables': []
                    }
                    
                    for env in self.env_data:
                        name, value, kind, scope = env
                        backup_data['variables'].append({
                            'name': name,
                            'value': value,
                            'kind': kind,
                            'scope': scope
                        })
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(backup_data, f, ensure_ascii=False, indent=2)
                else:
                    # 保存为YAML格式
                    save_env_to_yaml(self.env_data, filename)
                
                messagebox.showinfo("成功", f"环境变量已备份到:\n{filename}")
                self.status_var.set(f"已备份 {len(self.env_data)} 个环境变量")
                
            except Exception as e:
                messagebox.showerror("错误", f"备份失败: {str(e)}")
    
    def import_backup(self):
        """导入备份的环境变量"""
        filename = filedialog.askopenfilename(
            title="选择备份文件",
            filetypes=[
                ("YAML files", "*.yaml"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    # 从JSON格式导入
                    with open(filename, 'r', encoding='utf-8') as f:
                        backup_data = json.load(f)
                    
                    env_data = []
                    for var in backup_data.get('variables', []):
                        env_data.append([
                            var['name'],
                            var['value'],
                            var['kind'],
                            var['scope']
                        ])
                else:
                    # 从YAML格式导入
                    env_data = get_env_from_yaml(filename)
                
                self.env_data = env_data
                self.filtered_data = env_data.copy()
                
                # 自动读取系统环境变量并进行差异比较
                def import_and_compare():
                    try:
                        # 获取系统环境变量
                        system_data = get_all_env_list()
                        
                        # 在主线程中更新差异状态
                        self.root.after(0, lambda: self.update_diff_status(system_data))
                        self.root.after(0, lambda: messagebox.showinfo(
                            "导入成功", 
                            f"已导入 {len(env_data)} 个环境变量\n已自动与系统环境变量进行差异比较"
                        ))
                        
                    except Exception as e:
                        # 如果系统读取失败，只显示导入成功，提示手动比较
                        self.root.after(0, lambda: self.populate_tree())
                        self.root.after(0, lambda: messagebox.showinfo(
                            "导入成功", 
                            f"已导入 {len(env_data)} 个环境变量\n自动比较失败: {str(e)}\n请手动点击'读取当前环境变量'进行比较"
                        ))
                        self.root.after(0, lambda: self.status_var.set(f"已导入 {len(env_data)} 个环境变量 - 请手动比较差异"))
                
                # 启动后台线程进行系统环境变量读取和比较
                import threading
                thread = threading.Thread(target=import_and_compare, daemon=True)
                thread.start()
                
            except Exception as e:
                messagebox.showerror("错误", f"导入失败: {str(e)}")
    
    def load_and_compare_env_vars(self):
        """读取环境变量并与现有数据比较差异"""
        def load_and_compare_worker():
            try:
                self.root.after(0, lambda: self.status_var.set("正在读取环境变量..."))
                self.root.after(0, lambda: self.root.config(cursor="wait"))
                
                # 在后台线程中获取环境变量
                env_data = get_all_env_list()
                
                # 在主线程中更新界面并比较差异
                self.root.after(0, lambda: self.update_tree_data(env_data))
                
                # 如果之前有数据，进行差异比较
                if self.env_data:
                    self.root.after(100, lambda: self.update_diff_status(env_data))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"读取环境变量失败: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("就绪"))
                self.root.after(0, lambda: self.root.config(cursor=""))
        
        # 启动后台线程
        thread = threading.Thread(target=load_and_compare_worker, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = EnvironmentVariableGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
