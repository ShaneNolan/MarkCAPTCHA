import random
import os, os.path
from captcha.image import ImageCaptcha

path = r"C:\Users\Shane\Desktop\MarkCaptcha\markcaptcha\data\captchas\captcha_03\captchas\\"
while len(os.listdir(path)) != 3000 + 3:
    image = ImageCaptcha()
    #image = ImageCaptcha()
    word = ''.join(random.choice("ABCDEFGKMNPQRSTUVWXYZabcdefghkmnpqrstuvwxyz23456789") for _ in range(4))
    data = image.generate(word)
    image.write(word, path + word + '.png')
    print("Generated: " + word)

print("CAPTCHA generation completed.")
