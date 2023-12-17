# python imports
import argparse
import asyncio

# idotmatrix imports
from core.cmd import CMD


def main():
    parser = argparse.ArgumentParser(
        description="control all your 16x16 or 32x32 pixel displays"
    )
    parser.add_argument(
        "--address",
        action="store",
        help="the bluetooth address of the device",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="run the test function from the command line class",
    )
    args = parser.parse_args()
    asyncio.run(CMD().run(args))


if __name__ == "__main__":
    main()
