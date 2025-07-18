# Generated by Django 5.2.4 on 2025-07-08 18:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlefrota', '0005_remove_agente_ferias_agente_ferias_fim_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Escala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('horario_inicio', models.TimeField()),
                ('horario_fim', models.TimeField()),
            ],
        ),
        migrations.AddField(
            model_name='agente',
            name='escala',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agentes', to='controlefrota.escala'),
        ),
    ]
