from django.contrib.auth import get_user_model
from django.conf import settings
import cv2
import os

from config import celery_app
from sicop.users.models import Sicop

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task(bind=True, max_retries=5)
def resize_images(self, sicop_id: int):
    try:
        sicop = Sicop.objects.get(id=sicop_id)

        # resize
        img = cv2.imread(
            os.path.join(settings.MEDIA_ROOT, sicop.image.name), cv2.IMREAD_UNCHANGED
        )
        _, ext = os.path.splitext(sicop.image.name)
        ratio = Sicop.FIXED_LENGTH / img.shape[0]
        width = int(img.shape[0] * ratio)
        height = int(img.shape[1] * ratio)
        dim = (width, height)

        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(settings.MEDIA_ROOT, sicop.image.name), resized)

        # say that it is finished
        sicop.visible = True
        sicop.save()

        return True
    except Sicop.DoesNotExist as exc:
        self.retry(exc=exc, countdown=2**self.request.retries)

    return False
