# Generated by Django 5.0.3 on 2024-04-01 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_telegramsupport_telegramanswers'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Расхода, куда потратилась деньги.', max_length=100, verbose_name='Название расхода')),
                ('amount', models.BigIntegerField(default=0, help_text='Сумма расхода.', verbose_name='Сумма')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Временная метка, указывающая, когда был создан.', verbose_name='Создан')),
                ('user', models.ForeignKey(help_text='Пользователь, которому принадлежит расход.', on_delete=django.db.models.deletion.CASCADE, to='main.telegramuser', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Расход Telegram',
                'verbose_name_plural': 'Расходы Telegram',
                'ordering': ['-created_at'],
            },
        ),
    ]
