import datetime
from django.db import migrations, models
from django.utils.timezone import now

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20230312_1958'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField()),
                ('date', models.DateField(default=now, verbose_name='Posted Date')),
                ('candidate_id', models.ForeignKey(on_delete=models.CASCADE, to='app.candidate_detail')),
                ('voter_id', models.ForeignKey(on_delete=models.CASCADE, to='app.voter_detail')),
            ],
        ),
    ]