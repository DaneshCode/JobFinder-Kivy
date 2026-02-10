[app]
# Application info
title = Job Finder
package.name = jobfinder
package.domain = com.jobfinder

# Source code
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db

# Versioning
version = 1.0.0

# Application requirements
requirements = python3,kivy==2.3.0,kivymd==2.0.1.dev0,pillow,materialyoucolor,exceptiongroup,android,pyjnius

# Android configuration
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.arch = arm64-v8a

# Android app settings
android.accept_sdk_license = True
android.release_artifact = apk

# Orientation
orientation = portrait

# Fullscreen
fullscreen = 0

# Icon (will use default if not present)
# icon.filename = %(source.dir)s/assets/icon.png

# Presplash (will use default if not present)
# presplash.filename = %(source.dir)s/assets/presplash.png

# iOS configuration (optional)
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2

# OSX specific
osx.python_version = 3
osx.kivy_version = 2.3.0

[buildozer]
# Buildozer settings
log_level = 2
warn_on_root = 0

# Build directory
# build_dir = ./.buildozer

# Binary directory
# bin_dir = ./bin
