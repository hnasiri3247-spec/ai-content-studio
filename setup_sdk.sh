#!/bin/bash
set -e
echo "🚀 شروع تنظیم خودکار Android SDK برای Termux..."

# ۱. نصب پیش‌نیازها
pkg update -y
pkg install curl unzip -y

# ۲. تعریف مسیرها
SDK_DIR="$HOME/android-sdk"
CMDLINE_DIR="$SDK_DIR/cmdline-tools/latest"

# ۳. ساخت پوشه‌ها
mkdir -p "$CMDLINE_DIR"
mkdir -p "$SDK_DIR/licenses"

# ۴. دانلود cmdline-tools از آینه تنسنت
echo "📥 در حال دانلود ابزارهای خط فرمان..."
curl -L -o /tmp/cmdline.zip "https://mirrors.cloud.tencent.com/android/repository/commandlinetools-linux-11076708_latest.zip"

# ۵. استخراج و اصلاح ساختار پوشه‌ها
echo "📦 در حال استخراج..."
unzip -q -o /tmp/cmdline.zip -d /tmp/
mv /tmp/cmdline-tools/cmdline-tools/* "$CMDLINE_DIR/" 2>/dev/null || mv /tmp/cmdline-tools/* "$CMDLINE_DIR/" 2>/dev/null || true
rm -rf /tmp/cmdline-tools /tmp/cmdline.zip

# ۶. پذیرش خودکار قوانین
echo "✅ در حال پذیرش قوانین..."
yes | "$CMDLINE_DIR/bin/sdkmanager" --licenses --sdk_root="$SDK_DIR" > /dev/null 2>&1 || true

# ۷. دانلود پلتفرم ۳۴ و بیلد تولز ۳۴.۰.۰ از آینه تنسنت
echo "📥 در حال دانلود Platform 34 و Build-Tools 34.0.0..."
curl -L -o /tmp/plat.zip "https://mirrors.cloud.tencent.com/android/repository/platform-34_r02.zip"
curl -L -o /tmp/bt.zip "https://mirrors.cloud.tencent.com/android/repository/build-tools_r34-linux.zip"

# ۸. استخراج در مکان صحیح
echo "📦 در حال نصب اجزای SDK..."
mkdir -p "$SDK_DIR/platforms"
mkdir -p "$SDK_DIR/build-tools"
unzip -q -o /tmp/plat.zip -d "$SDK_DIR/platforms/"
unzip -q -o /tmp/bt.zip -d "$SDK_DIR/build-tools/"

# اصلاح نام پوشه‌ها در صورت نیاز
for dir in "$SDK_DIR/platforms"/*; do
    if [ -d "$dir" ] && [ "$(basename "$dir")" != "android-34" ]; then
        mv "$dir" "$SDK_DIR/platforms/android-34"
    fi
done

for dir in "$SDK_DIR/build-tools"/*; do
    if [ -d "$dir" ] && [ "$(basename "$dir")" != "34.0.0" ]; then
        mv "$dir" "$SDK_DIR/build-tools/34.0.0"
    fi
done

rm -f /tmp/plat.zip /tmp/bt.zip

# ۹. به‌روزرسانی فایل local.properties در پوشه پروژه
echo "sdk.dir=$SDK_DIR" > ~/android-ai-app-factory-work/AIContentStudio/local.properties

echo "🎉 تنظیم SDK با موفقیت کامل شد!"
