systemctl start postgresql
# migrate database
. .venv/bin/activate
eval "$(DB=pgsql make db_envs)"
make migrate
#Final step
. .venv/bin/activate
eval "$(DB=pgsql make db_envs)"
# make createsuperuser
python src/manage.py runserver 0.0.0.0:8080
