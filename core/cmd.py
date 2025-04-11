# python imports
from datetime import datetime
import logging
import os
from PIL import Image
import time
from utils import utils

# idotmatrix imports
from idotmatrix import ConnectionManager
from idotmatrix import Chronograph
from idotmatrix import Clock
from idotmatrix import Common
from idotmatrix import Countdown
from idotmatrix import Gif
from idotmatrix import Image
from idotmatrix import FullscreenColor
from idotmatrix import MusicSync
from idotmatrix import Scoreboard
from idotmatrix import Graffiti
from idotmatrix import Text


class CMD:
    conn = ConnectionManager()
    logging = logging.getLogger("idotmatrix." + __name__)

    def add_arguments(self, parser):
        # scan
        parser.add_argument(
            "--scan",
            action="store_true",
            help="scans all bluetooth devices in range for iDotMatrix displays",
        )
        # test
        parser.add_argument(
            "--test",
            action="store_true",
            help="run the test function from the command line class",
        )
        # time sync
        parser.add_argument(
            "--sync-time",
            action="store_true",
            help="sync time to device",
        )
        parser.add_argument(
            "--set-time",
            action="store",
            help="optionally set time to sync to device (use with --sync-time)",
            default=datetime.now().strftime("%d-%m-%Y-%H:%M:%S"),
        )
        # device screen rotation
        parser.add_argument(
            "--flip-screen",
            type=str,
            choices=["true", "false"],
            help="flips screen (true = flip, false = normal)",
        )
        # screen toggle
        parser.add_argument(
            "--toggle-screen-freeze",
            action="store_true",
            help="freezes or unfreezes the screen",
        )
        # enable or disable device screen
        parser.add_argument(
            "--screen",
            type=str,
            choices=["on", "off"],
            help="turns screen on or off",
        )
        # brightness
        parser.add_argument(
            "--set-brightness",
            action="store",
            help="sets the brightness of the screen in percent: range 5..100",
        )
        # password
        parser.add_argument(
            "--set-password",
            action="store",
            help="sets password",
        )
        # chronograph
        parser.add_argument(
            "--chronograph",
            action="store",
            help="sets the chronograph mode: 0 = reset, 1 = (re)start, 2 = pause, 3 = continue after pause",
        )
        # clock
        parser.add_argument(
            "--clock",
            action="store",
            help="sets the clock mode: 0 = default, 1 = christmas, 2 = racing, 3 = inverted full screen, 4 = animated hourglass, 5 = frame 1, 6 = frame 2, 7 = frame 3",
        )
        parser.add_argument(
            "--clock-with-date",
            action="store_true",
            help="shows the current date in addition to the current time.",
        )
        parser.add_argument(
            "--clock-24h",
            action="store_true",
            help="shows the current time in 24h format.",
        )
        parser.add_argument(
            "--clock-color",
            action="store",
            help="sets the color of the clock. Format: <R0-255>-<G0-255>-<B0-255> (example: 255-255-255)",
            default="255-255-255",
        )
        # countdown
        parser.add_argument(
            "--countdown",
            action="store",
            help="sets the countdown mode: 0 = disable, 1 = start, 2 = pause, 3 = restart",
        )
        parser.add_argument(
            "--countdown-time",
            action="store",
            type=str,
            help="sets the countdown mode: <MINUTES>-<SECONDS> (example: 10-30)",
            default="5-0",
        )
        # fullscreen color
        parser.add_argument(
            "--fullscreen-color",
            action="store",
            help="sets a fullscreen color. Format: <R0-255>-<G0-255>-<B0-255> (example: 255-255-255)",
        )
        # pixel color
        parser.add_argument(
            "--pixel-color",
            action="append",
            help="sets a pixel to a specific color. Could be used multiple times. Format: <PIXEL-X>-<PIXEL-Y>-<R0-255>-<G0-255>-<B0-255> (example: 0-0-255-255-255)",
            nargs="+",
        )
        # scoreboard
        parser.add_argument(
            "--scoreboard",
            action="store",
            help="shows the scoreboard with the given scores. Format: <0-999>-<0-999>",
        )
        # image upload
        parser.add_argument(
            "--image",
            action="store",
            help="enables or disables the image mode (true = enable, false = disable)",
        )
        parser.add_argument(
            "--set-image",
            action="store",
            help="uploads a given image file (fastest is png, max. pixel depending on your display). Format: ./path/to/image.png",
        )
        parser.add_argument(
            "--process-image",
            action="store",
            help="processes the image instead of sending it raw (useful when the size does not match or it is not a png). Format: <AMOUNT_PIXEL>",
        )
        # gif upload
        parser.add_argument(
            "--set-gif",
            action="store",
            help="uploads a given gif file (pixel depending on your display). Format: ./path/to/image.gif",
        )
        parser.add_argument(
            "--process-gif",
            action="store",
            help="processes the gif instead of sending it raw (useful when the size does not match). Format: <AMOUNT_PIXEL>",
        )
        # text upload
        parser.add_argument(
            "--set-text",
            action="store",
            type=str,
            help="sets the given text on your display.",
        )
        parser.add_argument(
            "--text-font-path",
            action="store",
            type=str,
            help="sets the given font for the text.",
        )
        parser.add_argument(
            "--text-size",
            action="store",
            type=int,
            help="Text size. Defaults to 16.",
            default=16,
        )
        parser.add_argument(
            "--text-mode",
            action="store",
            type=int,
            help="Text mode. Defaults to 0. 0 = replace text, 1 = marquee, 2 = reversed marquee, 3 = vertical rising marquee, 4 = vertical lowering marquee, 5 = blinking, 6 = fading, 7 = tetris, 8 = filling",
            default=0,
        )
        parser.add_argument(
            "--text-speed",
            action="store",
            type=int,
            help="speed (int, optional): Speed of Text. Defaults to 95.",
            default=95,
        )
        parser.add_argument(
            "--text-color-mode",
            action="store",
            type=int,
            help="Text Color Mode. Defaults to 1. 0 = white, 1 = use given RGB color, 2,3,4,5 = rainbow modes",
            default=1,
        )
        parser.add_argument(
            "--text-color",
            action="store",
            type=str,
            help="sets the text color. Format: <R0-255>-<G0-255>-<B0-255> (example: 255-255-255)",
            default="255-0-0",
        )
        parser.add_argument(
            "--text-bg-mode",
            action="store",
            type=int,
            help="Text Background Mode. Defaults to 0. 0 = black, 1 = use given RGB color",
            default=0,
        )
        parser.add_argument(
            "--text-bg-color",
            action="store",
            type=str,
            help="sets the text background color. Format: <R0-255>-<G0-255>-<B0-255> (example: 255-255-255)",
            default="255-255-255",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Sends the reset command to the display. This can sometimes help fix persistent glitches.",
        )
        parser.add_argument(
            "--weather-api-key",
            action="store",
            type=str,
            help="The 'https://weatherapi.com' api key for weather commands.",
        )
        parser.add_argument(
            "--weather-image-query",
            action="store",
            type=str,
            help="Query to send weatherapi, e.g. city name. Displays an image representing the current weather. \nThis arg requires you to also pass '--process-image' with your pixel size, and the '--weather-api-key' with your 'https://weatherapi.com/' API key.",
        )
        parser.add_argument(
            "--weather-gif-query",
            action="store",
            type=str,
            help="Query to send weatherapi, e.g. city name. Displays a gif representing current weather. \nThis arg requires you to also pass '--process-image' with your pixel size, and the '--weather-api-key' with your 'https://weatherapi.com/' API key.",
        )

    async def run(self, args):
        self.logging.info("initializing command line")
        address = None
        if args.scan:
            await self.conn.scan()
            quit()
        if args.address:
            self.logging.debug("using --address")
            address = args.address
        elif "IDOTMATRIX_ADDRESS" in os.environ:
            self.logging.debug("using IDOTMATRIX_ADDRESS")
            address = os.environ["IDOTMATRIX_ADDRESS"]
        if address is None:
            self.logging.error("no device address given")
            quit()
        elif str(address).lower() == "auto":
            await self.conn.connectBySearch()
        else:
            await self.conn.connectByAddress(address)
        # arguments which can be run in parallel
        if args.sync_time:
            await self.sync_time(args.set_time)
        if args.flip_screen:
            await self.flip_screen(args.flip_screen)
        if args.toggle_screen_freeze:
            await self.toggle_screen_freeze()
        if args.screen:
            await self.screen(args.screen)
        if args.set_brightness:
            await self.set_brightness(int(args.set_brightness))
        if args.set_password:
            await self.set_password(args.set_password)
        if args.reset:
            await self.reset(args)
        # arguments which cannot run in parallel
        if args.test:
            await self.test()
        elif args.chronograph:
            await self.chronograph(args.chronograph)
        elif args.clock:
            await self.clock(args)
        elif args.countdown:
            await self.countdown(args)
        elif args.fullscreen_color:
            await self.fullscreenColor(args.fullscreen_color)
        elif args.pixel_color:
            await self.pixelColor(args.pixel_color)
        elif args.scoreboard:
            await self.scoreboard(args.scoreboard)
        elif args.image:
            await self.image(args)
        elif args.set_gif:
            await self.gif(args)
        elif args.set_text:
            await self.text(args)
        elif args.weather_image_query:
            await self.weather_image_query(args)
        elif args.weather_gif_query:
            await self.weather_gif_query(args)

    async def test(self):
        """Tests all available options for the device"""
        self.logging.info("starting test of device")
        ## chronograph
        await Chronograph().setMode(1)
        time.sleep(5)
        await Chronograph().setMode(0)
        time.sleep(1)
        ## clock
        await Clock().setTimeIndicator(True)
        await Clock().setMode(0, True, True)
        time.sleep(5)
        ## countdown
        await Countdown().setMode(1, 0, 5)
        time.sleep(5)
        await Countdown().setMode(0, 0, 5)
        ## fullscreen color
        await FullscreenColor().setMode(255, 0, 0)
        time.sleep(5)
        ## scoreboard
        await Scoreboard().setMode(1, 0)
        time.sleep(1)
        await Scoreboard().setMode(1, 1)
        time.sleep(1)
        await Scoreboard().setMode(1, 2)
        time.sleep(1)
        await Scoreboard().setMode(2, 2)
        ## graffiti
        # load graffiti board and color pixel 0,0 red
        await Graffiti().setPixel(255, 0, 0, 0, 0)
        # load graffitti board and color pixel 1,1 green
        await Graffiti().setPixel(0, 255, 0, 1, 1)
        # load graffitti board and color pixel 2,2 blue
        await Graffiti().setPixel(0, 0, 255, 2, 2)
        time.sleep(5)
        ## diy image (png)
        await Image().setMode(1)
        await Image().uploadUnprocessed("./images/demo_32.png")

    async def sync_time(self, argument):
        """Synchronize local time to device"""
        self.logging.info("starting to synchronize time")
        try:
            date = datetime.strptime(argument, "%d-%m-%Y-%H:%M:%S")
        except ValueError:
            self.logging.error(
                "wrong format of --set-time: please use dd-mm-YYYY-HH-MM-SS"
            )
            quit()
        await Common().setTime(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second,
        )

    async def flip_screen(self, argument: str) -> None:
        """flip device screen 180 degrees"""
        self.logging.info("flipping screen")
        await Common().flipScreen(argument.upper() == "TRUE")

    async def toggle_screen_freeze(self) -> None:
        """toggles the screen freeze"""
        self.logging.info("toggling screen freeze")
        await Common().freezeScreen()

    async def screen(self, argument: str) -> None:
        """turns the screen on or off"""
        if argument.upper() == "ON":
            self.logging.info("turning screen on")
            await Common().screenOn()
        else:
            self.logging.info("turning screen off")
            await Common().screenOff()

    async def set_brightness(self, argument: int) -> None:
        """sets the brightness of the screen"""
        if argument in range(5, 101):
            self.logging.info(f"setting brightness of the screen: {argument}%")
            await Common().setBrightness(argument)
        else:
            self.logging.error("brightness out of range (should be between 5 and 100)")

    async def set_password(self, argument: str) -> None:
        """sets connection password"""
        try:
            conv_password = int(argument)
            if len(argument) == 6 and conv_password in range(0, 1000000):
                self.logging.info(f"setting password: {argument}")
                await Common().setPassword(conv_password)
            else:
                self.logging.error(
                    f"Password should be 6 digits long and in range 000000...999999"
                )
        except ValueError:
            self.logging.error(f"Invalid integer: {argument}")

    async def chronograph(self, argument):
        """sets the chronograph mode"""
        self.logging.info("setting chronograph mode")
        if int(argument) in range(0, 4):
            await Chronograph().setMode(int(argument))
        else:
            self.logging.error("wrong argument for chronograph mode")
            quit()

    async def clock(self, args):
        """sets the clock mode"""
        self.logging.info("setting clock mode")
        if int(args.clock) in range(0, 8):
            color = args.clock_color.split("-")
            if len(color) < 3:
                self.logging.error("wrong argument for --clock-color")
                quit()
            await Clock().setMode(
                style=int(args.clock),
                visibleDate=args.clock_with_date,
                hour24=args.clock_24h,
                r=int(color[0]),
                g=int(color[1]),
                b=int(color[2]),
            )
        else:
            self.logging.error("wrong argument for --clock")
            quit()

    async def countdown(self, args: str) -> None:
        """sets the countdown mode"""
        self.logging.info("setting countdown mode")
        mode = int(args.countdown)
        if mode not in range(0, 4):
            self.logging.error("wrong argument for --countdown")
            quit()
        times = args.countdown_time.split("-")
        if not len(times) == 2:
            self.logging.error("wrong argument for --countdown-time")
            quit()
        minutes, seconds = [int(x) for x in times]
        if minutes not in range(0, 100):
            self.logging.error(
                "wrong argument for --countdown-time - minutes must be between 0 and 99"
            )
            quit()
        if seconds not in range(0, 60):
            self.logging.error(
                "wrong argument for --countdown-time - seconds must be between 0 and 59"
            )
            quit()
        if minutes == 0 and seconds == 0:
            self.logging.error(
                "wrong argument for --countdown-time - time cannot be zero"
            )
            quit()
        await Countdown().setMode(
            mode=mode,
            minutes=minutes,
            seconds=seconds,
        )

    async def fullscreenColor(self, argument):
        """sets a given fullscreen color"""
        self.logging.info("setting fullscreen color")
        color = argument.split("-")
        if len(color) != 3:
            self.logging.error("wrong argument for --fullscreen-color")
            quit()
        await FullscreenColor().setMode(
            int(color[0]),
            int(color[1]),
            color[2],
        )

    async def pixelColor(self, argument):
        """sets the given pixel colors"""
        self.logging.info("setting pixel color")
        if len(argument) <= 0:
            self.logging.error("wrong argument for --pixel-color")
            quit()
        pixels = []
        # get all pixels to set
        for params in argument:
            for pixel in params:
                pixels.append(pixel)
        # validate all pixels and send them
        for pixel in pixels:
            split = pixel.split("-")
            # check if we got all data
            if len(split) != 5:
                self.logging.error(
                    "need exactly 5 arguments for a single pixel in --pixel-color"
                )
                quit()
            # TODO: proper check if we are within the pixel range of the device
            # TODO: maybe we can use a delimiter to make use of the MTU size (sending chunks instead of separate requests)
            # TODO: when filling 32x32 pixels it seems to have trouble to send all pixels. One pixel will be "forgotten" somehow
            await Graffiti().setPixel(
                x=int(split[0]),
                y=int(split[1]),
                r=int(split[2]),
                g=int(split[3]),
                b=int(split[4]),
            )

    async def scoreboard(self, argument):
        """sets given score on the scoreboard and shows it"""
        self.logging.info("setting scoreboard mode")
        scores = argument.split("-")
        if len(scores) != 2:
            self.logging.error("wrong argument for --scoreboard")
            quit()
        if int(scores[0]) < 0 or int(scores[1]) < 0:
            self.logging.error("no negative values allowed for --scoreboard")
            quit()
        if int(scores[0]) > 999 or int(scores[1]) > 999:
            self.logging.error("exceeded maximum value of 999 for --scoreboard")
            quit()
        await Scoreboard().setMode(
            count1=int(scores[0]),
            count2=int(scores[1]),
        )

    async def image(self, args):
        """enables or disables the image mode and uploads a given image file"""
        self.logging.info("setting image")
        image = Image()
        if args.image == "false":
            await image.setMode(
                mode=0,
            )
        else:
            await image.setMode(
                mode=1,
            )
            if args.set_image:
                if args.process_image:
                    await image.uploadProcessed(
                        file_path=args.set_image,
                        pixel_size=int(args.process_image),
                    )
                else:
                    await image.uploadUnprocessed(
                        file_path=args.set_image,
                    )

    async def gif(self, args):
        """enables or disables the gif mode and uploads a given gif file"""
        self.logging.info("setting (animated) GIF")
        gif = Gif()
        if args.process_gif:
            await gif.uploadProcessed(
                file_path=args.set_gif,
                pixel_size=int(args.process_gif),
            )
        else:
            await gif.uploadUnprocessed(
                file_path=args.set_gif,
            )

    async def text(self, args):
        """sets the given text on the device"""
        self.logging.info("setting text")
        text = Text()
        text_color = args.text_color.split("-")
        if len(text_color) != 3:
            self.logging.error("wrong argument for --text-color")
            quit()
        bg_color = args.text_bg_color.split("-")
        if len(bg_color) != 3:
            self.logging.error("wrong argument for --text-bg-color")
            quit()
        await text.setMode(
            text=args.set_text,
            font_size=args.text_size,
            font_path=args.text_font_path,
            text_mode=args.text_mode,
            speed=args.text_speed,
            text_color_mode=args.text_color_mode,
            text_color=(int(text_color[0]), int(text_color[1]), int(text_color[2])),
            text_bg_mode=args.text_bg_mode,
            text_bg_color=(int(bg_color[0]), int(bg_color[1]), int(bg_color[2])),
        )

    async def reset(self, args):
        # The following was figured out by 8none1:
        # https://github.com/8none1/idotmatrix/commit/1a08e1e9b82d78427ab1c896c24c2a7fb45bc2f0
        reset_packets = [
            bytes(bytearray.fromhex("04 00 03 80")),
            bytes(bytearray.fromhex("05 00 04 80 50")),
            ]
        for packet in reset_packets:
            await self.conn.send(packet)

    async def weather_image_query(self, args):
        api_key = args.weather_api_key
        pixels  = args.process_image
        if pixels==None:
            self.logging.error("The pixel-size wasn't given. "
                               "The arg '--process-image' must be used to provide this, e.g. '--process-image 32'.")
            return

        try:
            img_path = utils.get_weather_img(args.weather_image_query, pixels, api_key)
        except Exception as e:
            self.logging.error(f"failed to get weather info or make weather image: {e}")
        else:
            setattr(args, 'image', img_path)
            self.image(args)

    async def weather_gif_query(self, args):
        api_key = args.weather_api_key
        pixels  = args.process_image
        if pixels==None:
            self.logging.error("The pixel-size wasn't given. "
                               "The arg '--process-gif' must be used to provide this, e.g. '--process-gif 32'.")
            return

        try:
            gif_path = utils.get_weather_gif(args.weather_gif_query, pixels, api_key)
        except Exception as e:
            self.logging.error(f"failed to get weather info or make weather gif: {e}")
        else:
            setattr(args, 'gif', gif_path)
            self.gif(args)
