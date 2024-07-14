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


def store_experiment_as_gguf(experiment_description: str, operand1: torch.Tensor, operand2: torch.Tensor,
                             operation_callback, gguf_file_path: str):
    """
    Perform a mathematical operation on two tensors and store the operands, operator, and result in a gguf file.

    :param experiment_description: stores a description of the experiment
    :param operand1: First tensor operand
    :param operand2: Second tensor operand
    :param operation_callback: Callback function to perform the operation
    :param gguf_file_path: Path to the gguf file to store the results
    """
    # Get the names of the variables passed as arguments
    frame = inspect.currentframe().f_back
    args, _, _, values = inspect.getargvalues(frame)
    operand1_name = [name for name in values if values[name] is operand1][0]
    operand2_name = [name for name in values if values[name] is operand2][0]
    operation_callback_name = [name for name in values if values[name] is operation_callback][0]

    # Convert tensors to Little Endian format after capturing variable names

    operand1_le = __convert_to_f32__(__ensure_little_endian__(operand1.numpy()))
    operand2_le = __convert_to_f32__(__ensure_little_endian__(operand2.numpy()))

    # Perform the operation using the callback
    result = __convert_to_f32__(
        __ensure_little_endian__(operation_callback(operand1, operand2).numpy()))

    # Prepare data to write into gguf file
    writer = gguf.GGUFWriter(gguf_file_path, arch='llama')
    writer.add_description(experiment_description)
    writer.add_tensor(operand1_name, operand1_le)
    writer.add_tensor(operand2_name, operand2_le)
    writer.add_name(operation_callback_name)
    writer.add_tensor("result", result)
    writer.write_header_to_file()
    writer.write_kv_data_to_file()
    writer.write_tensors_to_file()
    writer.close()

    print(f"Experiment data stored in {gguf_file_path}")
