# Generated by Django 4.0.5 on 2022-07-05 20:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MealSummary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mealtime', models.CharField(choices=[(1, 'Breakfast'), (2, 'Snack 1'), (3, 'Lunch'), (4, 'Snack 2'), (5, 'Dinner'), (6, 'Night snack')], default=1, max_length=2)),
                ('diet', models.CharField(choices=[('RG', 'Regular'), ('VE', 'Vegetarian'), ('VG', 'Vegan')], default='RG', max_length=2)),
                ('calorie_intake_type', models.CharField(choices=[('HIC', 'Hipocaloric'), ('NOC', 'Normocaloric'), ('HYC', 'Hypercaloric')], default='NOC', max_length=3)),
                ('upper_calorie_intake', models.IntegerField(choices=[(1350, 'Between 1200 and 1350 Kcal'), (1600, 'Between 1351 and 1600 Kcal'), (2000, 'Between 1601 and 2000 Kcal'), (2399, 'Between 2001 and 2399 Kcal'), (2700, 'Between 2400 and 2700 Kcal'), (3050, 'Between 2701 and 3050 Kcal'), (3450, 'Between 3051 and 3450 Kcal')], default=1350)),
            ],
            options={
                'unique_together': {('mealtime', 'diet', 'calorie_intake_type', 'upper_calorie_intake')},
            },
        ),
        migrations.CreateModel(
            name='FoodGroupIntake',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('food_supergroup', models.CharField(choices=[('ENE', 'Energetic'), ('PRO', 'Protein'), ('DAI', 'Dairy'), ('LFD', 'Low Fat Dairy'), ('FAV', 'Fruits & Vegetables'), ('HFA', 'Healthy Fats'), ('OTH', 'Other'), ('NSU', 'Nutritional Supplements'), ('VEN', 'Vegetarian Energetic'), ('VPR', 'Vegetarian Protein')], default='ENE', max_length=3)),
                ('intake', models.FloatField()),
                ('meal_summary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_group_intakes', to='nutrition.mealsummary')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FoodGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('supergroup', models.CharField(choices=[('ENE', 'Energetic'), ('PRO', 'Protein'), ('DAI', 'Dairy'), ('LFD', 'Low Fat Dairy'), ('FAV', 'Fruits & Vegetables'), ('HFA', 'Healthy Fats'), ('OTH', 'Other'), ('NSU', 'Nutritional Supplements'), ('VEN', 'Vegetarian Energetic'), ('VPR', 'Vegetarian Protein')], default='ENE', max_length=3)),
                ('group', models.CharField(choices=[('CER', 'Cereals & Derivatives'), ('TUB', 'Tubercules'), ('PLA', 'Plantains'), ('ROT', 'Roots'), ('LEG', 'Legumes'), ('MEA', 'Red Meats, Chicken, Fish & Eggs'), ('MLK', 'Milk & Dairy Derivatives'), ('LFM', 'Low Fat Milk & Low Fat Dairy Derivatives'), ('FRT', 'Fruits'), ('VEG', 'Vegetables'), ('SED', 'Dry Fruits & Seeds'), ('POL', 'Polysaturated Fats'), ('MON', 'Monosaturated Fats'), ('SAT', 'Saturated Fats'), ('SUG', 'Simple Sugars'), ('SWT', 'Sweets & Desserts'), ('MIS', 'Miscellaneous'), ('PRE', 'Prepared Foods'), ('SPI', 'Spices'), ('ALH', 'Alcoholic Drinks'), ('SUP', 'Nutritional Supplements'), ('VGF', 'Vegetarian Foods'), ('VGP', 'Vegan Protein'), ('EGG', 'Eggs')], default='CER', max_length=3)),
            ],
            options={
                'unique_together': {('supergroup', 'group')},
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('calories', models.FloatField()),
                ('cooked_half_portion', models.FloatField()),
                ('raw_half_portion', models.FloatField()),
                ('proteins', models.FloatField()),
                ('fats', models.FloatField()),
                ('carbohydrates', models.FloatField()),
                ('home_measure_amount', models.CharField(max_length=8)),
                ('home_measure_type', models.CharField(choices=[('HP_SP', 'Heaping tablespoon'), ('LV_SP', 'Level tablespoon'), ('HP_TS', 'Heaping teaspoon'), ('LV_TS', 'Level teaspoon'), ('SM_MT', 'Small meatball'), ('SM_BA', 'Small ball'), ('BO', 'Bottle'), ('EG_YO', 'Egg yolk'), ('CU', 'Cup'), ('LA', 'Ladle'), ('SM_SG', 'Small segment'), ('LF', 'Leaf'), ('PA', 'Palm'), ('PI', 'Pill'), ('SM_PL', 'Small plate'), ('MD_PL', 'Medium plate'), ('BG_PL', 'Big plate'), ('PE_PL', 'Personal plate'), ('WE', 'Well'), ('CH_WE', 'Chocolate well'), ('TH_SL', 'Thin slices'), ('MD_SL', 'Medium slices'), ('BG_SL', 'Big slices'), ('CH', 'Chop'), ('TH_ST', 'Thin stems'), ('BW', 'Bowl'), ('DR', 'Drink'), ('SM_CT', 'Small cut'), ('MD_CT', 'Medium cut'), ('BG_CT', 'Big cut'), ('SM_UN', 'Small unit'), ('MD_UN', 'Medium unit'), ('BG_UN', 'Big unit'), ('GL', 'Glass'), ('SM_GL', 'Small glass'), ('MD_GL', 'Small glass'), ('BG_GL', 'Big glass'), ('PE_CN', 'Personal can'), ('ST', 'Strip'), ('HL', 'Halve'), ('PC', 'Pinch')], default='CU', max_length=5)),
                ('food_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrition.foodgroup')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
