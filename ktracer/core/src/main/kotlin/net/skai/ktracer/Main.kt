package net.skai.ktracer

import kotlin.io.path.Path

fun main(args: Array<String>) {
    if (args.isEmpty()) {
        println("Please provide the path to the directory containing GGUF files")
        return
    }

    val basePath = Path(args[0])
    val reader = GGUFReferencesReader(basePath)
    
    println("Iterating over GGUF files in $basePath")
    reader.iterateGGUFFiles().forEach { (path, tensors) ->
        println("\nFile: $path")
        println("Description: ${reader.getExperimentDescription(path)}")
        println("Tensors:")
        tensors.forEach { (name, data) ->
            println("  $name: $data")
        }
    }
}
