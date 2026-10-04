import os
import subprocess
import zipfile
import urllib.request

ANDROID_HOME = os.path.expanduser("~/android-sdk")
os.makedirs(ANDROID_HOME, exist_ok=True)

url = "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
zip_path = os.path.join(ANDROID_HOME, "cmdline-tools.zip")

if not os.path.exists(zip_path):
    print("Downloading Android SDK command-line tools (~150MB)...")
    urllib.request.urlretrieve(url, zip_path)

print("Extracting...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(ANDROID_HOME)

latest_dir = os.path.join(ANDROID_HOME, "cmdline-tools", "latest")
if not os.path.exists(latest_dir):
    os.makedirs(os.path.join(ANDROID_HOME, "cmdline-tools"), exist_ok=True)
    inner = os.path.join(ANDROID_HOME, "cmdline-tools", "cmdline-tools")
    if os.path.exists(inner):
        os.rename(inner, latest_dir)

sdkmanager = os.path.join(latest_dir, "bin", "sdkmanager")
if os.path.exists(sdkmanager):
    os.chmod(sdkmanager, 0o755)
    
    print("Accepting licenses...")
    subprocess.run([sdkmanager, f"--sdk_root={ANDROID_HOME}", "--licenses"], input=b"y\ny\ny\ny\ny\ny\ny\ny\n")
    
    print("Installing platforms and build-tools (this may take a few minutes)...")
    subprocess.run([sdkmanager, f"--sdk_root={ANDROID_HOME}", "platforms;android-34", "build-tools;34.0.0"])
    
    print("SDK installed at:", ANDROID_HOME)
    
    with open("local.properties", "w") as f:
        f.write(f"sdk.dir={ANDROID_HOME}\n")
    print("✅ local.properties created successfully!")
else:
    print("❌ Error: sdkmanager not found")
