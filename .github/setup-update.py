from git import Repo, Git
import yaml, os

with open('setup.yaml', 'r') as file:
    setup = yaml.load(file, Loader=yaml.FullLoader)

with open('.autosetup.yaml', 'r') as file:
    autosetup = yaml.load(file, Loader=yaml.FullLoader)

repo = Repo()
g = Git(os.getcwd())

repourl = 'https://github.com/' + os.environ["GITHUB_REPOSITORY"] # for local dev, set in bash: export GITHUB_REPOSITORY=<username>/<reponame>

# Set repo as instance if origin does not equal template target
if not autosetup['update-info']['isInitialized']:
    if setup['update-info']['template'] != repourl:
        autosetup['update-info']['isTemplate'] = False
        print('Detected difference between template and current repo URLs.')
        print('=> Marked repo as instance to .autosetup.yaml.')

print(autosetup['update-info']['isTemplate'])

if autosetup['update-info']['isTemplate']:
    
    print('This is set as a template repo.')
    # Set commit and date for current version
    autosetup['update-info']['version']['current']['commit'] = repo.head.commit.hexsha
    autosetup['update-info']['version']['current']['date'] = g.execute(["git", "log", "-1", "--format=%ci"])

    # Creating a list of files that should be updated from template to instance
    trackedfiles = g.execute(["git", "ls-tree", "-r", "HEAD", "--name-only"]).splitlines()
    # print(trackedfiles)
    updatefiles = []
    exampletwin = setup['update-info']['example-twin']
    for line in trackedfiles:
        # print(line[:4])
        # if line[:5] == 'docs/' and line[5:12] != 'static/' and line[5:14] != 'new-twin/':
        if not (line[:5] == 'docs/' and line[5:(5+len(exampletwin))] == exampletwin) and not line[:10] == 'setup.yaml':
            print('Including:     ' + line)
            updatefiles.append(line)
        else:
            print('Not including: ' + line)
    autosetup['update-info']['updateFiles'] = updatefiles

else:
    print('This is set as an instance repo.')

    if not autosetup['update-info']['isInitialized']:
        
        # Do initialization operations here
        print('Performing initialization operations...')

        autosetup['update-info']['isInitialized'] = True
        print('Initialization operations finished, marked repo as initialized.')
    else:
        print('Repo has been initialized earlier.')



# Write changes to .autosetup.yaml file
with open('.autosetup.yaml', 'w') as file:
        yaml.dump(autosetup, file, default_flow_style=False, sort_keys=False, allow_unicode=True)

print('Update setup finished')
