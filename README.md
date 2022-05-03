# ITEC

## Run Project:

### Python3.8

```bach
virtualenv -p python3.8 venv --no-site-packages
source venv/bin/activate
python3.8 -m pip install -r requirements.txt
```

Download [manage.sh](https://trello.com/c/Rp1cvIX8/54-managesh) and run:

```bash
chmod +x manage.sh
```

### Local database:

```bash
docker run --name itec-postgres -e POSTGRES_USER=itec -e POSTGRES_PASSWORD=itec-foundation -d postgres
```

After we realized postgres Docker container:

```bash
export DB_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' itec-postgres)
export DB_URL="postgresql://itec:itec@$DB_HOST/itec"
```

To connect to the database via the terminal:

```bash
docker run -it --rm --network container:itec-postgres postgres psql -h $DB_HOST -U itec
```

### Run Localhost:

```bash
./manage.sh migrate
./manage.sh loaddata fixtures/dev.yaml
./manage.sh runserver
```

### Make Translations:

```bash
manage.py makemessages -l bg -i venv/bin
```

После редактирай преводите в `locale` и `locale-allauth`. Накрая компилирай преводите:

```bash
manage.py compilemessages -l bg
```

### Save local information

```bash
./manage.sh dumpdata --natural-foreign --format yaml -o fixtures/dev.yaml -e auth.Permission -e sessions -e admin.logentry --exclude contenttypes
```

### Change password for a user:

```bash
manage.py changepassword <user_name>
```

```python
from django.contrib.auth import get_user_model
user = get_user_model()
user.objects.all()
u = user.objects.get(username='mavrov.georgi')
u.set_password('123123')
```
