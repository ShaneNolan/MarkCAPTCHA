import glob, os
from pathlib import Path
import argparse

from lib.MarkCAPTCHA import MarkCAPTCHA

ARGUMENT_CONFIG = "config"

ARGUMENT_PREDICT = "predict"
ARGUMENT_IMAGEPROCESSING = "imageprocessing"
ARGUMENT_BUILD = "build"
ARGUMENT_SHOW = "show"

IS_DOCKER = os.getenv('AM_I_IN_A_DOCKER_CONTAINER', False)

LOGO = r'''
             __
    |\/| /\ |__)|_/
    |  |/--\| \ | \

 __     __ ___ __
/   /\ |__) | /  |__| /\
\__/--\|    | \__|  |/--\

'''

def main():
    print(LOGO)
    parser = argparse.ArgumentParser(
        description='MarkCAPTCHA - Breaking CAPTCHA')
    parser.add_argument('--' + ARGUMENT_CONFIG,
        help='Provide filename for CAPTCHA config', metavar="config.json",
        required=True)

    parser.add_argument('--' + ARGUMENT_PREDICT,
        help='Provide CAPTCHA image in Base64 format to predict')
    parser.add_argument('--' + ARGUMENT_IMAGEPROCESSING,
        help='Clean CAPTCHA images', action='store_true', default=False)
    parser.add_argument('--' + ARGUMENT_BUILD,
        help='Build a new CAPTCHA classifier model', action='store_true', default=False)
    parser.add_argument('--' + ARGUMENT_SHOW,
        help='Display CAPTCHA text prediction', action='store_true', default=False)

    args = vars(parser.parse_args())

    mark = MarkCAPTCHA().importConfigs()

    if args[ARGUMENT_IMAGEPROCESSING]:
        mark.processImages(args[ARGUMENT_CONFIG])

    if args[ARGUMENT_BUILD]:
        mark.buildModel(args[ARGUMENT_CONFIG])

    if IS_DOCKER and args[ARGUMENT_SHOW]:
        print("WARNING: --show can not be used inside a container.\n")
        args[ARGUMENT_SHOW] = False

    if args[ARGUMENT_PREDICT]:
        prediction = mark.predict(args[ARGUMENT_CONFIG], args[ARGUMENT_PREDICT], args[ARGUMENT_SHOW])

        print("MARKCAPTCHA: {} ".format(prediction))

if __name__ == "__main__":
    main()
