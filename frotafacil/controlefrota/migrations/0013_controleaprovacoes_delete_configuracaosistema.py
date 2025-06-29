# Generated by Django 5.2.1 on 2025-06-24 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlefrota', '0012_configuracaosistema_ad_password_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControleAprovacoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aprovacao_automatica', models.BooleanField(default=False, verbose_name='Aprovação automática de requisições')),
            ],
            options={
                'verbose_name': 'Controle de Aprovações',
                'verbose_name_plural': 'Controle de Aprovações',
            },
        ),
        migrations.DeleteModel(
            name='ConfiguracaoSistema',
        ),
    ]
