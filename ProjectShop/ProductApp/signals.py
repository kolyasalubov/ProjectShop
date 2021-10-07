from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.db import models

from ProductApp.models import ProductMedia
from ProductApp.utils import delete_file_if_unused


@receiver(post_delete, sender=ProductMedia)
def delete_image_when_row_deleted_from_db(sender, instance, **kwargs) -> None:
    """
    Delete image if instance is deleted.

    :param sender: models.Model child class
    :param instance: sender instance
    :param kwargs: additional parameters
    :return: None
    """

    for field in sender._meta.concrete_fields:
        if isinstance(field, models.ImageField):
            instance_file_field = getattr(instance, field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)


@receiver(pre_save, sender=ProductMedia)
def delete_image_when_image_changed(sender, instance, **kwargs) -> None:
    """
    Delete image if it was switched.

    :param sender: models.Model child class
    :param instance: sender instance
    :param kwargs: additional parameters
    :return: None
    """
    # Don't run on initial save
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.ImageField):
            # its got a image field. Let's see if it changed
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                # We are probably in a transaction and the PK is just temporary
                return
            instance_in_db_file_field = getattr(instance_in_db, field.name)
            instance_file_field = getattr(instance, field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender, instance, field, instance_in_db_file_field)
