quick start
```
source venv/bin/activate
doppler run -- python manage.py runserver
```
http://127.0.0.1:8000/api/persons/  
```
pip install django-q setuptools
pip freeze > requirements.txt  
python manage.py makemigrations
doppler run -- python manage.py migrate
doppler run -- python manage.py seed_data
```
ModuleNotFoundError: No module named 'pkg_resources' -> pip install setuptools  
running with Gunicorn for render.
```
doppler run -- python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
```
http://127.0.0.1:8000/api/hello/  
get started
```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export DOPPLER_TOKEN='dp.st.dev.'
doppler run --config dev -- python manage.py runserver
```
instead of token
```
doppler login
doppler setup
```
```
export DOPPLER_TOKEN='dp.st.prd'
```  
doppler get started:  
https://github.com/wusixuan0/seed-supabase/blob/main/README.md  

- workflow to manage migration conflict  
    - When merging branches with model changes, always check if there are conflicting migrations.
    - After resolving model conflicts in `mode.py`, run `python [manage.py](http://manage.py/) makemigrations --merge`
    - Run `python manage.py migrate` locally to apply the merge migration.
    - Commit the merge migration file, push the changes to your remote repository.  
### simulate migration conflict using Render and Railway Postgres instance
    
summary

    - Both `imdevtwo` and `im_dev_three` were working on the same Dev Database - a Railway Postgres instance. Django is deployed by Render and connect to Prod Database - a different Railway Postgres instance.
    
    Local development:
    
    - Dev Two added a 'country' column
    - Dev Three added a 'discipline' column to same table
    - Both developers applied their migrations locally
    - After the two dev ran migrate, both 'country' and 'discipline' columns existed in the database.
    - Merge process:
        - Dev Two merged to main
        - **Dev Three rebased but forgot to use --merge flag**
        - Dev Three then merged into main (production)
    - Production build failure:
        - Render build failed due to migration conflict
    
    The core issue here is that two separate migrations (0003_person_country and 0003_person_discipline) are both trying to be the next migration after 0002. This creates a conflict because Django doesn't know which one should be applied first.

### merge migration process:
<img width="641" alt="1" src="https://github.com/user-attachments/assets/1c4a5724-7c2d-4795-9475-f2dd0c2da46e">

1. Initial state:
    - We start with `0001_initial` and `0002_previous_migration`.
2. Conflict occurs:
    - Two developers create migrations: `0003_person_country` and `0003_person_discipline`.
    - Both of these migrations are based on `0002_previous_migration`.
3. Merge migration is created:
    - A new migration `0004_merge_country_discipline` is generated.
    - This merge migration depends on both `0003` migrations.
4. How Django resolves the confusion:
    - The merge migration (`0004`) doesn't contain any operations itself.
    - Instead, it specifies both `0003` migrations as dependencies.
    - This tells Django the correct order to apply the migrations.
