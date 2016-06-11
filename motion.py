#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: pic.py
import RPi.GPIO as GPIO
import time
import urllib2
from urllib2 import URLError
from socket import socket




import sys, os, glob, time
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from pprint import pformat
from facepp import API
from subprocess import call

api = API(API_KEY, API_SECRET)

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)

GPIO.setup(4, GPIO.IN, GPIO.PUD_DOWN)
previous_state = False
current_state = False

conn = S3Connection(AWS_ACCESS,AWS_SECRET)
bucket = conn.get_bucket('imagesfrompi')
directory = '/home/pi/'

TARGET_IMAGE = 'https://imagesfrompi.s3.amazonaws.com/image2.jpg'

host = '162.243.246.25'
port = 3000

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

def getFiles(dir):
	return [os.path.basename(x) for x in glob.glob(str(dir) + '*.jpg')]

def setPinHigh():
	GPIO.output(7, GPIO.HIGH)	

def setPinLow():
	GPIO.output(7, GPIO.LOW)

def upload_S3(dir, file):
	k = Key(bucket)
	k.key = f
        setPinHigh()
	k.set_contents_from_filename(dir + f, cb=percent_cb, num_cb=10)
	setPinLow()

def removeLocal(dir, file):
	os.remove(dir + file)


def print_result(hint, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(k): encode(v) for (k, v) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hint
    result = encode(result)
    print '\n'.join(['  ' + i for i in pformat(result, width = 75).split('\n')])

while True:
    call(["fswebcam","image2.jpg"])
    time.sleep(1)
	print('go')
	filenames = getFiles(directory)
	print filenames
	for f in filenames:
        	print 'rnUploading %s to Amazon S3 bucket %s' % (f, bucket)
		upload_S3(directory, f)
        	removeLocal(directory, f)
	time.sleep(2)
	result = api.recognition.recognize(url = TARGET_IMAGE, group_name = 'test')
	print_result('Recognize result:', result)
        
        if result['face']:
		print '=' * 60
        result_name = result['face'][0]['candidate'][0]['person_name']
		# print 'The person with highest confidence:', \
  #       	result['face'][0]['candidate'][0]['person_name']
        print 'The person with highest confidence: ' +result_name]
		print("done")
		time.sleep(40)
        
	
