plugins {
    alias(libs.plugins.androidLibrary) apply false
    alias(libs.plugins.kotlinMultiplatform) apply  false
    alias(libs.plugins.jetbrainsKotlinJvm) apply false
    alias(libs.plugins.binaryCompatibility) apply false
}

allprojects {
    group = "sk.ai.net.ktracer"
    version = "0.0.1"

    tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().configureEach {
        compilerOptions {
            freeCompilerArgs = listOf("-Xdownload-sources=true")
        }
    }
}

