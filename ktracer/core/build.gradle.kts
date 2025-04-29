plugins {
    kotlin("jvm")
    `java-library`
}

dependencies {
    api(kotlin("stdlib"))
    api(kotlin("reflect"))
    
    // GGUF dependencies
    api("sk.ai.net:gguf:0.0.5")
    
    // Coroutines
    api("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    
    // IO
    implementation("org.jetbrains.kotlinx:kotlinx-io-core:0.3.0")
    implementation("org.jetbrains.kotlinx:kotlinx-io-jvm:0.3.0")
    
    // Testing
    testImplementation(kotlin("test"))
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    testImplementation("io.mockk:mockk:1.13.8")
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(17))
    }
}

tasks.test {
    useJUnitPlatform()
}
