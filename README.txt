== Django Firewall ==

Django Firewall is a middleware and models app that gives you access control over your application, it can also log requests!

It acts like a real firewall and log system in a lot of ways:
    * The first rule which matches the request applys, if this happens to be REJECT ALL, so be it, have fun breaking back into your site.
    * The Log model looks pretty much like an apache access log file

You can have as many rules as you like.

Rule Features:
    * Accept, Reject, Redirect, Require Basic Auth and 404 access control
    * Match requests against exact IP Addresses or ranges of IP Addresses
    * Can have start and stop datetimes for each rule
    * Username and password for the Require Basic Auth rule
    
Django Firewall cannot:
    * Restrict media files served outside your Django application, ie by apache, or;
    * be expected to be production ready/safe, USE AT OWN RISK, TEST TEST TEST.

Django Firewall requires the django.contrib.auth app because it needs to create a firewall permission.

REQUIREMENTS:
1. Python 2.7 (because of ipaddr lib)
2. Django 1.3
3. django.contrib.auth app must be installed.
4. django.contrib.admin app must be installed.

INSTALLATION:
1. Download the firewall app and put it in your project's folder or install into a virtualenv/system with $ pip install -e git://github.com/Rundll/django-firewall.git#egg=django_firewall.
2. Add the app to your INSTALLED_APPS in your settings.py any where under 'django.contrib.auth', 'django_firewall'
3. Add 'django_firewall.middleware.FirewallMiddleware' to the MIDDLEWARE_CLASSES in your settings.py file. The middleware class must come AFTER the authorization middleware because it depends on it.
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
    'django_firewall.middleware.FirewallMiddleware',
    ...
)
4. Run ./manage.py syncdb
5. The Admin requires some .js files which live in the static folder, and will be found by python manage.py collectstatic, otherwise move them to the correct location yourself

SETTINGS:
    FIREWALL_LOGGING = False # Logging is off by default, it may be resource heavy.
    FIREWALL_REFRESH = datetime.timedelta(seconds=60) # Not implemented yet, intended to cache the firewall rules.
    FIREWALL_REALM = 'Firewall' # The realm name used when prompting for Basic Auth.

That's it. Admin -> Django_firewall -> Rules -> Add rule
