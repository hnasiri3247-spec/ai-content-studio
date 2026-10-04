# 1. تنظیم نسخه پلاگین به 8.5.2 (پایدارترین نسخه)
build_gradle = """plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
    id("com.google.dagger.hilt.android") version "2.51.1" apply false
    id("com.google.devtools.ksp") version "1.9.24-1.0.20" apply false
}"""
with open("build.gradle.kts", "w", encoding="utf-8") as f:
    f.write(build_gradle)

# 2. استفاده از مخزن هوشمند google() که در ترموکس بهتر کار می‌کند
settings_gradle = """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "AIContentStudio"
include(":app")
"""
with open("settings.gradle.kts", "w", encoding="utf-8") as f:
    f.write(settings_gradle)

# 3. تنظیم گریدل روی نسخه 8.7 (هماهنگی کامل با AGP 8.5.2)
wrapper_props = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.7-bin.zip
networkTimeout=300000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""
with open("gradle/wrapper/gradle-wrapper.properties", "w", encoding="utf-8") as f:
    f.write(wrapper_props)

print("✅ تنظیمات طلایی (AGP 8.5.2 + Gradle 8.7) با موفقیت اعمال شد!")


