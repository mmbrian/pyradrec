#!/usr/bin/env /usr/local/bin/python2.7

# IMPORTANT!
# rename this file to settings.py before use!

RADIO_URL = 'url_to_an_station'
# recording time in seconds
RECORDING_TIME_IN_SECONDS = 2 * 60 * 60 + 10 * 60 # 2 hours (+ 10 minutes)

# required for generating download links to recorded tracks
STATIC_ROOT_URL = 'url_to_static_directory_on_your_server'
# seriously required!
APP_ROOT = 'absolute_address_to_data_and_logs_folder'

# set these accordingly so that you'd be notified when recording
# gets started or finished. you will also receive download links
# to recorded tracks
EMAIL_HOST = 'smtp.somewhere.com'
EMAIL_HOST_USER = 'you_username'
EMAIL_HOST_PASSWORD = 'your_password'

# the email address which receives recording notifications
EMAIL_RECIPIENT = 'your_email_address'
