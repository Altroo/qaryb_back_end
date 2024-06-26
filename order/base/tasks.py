from os import path
from django.template.loader import render_to_string
from Qaryb_API.celery_conf import app
from celery.utils.log import get_task_logger
from order.models import Order, OrderDetails
from offers.models import Offers
from shop.base.utils import ImageProcessor
from account.base.tasks import start_generating_avatar_and_thumbnail, from_img_to_io
from django.core.mail import EmailMessage

logger = get_task_logger(__name__)
parent_file_dir = path.abspath(path.join(path.dirname(__file__), "../.."))


def start_generating_thumbnail(img_path, duplicate):
    image_processor = ImageProcessor()
    loaded_img = image_processor.load_image(img_path)
    if duplicate:
        resized_thumb = image_processor.image_resize(loaded_img)
    else:
        resized_thumb = image_processor.image_resize(loaded_img, width=300, height=300)
    img_thumbnail = image_processor.from_img_to_io(resized_thumb, 'WEBP')
    return img_thumbnail


@app.task(bind=True, serializer='json')
def base_generate_user_thumbnail(self, order_pk):
    order = Order.objects.get(pk=order_pk)
    avatar, thumbnail = start_generating_avatar_and_thumbnail(str(order.last_name)[0].upper(),
                                                              str(order.first_name)[0].upper())
    thumbnail_ = from_img_to_io(thumbnail, 'WEBP')
    order.save_image('buyer_avatar_thumbnail', thumbnail_)


@app.task(bind=True, serializer='json')
def base_duplicate_order_offer_image(self, offer_pk, order_details_pk):
    offer = Offers.objects.get(pk=offer_pk)
    order_details = OrderDetails.objects.get(pk=order_details_pk)
    if offer.picture_1_thumbnail:
        offer_thumbnail = start_generating_thumbnail(offer.picture_1_thumbnail.path, True)
        order_details.save_image('offer_thumbnail', offer_thumbnail)


@app.task(bind=True, serializer='json')
def base_send_order_email(self, mail_subject, mail_template, email, first_name, href=None, shop_name=None):
    data_to_render = {
        'first_name': first_name,
        'email': email,
    }
    if href:
        data_to_render['href'] = href
    if shop_name:
        data_to_render['shop_name'] = shop_name
    message = render_to_string(mail_template, data_to_render)
    email_provider = EmailMessage(
        mail_subject, message, to=(email,)
    )
    email_provider.content_subtype = "html"
    email_provider.send(fail_silently=False)
