from ruamel import yaml
from jinja2 import Environment, FileSystemLoader, Template
import datetime
import os

# Edit ls output
def txt_editor(file_in, file_out):
    # Open in and out files
    f = open(file_in, "r")
    g = open(file_out, "w")

    # Get line by line
    for line in f:
        # If line not empty
        if line.strip():
            # If isnt a directory
            if not line.startswith('d'):
                # Write only last 3 columns in output
                g.write("\t".join(line.split()[2:]) + "\n")

    # Close files
    f.close()
    g.close()


now = datetime.datetime.now()

file = open('./config.yaml', 'r')
config_data = yaml.load(file, Loader=yaml.Loader)

# # List main server
os.system('lftp -c "source conf/original.conf && find -l . && exit" > lists/original.txt')
txt_editor("lists/original.txt", "lists/original_list.txt")

# Verify mirrors diff and update config data
mirrors = config_data['mirrors']
for mirror in mirrors:

    os.system('lftp -c "source conf/' + mirror + '.conf && find -l . && exit" > lists/'  + mirror + '.txt')
    txt_editor("lists/" + mirror + ".txt", "lists/" + mirror + "_list.txt")

    os.system("diff -u lists/original_list.txt lists/" + mirror + "_list.txt > webpage/" + mirrors[mirror]['diffFile'])

    if os.stat(mirrors[mirror]['diffFile']).st_size==0:
        if mirrors[mirror]['updated'] == False:
            mirrors[mirror]['lastUpdate'] = now.strftime("%Y-%m-%d %H:%M")
        mirrors[mirror]['updated'] = True
    else:
        mirrors[mirror]['updated'] = False

# Update time
config_data['lastRun'] = now.strftime("%Y-%m-%d %H:%M")
template_name = config_data['template']

# Save data
file = open('./config.yaml', 'w')
yaml.dump(config_data, file, Dumper=yaml.RoundTripDumper)

# Load Jinja2 template
env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('templates/' + template_name +'/template.j2')

# Update template files in the webpage folder
os.system('cp -r templates/' + template_name +'/* webpage/ ; rm webpage/template.j2')

# Render the template with data and save in webpage/index.html
file = open('webpage/index.html', 'w')
file.write(template.render(config_data))
