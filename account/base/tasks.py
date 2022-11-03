from Qaryb_API.celery_conf import app
from celery.utils.log import get_task_logger
from PIL import Image, ImageDraw, ImageFont
from account.models import CustomUser
from Qaryb_API.settings import STATIC_PATH
from io import BytesIO
from random import shuffle
from django.core.files import File
from chat.models import MessageModel
from os import remove
from django.core.exceptions import SuspiciousFileOperation
from django.core.mail import EmailMessage

logger = get_task_logger(__name__)


# For generating Avatar
def random_color_picker():
    return [
        "#F3DCDC",
        "#FFD9A2",
        "#F8F2DA",
        "#DBF4EA",
        "#DBE8F4",
        "#D5CEEE",
        "#F3D8E1",
        "#EBD2AD",
        "#E2E4E2",
        "#FFFFFF",
        "#FFA826",
        "#FED301",
        "#07CBAD",
        "#FF9DBF",
        "#CEB186",
        "#FF5D6B",
        "#0274D7",
        "#8669FB",
        "#878E88",
        "#0D070B"
    ]


def get_text_fill_color(bg_color):
    # white 255, 255, 255
    # black 0, 0, 0
    match bg_color:
        case ("#F3DCDC" | "#FFD9A2" | "#F8F2DA" | "#DBF4EA" | "#DBE8F4" | "#D5CEEE" | "#F3D8E1" | "#EBD2AD"
              | "#E2E4E2" | "#FFFFFF" | "#FFA826" | "#FED301" | "#07CBAD" | "#FF9DBF" | "#CEB186"):
            return 0, 0, 0
        case ("#FF5D6B" | "#0274D7" | "#8669FB" | "#878E88" | "#0D070B"):
            return 255, 255, 255
        case _:
            # Return black color as default
            return 0, 0, 0


def from_img_to_io(image, format_):
    bytes_io = BytesIO()
    image.save(File(bytes_io), format=format_, save=False)
    print(image)
    bytes_io.seek(0)
    return bytes_io


def start_generating_avatar_and_thumbnail(last_name, first_name):
    colors = random_color_picker()
    shuffle(colors)
    color = colors.pop()
    fill = get_text_fill_color(color)
    avatar = Image.new("RGB", (600, 600), color=color)
    font_avatar = ImageFont.truetype(STATIC_PATH + "/fonts/Poppins-Bold.ttf", 240)
    drawn_avatar = ImageDraw.Draw(avatar)
    drawn_avatar.text((100, 136), "{}.{}".format(first_name, last_name), font=font_avatar, fill=fill)
    thumbnail = Image.new("RGB", (300, 300), color=color)
    font_thumb = ImageFont.truetype(STATIC_PATH + "/fonts/Poppins-Bold.ttf", 120)
    drawn_thumb = ImageDraw.Draw(thumbnail)
    drawn_thumb.text((50, 68), "{}.{}".format(first_name, last_name), font=font_thumb, fill=fill)
    return avatar, thumbnail


@app.task(bind=True)
def base_send_email(self, user_pk, email_, mail_subject, message, code, type_):
    user = CustomUser.objects.get(pk=user_pk)
    email = EmailMessage(
        mail_subject, message, to=(email_,)
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)
    if type_ == 'activation_code':
        user.activation_code = code
    elif type_ == 'password_reset_code':
        user.password_reset_code = code
    user.save()


@app.task(bind=True)
def base_generate_user_thumbnail(self, user_pk):
    user = CustomUser.objects.get(pk=user_pk)
    last_name = str(user.last_name[0]).upper()
    first_name = str(user.first_name[0]).upper()
    avatar, thumbnail = start_generating_avatar_and_thumbnail(last_name, first_name)
    avatar_ = from_img_to_io(avatar, 'PNG')
    thumbnail_ = from_img_to_io(thumbnail, 'PNG')
    user.save_image('avatar', avatar_)
    user.save_image('avatar_thumbnail', thumbnail_)


@app.task(bind=True)
def base_mark_every_messages_as_read(self, user_blocked_pk, user_pk):
    msgs_sent = MessageModel.objects.filter(user=user_pk, recipient=user_blocked_pk)
    msgs_received = MessageModel.objects.filter(user=user_blocked_pk, recipient=user_pk)
    msgs_sent.update(viewed=True)
    msgs_received.update(viewed=True)

#
# @app.task(bind=True)
# def base_delete_user_account(self, user_pk):
#     user = CustomUser.objects.get(pk=user_pk)
#     # CustomUser
#     random_email = str(uuid4()) + '@qaryb.com'
#     user.first_name = ''
#     user.last_name = ''
#     user.gender = None
#     user.birth_date = None
#     user.is_active = False
#     user.email = random_email
#     user.save()


@app.task(bind=True)
def base_delete_user_media_files(self, media_paths_list):
    for media_path in media_paths_list:
        try:
            remove(media_path)
        except (ValueError, SuspiciousFileOperation, FileNotFoundError):
            pass


@app.task(bind=True)
def base_start_deleting_expired_codes(self, user_pk, type_):
    user = CustomUser.objects.get(pk=user_pk)
    if type_ == 'activation':
        user.activation_code = ''
    elif type_ == 'password_reset':
        user.password_reset_code = ''
    user.save()
