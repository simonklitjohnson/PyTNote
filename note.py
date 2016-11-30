#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

'''
    PyTNote (Python Terminal Notes) is a simple note manager for your terminal.
    It allows you to quickly and easily create and manage notes without ever leaving your Terminal workflow.

    Creating a new note is as simple as typing "note Remember to update readme".

    Stay on top of your productivity with PyTNote!

    This software has no license, so do whatever you want to with it. I'd prefer it if you didn't sell it though.
'''

import sys
import time
import datetime
import json
import os
import importlib
import zipfile
import shutil

def impmodule(module): # Function allows us to check whether a dependency is already met, and if not, install it with pip.
    try:
        __import__(module)
        return importlib.import_module(module)
    except ImportError:
        confirm = input("\n%s package is not installed and is required for PyTNote.\n\nDo you want to install it using pip? (y/n)\n(See https://pip.pypa.io/en/stable/installing if pip is not intalled on your machine)\n> " % (module))
        if confirm == "y":
            print(" ")
            os.system("pip install %s" % (module))
            print(" ")
            return importlib.import_module(module)
        else:
            print("%s is required. Stopping script." % (module))
            sys.exit(0)
        pass

appdirs = impmodule("appdirs")
pyperclip = impmodule("pyperclip")
requests = impmodule("requests")

appname = "PyTNote"
appauthor = "SimonKlitJohnson"
tag_name = 0.13
args = sys.argv[1:]
notes = []

print(" ")  # Padding at beginning of script

def prnt(msg, bold=False): # Allows us to easily make some text bold.
    if bold:
        print("\033[1m%s\033[0m" % (msg))
    else:
        print(msg)


def write_and_read(msg=None):
    write_notes()
    if msg == None:
        prnt("Note saved.\n", True)
    else:
        prnt(msg+"\n", True)
    read_notes()


def write_notes():
    with open(file, 'w+') as notefile:
        notefile.write(json.dumps(notes))


def read_notes():
    if os.path.exists(file):
        with open(file, 'r') as outfile:
            outfile = json.loads(outfile.read())
            if len(outfile) > 0:
                prnt("Your notes:", True)
                i = 1
                for note in outfile: # Convert timestamp to datetime and output the contents of the note.
                    prnt("("+str(i)+") "+"\033[4m" + datetime.datetime.fromtimestamp(int(note['creation_time'])).strftime('%d/%m - %H:%M') + "\033[0m: \"" +note['content'] + "\"")
                    i = i + 1
            else:
                prnt("You have no notes at this time.", True)

    else:
        prnt("You have no notes at this time.", True)

def check_update(retrn=True):
    try:
        r = requests.get("https://api.github.com/repos/simonklitjohnson/PyTNote/releases/latest", timeout=2).json()
        if float(r['tag_name']) > tag_name:
            if retrn:
                prnt("\nThere is a newer version of PyTNote available. Run PyTNote with \"-u\" argument to update. You will not lose your notes.", True)
            else:
                prnt(" ")
                return r
        else:
            if not retrn:
                return False
    except requests.exceptions.RequestException as e:
        return False
        pass

file = appdirs.user_data_dir(appname, appauthor) + "/pytnote.json" # Get OS-specific AppDirectory, in which to store the notes.

if not os.path.isdir(appdirs.user_data_dir(appname, appauthor)): # Create AppDirectory folder if it doesn't exists.
    os.mkdir(appdirs.user_data_dir(appname, appauthor))

if len(args) == 0: # If there are no arguments.
    read_notes()

elif args[0] == "-d":
    '''
        Deletes note by removing from list and then rewriting to notefile.
    '''
    try:
        with open(file, 'r') as notefile:
            notes = json.loads(notefile.read())
    except IOError:
        prnt("You have no notes at this time.\n", True)
        sys.exit(0)
    try:
        del(notes[int(args[1]) - 1])
        write_notes()
        prnt("Note %s deleted.\n" % (str(int(args[1]))), True)
    except IndexError:
        prnt("Note does not exist. Not deleted.\n", True)
        pass

    read_notes()

