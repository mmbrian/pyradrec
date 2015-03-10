#!/usr/bin/env /usr/local/bin/python2.7

import os, sys, urllib2
from logger import log, clear_logs
from time import time
from slugify import slugify
from settings import APP_ROOT, STATIC_ROOT_URL, RADIO_URL, RECORDING_TIME_IN_SECONDS
from smtpcon import send_mail as report

## References:
## https://stackoverflow.com/questions/10224488/python-script-to-record-online-live-streaming-videos
## http://www.smackfu.com/stuff/programming/shoutcast.html
## https://stackoverflow.com/questions/2757887/file-mode-for-creatingreadingappendingbinary

## Dependencies:
## https://github.com/un33k/python-slugify

def start():
    titles = []
    untitled_counter = 1

    # notify me by email
    try:
        report("Started", "Running Script...")
    except Exception, e:
        print e
        log("Exception occured:\n" + str(e))
    # Clearing old logs
    clear_logs()
    log("Generating request for stream:\n" + RADIO_URL)
    # This header would indicate we are requesting for shoutcast metadata info
    request = urllib2.Request(RADIO_URL, headers={"Icy-MetaData" : "1"})
    response = urllib2.urlopen(request)
    log("Initiated request...")
    # Reading meta intervals
    # This is the number of mp3 bytes between metadata blocks
    metaint = int(response.info()['icy-metaint'])
    log('Meta interval is: ' + str(metaint))
    # I'm using 1000 cause it is dividable by 16000 (metaint for klassikradio)
    block_size = 1000 
    read_bytes = 0
    last_track_title = ""

    # Temporary name until we fetch some metadata
    data_dir = os.path.join(APP_ROOT, 'data')
    if not os.path.exists(data_dir): os.makedirs(data_dir)
    filename = os.path.join(data_dir, "Temp.mp3")
    f = open(filename, 'wb')

    start = time()
    log("Started recording for " + str(RECORDING_TIME_IN_SECONDS) + " seconds...")
    while time() - start < RECORDING_TIME_IN_SECONDS:
        try:
            buffer = response.read(block_size)
            if not buffer:
                log("No more bytes to read...")
                break
            read_bytes += len(buffer)
            if read_bytes == metaint:
                # Reading metadata length byte
                meta_length = response.read(1)
                meta_length = ord(meta_length) * 16
                if meta_length > 0:
                    # Reading metadata
                    meta_data = response.read(meta_length)
                    # e.g: StreamTitle='Patrick Doyle - Non Nobis Domine (Heinrich V. / Film)';
                    track_title = meta_data[13:(meta_data.index(';')-1)]
                    if not track_title:
                        track_title = "untitled-" + str(untitled_counter)
                        untitled_counter += 1
                    track_title = slugify(track_title)
                    # print repr(track_title)
                    if not last_track_title:
                        # rename mp3 file
                        f.close()
                        new_path = os.path.join(data_dir, track_title + ".mp3")
                        # in case it already exists
                        if os.path.exists(new_path):
                            os.remove(new_path)
                        # cannot rename if a file with that name already exists
                        os.rename(filename, new_path)
                        filename = new_path
                        f = open(filename, 'ab+')
                        log("Currently playing " + track_title)
                    else:
                        if track_title != last_track_title:
                            # track changed on stream => create a new file
                            f.close()
                            filename = os.path.join(data_dir, track_title + ".mp3")
                            f = open(filename, 'wb')
                            log('%2.2f percent recorded...' % ((time() - start)/float(RECORDING_TIME_IN_SECONDS) * 100))
                            log("Track changed to " + track_title)
                    last_track_title = track_title
                    titles.append(track_title)
                read_bytes = 0
            # Writing to file    
            f.write(buffer)
        except Exception, e:
            print e
            log("Exception occured:\n" + str(e))
            if os.path.exists(filename):
                f = open(filename, 'ab')
            else:
                f = open(filename, 'ab+')
            # doing what we missed
            read_bytes = 0
            f.write(buffer)
            last_track_title = track_title
    f.close()
    log("Finished recording session")

    download_links = ""
    for title in titles:
        download_links += ''.join([STATIC_ROOT_URL, title, '.mp3', '\n'])
    log("Emailing download links...")
    try:
        report("Finished", download_links)
    except Exception, e:
        print e
        log("Exception occured:\n" + str(e))
    log("Task Finished")

def main():
    if 'rec' in sys.argv:
        start()
    else:
        print "No command was passed."

main()