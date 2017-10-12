import os

for dirname, dirnames, filenames in os.walk('/tipi_disk'):
    # print path to all subdirectories first.
    for subdirname in dirnames:

        print "subdirname: " + subdirname
 
        print(os.path.join(dirname, subdirname))

    # print path to all filenames.
    for filename in filenames:
        print(os.path.join(dirname, filename))


print "---------------------------------------------------------\n";


path = '/tipi_disk'

for item in os.listdir(path):

    item = os.path.join(path, item)

    if os.path.isdir(item):
        print item + " is a FUCKING dir god fucking damn it!"
 
