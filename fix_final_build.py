import os
import shutil

base = "app/src/main/java/com/aicontentstudio"

# پاک کردن فایل‌های قدیمی و معیوب
if os.path.exists(base):
    shutil.rmtree(base)
os.makedirs(base, exist_ok=True)

# ۱. فایل build.gradle.kts ساده شده (بدون KSP و Hilt)
app_build = """plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}
android {
    namespace = "com.aicontentstudio"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.aicontentstudio"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.14"
    }
}
dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.3")
    implementation("androidx.activity:activity-compose:1.9.0")
    implementation(platform("androidx.compose:compose-bom:2024.06.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    debugImplementation("androidx.compose.ui:ui-tooling")
}
"""
with open("app/build.gradle.kts", "w", encoding="utf-8") as f:
    f.write(app_build)

# ۲. فایل MainActivity.kt سالم و ساده
main_activity = """package com.aicontentstudio
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    Greeting("AI Content Studio")
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(text = "سلام! اپلیکیشن $name با موفقیت ساخته شد.", modifier = modifier)
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MaterialTheme {
        Greeting("Android")
    }
}
"""
with open(f"{base}/MainActivity.kt", "w", encoding="utf-8") as f:
    f.write(main_activity)

print("✅ پروژه با موفقیت به حالت ساده و تضمینی تغییر یافت!")


