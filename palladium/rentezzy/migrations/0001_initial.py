# Generated by Django 3.2.7 on 2021-11-21 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import rentezzy.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.IntegerField()),
                ('amt_received', models.IntegerField()),
                ('currency', models.CharField(max_length=50)),
                ('source', models.CharField(choices=[('VISA', 'Visa'), ('MASTERCARD', 'MasterCard')], default='Visa', max_length=10)),
                ('orderId', models.UUIDField(blank=True, default=None, null=True)),
                ('failure_reason', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('SUCCESS', 'Success'), ('FAILED', 'Failed'), ('RETURNED', 'Returned')], max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.CreateModel(
            name='RoomDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('CUSTOMER', 'Customer'), ('AGENT', 'Agent'), ('OWNER', 'Owner')], max_length=10, null=True)),
                ('enquiry_email', models.CharField(max_length=220)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Room Details',
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('eir_code', models.CharField(max_length=7, validators=[rentezzy.models.validate_length])),
                ('address', models.CharField(max_length=100)),
                ('county', models.CharField(choices=[('None', 'None'), ('Carlow', 'Carlow'), ('Cavan', 'Cavan'), ('Clare', 'Clare'), ('Cork', 'Cork'), ('Donegal', 'Donegal'), ('Dublin', 'Dublin'), ('Galway', 'Galway'), ('Kerry', 'Kerry'), ('Kildare', 'Kildare'), ('Kilkenny', 'Kilkenny'), ('Laois', 'Laois'), ('Leitrim', 'Leitrim'), ('Limerick', 'Limerick'), ('Longford', 'Longford'), ('Louth', 'Louth'), ('Mayo', 'Mayo'), ('Meath', 'Meath'), ('Monaghan', 'Monaghan'), ('Offaly', 'Offaly'), ('Roscommon', 'Roscommon'), ('Sligo', 'Sligo'), ('Tipperary', 'Tipperary'), ('Waterford', 'Waterford'), ('Westmeath', 'Westmeath'), ('Wexford', 'Wexford'), ('Wicklow', 'Wicklow')], default='None', max_length=10)),
                ('contract_details', models.FileField(blank=True, null=True, upload_to='media/')),
                ('monthly_rent_amount', models.IntegerField()),
                ('deposit_amount', models.IntegerField()),
                ('total_amount', models.IntegerField()),
                ('description', models.CharField(default='this is description', max_length=500)),
                ('image_url', models.FileField(blank=True, null=True, upload_to='media/')),
                ('img1', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('img2', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('img3', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('video_url', models.FileField(blank=True, null=True, upload_to='media/')),
                ('status', models.CharField(choices=[('AVAILABLE', 'Available'), ('TAKEN', 'Taken'), ('ONHOLD', 'OnHold'), ('BOOKED', 'Booked'), ('DELETED', 'Deleted')], default='Available', max_length=10)),
                ('property_age', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('room_details', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rentezzy.roomdetails')),
            ],
            options={
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('commented', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('room', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rentezzy.rooms')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('Description', models.CharField(max_length=400)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('room_details', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rentezzy.roomdetails')),
            ],
        ),
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_rooms_booked', models.IntegerField()),
                ('commission_amt', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('User', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('deposit_details', models.IntegerField()),
                ('cancellation_date', models.DateField(blank=True, null=True)),
                ('payments', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rentezzy.payments')),
                ('room', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rentezzy.rooms')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
