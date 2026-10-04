import os
import urllib.request
import zipfile
import glob

sdk_dir = os.path.expanduser("~/android-sdk")
os.makedirs(os.path.join(sdk_dir, "build-tools"), exist_ok=True)
os.makedirs(os.path.join(sdk_dir, "platforms"), exist_ok=True)

print("1. Downloading Build Tools 34.0.0 from Tencent Mirror...")
urllib.request.urlretrieve("https://mirrors.cloud.tencent.com/android/repository/build-tools_r34-linux.zip", "/tmp/bt.zip")
with zipfile.ZipFile("/tmp/bt.zip", 'r') as z:
    z.extractall(os.path.join(sdk_dir, "build-tools"))
os.remove("/tmp/bt.zip")

print("2. Downloading Platform 34 from Tencent Mirror...")
urllib.request.urlretrieve("https://mirrors.cloud.tencent.com/android/repository/android-34_r02.zip", "/tmp/plat.zip")
with zipfile.ZipFile("/tmp/plat.zip", 'r') as z:
    z.extractall(os.path.join(sdk_dir, "platforms"))
os.remove("/tmp/plat.zip")

# اطمینان از نام‌گذاری صحیح پوشه‌ها
for f in glob.glob(os.path.join(sdk_dir, "build-tools", "*")):
    if os.path.basename(f) != "34.0.0":
        os.rename(f, os.path.join(sdk_dir, "build-tools", "34.0.0"))

for f in glob.glob(os.path.join(sdk_dir, "platforms", "*")):
    if os.path.basename(f) != "android-34":
        os.rename(f, os.path.join(sdk_dir, "platforms", "android-34"))

print("✅ SDK components installed successfully!")
print("Now run: ./gradlew assembleDebug --no-daemon --no-parallel")
