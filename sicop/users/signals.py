from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from sicop.users.models import Sicop
from sicop.users.tasks import resize_images


@receiver(post_save, sender=Sicop)
def resize_image(sender, instance: Sicop, created, **kwargs):
    if instance.image.width != Sicop.FIXED_LENGTH:
        resize_images.apply_async((instance.id,))


@receiver(post_delete, sender=Sicop)
def delete_image(sender, instance: Sicop, **kwargs):
    instance.image.delete(False)
