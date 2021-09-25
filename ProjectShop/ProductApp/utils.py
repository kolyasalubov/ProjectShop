

def delete_file_if_unused(model, instance, field, instance_file_field) -> None:
    """
    Delete file if it has no connection to database.

    :param model: models.Model child class
    :param instance: model instance
    :param field: model field instance
    :param instance_file_field: field file instance
    :return: None
    """
    dynamic_field = dict()
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)

