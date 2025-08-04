from django.db.models.signals import pre_save, post_delete
from django.dispatch import receive
from .modelsimport Product 
from utils.media_cleanup import delete_old_file_on_update, delete_old_file_on_delete

@receiver(pre_save, sender=Product)
def product_pre_save_cleanup(sender, instance, **kwargs):
    delete_old_file_on_update(sender, instance, 'product_image')

    @