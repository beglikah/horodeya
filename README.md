# Хородея

## Python3.5
```bach
virtualenv -p python3.5 venv --no-site-packages
source venv/bin/activate
python3.5 -m pip install -r requirements.txt
```

## Настройка на средата за разработка

```bash
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```

Download [manage.sh](https://trello.com/c/Rp1cvIX8/54-managesh) and run:

```bash
chmod +x manage.sh
```

### Локална база данни

```bash
docker run --name horodeya-postgres -e POSTGRES_USER=horodeya -e POSTGRES_PASSWORD=horodeya -d postgres
```

След като сме пуснали postgres Docker изображението:

```bash
export DB_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' horodeya-postgres)
export DB_URL="postgresql://horodeya:horodeya@$DB_HOST/horodeya"
```

За връзка с база данни през терминал:

```bash
docker run -it --rm --network container:horodeya-postgres postgres psql -h $DB_HOST -U horodeya
```

### Стартиране

```bash
./manage.sh migrate
./manage.sh loaddata fixtures/dev.yaml
./manage.sh runserver
```

### Превод

```bash
manage.py makemessages -l bg -i venv/bin
```

После редактирай преводите в `locale` и `locale-allauth`. Накрая компилирай преводите:

```bash
manage.py compilemessages -l bg
```

### Запазване на локална информация

```bash
./manage.sh dumpdata --natural-foreign --format yaml -o fixtures/dev.yaml -e auth.Permission -e sessions -e admin.logentry --exclude contenttypes
```

### Смяна на парола за даден потребител

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
