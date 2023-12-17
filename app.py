# python imports
import argparse

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
    args = parser.parse_args()
    CMD(args)


if __name__ == "__main__":
    main()
