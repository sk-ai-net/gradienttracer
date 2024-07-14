import numpy
import torch
import gguf
import inspect
import numpy as np


def __ensure_little_endian__(tensor: torch.Tensor) -> torch.Tensor:
    """Ensures the tensor is in Little Endian format."""
    if tensor.dtype.byteorder not in ('<', '=', '|'):
        tensor = tensor.byteswap().newbyteorder('<')
    return tensor


def __convert_to_f32__(tensor: torch.Tensor) -> numpy.ndarray:
    """Converts the tensor to float32 if it is not already."""
    if tensor.dtype != np.float32:
        tensor = tensor.astype(np.float32)
    return tensor


def store_experiment_as_gguf(experiment_description: str, tensors: dict, operation_callback, gguf_file_path: str):
    """
    Perform a mathematical operation on an array of tensors and store the operands, operator, and result in a gguf file.

    :param experiment_description: stores a description of the experiment
    :param tensors: Dictionary containing tensor names and their values
    :param operation_callback: Callback function to perform the operation
    :param gguf_file_path: Path to the gguf file to store the results
    """
    # Convert tensors to Little Endian format after capturing variable names
    tensors_le = {name: __convert_to_f32__(__ensure_little_endian__(tensor.numpy())) for name, tensor in tensors.items()}

    # Perform the operation using the callback
    result = __convert_to_f32__(__ensure_little_endian__(operation_callback(*tensors.values()).numpy()))

    # Prepare data to write into gguf file
    writer = gguf.GGUFWriter(gguf_file_path, arch='llama')
    writer.add_description(experiment_description)
    for name, tensor_le in tensors_le.items():
        writer.add_tensor(name, tensor_le)
    writer.add_name(operation_callback.__name__)
    writer.add_tensor("result", result)
    writer.write_header_to_file()
    writer.write_kv_data_to_file()
    writer.write_tensors_to_file()
    writer.close()

    print(f"Experiment data stored in {gguf_file_path}")