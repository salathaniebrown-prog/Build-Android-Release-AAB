import re

gradle_path = "android/app/build.gradle"

signing_config = """
    signingConfigs {
        release {
            storeFile file("../../astra-release-key.jks")
            storePassword "AstraSecure2026!"
            keyAlias "astra_key_alias"
            keyPassword "AstraSecure2026!"
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
"""

try:
    with open(gradle_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace existing buildTypes block or inject signingConfigs
    if "signingConfigs {" not in content:
        content = re.sub(r'buildTypes\s*\{[\s\S]*?\}', signing_config, content)
        with open(gradle_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ [SUCCESS]: Signing configurations injected into build.gradle.")
    else:
        print("ℹ️ [GRADLE]: Signing configurations already present.")

except Exception as e:
    print(f"❌ [GRADLE ERROR]: {e}")