5. Migration application order:
    - Django will apply `0001_initial`
    - Then `0002_previous_migration`
    - Then `0003_person_country`
    - Then `0003_person_discipline`
    - Finally, `0004_merge_country_discipline` (which doesn't actually change the database)

The key point is that the merge migration (`0004`) doesn't introduce new changes. Its purpose is to specify the correct order of the two conflicting `0003` migrations.

Django isn't confused anymore because:

1. It knows that both `0003` migrations need to be applied.
2. The merge migration provides a clear path: apply one `0003`, then the other, then mark the merge as complete.
3. This creates a single, unambiguous history that can be followed in any environment.

In practice, when you run `python manage.py migrate`:

- If neither `0003` has been applied, Django will apply them both, then the merge.
- If one `0003` has been applied (like in your local environment), Django will apply the other, then the merge.
- If both `0003` have been applied (also possible in your local environment), Django will just mark the merge as applied.

This approach ensures that regardless of the state of any given database, all environments will end up with the same schema and the same migration history. The merge migration acts as a "checkpoint" that brings all possible paths back into alignment.

The merge migration file is important because:
- It resolves the conflict between the two 0003 migrations.
- It ensures that future developers or deployment environments will apply migrations in the correct order.
- It maintains a consistent migration history across all environments.

The content of the merge migration file typically doesn't introduce new changes. Instead, it lists both conflicting migrations as dependencies, effectively creating a new "checkpoint" in the migration history.

observations:

1. Local DB didn't break:
The local databases didn't break because migrations were applied sequentially. When you run migrations locally, Django applies them in the order they're run, regardless of their numbering.
    
    both migration files (0003_person_country and 0003_person_discipline) were created and applied separately. Even though the database reflects both changes, Django keeps track of which migrations have been applied through its migration history table (usually named django_migrations).
    
2. Django migration history:
The `django_migrations` table keeps track of which migrations at what time have been applied.

3. Production build failure:
The conflict becomes apparent when trying to apply migrations in a new environment (like production) where neither 0003 migration has been applied yet. Django can't determine the correct order automatically.
- Should you apply `python manage.py migrate` in the local db to apply the 004 merge file?
    - Yes, you should run `python manage.py migrate` in your local environment. Even though your local database is working fine, it's important to apply the merge migration for consistency. This ensures that your local migration history matches what will be in production.
- What's the best practice: rename migration to 0004_person_discipline, or merge and have a new file that contains two migration changes?
    - The best practice is to keep the merge migration file (0004) generated by Django. This file serves as a "checkpoint" that resolves the conflict between the two 0003 migrations. It doesn't typically contain new changes but instead specifies the correct order of applying the previous migrations.
- 
- The Conflict:
    
    after fixing conflict, `im_dev_three` didn’t run merge
    
    - The conflict arises not because of the database state, but because of Django's migration graph.
    - Django sees two different migration paths from the same starting point, and it doesn't know which one should come first.

Why it worked locally but failed on Render:

- Locally, migrations were applied sequentially, so Django's migration history reflected this.
- On Render, it's trying to apply all migrations from scratch, encountering both 0003 migrations simultaneously.

Detail steps:

table person has name and create_at

On branch `imdevtwo`

- `imdevtwo` add column `country` to table `person`,
- makemigration and migrate
- and add more seed data with country info
- and seed

On branch `im_dev_three`

- `im_dev_three` add column `discipline` to table `person`
- makemigration and migrate
- `im_dev_three` is unaware of `imdevtwo`'s changes
- now im_dev_three try to seed data with discipline info fail without country info

Now Dev Two merged changes into main

`im_dev_three` update branch with the latest changes from `main`

`git checkout dev_three
git fetch origin
git rebase origin/main`

```jsx
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
<<<<<<< HEAD
    country = models.CharField(max_length=100)
=======
    discipline = models.CharField(max_length=100)
>>>>>>> 5fcd4b9 (im_dev_three add column discipline to table person, makemigration and migrate)

    def __str__(self):
        return self.name
```

`git add conflict_file`

`git rebase --continue`

`git push -f`


### `im_dev_three` merge into main

**Render fail to build due to migrate**

`CommandError: Conflicting migrations detected; multiple leaf nodes in the migration graph: (0003_person_country, 0003_person_discipline in api).`

`to fix them run 'python manage.py makemigrations --merge'`

- The issue:
two migrations (0003_person_country and 0003_person_discipline) that both descend from the same parent migration. Django doesn't know which one should come first.
- Where you missed:
When you resolved the Git conflict in the models.py file, you correctly combined the changes. However, you didn't address the conflicting migrations. Each branch created its own migration file, and these weren't merged properly.

how to fix

python manage.py makemigrations --merge  
doppler run -- python manage.py makemigrations --merge
his will create a new migration file that combines the two conflicting migrations.
b. Review the newly created merge migration to ensure it looks correct.
c. Apply the migrations: `python manage.py migrate`

d. Commit the new merge migration file.
e. Push the changes to your repository.
f. Rebuild on Render.

dev three hasn’t apply seed in dev db, but seed command was in [build.sh](http://build.sh) so production has those new data

- When you run `python manage.py migrate`, Django compares the migrations in your project's files with the records in the `django_migrations` table.

Switching to an empty PostgreSQL database:

- If you switch to a completely empty PostgreSQL database and run `python manage.py migrate`, Django will attempt to apply all migrations.
- This is because the new database doesn't have a `django_migrations` table, so Django assumes no migrations have been applied yet.



### create Django tutorial steps:  
```
touch django-api
cd django-api
# Create a virtual environment to isolate our package dependencies locally
python3 -m venv venv
source venv/bin/activate
pip install django djangorestframework && pip freeze > requirements.txt
// Create the Django project in the current directory
django-admin startproject config .
python manage.py startapp api
```

Your project structure should now look like this:
```
my-project/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── venv/
└── requirements.txt
```


```
touch api/urls.py

```
add app route to config/urls.py  
add Hello World to api/urls.py  
http://127.0.0.1:8000/api/hello/

