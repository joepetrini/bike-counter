cordova build ios --device
cd platforms/ios/build/device
/usr/bin/xcrun -sdk iphoneos PackageApplication "$(pwd)/Bikecount.app" -o "$(pwd)/Bikecount.ipa"
