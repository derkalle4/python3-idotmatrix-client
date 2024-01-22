<br/>

## About The Project

Fork based on https://github.com/derkalle4/python3-idotmatrix-client, just slimmer using gif function for everything, because on my 16x16 image function is not working reliable. Used on a debian based system, therefore mtu size is handled by btstack for faster transmission

## Goals
* build a webserver accepting json formatted instructions
* accept png/gif data (serialized) which is then sent to the display
* accept on off commands (just set a black 1 frame gif, save png/gif before so state is restored keep it simple)

## Built With

* [Python 3](https://www.python.org/downloads/)
* [argparse](https://docs.python.org/3/library/argparse.html)
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [bleak](https://github.com/hbldh/bleak)
* [pillow](https://python-pillow.org)

## TODOs

Strip project form everything which is not needed

Measure standby power ("real of" and black frame gif)

Keep connection persistent with specified address (no autodiscovery planned, just use ``` sudo hcitool -i hci0 lescan ``` to scan for ble devices)

## License

Distributed under the GNU GENERAL PUBLIC License. See [LICENSE](https://github.com/derkalle4/python3-idotmatrix-client/blob/main/LICENSE) for more information.

## Authors

* [Christoph Butzhammer](https://github.com/butz6617)

## Acknowledgements

* [Kalle Minkner](https://github.com/derkalle4) - *Project Founder of forked project*
* [Jon-Mailes Graeffe](https://github.com/jmgraeffe) - *Co-Founder of forked project*
* [Othneil Drew](https://github.com/othneildrew/Best-README-Template) - *README Template*
* [LordRippon](https://github.com/LordRippon) - *Reverse Engineering for the Displays*
* [8none1](https://github.com/8none1) - *Reverse Engineering for the Displays*
* [schorsch3000](https://github.com/schorsch3000) - *smaller fixes*
* [tekka007](https://github.com/tekka007) - *code refactoring and reverse engineering*
* [inselberg](https://github.com/inselberg) - *Reverse Engineering for the Displays*
