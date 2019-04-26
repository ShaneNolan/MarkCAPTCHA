import os
import sys
import glob, random
from pathlib import Path
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from lib.MarkCAPTCHA import MarkCAPTCHA

ARGUMENT_CONFIG = "config"
ARGUMENT_FOLDER = "folder"

ARGUMENT_SAMPLE = "sample"
ARGUMENT_SHOW = "show"
ARGUMENT_PRINT = "print"

def main():
    print("Sample Usage:\n{}".format(r"python tests/test_Accuracy.py --config \
        simplecaptcha.json --folder C:\MarkCaptcha\markcaptcha\data\captchas\really_simple_captcha\modified\tmp\testing \
        --sample 150"))

    parser = argparse.ArgumentParser(
        description='MarkCAPTCHA - Testing Accuracy')
    parser.add_argument('--' + ARGUMENT_CONFIG,
        help='Provide filename for CAPTCHA config', metavar="config.json",
        required=True)
    parser.add_argument('--' + ARGUMENT_FOLDER,
        help='Provide directory with CAPTCHA images',
        required=True)

    parser.add_argument('--' + ARGUMENT_SAMPLE,
        help='Amount of images to Sample', type=int, default=100)
    parser.add_argument('--' + ARGUMENT_SHOW,
        help='Display CAPTCHA if prediction is incorrect', action='store_true',
        default=False)
    parser.add_argument('--' + ARGUMENT_PRINT,
        help='Display CAPTCHA prediction output', action='store_true',
        default=False)

    args = vars(parser.parse_args())

    mark = MarkCAPTCHA().importConfigs()
    path = Path(args[ARGUMENT_FOLDER])

    if not path.exists():
        raise Exception("Invalid path provided: {}".format(path))

    images = random.sample(list(path.glob('*.png')), args[ARGUMENT_SAMPLE])

    success_counter = skipped_counter = 0

    for counter, image in enumerate(images):
        prediction = mark.predict(args[ARGUMENT_CONFIG], str(image))
        image_filename = mark.getImageFilename()

        is_success = prediction.lower() in image_filename.lower()

        if args[ARGUMENT_PRINT]:
            print("MARKCAPTCHA {}: {} : {} | Success: {}".format(counter + 1,
                image_filename, prediction, is_success))

        if is_success:
            success_counter += 1
        else:
            skipped_counter += 1
            if args[ARGUMENT_SHOW]:
                mark.predict(args[ARGUMENT_CONFIG], str(image), True)

    total_amount = args[ARGUMENT_SAMPLE] - skipped_counter

    print("\nResult: {} / {} -> {}%, Skipped:{} -> {}%".format(
        success_counter, total_amount, round((success_counter/total_amount) * 100, 2), skipped_counter,
        round((skipped_counter/args[ARGUMENT_SAMPLE]) * 100, 2)))

    print("Overall: {} / {} => {}".format(success_counter, args[ARGUMENT_SAMPLE], round((success_counter/args[ARGUMENT_SAMPLE]) * 100, 2)))

    return

if __name__ == "__main__":
    main()
