# UC-001.py

from core import Executable
import torch


@Executable('simple expression with relu')
def simple_expression_with_relu():
    x = torch.Tensor([-4.0]).double()
    x.requires_grad = True
    z = 2 * x + 2 + x
    q = z.relu() + z * x
    h = (z * z).relu()
    y = h + q + q * x
    y.backward()
    return [x], y


@Executable("simple multiplication")
def simple_multiplication():
    a = torch.tensor(3.0, requires_grad=True)
    b = torch.tensor(2.0, requires_grad=True)
    c = a * b
    c.backward()
    return [a, b], c
