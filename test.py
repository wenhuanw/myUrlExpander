
from selenium import webdriver
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
from io import StringIO
from io import BytesIO
import urllib
from PIL import Image
import requests
import urllib.request
import hashlib

    # setup webdriver
driver = webdriver.PhantomJS() # or add to your PATH
driver.set_window_size(1024, 768) # optional
    #driver.get('http://www.facebook.com/')
    #s = 'http://www.facebook.com/'
driver.get('http://web.archive.org/web/20111120000707/http://www.facebook.com/')

    #save screenshot of the website in memory
driver.save_screenshot('screenshot.png')

    #get screenshot as png format
screen = driver.get_screenshot_as_png()
    #name = driver.current_url


    #connect to S3 and upload image to S3
conn = S3Connection('AKIAJFXQK5BUTQKE6P4A', 'L6Ve/N/kGzTRRowYj5k4pxB9l7swJQWy6T12iIZs')
bucket = conn.get_bucket('wwhb1')
k = Key(bucket)
ff = abs(hash('http://web.archive.org/web/20111120000707/http://www.facebook.com/')) % (10 ** 8)
fff = str(ff)
k.key = 'image/'+fff+'.png'
k.set_contents_from_string(screen)
