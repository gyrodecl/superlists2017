from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/gyrodecl/superlists2015.git'

env.key_filename=['cs184-gyrcl.pem'] 
env.hosts = ["ubuntu@54.213.139.227"] 

# call this:  fab deploy:host=elspeth@superlists.staging.ottg.eu

def deploy(username='ubuntu',site_name='tdd-lists-staging',
           site_url='ec2-54.213.139.227.us-west-2.compute.amazonaws.com/'):
    site_folder = '/home/%s/sites/%s' % (username, site_name)  
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, site_url)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

#now have a bunch of helper functions
def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))
        #python3.6 version with f string
        #run(f'mkdir -p {site_folder}/{subfolder}')
        
#run runs it on the remote server 
#local runs it on the local machine 
def _get_latest_source(source_folder): 
    print source_folder 
    if exists(source_folder + '/.git'): 
        run('cd %s && git fetch' % (source_folder,))
        #python3.6 version with f string
        #run(f'cd {source_folder} && git fetch')
    else: 
        run('git clone %s %s' % (REPO_URL, source_folder))
        #python3.6 version with f string
        #run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))
        #python3.6 version with f string
        #run(f'cd {source_folder} && git reset --hard {current_commit}')

#here the "site_name" needs to be the web accessible url 
#we also should probably use environmental variables to set secret keys! 
#in settings.py we have DOMAIN varaible and ALLOWED_HOSTS=[DOMAIN]
def _update_settings(source_folder, site_name): 
    settings_path = source_folder + '/superlists2017/settings.py' 
    sed(settings_path, "DEBUG = TRUE", "DEBUG = False") 
    sed(settings_path, 'DOMAIN = "localhost"', 'DOMAIN = "%s"' % (site_name,))
    #sed(settings_path, 
    #    'ALLOWED_HOSTS = .+$', 
    #    'ALLOWED_HOSTS = ["%s"]' % (site_name,) 
    #) 
    secret_key_file = source_folder + '/superlists2017/secret_key.py' 
    if not exists(secret_key_file): 
        print 'doesnt exist' 
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)' 
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50)) 
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
        # python 3.6 version
        # append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')
    
    
def _update_virtualenv(source_folder): 
    virtualenv_folder = source_folder + '/../virtualenv' 
    if not exists(virtualenv_folder + '/bin/pip'): 
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
        # python 3.6 version
        # run(f'python3.6 -m venc {virtualenv_folder}')
    
    run('%s/bin/pip install -r %s/requirements.txt' % ( 
            virtualenv_folder, source_folder 
    ))
    # python 3.6 version
    #run(f'{virtualenv_folder}/bin/pip install -r {source_folder/requirements.txt})
    

#notice how we run the virtualenv version of python, but we 
#can't just activate the environment; we call the binary python3 function directly 
def _update_static_files(source_folder): 
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % ( 
        source_folder, 
    )) 

def _update_database(source_folder): 
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % ( 
        source_folder, 
    ))

