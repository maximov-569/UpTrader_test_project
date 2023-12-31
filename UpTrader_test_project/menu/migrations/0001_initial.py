# Generated by Django 4.2.6 on 2023-10-05 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('main_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submenus', to='menu.menu')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='menu.menu')),
            ],
        ),
    ]
