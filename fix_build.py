# اصلاح نسخه پلاگین به نسخه فوق‌العاده پایدار 8.4.0
with open("build.gradle.kts", "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("8.5.0", "8.4.0")
with open("build.gradle.kts", "w", encoding="utf-8") as f:
    f.write(content)

# نوشتن تنظیمات مخزن با آدرس مستقیم و بدون تغییرمسیر گوگل
settings_content = """pluginManagement {
    repositories {
        maven { url = uri("https://dl.google.com/dl/android/maven2/") }
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        maven { url = uri("https://dl.google.com/dl/android/maven2/") }
        mavenCentral()
    }
}
rootProject.name = "AIContentStudio"
include(":app")
"""
with open("settings.gradle.kts", "w", encoding="utf-8") as f:
    f.write(settings_content)

print("✅ تنظیمات با موفقیت اصلاح شد (نسخه پایدار 8.4.0 و آدرس مستقیم گوگل)")


