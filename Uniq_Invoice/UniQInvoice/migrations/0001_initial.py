# Generated by Django 4.0.5 on 2022-07-26 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Company_Name', models.CharField(max_length=250)),
                ('GST_Number', models.CharField(max_length=250)),
                ('Address', models.CharField(max_length=250)),
                ('Email_Address', models.EmailField(max_length=250, unique=True)),
                ('Phone_Number', models.IntegerField()),
                ('Office_Number', models.IntegerField()),
                ('Owner_name', models.CharField(max_length=100)),
                ('Company_website', models.CharField(max_length=200)),
                ('IsDeleted', models.IntegerField()),
                ('IsActive', models.IntegerField()),
                ('CreatedBy', models.CharField(max_length=250)),
                ('CreatedDate', models.DateField()),
                ('ModifiedBy', models.CharField(max_length=250)),
                ('ModifiedDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Login_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_Name', models.EmailField(max_length=250)),
                ('Password', models.CharField(max_length=250)),
                ('Company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniQInvoice.company_master')),
            ],
        ),
        migrations.CreateModel(
            name='Dealer_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dealer_company_name', models.CharField(max_length=250)),
                ('dealre_name', models.CharField(max_length=250)),
                ('dealer_address', models.CharField(max_length=250)),
                ('gst_number', models.CharField(max_length=250, null=True)),
                ('dealer_email_address', models.CharField(max_length=250)),
                ('dealer_phone_number', models.CharField(max_length=250)),
                ('dealer_office_number', models.CharField(max_length=250)),
                ('IsActive', models.IntegerField()),
                ('IsDeleted', models.IntegerField()),
                ('CreatedBy', models.CharField(max_length=250)),
                ('CreatedDate', models.DateField()),
                ('ModifiedBy', models.CharField(max_length=250)),
                ('ModifiedDate', models.DateField()),
                ('IsDealer', models.BooleanField(null=True)),
                ('Company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniQInvoice.company_master')),
            ],
        ),
    ]
