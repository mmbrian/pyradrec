##pyRadRec
This script can record an mp3 SHOUTcast station for a given amount of time. It stores tracks in separate files inside a "data" folder. It also keeps a log of each recording session. Furthermore, you can specify an email address to receive event notifications including download links to recorded tracks.

###Requirements
In order to use this script, you need access to an SMTP server for sending email notifications or you could just comment that piece of code. Also, it is assumed you have access to a static directory from a root url (possibly a web server is handling that). This is required in order to generate accessible download links, but again, it isn't required if you want to run it only locally.

###Dependencies
- [python-slugify] (https://github.com/un33k/python-slugify) I use this just to make sure file names are okay for download links, so not really a dependency.

###Usage
Start recorder by executing:

    python capturer.py rec
    
You can schedule it on cron. That's what I am doing so I can record my favarite radio show every week. It streams during midnight so I had to find a way of recording it.

###License
© 2013, Mohsen Mansouryar Released under the [MIT License] (/LICENSE).
