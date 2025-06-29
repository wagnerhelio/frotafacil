# Generated by Django 5.2.1 on 2025-06-24 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlefrota', '0011_configuracaosistema'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracaosistema',
            name='ad_password',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Senha AD'),
        ),
        migrations.AddField(
            model_name='configuracaosistema',
            name='ad_user',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Usuário AD'),
        ),
        migrations.AddField(
            model_name='configuracaosistema',
            name='azure_audience',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Azure Audience'),
        ),
        migrations.AddField(
            model_name='configuracaosistema',
            name='azure_client_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Azure Client ID'),
        ),
        migrations.AddField(
            model_name='configuracaosistema',
            name='azure_client_secret',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Azure Client Secret'),
        ),
        migrations.AddField(
            model_name='configuracaosistema',
            name='azure_relying_party_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Azure Relying Party ID'),
        ),
        migrations.AddField(
            model_name='configuracaosistema',
            name='azure_resource',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Azure Resource'),
        ),
        migrations.AddField(
            model_name='configuracaosistema',
            name='azure_tenant_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Azure Tenant ID'),
        ),
    ]
