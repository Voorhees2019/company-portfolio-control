# Generated by Django 3.2.8 on 2021-11-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_rename_original_project_is_original'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='industries',
            field=models.ManyToManyField(related_name='projects_containing_industry', to='projects.Industry'),
        ),
        migrations.AlterField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(related_name='projects_containing_technology', to='projects.Technology'),
        ),
        migrations.AlterField(
            model_name='set',
            name='projects',
            field=models.ManyToManyField(related_name='sets_containing_project', to='projects.Project'),
        ),
    ]
