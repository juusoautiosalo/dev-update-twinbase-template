import yaml, requests

print('Updating Twinbase')

# Load setup and autosetup yaml files
with open('setup.yaml', 'r') as file:
    setup = yaml.load(file, Loader=yaml.FullLoader)
with open('.autosetup.yaml', 'r') as file:
    autosetup = yaml.load(file, Loader=yaml.FullLoader)

# Check that preferred version is latest
if not setup['update-info']['version']['target'] == 'latest':
    print('Preferred version is not latest, exiting update procedure...')
    exit()


# Fetch commit hash of template repo
try:
    print('Fetching from raw github')
    # from raw github content
    reposplit= setup['update-info']['template'].split('/')
    repostring = reposplit[3] + '/' +  reposplit[4]
    url = 'https://raw.githubusercontent.com/' + repostring + '/main/.autosetup.yaml'
    r = requests.get(url, allow_redirects=True)
    print(r.status_code)
    r.raise_for_status()
    autosetup_template = yaml.load(r.text, Loader=yaml.FullLoader)
    print(autosetup_template)
except:
    # With git operations in case of failures (e.g.)
    # e.g. by cloning template or checking with some remote operation
    print('Error occurred, start using Git magic [TODO]')
    autosetup_template = autosetup # FIXME
    print('Fetched .autosetup.yaml of template with git magic.')

# Start update if 
try:
    if autosetup_template['update-info']['version']['current']['commit'] != autosetup['update-info']['version']['current']['commit']:
        # Overwrite files.
        # How to download?
        print('Starting update...')
        for filename in autosetup_template['updatefiles']:
            url = 'https://raw.githubusercontent.com/' + repostring + '/main/' + filename
            r = requests.get(url, allow_redirects=True)
            r.raise_for_status()
            print(r.status_code)
            print(r.content)
            break
        
        # Update complete, update local version info
        autosetup['update-info']['version']['current']['commit'] = autosetup_template['update-info']['version']['current']['commit']
        autosetup['update-info']['version']['current']['date'] = autosetup_template['update-info']['version']['current']['date']
    else:
        print('Already at latest version.')
except:
    print('Error occurred, could not update')
