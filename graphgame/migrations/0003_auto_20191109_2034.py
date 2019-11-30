# Generated by Django 2.2.6 on 2019-11-09 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graphgame', '0002_auto_20191109_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vertex',
            name='end',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ends', to='graphgame.Edge'),
        ),
        migrations.AlterField(
            model_name='vertex',
            name='start',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='starts', to='graphgame.Edge'),
        ),
    ]
