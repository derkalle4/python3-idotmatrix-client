# python imports
import argparse
import asyncio
import logging

# idotmatrix imports
from core.cmd import CMD


def log():
    # set basic logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
        handlers=[logging.StreamHandler()],
    )
    # set log level of asyncio
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    # set log level of bleak
    logging.getLogger("bleak").setLevel(logging.WARNING)


def main():
    cmd = CMD()
    parser = argparse.ArgumentParser(
        description="control all your 16x16 or 32x32 pixel displays"
    )
    # global argument
    parser.add_argument(
        "--address",
        action="store",
        help="the bluetooth address of the device",
    )
    # add cmd arguments
    cmd.add_arguments(parser)
    # parse arguments
    args = parser.parse_args()
    # run command
    asyncio.run(cmd.run(args))


if __name__ == "__main__":
    log()
    log = logging.getLogger("idotmatrix")
    log.info("initialize app")
    try:
        main()
    except KeyboardInterrupt:
        log.info("Caught keyboard interrupt. Stopping app.")
