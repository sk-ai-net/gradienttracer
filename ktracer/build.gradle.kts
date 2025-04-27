plugins {
    kotlin("jvm") version "2.1.0"
    application
}

group = "net.skai.ktracer"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
    maven {
        url = uri("https://maven.pkg.github.com/sk-ai-net/skainet")
        credentials {
            username = System.getenv("GITHUB_USER")
            password = System.getenv("GITHUB_TOKEN")
        }
    }
}

dependencies {
    implementation("sk.ai.net:gguf:0.0.5")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    implementation(libs.kotlinx.io.core)


    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}

kotlin {
    jvmToolchain(17)
}

application {
    mainClass.set("net.skai.ktracer.MainKt")
}
