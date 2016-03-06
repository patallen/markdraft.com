from fabric.api import *
from fabric.contrib.files import exists


env.use_ssh_config = True
env.warn_only = True

env.user = "vagrant"
env.host = "10.10.10.6"

app_name = "api"

connection = "%s@%s" % (env.user, env.host)
virtualenv = "/var/%senv" % app_name
root = "/var/%s" % app_name

apt_packages = [
    'python-dev',
    'gcc',
    'libncurses5-dev',
    'libffi-dev',
    'build-essential',
    'python-pip',
    'postgresql',
    'libpq-dev',
    'nginx',
    'htop',
    'vim',
    'redis-server',
]


@hosts(connection)
def runserver(host="0.0.0.0"):
    with cd(root):
        run(
            "%s/bin/python manage.py runserver -h %s" %
            (virtualenv, host)
        )


@hosts(connection)
def manage(task):
    with cd(root):
        run("%s/bin/python manage.py %s" % (virtualenv, task))


@hosts(connection)
def db(task):
    with cd(root):
        run("%s/bin/python manage.py db %s" % (virtualenv, task))

@hosts(connection)
def db_init():
    with cd(root):
        run("%s/bin/python manage.py db init" % (virtualenv, ))
        run("cp script.py.mako.default migrations/script.py.mako")


@hosts(connection)
def setup_virtualenv():
    if not exists(virtualenv):
        sudo("pip install virtualenv")
        run("sudo virtualenv %s" % virtualenv)
    sudo("chown -R vagrant:vagrant %s" % virtualenv)
    run("%s/bin/pip install -r  %s/requirements.txt" % (virtualenv, root))


@hosts(connection)
def setup_db():
    sudo("apt-get install postgresql-server-dev-all "
         "postgresql postgresql-contrib -y")
    run("sudo -u postgres createuser --superuser vagrant")
    run("sudo -u postgres psql -c \"ALTER USER "
        "vagrant WITH PASSWORD 'vagrant';\"")
    run("sudo -u vagrant createdb -O vagrant markdraft")
    run("sudo -u vagrant createdb -O vagrant markdraft_test")


@hosts(connection)
def setup_nginx():
    sudo("apt-get install nginx")
    with cd("/etc/nginx"):
        sudo("chown -R vagrant:vagrant .")

        if not exists("sites-available/%s", app_name):
            print "Creating api config."
            put("server/nginx/%s" % app_name, "sites-available")
            run("ln -s /etc/nginx/sites-available/%s "
                "/etc/nginx/sites-enabled/%s" % (app_name, app_name))

        if exists("sites-available/default"):
            print "Removing default nginx configuration."
            run("rm sites-available/default")

        sudo("service nginx restart")


@hosts(connection)
def apt_install():
    sudo("apt-get update -y")
    sudo("apt-get install %s -y" % " ".join(apt_packages))


@hosts(connection)
def apt_upgrade():
    sudo("apt-get update -y")
    sudo("apt-get dist-upgrade -y")


@hosts(connection)
def setup_server():
    apt_install()
    apt_upgrade()
    setup_virtualenv()
    setup_nginx()
    setup_db()
    db_init()
    db("migrate")
    db("upgrade")


@hosts(connection)
def test():
    with cd(root):
        run("%s/bin/python -m unittest discover" % (virtualenv,))
