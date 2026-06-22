from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создание групп и назначение прав'

    def handle(self, *args, **options):
        self.stdout.write('Создаем группы и права...')

        # Получаем ContentType для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)

        # Создаем или получаем права
        can_unpublish, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=product_content_type
        )

        # Право на удаление продукта
        delete_permission = Permission.objects.get(
            codename='delete_product',
            content_type=product_content_type
        )

        # Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write('Группа "Модератор продуктов" создана')
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        # Назначаем права группе
        moderator_group.permissions.add(can_unpublish, delete_permission)
        moderator_group.save()

        self.stdout.write(self.style.SUCCESS(
            f'Группе "Модератор продуктов" назначены права:\n'
            f'  - {can_unpublish.name}\n'
            f'  - {delete_permission.name}'
        ))

        # Группа "Контент-менеджер"
        from blog.models import BlogPost
        blog_content_type = ContentType.objects.get_for_model(BlogPost)

        # Права для блога
        blog_permissions = Permission.objects.filter(
            content_type=blog_content_type,
            codename__in=['add_blogpost', 'change_blogpost', 'delete_blogpost', 'view_blogpost']
        )

        content_group, created = Group.objects.get_or_create(name='Контент-менеджер')

        if created:
            self.stdout.write('Группа "Контент-менеджер" создана')

        content_group.permissions.set(blog_permissions)
        content_group.save()

        self.stdout.write(self.style.SUCCESS(
            f'Группе "Контент-менеджер" назначены права на управление блогом'
        ))

        self.stdout.write(self.style.SUCCESS('Готово!'))