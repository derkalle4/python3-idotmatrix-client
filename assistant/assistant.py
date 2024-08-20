
import asyncio
from GPTController import GPTController
import logging


logging.basicConfig(level=logging.INFO)
logging.getLogger('openai').setLevel(logging.INFO)

obj = GPTController()
asyncio.run(obj.initialize())