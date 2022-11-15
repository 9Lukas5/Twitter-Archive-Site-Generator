#!python3
#

import glob
import os
import re
import shutil
import yaml

docsDir = "docs"
mediaDir = "media"

# create docs folder
if os.path.exists(docsDir):
    if not os.path.isdir(docsDir):
        raise Exception("Folder 'docs' already exists")
else:
    print("Create folder: '{}'".format(docsDir))
    os.mkdir(docsDir)

# moving markdown and media files to the docs folder
if os.path.exists(mediaDir) and not os.path.exists(os.path.join(docsDir, mediaDir)):
    print("Move {} into '{}'".format(mediaDir, docsDir))
    shutil.move(mediaDir, docsDir)
else:
    print("WARNING: media folder not moved (either not found or already exists in target")

for entry in glob.glob("*Tweet-Archive*.md"):
    print("move {} into {}".format(entry, docsDir))
    shutil.move(entry, docsDir)

# create mkdocs config
print("Generating MkDocs-Config...")
mkdocsConfig = dict()

mkdocsConfig['nav'] = list()

for entry in glob.glob("*.md", root_dir=docsDir):
    # add file to navigation
    pattern = re.compile("^(\\d\\d\\d\\d-\\d\\d-\\d\\d).*(\\d\\d\\d\\d-\\d\\d)\\.md$")
    match = pattern.match(entry)
    if match:
        mkdocsConfig['nav'].append({match.group(1) + " to " + match.group(2): entry})

    # find author
    if ('site_author' not in mkdocsConfig):
        with open(os.path.join(docsDir, entry)) as f:
            for line in f:
                pattern = re.compile(".*Originally on Twitter.*https:\\/\\/twitter.com\\/(.*)\\/status.*")
                match = pattern.match(line)
                if match:
                    mkdocsConfig['site_author'] = "@" + match.group(1)
                    break

mkdocsConfig['site_name'] = mkdocsConfig['site_author'] + "'s Twitter Archive"
mkdocsConfig['docs_dir'] = docsDir
mkdocsConfig['use_directory_urls'] = False

theme = dict()
theme['name'] = 'material'
theme['font'] = False
theme['palette'] = list()

nextItem = {'media': '(prefers-color-scheme: light)',
                'scheme': 'default',
                'primary': 'blue',
                'accent': 'blue gray',
                'toggle': {'icon': 'material/brightness-7', 'name': 'Light off'}}
theme['palette'].append(nextItem)

nextItem = {'media': '(prefers-color-scheme: dark)',
            'scheme': 'slate',
            'primary': 'blue',
            'accent': 'blue gray',
            'toggle': {'icon': 'material/brightness-4', 'name': 'Light on'}}
theme['palette'].append(nextItem)

mkdocsConfig['theme'] = theme

print("Writing index page")
with open(os.path.join(docsDir, 'index.md'), 'w') as file:
    file.write("# Twitter Archive of " + mkdocsConfig['site_author'] + "\n")
    file.write("\n")
    file.write("Find your Tweets in the navigation and have fun :)\n")
    mkdocsConfig['nav'].insert(0, {'Index': 'index.md'})

print("Writing mkdocs config")
with open(r'mkdocs.yaml', 'w') as file:
    outputs = yaml.dump(mkdocsConfig, file)
