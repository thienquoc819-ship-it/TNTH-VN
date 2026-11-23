[app]

title = TNTH VN
package.name = tnthvn
package.domain = vn.tnth

source.dir = .
source.include_exts = py,png,jpg,kv
version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

log_level = 2
warn_on_root = 1
android.build_tools = 34.0.0
