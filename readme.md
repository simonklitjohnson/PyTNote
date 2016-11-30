# PyTNote
## PyTNote (Python Terminal Notes) is a simple note manager for your terminal.

PyTNote (Python Terminal Notes) is a simple note manager for your terminal.
It allows you to quickly and easily create and manage notes (or todo notes) without ever leaving your terminal workflow.

Creating a new note is as simple as typing "note Remember to update readme".

![alt tag](https://cloud.githubusercontent.com/assets/7118482/20732386/53157b12-b643-11e6-87ef-f6e7590927d7.png)

Stay on top of your productivity with PyTNote!

As of release 0.2 the script also includes a so-called "todo extension". This extension creates a small, separate script which allows you to create todo notes that can be marked as either done or not done. You do not have to install the todo extension as a separate script to gain access to the todo functionality, though. Instead of typing "todo", simply type "note -t".

Example: "note -t buy potatoes" is the same as "todo buy potatoes", as "note -t -m 1" is the same as "todo -m 1".

This software has no license, so do whatever you want to with it. I'd prefer it if you didn't sell it though.

## Getting started

Using PyTNote is really simple, but the script has a lot of extra functionality that can be nifty and nice to know about.

#### Arguments
You can use the following arguments when running the script:
```
no arguments	   - lists all your notes and their times of creation
*                  - creates a new note consisting of all arguments joined.

-c [note no.]	   - copies the contents of the note to the clipboard
-cl                - clears all notes (asks you to confirm before doing so)
-d [note no.]      - deletes note with corresponding no.
-e [note no.]      - edits note with corresponding no.
-h                 - lists this help menu
-t                 - create todo (offers to install todo extension on non-Windows)
-t -h              - list the help menu for todos
-u                 - update PyTNote if update is available
-uninstall         - uninstall PyTNote (asks you to confirm before doing so)
-uninstall -todo   - uninstall only the todo extension
-s [note no.]      - shares note with corresponding no. to hastebin (and copies URL to clipboard)
-sw [note no.]     - switches note with corresponding no. between being a todo and a note
```

And you can use the following arguments when running the todo extension:
```
no arguments	   - lists all your notes and their times of creation
*		           - creates a new todo consisting of all arguments joined.

-d [note no.]	   - deletes note with corresponding no.
-h		           - shows this help menu
-m [note no.]	   - marks the note as the opposite of what it currently is (done/not done)

-sw [note no.]	   - switches note with corresponding no. between begin a todo and a note
```

#### Dependencies
PyTNote requires Python 3.0 or newer to function.

PyTNote requires the following modules to work:
* appdirs (finds the correct place to store the notes depending on your OS)
* pyperclip (allows you to copy the note to clipboard)
* requests (allows you to share the note to hastebin.com)

But don't fret; if you have pip installed, all of the modules will automatically be installed upon running the script.

### macOS and Linux
Installing PyTNote on macOS and Linux distributions is as simple as running the following one-liner in your terminal:

`curl -o note https://raw.githubusercontent.com/simonklitjohnson/PyTNote/master/note.py && chmod +x note && mv note /usr/local/bin`

### Windows
I do not have a Windows machine, but I suppose you can pretty easily find a guide on how to make a python file executable in cmd on Windows somewhere.
