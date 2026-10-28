gradle_path = "android/app/build.gradle"

gradle_template = """apply plugin: 'com.android.application'

android {
    namespace "com.alstra.astrastudio"
    compileSdk rootProject.ext.compileSdkVersion

    defaultConfig {
        applicationId "com.alstra.astrastudio"
        minSdkVersion rootProject.ext.minSdkVersion
        targetSdkVersion rootProject.ext.targetSdkVersion
        versionCode 1
        versionName "1.0"
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        aaptOptions {
             ignoreAssetsPattern '!.svn:!.git:!.ds_store:!*.scc:.*:!CVS:!thumbs.db:!picasa.ini:!*~'
        }
    }

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
}

repositories {
    flatDir{
        dirs 'libs'
    }
}

dependencies {
    implementation fileTree(dir: 'libs', include: ['*.jar'])
    implementation "androidx.appcompat:appcompat:$androidxAppCompatVersion"
    implementation project(':capacitor-android')
    testImplementation "junit:junit:$junitVersion"
    androidTestImplementation "androidx.test.ext:junit:$androidxJunitVersion"
    androidTestImplementation "androidx.test.espresso:espresso-core:$androidxEspressoCoreVersion"
    implementation project(':capacitor-cordova-android-plugins')
}

try {
    def servicesJSON = file('google-services.json')
    if (servicesJSON.text) {
        apply plugin: 'com.google.gms.google-services'
    }
} catch(Exception e) {
    logger.info("google-services.json not found, google-services plugin not applied. Push Notifications won't work")
}
"""

with open(gradle_path, "w", encoding="utf-8") as f:
    f.write(gradle_template)

print("✅ [FIX APPLIED]: android/app/build.gradle cleaned up successfully.")