elif args[0] == "-c":
    '''
        Copies contents of the note to the clipboard using pyperclip module.
    '''
    
    try:
        with open(file, 'r') as notefile:
            notes = json.loads(notefile.read())
    except IOError:
        prnt("You have no notes at this time.\n", True)
        sys.exit(0)
    try:
        pyperclip.copy(notes[int(args[1]) - 1]["content"])
        prnt("Copied note %s to clipboard.\n" % (str(args[1])), True)
        read_notes()
    except IndexError:
        prnt("Note does not exist. Not copied.\n", True)
        read_notes()

elif args[0] == "-cl":
    '''
        Deletes all notes by simply deleting the notefile.
    '''
    confirm = input("Are you sure you want to clear your notes? (y/n)\n> ")
    print(" ")
    if confirm == "y":
        if os.path.exists(file): # Delete file containing notes = clear.
            os.remove(file)
            prnt("Notes cleared.\n", True)
        else:
            prnt("You have no notes to clear.", True)
    read_notes()

elif args[0] == "-h":

    prnt("Help:\n",True)
    prnt("\033[1mno arguments\033[0m\t- lists all your notes and their times of creation")
    prnt("\033[1m*\033[0m\t\t- creates a new note consisting of all arguments joined.\n")
    prnt("\033[1m-c [note no.]\033[0m\t- copies the contents of the note to the clipboard")
    prnt("\033[1m-cl\033[0m\t\t- clears all notes (asks you to confirm before doing so)")
    prnt("\033[1m-d [note no.]\033[0m\t- deletes note with corresponding no.")
    prnt("\033[1m-e [note no.]\033[0m\t- edits note with corresponding no.")
    prnt("\033[1m-h\033[0m\t\t- lists this help menu")
    prnt("\033[1m-u\033[0m\t\t- update PyTNote if update is available")
    prnt("\033[1m-uninstall\033[0m\t\t- uninstall PyTNote (asks you to confirm before doing so)")
    prnt("\033[1m-s [note no.]\033[0m\t- shares note with corresponding no. to hastebin (and copies URL to clipboard)")


elif args[0] == "-s":
    '''
        Shares the note to the pastebin platform hastebin. We use hastebin as it doesn't require you to have an API key.
        We could potentially add the option for different platforms, but for now hastebin will do fine.
    '''
    try:
        with open(file, 'r') as notefile:
            notes = json.loads(notefile.read())
    except IOError:
        prnt("You have no notes at this time.\n", True)
        sys.exit(0)
    try:
        r = requests.post("http://hastebin.com/documents", data=notes[int(args[1]) -1]['content'])
        r = json.loads(r.text)
        url = "http://hastebin.com/" + r['key']
        pyperclip.copy(url)
        prnt("Note shared to URL %s. URL copied to clipboard.\n" % (url), True)
        read_notes()
    except IndexError:
        prnt("Note does not exist. Not shared.\n", True)
        read_notes()
    except requests.exceptions.RequestException as e:
        prnt("Unable to share note. Do you have an internet connection?\n", True)
        read_notes()


elif args[0] == "-e":
    '''
        Edits the note so the timestamp will remain the same, but the content differs; for fixing typo etc.
    '''
    if os.path.exists(file):
        with open(file, 'r') as notefile:
            notes = json.loads(notefile.read())
    try:
        note = notes[int(args[1]) -1]
        prnt("Editing note %s:\n" % (str(int(args[1]))), True)
        prnt("Old note is: \"%s\"." % (note['content']))

        if sys.platform == "darwin": # Script runs on macOS

            '''

            macOS allows us to use the proprietary scripting language AppleScript to control different aspects of the window
                manager and the system in general. This allows us to enter in the old note in the edit line, so the user actually
                edits the old note instead of simply retyping it.
                Not possible to do similar in Linux and Windows without installing complex external software.

            Example of difference:

            macOS:
                ~$ note -e 1

                Editing note 1:

                Old note is: "test"

                Edit note below:
                > test █

            Other OS:
                ~$ note -e 1

                Editing note 1:

                Old note is: "test"

                Type the new note below:
                > █

            '''

            prnt("\nEdit note below:")

            code = """osascript -e 'tell application "Terminal" to activate
                            delay 0.2
                            tell application "System Events"
                                keystroke "> %s"
                        end tell'
                    """ % (note['content'])

            os.system(code.encode('utf-8', 'ignore')) # Run AppleScript code.

            newnote = input("")

            # We now have to remove the pseudo-prompt "> " that we added using AppleScript, so that it doesn't become part of the edited notes contents.

            if newnote[:2] == "> ":
                newnote = newnote[2:]
            elif newnote[:1] == ">":
                newnote = newnote[1:]

            notes[int(args[1]) -1]['content'] = newnote

            write_and_read("\nNote succesfully edited.")

        else:
            prnt("\nType the new note below:")

            notes[int(args[1]) -1]['content'] = input("> ")

            write_and_read("\nNote succesfully edited.")
    except IndexError:
        prnt("Note does not exist. Not editable.\n", True)
        read_notes()

