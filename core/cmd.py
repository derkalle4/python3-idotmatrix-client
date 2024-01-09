# python imports
from datetime import datetime
import logging
import os
from PIL import Image
import time

# idotmatrix imports
from .bluetooth import Bluetooth
from .idotmatrix.chronograph import Chronograph
from .idotmatrix.clock import Clock
from .idotmatrix.common import Common
from .idotmatrix.countdown import Countdown
from .idotmatrix.gif import Gif
from .idotmatrix.image import Image
from .idotmatrix.fullscreenColor import FullscreenColor
from .idotmatrix.musicSync import MusicSync
from .idotmatrix.scoreboard import Scoreboard
from .idotmatrix.graffiti import Graffiti


class CMD:
    bluetooth = None
    logging = logging.getLogger("idotmatrix." + __name__)

    def add_arguments(self, parser):
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
            choices=["on", "off"],
            help="flips screen (on = flip, off = normal)",
        )
        # screen toggle
        parser.add_argument(
            "--toggle-screen",
            action="store_true",
            help="toggles the screen on or off",
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

    async def run(self, args):
        self.logging.info("initializing command line")
        address = None
        if args.address:
            self.logging.debug("using --address")
            address = args.address
        elif "IDOTMATRIX_ADDRESS" in os.environ:
            self.logging.debug("using IDOTMATRIX_ADDRESS")
            address = os.environ["IDOTMATRIX_ADDRESS"]
        if address is None:
            self.logging.error("no device address given")
            quit()
        else:
            self.bluetooth = Bluetooth(address)
        # arguments which can be run in parallel
        if args.sync_time:
            await self.sync_time(args.set_time)
        if args.flip_screen:
            await self.flip_screen(args.flip_screen)
        if args.toggle_screen:
            await self.toggle_screen()
        if args.set_brightness:
            await self.set_brightness(args.set_brightness)
        if args.set_password:
            await self.set_password(args.set_password)
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

    async def test(self):
        """Tests all available options for the device"""
        self.logging.info("starting test of device")
        ## chronograph
        await self.bluetooth.send(Chronograph().setChronograph(1))
        time.sleep(5)
        await self.bluetooth.send(Chronograph().setChronograph(0))
        time.sleep(1)
        ## clock
        await self.bluetooth.send(Clock().setTimeIndicator(True))
        await self.bluetooth.send(Clock().setClockMode(0, True, True))
        time.sleep(5)
        ## countdown
        await self.bluetooth.send(Countdown().setCountdown(1, 0, 5))
        await self.bluetooth.send(Countdown().setCountdown(0, 0, 5))
        time.sleep(5)
        ## fullscreen color
        await self.bluetooth.send(FullscreenColor().setColor(255, 0, 0))
        time.sleep(5)
        ## scoreboard
        await self.bluetooth.send(Scoreboard().setScoreboard(1, 0))
        time.sleep(1)
        await self.bluetooth.send(Scoreboard().setScoreboard(1, 1))
        time.sleep(1)
        await self.bluetooth.send(Scoreboard().setScoreboard(1, 2))
        time.sleep(1)
        await self.bluetooth.send(Scoreboard().setScoreboard(2, 2))
        ## graffiti
        # load graffiti board and color pixel 0,0 red
        await self.bluetooth.send(Graffiti().setPixelColor(255, 0, 0, 0, 0))
        # load graffitti board and color pixel 1,1 green
        await self.bluetooth.send(Graffiti().setPixelColor(0, 255, 0, 1, 1))
        # load graffitti board and color pixel 2,2 blue
        await self.bluetooth.send(Graffiti().setPixelColor(0, 0, 255, 2, 2))
        time.sleep(5)
        ## diy image (png)
        await self.bluetooth.send(Image().show(1))
        await self.bluetooth.send(Image().upload_unprocessed("./demo.png"))

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
        await self.bluetooth.send(
            Common().set_time(
                date.year,
                date.month,
                date.day,
                date.hour,
                date.minute,
                date.second,
            )
        )

    async def flip_screen(self, argument: str) -> None:
        """flip device screen 180 degrees"""
        self.logging.info("flipping screen")
        await self.bluetooth.send(Common().flip_screen(argument.upper() == "ON"))
    
    async def toggle_screen(self) -> None:
        """toggles the screen on or off"""
        self.logging.info("toggling screen")
        await self.bluetooth.send(Common().toggle_screen())

    async def set_brightness(self, argument: int) -> None:
        """sets the brightness of the screen"""
        try:
            conv_brightness = int(argument)
            if conv_brightness in range (5, 101):
                self.logging.info(f"setting brightness of the screen: {argument}%")
                await self.bluetooth.send(Common().set_screen_brightness(brightness_percent=conv_brightness))
            else:
                self.logging.error("brightness out of range")
        except ValueError:
            self.logging.error(f"Invalid integer: {argument}")
                    
    async def set_password(self, argument: str) -> None:
        """sets connection password"""
        try:
            conv_password = int(argument)
            if len(argument) == 6 and conv_password in range(0, 1000000):
                self.logging.info(f"setting password: {argument}")
                await self.bluetooth.send(Common().set_password(conv_password))
            else:
                self.logging.error(f"Password should be 6 digits long and in range 000000...999999")
        except ValueError:
            self.logging.error(f"Invalid integer: {argument}")
            
    async def chronograph(self, argument):
        """sets the chronograph mode"""
        self.logging.info("setting chronograph mode")
        if int(argument) in range(0, 4):
            await self.bluetooth.send(Chronograph().setChronograph(int(argument)))
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
            await self.bluetooth.send(
                Clock().setClockMode(
                    style=int(args.clock),
                    visibleDate=args.clock_with_date,
                    hour24=args.clock_24h,
                    r=int(color[0]),
                    g=int(color[1]),
                    b=int(color[2]),
                )
            )
        else:
            self.logging.error("wrong argument for --clock")
            quit()

    async def countdown(self, args):
        """sets the countdown mode"""
        self.logging.info("setting countdown mode")
        if not int(args.countdown) in range(0, 4):
            self.logging.error("wrong argument for --countdown")
            quit()
        times = args.countdown_time.split("-")
        if not len(times) == 2:
            self.logging.error("wrong argument for --countdown-time")
            quit()
        if int(times[0]) < 0 or int(times[0]) > 99:
            self.logging.error(
                "wrong argument for --countdown-time - minutes must be between 0 and 99"
            )
            quit()
        if int(times[1]) < 0 or int(times[1]) > 59:
            self.logging.error(
                "wrong argument for --countdown-time - seconds must be between 0 and 59"
            )
            quit()
        if int(times[0]) == 0 and int(times[1]) == 0:
            self.logging.error(
                "wrong argument for --countdown-time - time cannot be zero"
            )
            quit()
        await self.bluetooth.send(
            Countdown().setCountdown(
                mode=int(args.countdown),
                minutes=int(times[0]),
                seconds=int(times[1]),
            )
        )

    async def fullscreenColor(self, argument):
        """sets a given fullscreen color"""
        self.logging.info("setting fullscreen color")
        color = argument.split("-")
        if len(color) != 3:
            self.logging.error("wrong argument for --fullscreen-color")
            quit()
        await self.bluetooth.send(
            FullscreenColor().setColor(
                int(color[0]),
                int(color[1]),
                color[2],
            )
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
            await self.bluetooth.send(
                Graffiti().setPixelColor(
                    x=int(split[0]),
                    y=int(split[1]),
                    r=int(split[2]),
                    g=int(split[3]),
                    b=int(split[4]),
                )
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
        await self.bluetooth.send(
            Scoreboard().setScoreboard(
                count1=int(scores[0]),
                count2=int(scores[1]),
            )
        )

    async def image(self, args):
        """enables or disables the image mode and uploads a given image file"""
        self.logging.info("setting image")
        image = Image()
        if args.image == "false":
            await self.bluetooth.send(
                image.show(
                    mode=0,
                )
            )
        else:
            await self.bluetooth.send(
                image.show(
                    mode=1,
                )
            )
            if args.set_image:
                if args.process_image:
                    await self.bluetooth.send(
                        image.upload_processed(
                            file_path=args.set_image,
                            pixel_size=int(args.process_image),
                        )
                    )
                else:
                    await self.bluetooth.send(
                        image.upload_unprocessed(
                            file_path=args.set_image,
                        )
                    )

    async def gif(self, args):
        """enables or disables the gif mode and uploads a given gif file"""
        self.logging.info("setting (animated) GIF")
        gif = Gif()
        if args.process_gif:
            await self.bluetooth.send(
                gif.upload_processed(
                    file_path=args.set_gif,
                    pixel_size=int(args.process_gif),
                )
            )
        else:
            await self.bluetooth.send(
                gif.upload_unprocessed(
                    file_path=args.set_gif,
                )
            )
