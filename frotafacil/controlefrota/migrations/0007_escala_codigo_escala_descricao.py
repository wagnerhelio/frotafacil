# Generated by Django 5.2.4 on 2025-07-08 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlefrota', '0006_escala_agente_escala'),
    ]

    operations = [
        migrations.AddField(
            model_name='escala',
            name='codigo',
            field=models.CharField(default='ESCALA_ANTIGA', max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='escala',
            name='descricao',
            field=models.TextField(blank=True),
        ),
    ]
