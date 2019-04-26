import urllib.request
import random
from pathlib import Path

for i in range(100):
    urllib.request.urlretrieve("https://pastebin.com/etc/captcha/random.php?{}" \
        .format(random.randint(1,10000000000000000+1)),
            str(Path("captchas/testing/" + "{}.png".format(i))))

    print(i)
