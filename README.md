<br/>

## About The Project

Fork based on https://github.com/derkalle4/python3-idotmatrix-client
Just slimmer using gif function for everything, on my 16x16 image is not working reliable
Used on a debian based system mtu size is handled by btstack for faster transmission

## Built With

* [Python 3](https://www.python.org/downloads/)
* [argparse](https://docs.python.org/3/library/argparse.html)
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [bleak](https://github.com/hbldh/bleak)
* [pillow](https://python-pillow.org)

##### --set-gif

Path to an GIF to display on the device. See --process-gif for more information! The [Demo GIF](https://opengameart.org/content/animated-pixel-torch) was downloaded from OpenGameArt.org.

###### --process-gif

If specified it will process the given image. If used, the Python3 library Pillow will be utilized to convert the given image to a GIF with the given amount of pixels (e.g. 32 for 32x32 or 16 for 16x16 pixels). Technically you could use all kind of sizes for the GIF. Keep in mind: processing could take some time depending on your computer and using larger GIFs may result in a bad image quality. You should hand-craft your GIFs in the correct format for best results!

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
