package net.skai.ktracer

import kotlinx.coroutines.*
import kotlinx.io.asSource
import kotlinx.io.buffered
import java.nio.file.Path
import kotlin.io.path.*

/**
 * Data class representing a test execution result
 */
data class TestExecutionResult(
    val name: String,
    val description: String,
    val inputs: List<Any>,
    val result: Any,
    val testSuite: String,
    val useCase: String,
    val executionTimeMs: Long,
    val success: Boolean,
    val error: String? = null
)

/**
 * Class responsible for executing tests and storing results
 */
class TestSuiteExecutor(
    private val outputPath: Path,
    private val generateDot: Boolean = false,
    private val parallelExecution: Boolean = true
) {
    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())

    /**
     * Execute a test case and capture its result
     */
    private suspend fun executeTest(
        testCase: TestCase,
        suiteName: String,
        useCaseName: String
    ): TestExecutionResult = withContext(Dispatchers.Default) {
        try {
            val startTime = System.currentTimeMillis()
            
            // Execute the test case
            val result = testCase.execute()
            
            val executionTime = System.currentTimeMillis() - startTime
            
            TestExecutionResult(
                name = "${suiteName}_${useCaseName}_${testCase.description.replace(" ", "_")}",
                description = testCase.description,
                inputs = testCase.inputs,
                result = result,
                testSuite = suiteName,
                useCase = useCaseName,
                executionTimeMs = executionTime,
                success = true
            )
        } catch (e: Exception) {
            TestExecutionResult(
                name = "${suiteName}_${useCaseName}_${testCase.description.replace(" ", "_")}",
                description = testCase.description,
                inputs = testCase.inputs,
                result = Any(),
                testSuite = suiteName,
                useCase = useCaseName,
                executionTimeMs = 0,
                success = false,
                error = e.message
            )
        }
    }

    /**
     * Store test result in GGUF format
     */
    private fun storeResult(result: TestExecutionResult) {
        val tsFolder = outputPath.resolve("TS-${result.testSuite}")
        tsFolder.createDirectories()
        
        val ggufPath = tsFolder.resolve("${result.name}.gguf")
        
        // Store tensors and metadata in GGUF format
        GGUFWriter(ggufPath).use { writer ->
            writer.addMetadata("experiment_description", result.description)
            writer.addMetadata("execution_time_ms", result.executionTimeMs.toString())
            writer.addMetadata("success", result.success.toString())
            result.error?.let { writer.addMetadata("error", it) }
            
            // Store inputs
            result.inputs.forEachIndexed { index, input ->
                writer.addTensor("input_$index", input)
            }
            
            // Store result
            writer.addTensor("result", result.result)
        }
        
        // Generate DOT visualization if enabled
        if (generateDot && result.success) {
            val graph = trace(result.result)
            val dot = dag_2_dot(graph)
            val dotPath = tsFolder.resolve("${result.name}.dot")
            dot.render(dotPath.toString())
        }
    }

    /**
     * Execute all test cases in a use case
     */
    suspend fun executeUseCase(useCase: UseCase): List<TestExecutionResult> = coroutineScope {
        val results = mutableListOf<TestExecutionResult>()
        
        useCase.getSuites().forEach { suite ->
            val testCases = suite.getCases()
            
            if (parallelExecution) {
                // Execute test cases in parallel
                val deferredResults = testCases.map { testCase ->
                    async {
                        executeTest(testCase, suite.name, useCase.name)
                    }
                }
                
                deferredResults.awaitAll().forEach { result ->
                    results.add(result)
                    storeResult(result)
                }
            } else {
                // Execute test cases sequentially
                testCases.forEach { testCase ->
                    val result = executeTest(testCase, suite.name, useCase.name)
                    results.add(result)
                    storeResult(result)
                }
            }
        }
        
        results
    }

    /**
     * Execute a use case and return results
     */
    fun execute(useCase: UseCase): List<TestExecutionResult> = runBlocking {
        executeUseCase(useCase)
    }

    /**
     * Clean up resources
     */
    fun close() {
        scope.cancel()
    }
}
