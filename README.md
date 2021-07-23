# flask server

## requirements

```
Flask==1.0.2
Flask-Cors==3.0.6
Flask-HTTPAuth==3.2.4
Flask-Login==0.4.1
Flask-Mail==0.9.1
Flask-SQLAlchemy==2.3.2
Flask-WTF==0.14.2
Flask-Migrate==2.1.1
Flask-Script==2.0.6
cymysql==0.9.12
requests==2.19.1
pyDes==2.0.1
```

## launch

### development

```bash
pip install -r requirements.txt
python runserver.py
```

### production

```shell
gunicorn -c gunicorn_config.py runserver:app -D
```