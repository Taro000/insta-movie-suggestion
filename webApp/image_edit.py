from PIL import Image, ImageFilter, ImageFont, ImageDraw
import random
import numpy as np
from django.conf import settings
import os
import base64
from io import BytesIO


def random_rgb():
    rgba = ()
    for i in range(3):
        rgba += (random.randint(0, 255),)
    return rgba


def get_gradient_2d(start, stop, width, height, is_horizontal):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T


def get_gradient_3d(width, height, start_list, stop_list, is_horizontal_list):
    result = np.zeros((height, width, len(start_list)), dtype=np.float)

    for i, (start, stop, is_horizontal) in enumerate(zip(start_list, stop_list, is_horizontal_list)):
        result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)

    return result


def crop_center(pil_img, crop_width, crop_height, img_width, img_height):
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def make_normal_story(img_path, title, year):
    rgb = random_rgb()
    # backbground_img = Image.new('RGBA', (1080, 1920), rgba)
    array = get_gradient_3d(1080, 1920, rgb, (0, 0, 0), (False, False, False))
    backbground_img = Image.fromarray(np.uint8(array))
    poster = Image.open(img_path)
    copied_poster = poster.copy()
    w, h = copied_poster.size
    resized_poster = copied_poster.resize((int(w/4), int(h/4)))
    poster_w, poster_h = resized_poster.size
    backbground_w, backbground_h = backbground_img.size
    print(resized_poster.size)
    backbground_img.paste(resized_poster, (backbground_w//2 - poster_w//2, backbground_h//2 - poster_h//2))

    draw = ImageDraw.Draw(backbground_img)
    font_title = ImageFont.truetype(os.path.join(settings.MEDIA_ROOT, "NotoSansJP-Black.otf"), size=50)
    font_year = ImageFont.truetype(os.path.join(settings.MEDIA_ROOT, "NotoSansJP-Black.otf"), size=25)

    if not title.isalnum():
        title = title.split()
    else:
        title = [title]

    dat, current_h = 60, backbground_h // 2 + poster_h // 2 + 70
    for line in title:
        title_w, title_h = draw.textsize(line, font=font_title)
        draw.text(((backbground_w - title_w) // 2, current_h), line, fill=(255, 255, 255), font=font_title)
        current_h += dat
    year_w, year_h = draw.textsize(year, font=font_year)
    draw.text(((backbground_w - year_w) // 2 - 10, current_h + 20), year, fill=(153, 153, 153), font=font_year)

    buffer = BytesIO()
    backbground_img.save(buffer, format='PNG')
    base64_img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    return base64_img


def make_cover_story(img_path, title, year):
    poster = Image.open(img_path)
    copied_poster_1 = poster.copy()
    copied_poster_2 = poster.copy()
    w, h = copied_poster_1.size
    resized_poster_1 = copied_poster_1.resize((1080, 1920))
    backbground_img = Image.new('RGB', (1080, 1920), 'white')
    backbground_img.paste(resized_poster_1, (0, 0))
    backbground_img = backbground_img.point(lambda x: x * 0.5)
    backbground_img = backbground_img.filter(ImageFilter.GaussianBlur(4))

    resized_poster_2 = copied_poster_2.resize((int(w / 4), int(h / 4)))
    poster_w, poster_h = resized_poster_2.size
    backbground_w, backbground_h = backbground_img.size
    white_img = Image.new('RGB', (poster_w + 50, poster_h + 50), 'white')
    white_w, white_h = white_img.size
    backbground_img.paste(white_img, (backbground_w // 2 - white_w // 2, backbground_h // 2 - white_h // 2))
    backbground_img.paste(resized_poster_2, (backbground_w // 2 - poster_w // 2, backbground_h // 2 - poster_h // 2))

    draw = ImageDraw.Draw(backbground_img)
    font_title = ImageFont.truetype(os.path.join(settings.MEDIA_ROOT, "NotoSansJP-Black.otf"), size=50)
    font_year = ImageFont.truetype(os.path.join(settings.MEDIA_ROOT, "NotoSansJP-Black.otf"), size=25)

    if not title.isalnum():
        title = title.split()
    else:
        title = [title]

    dat, current_h  = 60, backbground_h // 2 + poster_h // 2 + 70
    for line in title:
        title_w, title_h = draw.textsize(line, font=font_title)
        draw.text(((backbground_w - title_w) // 2, current_h), line, fill=(255, 255, 255), font=font_title)
        current_h += dat
    year_w, year_h = draw.textsize(year, font=font_year)
    draw.text(((backbground_w - year_w) // 2 - 10, current_h + 20), year, fill=(153, 153, 153), font=font_year)

    buffer = BytesIO()
    backbground_img.save(buffer, format='PNG')
    base64_img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    return base64_img


def make_black_story(img_path, title, year):
    poster = Image.open(img_path)
    copied_poster = poster.copy()
    w, h = copied_poster.size
    resized_poster = copied_poster.resize((int(w / 4), int(h / 4)))
    black = Image.open(os.path.join(settings.MEDIA_ROOT, "black_00062.jpg"))
    background_img = black.copy()
    poster_w, poster_h = resized_poster.size
    backbground_w, backbground_h = background_img.size
    background_img.paste(resized_poster, (backbground_w // 2 - poster_w // 2, backbground_h // 2 - poster_h // 2))

    draw = ImageDraw.Draw(background_img)
    font_title = ImageFont.truetype(os.path.join(settings.MEDIA_ROOT, "NotoSansJP-Black.otf"), size=50)
    font_year = ImageFont.truetype(os.path.join(settings.MEDIA_ROOT, "NotoSansJP-Black.otf"), size=25)

    if not title.isalnum():
        title = title.split()
    else:
        title = [title]

    dat, current_h = 60, backbground_h // 2 + poster_h // 2 + 70
    for line in title:
        title_w, title_h = draw.textsize(line, font=font_title)
        draw.text(((backbground_w - title_w) // 2, current_h), line, fill=(255, 0, 0), font=font_title)
        current_h += dat
    year_w, year_h = draw.textsize(year, font=font_year)
    draw.text(((backbground_w - year_w) // 2 - 10, current_h + 20), year, fill=(153, 153, 153), font=font_year)

    buffer = BytesIO()
    background_img.save(buffer, format='PNG')
    base64_img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    return base64_img


def make_white_story(img_path, title, year):
    poster = Image.open(img_path)
    copied_poster = poster.copy()
    w, h = copied_poster.size
    resized_poster = copied_poster.resize((int(w / 4), int(h / 4)))
    poster_w, poster_h = resized_poster.size
    # shadow = Image.open('/Users/shintarotakahashi/PycharmProjects/MovieSuggetion/media/shadow.jpg')
    # copied_shadow = shadow.copy()
    # resized_shadow = copied_shadow.resize((poster_w + 10, poster_h + 30))
    # shadow_w, shadow_h = resized_shadow.size

    white = Image.open(os.path.join(settings.MEDIA_ROOT, "white_00052.jpg"))
    background_img = white.copy()
    backbground_w, backbground_h = background_img.size
    # background_img.paste(shadow, (backbground_w // 2 - poster_w // 2, backbground_h // 2 - poster_h // 2))
    background_img.paste(resized_poster, (backbground_w // 2 - poster_w // 2, backbground_h // 2 - poster_h // 2))

    draw = ImageDraw.Draw(background_img)
    font_title = ImageFont.truetype(os.path.join(settings.MEDIA_ROOT, "NotoSansJP-Black.otf"), size=50)
    font_year = ImageFont.truetype(os.path.join(settings.MEDIA_ROOT, "NotoSansJP-Black.otf"), size=25)

    if not title.isalnum():
        title = title.split()
    else:
        title = [title]

    dat, current_h = 60, backbground_h // 2 + poster_h // 2 + 70
    for line in title:
        title_w, title_h = draw.textsize(line, font=font_title)
        draw.text(((backbground_w - title_w) // 2, current_h), line, fill=(255, 0, 0), font=font_title)
        current_h += dat
    year_w, year_h = draw.textsize(year, font=font_year)
    draw.text(((backbground_w - year_w) // 2 - 10, current_h + 20), year, fill=(153, 153, 153), font=font_year)
    background_img.show()

    buffer = BytesIO()
    background_img.save(buffer, format='PNG')
    base64_img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    return base64_img


def pillow_test():
    make_white_story('/Users/shintarotakahashi/PycharmProjects/MovieSuggetion/media/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg', 'INCEPTION', '2019年')
