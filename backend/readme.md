# Olist backend

## Prérequis

### Installer un environement virtuelle python

    - python3 ou py -m venv .venv
  
lancer l'environement:

    Linux: 
      - source bin/activate
    Windows:
      - bin/Activate.ps1

### Installer les dépendance python via pip
  pip install -r requirements.txt
    - sqlalchemy
    - psycopg2
    - hug
    - pyjwt

Une fois l'environement créer, dans le fichier "pyvenv.cfg" rajouter:

    [venv]
    ....
    - user     = database user
    - password = database password
    - database = database name
    - secretkey = pour le token
    - salt      = pourle hashage

