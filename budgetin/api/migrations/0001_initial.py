# Generated by Django 3.2 on 2022-01-21 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Coa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField(blank=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('definition', models.CharField(blank=True, max_length=1000, null=True)),
                ('hyperion_name', models.CharField(max_length=200)),
                ('is_capex', models.BooleanField(default=False)),
                ('minimum_item_origin', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MonitoringStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PicBudget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField(blank=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('biro_id', models.BigIntegerField()),
                ('employee_id', models.BigIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Planning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField(blank=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('year', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('due_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField(blank=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('product_code', models.CharField(max_length=200, unique=True)),
                ('product_name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField(blank=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('itfam_id', models.CharField(max_length=200)),
                ('project_name', models.CharField(max_length=200)),
                ('project_description', models.CharField(max_length=500)),
                ('biro_id', models.BigIntegerField()),
                ('rcc', models.IntegerField()),
                ('start_year', models.IntegerField()),
                ('end_year', models.IntegerField()),
                ('total_investment_value', models.BigIntegerField()),
                ('is_tech', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField(blank=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('dcsp_id', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('planning', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.planning')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.project')),
                ('project_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.projecttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='strategy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.strategy'),
        ),
        migrations.CreateModel(
            name='Monitoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('biro_id', models.BigIntegerField()),
                ('monitoring_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.monitoringstatus')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField(blank=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('expense_type', models.CharField(max_length=200)),
                ('planning_nominal', models.CharField(max_length=200)),
                ('planning_q1', models.BigIntegerField()),
                ('planning_q2', models.BigIntegerField()),
                ('planning_q3', models.BigIntegerField()),
                ('planning_q4', models.BigIntegerField()),
                ('realization_nominal', models.BigIntegerField()),
                ('realization_jan', models.BigIntegerField()),
                ('realization_feb', models.BigIntegerField()),
                ('realization_mar', models.BigIntegerField()),
                ('realization_apr', models.BigIntegerField()),
                ('realization_may', models.BigIntegerField()),
                ('realization_jun', models.BigIntegerField()),
                ('realization_jul', models.BigIntegerField()),
                ('realization_aug', models.BigIntegerField()),
                ('realization_sep', models.BigIntegerField()),
                ('realization_oct', models.BigIntegerField()),
                ('realization_nov', models.BigIntegerField()),
                ('realization_des', models.BigIntegerField()),
                ('switching_in', models.BigIntegerField()),
                ('switching_out', models.BigIntegerField()),
                ('top_up', models.BigIntegerField()),
                ('returns', models.BigIntegerField()),
                ('allocate', models.BigIntegerField()),
                ('coa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.coa')),
                ('project_detail_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.projectdetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('modified_by', models.BigIntegerField()),
                ('entity_id', models.BigIntegerField()),
                ('serialized_data', models.CharField(max_length=5000)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.action')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.table')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.BigIntegerField(blank=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('role', models.CharField(default='user', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
