package net.skai.ktracer.tests

import net.skai.ktracer.dsl.*
import sk.ai.net.Tensor
import sk.ai.net.impl.DoublesTensor
import sk.ai.net.nn.Conv2d
import kotlin.io.path.Path

fun main() {
    val runner = TestRunner(Path("test-output"))

    runner.useCase("001") {
        suite("001") {
            test("Basic 2D Convolution") {
                // Create input tensor
                val x = readInput(0)

                // Create and apply convolution
                val conv = Conv2d(3, 16, kernelSize = 3, stride = 3, padding = 0)
                val y = conv.forward(x)

                // Set test inputs and expected output
                input(x)
                expect(y)
            }

            test("Strided Convolution") {
                // Create input tensor
                val x = readInput(0)

                // Create and apply convolution
                val conv = Conv2d(3, 16, kernelSize = 3, stride = 2, padding = 0)
                val y = conv.forward(x)

                // Set test inputs and expected output
                input(x)
                expect(y)
            }
        }
    }.also { runner.execute(it) }
}
