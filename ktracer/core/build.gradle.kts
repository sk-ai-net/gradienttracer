plugins {
    kotlin("jvm")
    `java-library`
}

dependencies {
    api(kotlin("stdlib"))

    // GGUF dependencies
    implementation(libs.skainet.core)
    implementation(libs.skainet.io)
    implementation(libs.skainet.gguf)
    implementation(libs.kotlinx.io.core)
    implementation(libs.kotlinx.coroutines)


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
