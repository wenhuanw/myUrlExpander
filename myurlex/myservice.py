import requests
from selenium import webdriver
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
import hashlib


def get_url(url, timestamp):
    api = 'http://archive.org/wayback/available' 
    params = {'url': url, 'timestamp': timestamp}
    r = requests.get(api, params=params)
    urls = r.json()
    if (urls['archived_snapshots'] == {}):
        return None
    waybackurl = urls['archived_snapshots']['closest']['url']
   # timestamp = urls['archived_snapshots']['closest']['timestamp']
    return waybackurl

def upload_image(wayback_url, image_id):

    # setup webdriver
    driver = webdriver.PhantomJS() # or add to your PATH
    driver.set_window_size(1024, 768) # optional
    #driver.get('http://www.facebook.com/')
    #s = 'http://www.facebook.com/'
    driver.get(wayback_url)

    #save screenshot of the website in memory
    driver.save_screenshot('screenshot.png')

    #get screenshot as png format
    screen = driver.get_screenshot_as_png()
    #name = driver.current_url


    #connect to S3 and upload image to S3
    conn = S3Connection('AKIAJFXQK5BUTQKE6P4A', 'L6Ve/N/kGzTRRowYj5k4pxB9l7swJQWy6T12iIZs')
    bucket = conn.get_bucket('wwhb1')
    k = Key(bucket)
    #ff = abs(hash(wayback_url)) % (10 ** 8)
    #fff = str(ff)
    k.key = 'image/'+image_id+'.png'
    k.set_contents_from_string(screen)



def delete_image(image_id):

    conn = S3Connection('AKIAJFXQK5BUTQKE6P4A', 'L6Ve/N/kGzTRRowYj5k4pxB9l7swJQWy6T12iIZs')
    bucket = conn.get_bucket('wwhb1')
    k = Key(bucket)
    k.key = 'image/'+str(image_id)+'.png'
    bucket.delete_key(k)



def get_id(url):
    hashcode = abs(hash(url)) % (10 ** 8)
    return str(hashcode)