elif args[0] == "-u":
    '''
        Update the script by downloading latest release zipball, unzipping and asking user to replace note script with new one.
    '''
    update = check_update(False)
    if update != False:
        prnt("Update available.\n", True)
        prnt("Update changelog: \"%s\"\n" % (update['body']))
        confirm = input("Do you want to download and install the new update? You won't lose your notes. (y/n)\n\n> ")
        if confirm == "y":
            if sys.platform != "win32":
                try:
                    prnt("\nUpdating PyTNote.\n", True)
                    prnt("Downloading...\n")

                    # Download update with cURL
                    os.system("curl -L %s > \"%s/note.zip\"" % (update['zipball_url'], appdirs.user_data_dir(appname, appauthor)))
                    
                    # Extract update zip.
                    prnt("\nExtracting...")
                    zip = zipfile.ZipFile(appdirs.user_data_dir(appname, appauthor) + '/note.zip', 'r')
                    namelist = zip.namelist()
                    zip.extractall(appdirs.user_data_dir(appname, appauthor))
                    zip.close()
                    
                    # Install update by making script executable and moving to correct location.
                    prnt("Installing...\n")
                    os.rename("%s/%snote.py" % (appdirs.user_data_dir(appname, appauthor), namelist[0]),  "%s/%snote" % (appdirs.user_data_dir(appname, appauthor), namelist[0]))
                    
                    # Make new note script executable.
                    os.system("chmod +x \"%s/%snote\"" % (appdirs.user_data_dir(appname, appauthor), namelist[0]))

                    # Move new note script to $/usr/local/bin for easy execution in terminal.
                    os.system("mv \"%s/%snote\" \"%s\"" % (appdirs.user_data_dir(appname, appauthor), namelist[0], os.path.dirname(os.path.realpath(__file__)) + "/" + os.path.basename(__file__)))

                    prnt("PyTNote succesfully updated.",True)
                except:
                    prnt("Something went wrong during the update. Try doing a manual update by following this URL (also copied to clipboard): %s" % (update['url']), True)
                    pyperclip.copy(update['url'])
            else:
                prnt("You can get the new update at: %s. URL copied to clipboard." % update['url'], True)
                pyperclip.copy(update['url'])
        else:
            prnt("\nNot updating.")
    else:
        prnt("No update available.\n", True)
        read_notes()
elif args[0] == "-uninstall":
    prompt = input("Are you sure you want to uninstall PyTNote? (y/n)\n> ")
    if prompt == "y":
        prompt = input("Do you want to delete all of your notes? (y/n)\n> ")
        if prompt == "y":
            shutil.rmtree(appdirs.user_data_dir(appname, appauthor))
        os.remove(os.path.dirname(os.path.realpath(__file__)) + "/" + os.path.basename(__file__))
        prnt("\nPyTNote uninstalled. Sad to see you go!\n", True)
        sys.exit(0)
    else:
        prnt("\nAborting uninstallation.",True)
else: # If the text passed does not match any of our commands = create new note.
    if os.path.exists(file): # If we already have some notes saved
        with open(file, 'r') as notefile:
            notes = json.loads(notefile.read())   
    notes.append({"creation_time":int(time.time()),"content":" ".join(args)})
    write_and_read()        

if "-u" not in args: # If we're not trying to update the script, check if an update is available.
    check_update()

print(" ")  # Padding at end of script
