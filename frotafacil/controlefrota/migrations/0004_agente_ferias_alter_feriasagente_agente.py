# Generated by Django 5.2.4 on 2025-07-03 22:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlefrota', '0003_feriasagente'),
    ]

    operations = [
        migrations.AddField(
            model_name='agente',
            name='ferias',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Férias'),
        ),
        migrations.AlterField(
            model_name='feriasagente',
            name='agente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ferias_periodos', to='controlefrota.agente'),
        ),
    ]
