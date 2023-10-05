from django.db import models, transaction
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Category connects all submenus with one root.

    name - equal to name of root menu,
    root_menu - can be used for future coming features
        and allows CASCADE delete when delete root_menu."""
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        unique=True,
    )
    root_menu = models.ForeignKey(
        'Menu', on_delete=models.CASCADE,
        related_name='related_category',
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name) + str(self.pk)


class Menu(models.Model):
    """Main model.

    category - relation to one category for all menus with same root.
    parent - menu placed one level upper in tree than obj.

    save() - reassembled to provide category autocreating.
    clean() - ensures that category with same name does not exist."""
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
    )
    parent = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name) + str(self.pk)

    @transaction.atomic
    def _save_root_menu(self, *args, **kwargs):
        category = Category.objects.create(name=self.name)
        self.category = category
        super().save(*args, *kwargs)
        category.root_menu = self
        category.save()

    def save(self, *args, **kwargs):
        if not self.parent:
            self._save_root_menu(*args, **kwargs)
        else:
            self.category = self.parent.category
            super().save(*args, *kwargs)

    def clean(self):
        if not self.parent:
            if Category.objects.filter(name=self.name).exists():
                raise ValidationError(
                    'Name should be unique when creating new root menu.'
                )
