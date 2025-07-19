import yaml

def save_env_to_yaml(env_list, filename="env.yaml"):
    """将环境变量列表保存到 YAML 文件中"""
    machine_envs = []
    user_envs = []

    for env in env_list:
        name, value, kind, scope = env
        env_data = {"name": name, "value": value, "kind": kind}

        if scope == "Machine":
            machine_envs.append(env_data)
        else:
            user_envs.append(env_data)

    yaml_data = {"machine": machine_envs, "user": user_envs}

    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(
            yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )

    print(f"环境变量已保存到 {filename}")

def get_env_from_yaml(filename="env.yaml"):
    """从 YAML 文件中读取环境变量"""
    with open(filename, "r", encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)

    env_list = []
    for scope, envs in yaml_data.items():
        for env in envs:
            temp = [env["name"], env["value"], env["kind"], scope]
            if scope.lower() == "machine":
                temp[3] = "Machine"
            else:
                temp[3] = "User"
            env_list.append(temp)

    return env_list
