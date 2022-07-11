from typing import Any, Mapping
import json
import sys
import re

def normalize_key(key: str) -> str:
    return re.sub(r'[^A-Z0-9]', '_', key, 0, re.MULTILINE)

def create_val(obj: Any, obj_key: str) -> Any:
    key_prefix = obj_key + '_' if obj_key != '' else ''
    if isinstance(obj, list):
        new_obj = []
        for index, val in enumerate(obj):
            new_obj.append(create_val(val, normalize_key(key_prefix + str(index))))
        return new_obj
    if isinstance(obj, dict):
        new_obj = {}
        for key, val in obj.items():
            new_obj[key] = create_val(val, normalize_key(key_prefix + key.upper()))
        return new_obj
    return "os.getenv('{}', '{}')".format(obj_key, obj)


def create_env(obj: Any, obj_key: str) -> Mapping[str, str]:
    key_prefix = obj_key + '_' if obj_key != '' else ''
    if isinstance(obj, list):
        env: Mapping[str, str] = {}
        for index, val in enumerate(obj):
            new_env = create_env(val, normalize_key(key_prefix + str(index)))
            env = {**env, **new_env}
        return env
    if isinstance(obj, dict):
        env: Mapping[str, str] = {}
        for key, val in obj.items():
            new_env = create_env(val, normalize_key(key_prefix + key.upper()))
            env = {**env, **new_env}
        return env
    return {obj_key: obj}


def create_value_script(obj: Mapping[str, Any]) -> str:
    value_obj = create_val(obj, '')
    raw_value_definition_script = json.dumps(value_obj, indent=4)
    # remove quotes
    value_definition_script = re.sub(r'(.*)"(os\.getenv.*)"(.*)', r'\1\2\3', raw_value_definition_script, 0, re.MULTILINE)
    value_definition_script = 'values = ' + value_definition_script + ','
    # adjust True value
    value_definition_script = re.sub(r"(os\.getenv\('.*', 'True'\))", r"\1 == 'True'", value_definition_script, 0, re.MULTILINE)
    # adjust False value
    value_definition_script = re.sub(r"(os\.getenv\('.*', 'False'\))", r"\1 == 'True'", value_definition_script, 0, re.MULTILINE)
    # adjust int value
    value_definition_script = re.sub(r"(os\.getenv\('.*', '[0-9]+'\))", r"int(\1)", value_definition_script, 0, re.MULTILINE)
    return value_definition_script


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'env'
    json_string = sys.argv[2] if len(sys.argv) > 2 else '{}'
    obj = json.loads(json_string)
    if mode == 'json-env-map':
        print(json.dumps(create_env(obj, '')))
    elif mode == 'env':
        env_map = create_env(obj, '')
        lines = []
        for key, val in env_map.items():
            lines.append('{}={}'.format(key, val))
        print('\n'.join(lines))
    elif mode == 'python-value':
        print(create_value_script(obj))
