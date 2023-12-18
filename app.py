# python imports
import argparse
import asyncio

# idotmatrix imports
from core.cmd import CMD


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
    main()
