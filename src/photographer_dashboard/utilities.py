from PIL import Image
import zipfile
from django.shortcuts import get_object_or_404
from likeme_one.settings import BASE_DIR
from photo_reports.models import PhotoReport, Photo


Image.LOAD_TRUNCATED_IMAGES = True


def get_watermark_resize(
        img_bg_width, 
        img_bg_height, 
        wtrmrk_width, 
        wtrmrk_height,
        wtrmrk_scale):
    """ get watermark resize """
    if img_bg_width > img_bg_height:
        wtrmrk_width_new = int(img_bg_width / wtrmrk_scale)
        scale_factor = wtrmrk_width_new / wtrmrk_width
        wtrmrk_height_new = int(wtrmrk_height * scale_factor)
    else:
        wtrmrk_width_new = int(img_bg_height / wtrmrk_scale)
        scale_factor = wtrmrk_width_new / wtrmrk_width
        wtrmrk_height_new = int(wtrmrk_height * scale_factor)

    return wtrmrk_width_new, wtrmrk_height_new


def paste_watermarks(photos, place):
    """ paste watermarks """    
    WTRMRK_1 = Image.open(f'{ BASE_DIR }/static/images/watermark-logo.png').convert('RGBA')

    if place.image_watermark:
        WTRMRK_2 = Image.open(f'{ BASE_DIR }{ place.image_watermark.url }').convert('RGBA')
        WTRMRK_2_WIDTH, WTRMRK_2_HEIGHT = WTRMRK_2.size

        if place.watermark_position == '1':
            # top left
            for photo in photos:
                try:
                    img_bg = Image.open(f'{ BASE_DIR }{ photo.image.url }')
                except:
                    pass
                else:
                    img_bg_width, img_bg_height = img_bg.size

                    box_width = int(img_bg_width - WTRMRK_1.size[0] - 18)
                    img_bg.paste(WTRMRK_1, (box_width, 18), WTRMRK_1)

                    wtrmrk_2_width_new, wtrmrk_2_height_new = get_watermark_resize(
                        img_bg_width,
                        img_bg_height,
                        WTRMRK_2_WIDTH,
                        WTRMRK_2_HEIGHT,
                        place.watermark_scale)

                    wtrmrk_2_new = WTRMRK_2.resize(
                        (wtrmrk_2_width_new, wtrmrk_2_height_new),
                        Image.LANCZOS)

                    img_bg.paste(wtrmrk_2_new, (18, 18), wtrmrk_2_new)
                    img_bg.save(f'{ BASE_DIR }{ photo.image.url }')
        elif place.watermark_position == '2':
            # top right
            for photo in photos:
                try:
                    img_bg = Image.open(f'{ BASE_DIR }{ photo.image.url }')
                except:
                    pass
                else:
                    img_bg_width, img_bg_height = img_bg.size

                    img_bg.paste(WTRMRK_1, (18, 18), WTRMRK_1)

                    wtrmrk_2_width_new, wtrmrk_2_height_new = get_watermark_resize(
                        img_bg_width,
                        img_bg_height,
                        WTRMRK_2_WIDTH,
                        WTRMRK_2_HEIGHT,
                        place.watermark_scale)
                    
                    wtrmrk_2_new = WTRMRK_2.resize(
                        (wtrmrk_2_width_new, wtrmrk_2_height_new),
                        Image.LANCZOS)

                    box_width = int(img_bg_width - wtrmrk_2_width_new - 18)

                    img_bg.paste(wtrmrk_2_new, (box_width, 18), wtrmrk_2_new)
                    img_bg.save(f'{ BASE_DIR }{ photo.image.url }')
        elif place.watermark_position == '3':
            # bottom left
            for photo in photos:
                try:
                    img_bg = Image.open(f'{ BASE_DIR }{ photo.image.url }')
                except:
                    pass
                else:
                    img_bg_width, img_bg_height = img_bg.size

                    img_bg.paste(WTRMRK_1, (18, 18), WTRMRK_1)

                    wtrmrk_2_width_new, wtrmrk_2_height_new = get_watermark_resize(
                        img_bg_width,
                        img_bg_height,
                        WTRMRK_2_WIDTH,
                        WTRMRK_2_HEIGHT,
                        place.watermark_scale)

                    wtrmrk_2_new = WTRMRK_2.resize(
                        (wtrmrk_2_width_new, wtrmrk_2_height_new),
                        Image.LANCZOS)

                    box_height = int(img_bg_height - wtrmrk_2_height_new - 18)

                    img_bg.paste(wtrmrk_2_new, (18, box_height), wtrmrk_2_new)
                    img_bg.save(f'{ BASE_DIR }{ photo.image.url }')
        elif place.watermark_position == '4':
            # bottom middle
            for photo in photos:
                try:
                    img_bg = Image.open(f'{ BASE_DIR }{ photo.image.url }')
                except:
                    pass
                else:
                    img_bg_width, img_bg_height = img_bg.size

                    img_bg.paste(WTRMRK_1, (18, 18), WTRMRK_1)

                    wtrmrk_2_width_new, wtrmrk_2_height_new = get_watermark_resize(
                        img_bg_width,
                        img_bg_height,
                        WTRMRK_2_WIDTH,
                        WTRMRK_2_HEIGHT,
                        place.watermark_scale)

                    wtrmrk_2_new = WTRMRK_2.resize(
                        (wtrmrk_2_width_new, wtrmrk_2_height_new),
                        Image.LANCZOS)

                    box_width = int(img_bg_width / 2 - wtrmrk_2_width_new / 2)
                    box_height = int(img_bg_height - wtrmrk_2_height_new - 18)

                    img_bg.paste(wtrmrk_2_new, (box_width, box_height), wtrmrk_2_new)
                    img_bg.save(f'{ BASE_DIR }{ photo.image.url }')
        elif place.watermark_position == '5':
            # bottom right
            for photo in photos:
                try:
                    img_bg = Image.open(f'{ BASE_DIR }{ photo.image.url }')
                except:
                    pass
                else:
                    img_bg_width, img_bg_height = img_bg.size

                    img_bg.paste(WTRMRK_1, (18, 18), WTRMRK_1)

                    wtrmrk_2_width_new, wtrmrk_2_height_new = get_watermark_resize(
                        img_bg_width,
                        img_bg_height,
                        WTRMRK_2_WIDTH,
                        WTRMRK_2_HEIGHT,
                        place.watermark_scale)

                    wtrmrk_2_new = WTRMRK_2.resize(
                        (wtrmrk_2_width_new, wtrmrk_2_height_new),
                        Image.LANCZOS)

                    box_width = int(img_bg_width - wtrmrk_2_width_new - 18)
                    box_height = int(img_bg_height - wtrmrk_2_height_new - 18)

                    img_bg.paste(wtrmrk_2_new, (box_width, box_height), wtrmrk_2_new)
                    img_bg.save(f'{ BASE_DIR }{ photo.image.url }')
    else:
        for photo in photos:
            img_bg = Image.open(f'{ BASE_DIR }{ photo.image.url }')
            img_bg_width, img_bg_height = img_bg.size

            img_bg.paste(WTRMRK_1, (18, 18), WTRMRK_1)
            img_bg.save(f'{ BASE_DIR }{ photo.image.url }')


def zip_create(photo_report_id):
    """ zip create """
    photo_report = get_object_or_404(PhotoReport, id=photo_report_id)
    photos = Photo.objects.filter(photo_report=photo_report, is_available=True)

    zip_path = f'{ BASE_DIR }/media/archives/{ photo_report_id }.zip'
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for photo in photos:
            photo_path = f'{ BASE_DIR }{ photo.image.url }'
            photo_name = photo.image.url.split('/')[-1]
            try:
                zip_file.write(photo_path, photo_name)
            except:
                pass
