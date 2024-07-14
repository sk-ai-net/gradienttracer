# core.py

import os
import importlib.util
from typing import List, Dict, Callable
import torch

from gt.pytorch.io.writer import store_experiment_as_gguf


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


def exec_and_store(folder_path, output_path):
    experiment_results = iterate_and_execute(folder_path)
    for result in experiment_results:
        ts_folder = os.path.join(output_path, result['test_suite'])
        os.makedirs(ts_folder, exist_ok=True)
        gguf_file_path = os.path.join(ts_folder, f"{result['use_case']}_{result['name']}.gguf")
        tensors = {f"input_{i}": tensor for i, tensor in enumerate(result['inputs'])}
        store_experiment_as_gguf(
            experiment_description=result['description'],
            tensors=tensors,
            operation_callback=lambda *args: result['result'],
            gguf_file_path=gguf_file_path
        )
