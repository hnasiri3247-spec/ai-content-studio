import os

# خواندن فایل build.gradle.kts
with open("app/build.gradle.kts", "r", encoding="utf-8") as f:
    content = f.read()

# تغییر minSdk از 26 به 21
content = content.replace("minSdk = 26", "minSdk = 21")

# اضافه کردن signingConfig قبل از dependencies
signing_config = """
android {
    defaultConfig {
        applicationId = "com.aicontentstudio"
        minSdk = 21
        targetSdk = 34
        versionCode = 2
        versionName = "1.1"
    }
    signingConfigs {
        create("debug") {
            keyAlias = "androiddebugkey"
            keyPassword = "android"
            storeFile = file("debug.keystore")
            storePassword = "android"
        }
    }
    buildTypes {
        debug {
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}
"""

# جایگزینی بخش android
import re
content = re.sub(r'android\s*\{.*?\n\}', signing_config, content, flags=re.DOTALL)

with open("app/build.gradle.kts", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ تنظیمات APK اصلاح شد (minSdk=21, signing enabled)")
