# Generated by Django 4.2.5 on 2023-09-28 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0002_alter_book_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='section',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='section',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='books.book'),
        ),
        migrations.AlterField(
            model_name='section',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subsections', to='books.section'),
        ),
        migrations.DeleteModel(
            name='SubSection',
        ),
    ]
