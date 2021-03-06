# Generated by Django 3.2 on 2022-02-23 03:13

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.CharField(max_length=100)),
                ('action', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField()),
                ('modified_by', models.BigIntegerField()),
                ('entity_id', models.BigIntegerField()),
                ('serialized_data', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Biro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ithc_biro', models.BigIntegerField()),
                ('rcc', models.IntegerField(blank=True, null=True)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=200)),
                ('sub_group_code', models.CharField(max_length=10)),
                ('group_code', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('all_object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expense_type', models.CharField(blank=True, max_length=200, null=True)),
                ('notes', models.CharField(blank=True, max_length=500, null=True)),
                ('planning_q1', models.BigIntegerField(blank=True, default=0)),
                ('planning_q2', models.BigIntegerField(blank=True, default=0)),
                ('planning_q3', models.BigIntegerField(blank=True, default=0)),
                ('planning_q4', models.BigIntegerField(blank=True, default=0)),
                ('allocate', models.BigIntegerField(blank=True, default=0)),
                ('is_active', models.BooleanField(blank=True, default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Coa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('definition', models.CharField(blank=True, max_length=1000, null=True)),
                ('hyperion_name', models.CharField(blank=True, max_length=200, null=True)),
                ('is_capex', models.BooleanField(blank=True, default=False)),
                ('minimum_item_origin', models.BigIntegerField(blank=True, null=True)),
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
                ('year', models.IntegerField(unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('notification', models.BooleanField(default=False)),
                ('due_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('all_object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_code', models.CharField(max_length=200)),
                ('product_name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('all_object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('itfam_id', models.CharField(blank=True, max_length=200)),
                ('project_name', models.CharField(max_length=200)),
                ('project_description', models.CharField(blank=True, max_length=500, null=True)),
                ('start_year', models.IntegerField(blank=True, null=True)),
                ('end_year', models.IntegerField(blank=True, null=True)),
                ('total_investment_value', models.BigIntegerField(blank=True, default=0)),
                ('is_tech', models.BooleanField(default=False)),
                ('biro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.biro')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dcsp_id', models.CharField(blank=True, max_length=200, null=True)),
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
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee_id', models.BigIntegerField(blank=True, unique=True)),
                ('display_name', models.CharField(blank=True, max_length=100)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('initial', models.CharField(blank=True, max_length=10, null=True)),
                ('eselon', models.CharField(blank=True, max_length=10, null=True)),
                ('role', models.CharField(default='User', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_fk_created', to='api.user')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_fk_updated', to='api.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Switching',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nominal', models.BigIntegerField()),
                ('type', models.CharField(max_length=300)),
                ('from_minus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='switching_from', to='api.budget')),
                ('to_plus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='switching_to', to='api.budget')),
            ],
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='strategy_fk_created', to='api.user')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='strategy_fk_updated', to='api.user')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Realization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('realization_jan', models.BigIntegerField(blank=True, default=0)),
                ('realization_feb', models.BigIntegerField(blank=True, default=0)),
                ('realization_mar', models.BigIntegerField(blank=True, default=0)),
                ('realization_apr', models.BigIntegerField(blank=True, default=0)),
                ('realization_may', models.BigIntegerField(blank=True, default=0)),
                ('realization_jun', models.BigIntegerField(blank=True, default=0)),
                ('realization_jul', models.BigIntegerField(blank=True, default=0)),
                ('realization_aug', models.BigIntegerField(blank=True, default=0)),
                ('realization_sep', models.BigIntegerField(blank=True, default=0)),
                ('realization_oct', models.BigIntegerField(blank=True, default=0)),
                ('realization_nov', models.BigIntegerField(blank=True, default=0)),
                ('realization_dec', models.BigIntegerField(blank=True, default=0)),
                ('allocate', models.BigIntegerField(blank=True, default=0)),
                ('budget', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.budget')),
                ('coa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.coa')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='realization_fk_created', to='api.user')),
                ('project_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.projectdetail')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='realization_fk_updated', to='api.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projectdetail_fk_created', to='api.user'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='planning',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.planning'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_detail', to='api.project'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='project_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.projecttype'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projectdetail_fk_updated', to='api.user'),
        ),
        migrations.AddField(
            model_name='project',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_fk_created', to='api.user'),
        ),
        migrations.AddField(
            model_name='project',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product'),
        ),
        migrations.AddField(
            model_name='project',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_fk_updated', to='api.user'),
        ),
        migrations.AddField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_fk_created', to='api.user'),
        ),
        migrations.AddField(
            model_name='product',
            name='strategy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.strategy'),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_fk_updated', to='api.user'),
        ),
        migrations.AddField(
            model_name='planning',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planning_fk_created', to='api.user'),
        ),
        migrations.AddField(
            model_name='planning',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planning_fk_updated', to='api.user'),
        ),
        migrations.CreateModel(
            name='Monitoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('monitoring_status', models.CharField(max_length=50)),
                ('pic_employee_id', models.BigIntegerField(blank=True, null=True)),
                ('pic_initial', models.CharField(blank=True, max_length=10, null=True)),
                ('pic_display_name', models.CharField(blank=True, max_length=50, null=True)),
                ('biro', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.biro')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='monitoring_fk_created', to='api.user')),
                ('planning', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.planning')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='monitoring_fk_updated', to='api.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='coa',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coa_fk_created', to='api.user'),
        ),
        migrations.AddField(
            model_name='coa',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coa_fk_updated', to='api.user'),
        ),
        migrations.AddField(
            model_name='budget',
            name='coa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.coa'),
        ),
        migrations.AddField(
            model_name='budget',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='budget_fk_created', to='api.user'),
        ),
        migrations.AddField(
            model_name='budget',
            name='project_detail',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='budget', to='api.projectdetail'),
        ),
        migrations.AddField(
            model_name='budget',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='budget_fk_updated', to='api.user'),
        ),
    ]
