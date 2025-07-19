import subprocess
from tqdm import tqdm

def get_all_env_list():
    """获取所有环境变量列表，包括用户和系统环境变量"""
    env_list = []

    # 获取所有用户环境变量
    user_ps_script = """
    $envVars = @()
    $userKey = Get-Item -Path 'HKCU:\\Environment' -ErrorAction SilentlyContinue
    if ($userKey) {
        foreach ($name in $userKey.GetValueNames()) {
            try {
                $value = $userKey.GetValue($name, '', 'DoNotExpandEnvironmentNames')
                $kind = $userKey.GetValueKind($name)
                $output = '{0}|{1}|{2}|User' -f $name, $value, $kind
                $envVars += $output
            } catch {
                Write-Host "Error reading user env var: $name" -ForegroundColor Yellow
            }
        }
    }
    $envVars | ForEach-Object { Write-Output $_ }
    """

    try:
        user_result = subprocess.run(
            ["powershell", "-Command", user_ps_script],
            capture_output=True,
            text=True,
            check=True,
        )

        for line in tqdm(
            user_result.stdout.strip().split("\n"),
            desc="Processing User environment variables",
        ):
            line = line.strip()
            if line and "|" in line:
                parts = line.split("|", 3)
                if len(parts) == 4:
                    name, value, kind, scope = parts
                    env_list.append([name, value, kind, scope])

    except subprocess.CalledProcessError as e:
        print(f"获取用户环境变量失败: {e}")

    # 获取所有系统环境变量
    machine_ps_script = """
    $envVars = @()
    $machineKey = Get-Item -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment' -ErrorAction SilentlyContinue
    if ($machineKey) {
        foreach ($name in $machineKey.GetValueNames()) {
            try {
                $value = $machineKey.GetValue($name, '', 'DoNotExpandEnvironmentNames')
                $kind = $machineKey.GetValueKind($name)
                $output = '{0}|{1}|{2}|Machine' -f $name, $value, $kind
                $envVars += $output
            } catch {
                Write-Host "Error reading machine env var: $name" -ForegroundColor Yellow
            }
        }
    }
    $envVars | ForEach-Object { Write-Output $_ }
    """

    try:
        machine_result = subprocess.run(
            ["powershell", "-Command", machine_ps_script],
            capture_output=True,
            text=True,
            check=True,
        )

        for line in tqdm(
            machine_result.stdout.strip().split("\n"),
            desc="Processing Machine environment variables",
        ):
            line = line.strip()
            if line and "|" in line:
                parts = line.split("|", 3)
                if len(parts) == 4:
                    name, value, kind, scope = parts
                    env_list.append([name, value, kind, scope])

    except subprocess.CalledProcessError as e:
        print(f"获取系统环境变量失败: {e}")

    # 按名称排序
    env_list.sort(key=lambda x: x[0].lower())
    return env_list

def set_env_to_system(env_list):
    """将环境变量列表写入系统"""
    user_count = 0
    machine_count = 0

    for env in tqdm(env_list, desc="Setting environment variables"):
        name, value, kind, scope = env

        # 转义单引号，但不要对反斜杠进行双重转义
        escaped_name = name.replace("'", "''")
        escaped_value = value.replace("'", "''")

        if scope.lower() == "machine":
            # 设置系统环境变量
            hive = "HKLM"
            subkey = "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"
            machine_count += 1
        else:
            # 设置用户环境变量
            hive = "HKCU"
            subkey = "Environment"
            user_count += 1

        # 根据数据类型设置环境变量
        if kind == "ExpandString":
            kind_flag = "ExpandString"
        else:
            kind_flag = "String"

        try:
            # 使用更简单的 PowerShell 命令设置环境变量
            if scope.lower() == "machine":
                ps_command = f"Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment' -Name '{escaped_name}' -Value '{escaped_value}' -Type {kind_flag}"
            else:
                ps_command = f"Set-ItemProperty -Path 'HKCU:\\Environment' -Name '{escaped_name}' -Value '{escaped_value}' -Type {kind_flag}"

            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                check=True,
            )

        except subprocess.CalledProcessError as e:
            print(f"设置环境变量 {name} 失败: {e.stderr if e.stderr else str(e)}")
            continue

    print(f"成功设置 {user_count} 个用户环境变量和 {machine_count} 个系统环境变量")
    print("注意: 系统环境变量需要管理员权限才能设置成功")

def delete_env_vars(env_list):
    """删除环境变量"""
    deleted_count = 0

    for env in tqdm(env_list, desc="Deleting environment variables"):
        name, value, kind, scope = env

        # 转义单引号
        escaped_name = name.replace("'", "''")

        if scope.lower() == "machine":
            # 删除系统环境变量
            ps_command = f"Remove-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment' -Name '{escaped_name}' -ErrorAction SilentlyContinue"
        else:
            # 删除用户环境变量
            ps_command = f"Remove-ItemProperty -Path 'HKCU:\\Environment' -Name '{escaped_name}' -ErrorAction SilentlyContinue"

        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                check=True,
            )

            deleted_count += 1

        except subprocess.CalledProcessError as e:
            print(f"✗ 删除 {name} ({scope}) 失败: {e.stderr if e.stderr else str(e)}")

    print(f"\n删除结果: 成功删除 {deleted_count}/{len(env_list)} 个环境变量")
    return deleted_count
