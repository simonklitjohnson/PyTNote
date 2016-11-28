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

try:
    __import__("appdirs")
except ImportError:
    confirm = input("Appdirs package is not installed and is required for PyTNote.\n\nDo you want to install it with pip? y/n \n(Note that if you do not have pip installed this will not work, and in that case see https://pip.pypa.io/en/stable/installing)\n> ")
    if confirm == "y":
        print(" ")
        os.system("pip install appdirs")
    else:
        print("Appdirs required. Stopping script.")
        sys.exit(0)
    pass

from appdirs import *

try:
    __import__("pyperclip")
except ImportError:
    confirm = input("Pyperclip package is not installed and is required for PyTNote.\n\nDo you want to install it with pip? y/n \n(Note that if you do not have pip installed this will not work, and in that case see https://pip.pypa.io/en/stable/installing)\n> ")
    if confirm == "y":
        print(" ")
        os.system("pip install pyperclip")
    else:
        print("Pyperclip required. Stopping script.")
        sys.exit(0)
    pass

import pyperclip

appname = "PyTNote"
appauthor = "SimonKlitJohnson"
args = sys.argv[1:]
notes = []

print(" ")  # Padding at beginning of script


def prnt(msg, bold=False):
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
				for note in outfile:
					prnt("("+str(i)+") "+"\033[4m" + datetime.datetime.fromtimestamp(int(note['creation_time'])).strftime('%d/%m - %H:%M') + "\033[0m: \"" +note['content'] + "\"")
					i = i + 1
			else:
				prnt("You have no notes at this time.", True)

	else:
		prnt("You have no notes at this time.", True)

file = user_data_dir(appname, appauthor) + "/pytnote.json"

if not os.path.isdir(user_data_dir(appname, appauthor)):
    os.mkdir(user_data_dir(appname, appauthor))

if len(args) == 0:
	read_notes()
elif args[0][:2] == "-d":
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

	confirm = input("Are you sure you want to clear your notes? y/n\n> ")
	print(" ")
	if confirm == "y":
		if os.path.exists(file): # Delete file containing notes = clear.
			os.remove(file)
			prnt("Notes cleared.\n", True)
		else:
			prnt("You have no notes to clear.", True)
	read_notes()

elif args[0][:2] == "-h":

	prnt("Help:\n",True)
	prnt("\033[1mno arguments\033[0m\t- lists all your notes and their times of creation")
	prnt("\033[1m*\033[0m\t\t- creates a new note consisting of all arguments joined.\n")
	prnt("\033[1m-c [note no.]\033[0m\t- copies the contents of the note to the clipboard")
	prnt("\033[1m-cl\033[0m\t\t- clears all notes (asks you to confirm before doing so)")
	prnt("\033[1m-d [note no.]\033[0m\t- deletes note with corresponding id")
	prnt("\033[1m-e [note no.]\033[0m\t- edits note with corresponding id")
	prnt("\033[1m-h\033[0m\t\t- lists this help menu")

elif args[0][:2] == "-e":
	if os.path.exists(file):
		with open(file, 'r') as notefile:
			notes = json.loads(notefile.read())
	note = notes[int(args[1]) -1]
	prnt("Editing note %s:\n" % (str(int(args[1]))), True)
	prnt("Old note is: \"%s\"." % (note['content']))

	if sys.platform == "darwin": # Script runs on macOS

		'''

		macOS allows us to use the proprietary scripting language AppleScript to control different aspects of the window
			manager and the system in general. This allows us to enter in the old note in the edit line, so the user actually
			edits the old note instead of simply retyping it.
			Not possible to do similar in Linux and Windows without installing
			external software.

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

		os.system(code.encode('utf-8', 'ignore'))

		newnote = input("")
		if newnote[:2] == "> ":
			newnote = newnote[2:]
		elif newnote[:1] == ">":
			newnote = newnote[1:]
		notes[int(args[1]) -1]['content'] = newnote

		write_and_read("\nNote succesfully edited.")

	else:
		prnt("\nType the new note below:")

		newnote = input("> ")
		notes[int(args[1]) -1]['content'] = newnote

		write_and_read("\nNote succesfully edited.")

else:
	if os.path.exists(file):
		with open(file, 'r') as notefile:
			notes = json.loads(notefile.read())
		notes.append({"creation_time":int(time.time()),"content":" ".join(args)})
		write_and_read()		
	else:
		notes.append({"creation_time":int(time.time()),"content":" ".join(args)})
		write_and_read()		

print(" ")  # Padding at end of script

