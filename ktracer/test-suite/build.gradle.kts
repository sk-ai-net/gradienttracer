plugins {
    kotlin("jvm")
    `java-library`
}


dependencies {
    implementation(project(":core"))
    implementation(libs.skainet.core)
    implementation(libs.skainet.io)
    implementation(libs.skainet.gguf)


    testImplementation(kotlin("test"))
}

kotlin {
    jvmToolchain(17)
}
