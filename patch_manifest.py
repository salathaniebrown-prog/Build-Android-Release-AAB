import re

manifest_path = "android/app/src/main/AndroidManifest.xml"

try:
    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'android:usesCleartextTraffic="true"' not in content:
        content = re.sub(
            r'<application\b',
            '<application android:usesCleartextTraffic="true"',
            content
        )
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ [SUCCESS]: Cleartext traffic enabled for local server calls.")
    else:
        print("ℹ️ [MANIFEST]: Cleartext traffic already enabled.")

except Exception as e:
        print(f"❌ [MANIFEST ERROR]: {e}")
