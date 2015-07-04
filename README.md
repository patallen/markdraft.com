# Markdraft
Version control for your markdown documents.

## Setting up for Development
### Set up the Environment
1. Install Virtualenvwrapper
1. Install postgresql & libpq-dev
1. Create and workon python3 virtualenv
1. cd into the markdraft.com repo
1. `$ pip install -r requirements.txt`

### Set up the Database
1. `$ sudo su - postgres`
1. `$ createdb markdraftdb`
1. `$ createuser --interactive`

```
Enter name of role to add: username
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n
```
4. `$ psql`
5. `# alter role username with password 'password';`
6. `# grant all privileges on database markdraftdb to username;`
7. Press`ctrl+d` twice to get back to sudo user.

### Finish Setting up the Django Project
1. `$ python manage.py migrate`
1. `$ python manage.py createsuperuser`
1. Follow steps to create your superuser.

### Set up Grunt
1. `$ sudo apt-get install nodejs-legacy`
1. `$ sudo apt-get install npm`
1. `$ sudo npm install -g grunt-cli`
1. `$ sudo gem install sass`

### Using Grunt
1. First, compile current assets using `grunt sass`
1. To run django's dev server and grunt watch at the same time:
	- Run grunt with `$ grunt`
	- Press Ctrl+Z to halt grunt
	- `$ bg` to run it in the background
	- `$ python manage.py runserver 0:5000`
1. Grunt will now watch for changes to precompiled assets.
