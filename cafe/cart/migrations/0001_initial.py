
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models
import users.validation


class Migration(migrations.Migration):

    initial = True

    dependencies = [

        migrations.swappable_dependency(settings.AUTH_USER_MODEL),

        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=6)),

                ('time', models.DateTimeField(auto_now_add=True)),
                ('total_quantity', models.PositiveIntegerField()),
                ('customer_number', users.models.PhoneNumberField(max_length=14, validators=[users.validation.phone_number_validator], verbose_name='phone number')),
                ('status', models.CharField(choices=[('a', 'Accept'), ('r', 'Refuse'), ('w', 'Waiting')], default='w', max_length=1)),

            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('unavailable', 'unavailable')], default='unavailable', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='cart.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cart.table'),
        ),

        migrations.AddField(
            model_name='cart',
            name='cart_users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),

    ]
