# core.py

import os
import importlib.util
from typing import List, Dict, Callable
import torch


# Custom annotation
def Executable(description):
    def decorator(func):
        func.executable = True
        func.description = description
        return func

    return decorator


def load_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_executable_functions(module):
    executables = []
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if callable(attr) and hasattr(attr, 'executable'):
            executables.append((attr, attr.description))
    return executables


def iterate_and_execute(folder_path):
    results = []
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            if dir_name.startswith("TS-"):
                ts_number = dir_name.split('-')[1]
                ts_path = str(os.path.join(root, dir_name))
                for file_name in os.listdir(ts_path):
                    if file_name.startswith("UC-") and file_name.endswith(".py"):
                        uc_number = file_name.split('-')[1].split('.')[0]
                        file_path = os.path.join(ts_path, file_name)
                        module_name = f"{ts_number}_UC_{uc_number}"
                        module = load_module_from_file(module_name, file_path)
                        executable_functions = find_executable_functions(module)
                        for func, description in executable_functions:
                            inputs, result = func()
                            results.append({
                                'name': f"{module_name}.{func.__name__}",
                                'description': description,
                                'inputs': inputs,
                                'result': result,
                                'test_suite': f"TS-{ts_number}",
                                'use_case': f"UC-{uc_number}"
                            })
    return results


if __name__ == "__main__":
    scr_results = iterate_and_execute("/Users/A9973957/projects/tribit.ai/gradienttracer/gt/examples")
    for result in scr_results:
        print(result)
