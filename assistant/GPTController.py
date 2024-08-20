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

from datetime import datetime
import logging
import os

from gpt import gpt_call


import json 



class GPTController:
    conn = ConnectionManager()
    logging = logging.getLogger("gptcontroller." + __name__)
    
    
    async def initialize(self):
        """Initializes the connection to the device and starts the controller"""
        
        
        if 'IDOTMATRIX_ADDRESS' in os.environ: # if the address is provided in the environment
            address = os.getenv("IDOTMATRIX_ADDRESS")
            await self.conn.connectByAddress(address)
            
        else: # if the address is not provided in the environment, search for the device
            self.logging.info("Searching for device...")
            await self.conn.connectBySearch()

        await self.controller()

    async def controller(self):
        
        # mapping of function names to their respective functions
        function_mapping = {'fullscreenColor': self.fullscreenColor,
                'sync_time': self.sync_time,
                    'flip_screen': self.flip_screen,
                    'toggle_screen_freeze': self.toggle_screen_freeze,
                    'screen': self.screen,
                    'set_brightness': self.set_brightness,
                    'set_password': self.set_password,
                    'chronograph': self.chronograph,
                    'clock': self.clock,
                    'countdown': self.countdown,
                    'pixelColor': self.pixelColor,
                    'setText': self.setText,
                    'scoreboard': self.scoreboard,
                    'setImage': self.setImage,
                    'setGif': self.setGif}

        # Start loop to converse with the user
        while True:

            # Get user input
            inp = input("Enter a message: ")

            # Exit if user types "exit"
            if inp.lower() == "exit":
                break
                
            # Call GPT-4o-mini model
            response = gpt_call(messages = [inp])

            # Execute the functions returned by GPT-4o-mini
            self.logging.info(response.choices[0])
            for tool_call in response.choices[0].message.tool_calls:
                
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                self.logging.info(function_name)
                self.logging.info(function_args)

                self.logging.info("Executing Function")

                await function_mapping[function_name](**function_args)

    async def sync_time(self, datetime_str = None) -> None:
        """Synchronize local time to device"""
        self.logging.info("starting to synchronize time")
        
        if datetime_str:
            try:
                dt_object = datetime.strptime(datetime_str, "%d-%m-%Y-%H:%M:%S")
            except ValueError:
                self.logging.error(
                    "wrong format of --set-time: please use dd-mm-YYYY-HH:MM:SS"
                )
                return
        else:
            dt_object = datetime.now()

        await Common().setTime(
            dt_object.year,
            dt_object.month,
            dt_object.day,
            dt_object.hour,
            dt_object.minute,
            dt_object.second,
        )

    async def flip_screen(self, flip = "TRUE") -> None:
        """flip device screen 180 degrees"""
        self.logging.info("flipping screen")
        await Common().flipScreen(flip.upper() == "TRUE")

    async def toggle_screen_freeze(self) -> None:
        """toggles the screen freeze"""
        self.logging.info("toggling screen freeze")
        await Common().freezeScreen()

    async def screen(self, toggle: str) -> None:
        """turns the screen on or off"""
        if toggle.upper() == "ON":
            self.logging.info("turning screen on")
            await Common().screenOn()
        else:
            self.logging.info("turning screen off")
            await Common().screenOff()

    async def set_brightness(self, intensity: int) -> None:
        """sets the brightness of the screen"""
        if intensity in range(5, 101):
            self.logging.info(f"setting brightness of the screen: {intensity}%")
            await Common().setBrightness(intensity)
        else:
            self.logging.error("brightness out of range (should be between 5 and 100)")

    async def set_password(self, password: str) -> None:
        """sets connection password"""
        try:
            conv_password = int(password)
            if len(password) == 6 and conv_password in range(0, 1000000):
                self.logging.info(f"setting password: {password}")
                await Common().setPassword(conv_password)
            else:
                self.logging.error(
                    f"Password should be 6 digits long and in range 000000...999999"
                )
        except ValueError:
            self.logging.error(f"Invalid integer: {password}")

    async def chronograph(self, chronograph_mode: str) -> None:
        """sets the chronograph mode"""
        self.logging.info("setting chronograph mode")
        if int(chronograph_mode) in range(0, 4):
            await Chronograph().setMode(int(chronograph_mode))
        else:
            self.logging.error("wrong argument for chronograph mode")
            return 

    async def clock(self,
                    clock_mode: str,
                    clock_color: str,
                    clock_with_date: str = None,
                    clock_24h: str = None) -> None:
        
        """sets the clock mode"""
        self.logging.info("setting clock mode")
        if int(clock_mode) in range(0, 8):
            color = clock_color.split("-")
            if len(color) < 3:
                self.logging.error("wrong argument for --clock-color")
                return 
            await Clock().setMode(
                style=int(clock_with_date),
                visibleDate=clock_with_date,
                hour24=clock_24h,
                r=int(color[0]),
                g=int(color[1]),
                b=int(color[2]),
            )
        else:
            self.logging.error("wrong argument for --clock")

    async def countdown(self, countdown_mode : str,
                        countdown_timer_minutes: str = 0,
                        countdown_timer_seconds: str = 0) -> None:
        """sets the countdown mode"""
        self.logging.info("setting countdown mode")
        mode = int(countdown_mode)
        if mode not in range(0, 4):
            self.logging.error("wrong argument for --countdown")
            return
        # times = .split("-")
        # if not len(times) == 2:
        #     self.logging.error("wrong argument for --countdown-time")
        #     return
        minutes, seconds = int(countdown_timer_minutes), int(countdown_timer_seconds)
        if minutes not in range(0, 100):
            self.logging.error(
                "wrong argument for --countdown-time - minutes must be between 0 and 99"
            )
            return
        if seconds not in range(0, 60):
            self.logging.error(
                "wrong argument for --countdown-time - seconds must be between 0 and 59"
            )
            return

        await Countdown().setMode(
            mode=mode,
            minutes=minutes,
            seconds=seconds,
        )

    async def fullscreenColor(self,r, g, b):
        """sets a given fullscreen color"""

        self.logging.info("setting fullscreen color")

        await FullscreenColor().setMode(
            int(r),
            int(g),
            int(b)
        )

    async def pixelColor(self, pixel_argument: list) -> None:
        """sets the given pixel colors"""
        self.logging.info("setting pixel color")
        if len(pixel_argument) <= 0:
            self.logging.error("wrong argument for --pixel-color")
            return 
        pixels = []

        pixels = [i.split("-") for i in pixel_argument]
       
        for pixel in pixels:
            # split = pixel.split("-")
            # check if we got all data
            if len(pixel) != 5:
                self.logging.error(
                    "need exactly 5 arguments for a single pixel in --pixel-color"
                )
                return 
            # TODO: proper check if we are within the pixel range of the device
            # TODO: maybe we can use a delimiter to make use of the MTU size (sending chunks instead of separate requests)
            # TODO: when filling 32x32 pixels it seems to have trouble to send all pixels. One pixel will be "forgotten" somehow
            await Graffiti().setPixel(
                x=int(pixel[0]),
                y=int(pixel[1]),
                r=int(pixel[2]),
                g=int(pixel[3]),
                b=int(pixel[4]),

            )

    async def setText(self, text_str: str = None,
                   text_size: int = 16,
                #    text_font_path: str = None,
                   text_mode: str = 0,
                   text_speed: str = 95,
                   text_color: str = "255-0-0",
                   text_bg_color: str = "255-255-255",
                   text_color_mode: str = 1,
                   text_bg_mode: str = 0) -> None:
        """sets the given text on the device"""

        self.logging.info("setting text")
        text = Text()
        text_color = text_color.split("-")
        if len(text_color) != 3:
            self.logging.error("wrong argument for --text-color")
            return
        bg_color = text_bg_color.split("-")
        if len(bg_color) != 3:
            self.logging.error("wrong argument for --text-bg-color")
            return
        await text.setMode(
            text=text_str,
            font_size=text_size,
            # font_path=text_font_path,
            text_mode=text_mode,
            speed=text_speed,
            text_color_mode=text_color_mode,
            text_color=(int(text_color[0]), int(text_color[1]), int(text_color[2])),
            text_bg_mode=text_bg_mode,
            text_bg_color=(int(bg_color[0]), int(bg_color[1]), int(bg_color[2])),
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

    async def setImage(self, image_name: str = None, process_image: int = None):
        """enables or disables the image mode and uploads a given image file"""
        self.logging.info("setting image")

        image_path = 'images/' + image_name
        image = Image()
        if not image_name:
            await image.setMode(
                mode=0,
            )
        else:
            await image.setMode(
                mode=1,
            )
        
            if process_image:
                await image.uploadProcessed(
                    file_path=image_path,
                    pixel_size=process_image,
                )
            else:
                await image.uploadUnprocessed(
                    file_path=image_path
                )

    async def setGif(self, gif_name: str = None, process_gif: int = None):
        """enables or disables the image mode and uploads a given image file"""
        self.logging.info("setting image")

        gif_path = 'images/' + gif_name
        gif = Gif()
        
        if process_gif:
            await gif.uploadProcessed(
                file_path=gif_path,
                pixel_size=process_gif,
            )
        else:
            await gif.uploadUnprocessed(
                file_path=gif_path,
            )
