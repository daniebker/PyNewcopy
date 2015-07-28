__author__ = 'dbaker'

import hashlib
import optparse
import os
from shutil import copyfile


def hashfile(filePath):
    sha1 = hashlib.sha1()
    f = open(filePath, 'rb')

    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()


parser = optparse.OptionParser()

parser.add_option('-o', '--origin',
                  action="store", dest="origin",
                  help="the origin of the copy items")

parser.add_option('-d', '--destination',
                  action="store", dest="destination",
                  help="the destination of the copy items")

options, args = parser.parse_args()

for root, directories, files in os.walk(options.origin):
    for file in files:
        originFilePath = root + "\\" + file
        destinationFilePath = options.destination + root.split(options.origin)[-1] + "\\" + file

        if not os.path.exists(os.path.dirname(destinationFilePath)):
            os.makedirs(os.path.dirname(destinationFilePath))

        if os.path.isfile(originFilePath) and not os.path.isfile(destinationFilePath):
            print "File does not exist. Copying " + file + " to " + destinationFilePath
            copyfile(originFilePath, destinationFilePath)
        elif hashfile(originFilePath) != hashfile(destinationFilePath):
            print "Files differ. Copying " + file + " to " + destinationFilePath
            copyfile(originFilePath, destinationFilePath)
        else:
            print "File " + file + " exists at destination. Doing nothing."


