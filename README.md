# iDotMatrix Python3 Client
This repository contains a reverse engineering project of the [iDotMatrix](https://play.google.com/store/apps/details?id=com.tech.idotmatrix&pli=1) Android App for pixel screen displays like [this one on Aliexpress](https://de.aliexpress.com/item/1005006105517779.html).

## Why do you reverse-engineer the app?
The main idea is to make use of these devices for my [livestreams](https://nerdiacs.tv) I did before LongCovid hit me hard. I wanted to have another additional gimmick for viewers to interact with when I am able to [stream](http://nerdiacs.stream) again.

The second idea was to avoid the use of an China-made App. I do not like having a 100MB+ App which has a lot of overhead, is slow and not really thoughtful when it comes to it's features.

## Do you need help?
Yes. There is still a lot of reverse-engineering to do:
- how does the DIY feature work? how to send pixel data to the device correct and efficient?
-  are there hidden features inside the device?
- what about the functions that are not referenced in the app (yet). Are they working? Can we make use of them?
- are there any buffer overflows to own the device?
- how does the API work?
    - does the APi have any security vulnerabilities to report to them?
    - API URLs from the Android App:
        - https://api.e-toys.cn/api/
        - https://tapi.e-toys.cn/api/
        - https://api.e-toys.cn/api/ResourceApp/getMaterialUnderCategory
        - https://api.e-toys.cn/api/ResourceApp/getFirmwareInfo
        - https://api.e-toys.cn/api/app/lastUpdate
        - https://api.e-toys.cn/api/app/count
        - https://api.e-toys.cn/api/App/add_app_status_info
        - https://api.e-toys.cn/api/App/add_app_crash
        - https://api.e-toys.cn/api/app/bluetoothFilter

## Roadmap
* [ ] Reverse Engineering
    * [X] Chronograph
    * [X] Clock
    * [X] Countdown
    * [ ] DIY-Mode
    * [ ] Animated Images
    * [ ] Cloud-API to download images
    * [ ] Cloud-API to upload images to device
    * [ ] Cloud-Firmware Update possible?
    * [X] Eco-Mode
    * [X] Fullscreen Color
    * [ ] MusicSync
    * [X] Scoreboard
    * [ ] bluetooth pasword protection
* [ ] Build command line interface with all features to interact with the device
    * [ ] build configuration file to manage (multiple) devices
    * [ ] build search tool to find displays nearby
    * [ ] build 

## how to use?
not usable yet