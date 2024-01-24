<br/>

## About The Project

Fork based on https://github.com/derkalle4/python3-idotmatrix-client, just slimmer using gif function for image and gifs, because on my 16x16 tge image function was not working reliable. Used on a debian based system, therefore mtu size is handled by btstack for faster transmission. I dont know about win or other OSs.

## How to
  * change port number to whatever you want inside app.py
  * find out the bluetooth address of your display eg `sudo hcitool -i hci0 lescan` for debain based os
  * run `python3 app.py` (you maybe need to install dependencies)
  * connect with your browser to `http://HOSTIP:PORT/docs`
  * first you can connect to your display with `http://HOSTIP:PORT/BLEconnect/ADDRESS/PIXELS` with ADDRESS being the bluetooth address without the ':' (non case sensitive) and pixels being the size of your display (most times 16 or 32)
  * you can check the ble status with `http://HOSTIP:PORT/BLEstatus`
  * you can upload .gif or .png with POST to `http://HOSTIP:PORT/upload`, this immediatly sends it to the display if connected and the file is saved inside the upload directory (doubles will overwrite without error)
  * you can set already uploaded files with `http://HOSTIP:PORT/uselocal/FILENAME` and can retrive a list of available files with `http://HOSTIP:PORT/getFileNames`
  * you can use `/shutdown` to stop the server or CTRL+C on the host
  * other basic commands are:
   `/brightness/{brightness}` 
   `/BLEdisconnect`
   `/turnon`
   `/turnoff` (this does not disconnect the display, only turns of LEDs)
  * you can integrate it into hone assistant with the contents of automations.yaml and configuration.yaml (host, port, macaddress and pixels need to be adjusted)


## Goals
- [x] build a webserver accepting rest commands 
- [x] accept png/gif data which is then sent to the display
- [x] accept on off commands 
- [x] accept brightness commands
- [x] accept shutdown command
- [x] save files and set via filename
- [x] retrieve local file list
- [x] homeassistant example configuration.yaml and automations.yaml
- [ ] option to save files processed

## Built With

* [Python 3](https://www.python.org/downloads/)
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [bleak](https://github.com/hbldh/bleak)
* [pillow](https://python-pillow.org)
* [fastapi](https://fastapi.tiangolo.com/)
* [uvicorn](https://www.uvicorn.org/)

## TODOs

Strip project form everything unneeded

Move everything into a docker

## Notes 

If you really need other functions via REST, feel free to implement them yourself, the "old" code is still in the project and it can easily be integrated. Or if you really struggle you can open a issue and I will implement it. (I wont do any further reverse engineering)

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
