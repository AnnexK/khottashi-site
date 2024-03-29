# Generated by Django 2.2.6 on 2019-11-06 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False, unique=True, verbose_name='Graph name')),
            ],
        ),
        migrations.CreateModel(
            name='Vertex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField(verbose_name='x coordinate')),
                ('y', models.IntegerField(verbose_name='y coordinate')),
                ('end', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='end', to='graphgame.Edge')),
                ('g', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graphgame.Graph')),
                ('start', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='start', to='graphgame.Edge')),
            ],
        ),
        migrations.AddField(
            model_name='edge',
            name='g',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graphgame.Graph'),
        ),
    ]
