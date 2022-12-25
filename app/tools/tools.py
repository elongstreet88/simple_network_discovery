from functools import reduce
import json
import os
import typing
from fastapi import Response
import os

def deep_get(dictionary:dict, keys:str, default=None):
    """ Get value from nested dictionary without having to chain .get() calls
    Example:
        my_dict =  {"a": {"b": {"c": 1}}}
        result1 = deep_get(my_dict, "a.b.c")
        result2 = deep_get(my_dict, "a.b.bad")

        print(result1)
        # 1
        print(result2)
        # None

    Args:
        dictionary (dict): The dictionary to search
        keys (str): The string of keys separated by '.'
        default (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: Value from nested dictionary if found, otherwise default
    """
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

class FormatJSON(Response):
    """
    Simple class to allow FAT API to return JSON formatted responses.
    Can be used in fastapi route such as:
    @router.get("", response_model=list[IPNetwork], response_class=FormatJSON)
    
    Ex: {"a": 1, "b": 2} -> 
    {
        "a": 1,
        "b": 2
    }
    """
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            indent=4,
        ).encode("utf-8")

def load_environment_variables_from_vscode_settings(default_relative_path=".vscode/tasks.json"):
    # Load vscode settings (be sure no "//" or other comments exist or it will trip)
    parent_dir              = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vs_code_settings_file   = os.path.join(parent_dir, default_relative_path)
    
    with open(vs_code_settings_file, "r") as f:
        settings = json.load(f)
        for env_var in settings["tasks"][0]["dockerRun"]["env"]:
            if os.environ.get(env_var):
                #Alreay set, skip
                continue
            value = settings["tasks"][0]["dockerRun"]["env"][env_var]
            if value.startswith("$("):
                value = os.popen("echo " + value).read()
            
            os.environ[env_var] = value