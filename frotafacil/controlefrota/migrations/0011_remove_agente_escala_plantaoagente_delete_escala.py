# Generated by Django 5.2.4 on 2025-07-08 23:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlefrota', '0010_escala_ciclo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agente',
            name='escala',
        ),
        migrations.CreateModel(
            name='PlantaoAgente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('horas', models.PositiveIntegerField(default=12)),
                ('agente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plantoes', to='controlefrota.agente')),
            ],
            options={
                'verbose_name': 'Plantão do Agente',
                'verbose_name_plural': 'Plantões dos Agentes',
                'unique_together': {('agente', 'data')},
            },
        ),
        migrations.DeleteModel(
            name='Escala',
        ),
    ]
