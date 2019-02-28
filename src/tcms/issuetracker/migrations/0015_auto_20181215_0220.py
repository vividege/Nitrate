# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-15 02:20
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


"""
Both of these fields were updated some time ago but forgot the concrete time.
Anyway, this migration fixes that.
"""


class Migration(migrations.Migration):

    dependencies = [
        ('issuetracker', '0014_correct_issue_url_fmt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='case',
            field=models.ForeignKey(error_messages={'required': 'Case is missed.'}, help_text='A test case this issue is associated with.', on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='testcases.TestCase'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='issue_key',
            field=models.CharField(help_text='Actual issue ID corresponding issue tracker. Different issue tracker may have issue IDs in different type or format. For example, in Bugzilla, it could be an integer, or in JIRA, it could be a string in format PROJECTNAME-number, e.g. PROJECT-1000.', max_length=50, validators=[django.core.validators.MaxLengthValidator(50, 'Issue key has too many characters. It should have 50 characters at most.')]),
        ),
    ]
