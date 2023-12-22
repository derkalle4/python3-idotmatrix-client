<br/>
<p align="center">
  <a href="https://github.com/derkalle4/python3-idotmatrix-client">
    <img src="images/logo.png" alt="Logo" width="250" height="250">
  </a>

  <h3 align="center">Pixel Display Client</h3>

  <p align="center">
    control all your 16x16 or 32x32 pixel displays
    <br/>
    <br/>
    <a href="https://github.com/derkalle4/python3-idotmatrix-client"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/derkalle4/python3-idotmatrix-client/issues">Report Bug</a>
    .
    <a href="https://github.com/derkalle4/python3-idotmatrix-client/issues">Request Feature</a>
  </p>
</p>

![Downloads](https://img.shields.io/github/downloads/derkalle4/python3-idotmatrix-client/total) ![Contributors](https://img.shields.io/github/contributors/derkalle4/python3-idotmatrix-client?color=dark-green) ![Forks](https://img.shields.io/github/forks/derkalle4/python3-idotmatrix-client?style=social) ![Stargazers](https://img.shields.io/github/stars/derkalle4/python3-idotmatrix-client?style=social) ![Issues](https://img.shields.io/github/issues/derkalle4/python3-idotmatrix-client) ![License](https://img.shields.io/github/license/derkalle4/python3-idotmatrix-client) 

## Table Of Contents

* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## About The Project

This repository aims to reverse engineer the [iDotMatrix](https://play.google.com/store/apps/details?id=com.tech.idotmatrix&pli=1) Android App for pixel screen displays like [this one on Aliexpress](https://de.aliexpress.com/item/1005006105517779.html). The goal is to be able to control multiple pixel screen displays via a GUI, an Rest API and the command line.

The initial reason for this project was to have a foundation to update one or multiple pixel displays during live streams on Twitch or other platforms where one can use this to further automate interactions with the audience. Please let us know if you're using this to do so :)

## Built With

Love for Open Source :D and Python 3.

## Getting Started

To get a local copy up and running follow these simple example steps:

### Prerequisites

Please install the following for your distribution (Windows may work but it is untested):

* latest Python3
* Python3 Virtual Env

### Installation

1. Clone the repo

```sh
git clone https://github.com/derkalle4/python3-idotmatrix-client.git
```

2. Create virtual environment and install all dependencies

```sh
./create_venv.sh
```

## Usage

If you used the ./create_venv.sh you should use this command to run the app:

```sh
./run_in_venv.sh <YOUR_COMMAND_LINE_ARGUMENTS>
```
If you do not use a virtual environment the command will look like this:

```sh
python3 .\app.py <YOUR_COMMAND_LINE_ARGUMENTS>
```

#### command line arguments

##### --address (required)

Specifies the address of the pixel display device.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff
```

##### --sync-time

Sets the time of the device to the current local time.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --sync-time
```

###### --set-time

Sets the time of the device to any time you want.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --sync-time --set-time 18-12-2023-19:10:10
```

##### --rotate180degrees

Rotates the device display 180 degrees. True to rotate. False to disable rotation.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --rotate180degrees true
```

##### --togglescreen

Disables or enables the screen. Does not seem to work currently.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --togglescreen
```

##### --chronograph

Sets the mode of the cronograph:

- 0 = reset
- 1 = (re)start
- 2 = pause
- 3 = continue after pause

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --chronograph 0
```

##### --clock

Sets the mode of the clock:

- 0 = default
- 1 = christmas
- 2 = racing
- 3 = inverted full screen
- 4 = animated hourglass
- 5 = frame 1
- 6 = frame 2
- 7 = frame 3

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --clock 0
```

###### --clock-with-date

Shows the date in addition to the time.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --clock 0 --clock-with-date
```

###### --clock-24h

Shows the time in 24h format.

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --clock 0 --clock-24h
```

###### --clock-color

Sets the color of the clock in format <R0-255>-<G0-255>-<B0-255>

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --clock 0 --clock-color 255-0-0
```

##### --countdown

Sets the mode of the countdown:

- 0 = disable
- 1 = start
- 2 = pause
- 3 = restart

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --countdown 1
```

###### --countdown-time

Sets the time of the countdown in format <MINUTES>-<SECONDS>

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --countdown 1 --countdown-time 5-0
```

##### --fullscreen-color

Sets all pixels to the given color in format <R0-255>-<G0-255>-<B0-255>

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --fullscreen-color 255-255-255
```

##### --pixel-color

Sets one or multiple pixels to the given color in format <PIXEL-X>-<PIXEL-Y>-<R0-255>-<G0-255>-<B0-255>

```sh
./run_in_venv.sh --address 00:11:22:33:44:ff --fullscreen-color 255-255-255
```

## Roadmap

If you want to contribute please focus on the reverse-engineering part because my personal skills are not that good. Many thanks for all contributions! If you want to dive deep into other issues please check for "#TODO" comments in the source code as well.

* [ ] Reverse Engineering
    * [X] Chronograph
    * [X] Clock
    * [X] Countdown
    * [x] Graffiti Board
    * [X] DIY-Mode
    * [ ] Animated Images
    * [ ] Cloud-API to download images
    * [ ] Cloud-API to upload images to device
    * [ ] Cloud-Firmware Update possible?
    * [X] Eco-Mode
    * [X] Fullscreen Color
    * [ ] MusicSync
    * [X] Scoreboard
    * [ ] bluetooth pasword protection
* [ ] build configuration file to manage (multiple) devices
* [ ] Build command line interface with all features to interact with the device
* [ ] Build RestAPI to interact with the device remotely
* [ ] Build GUI to allow non-technical people to use this software
* [ ] build search tool to find displays nearby
* [ ] make this software compatible with Windows and Linux
* [ ] provide executables for Windows

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/derkalle4/python3-idotmatrix-client/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/derkalle4/python3-idotmatrix-client/blob/main/CODE_OF_CONDUCT.md) before posting your first idea as well.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the GNU GENERAL PUBLIC License. See [LICENSE](https://github.com/derkalle4/python3-idotmatrix-client/blob/main/LICENSE) for more information.

## Authors

* [Kalle Minkner](https://github.com/derkalle4) - *Project Founder*
* [Jon-Mailes Graeffe](https://github.com/jmgraeffe) - *Co-Founder*

## Acknowledgements

* [Othneil Drew](https://github.com/othneildrew/Best-README-Template) - *README Template*
* [LordRippon](https://github.com/LordRippon) - *Reverse Engineering for the Displays*
* [8none1](https://github.com/8none1) - *Reverse Engineering for the Displays*
