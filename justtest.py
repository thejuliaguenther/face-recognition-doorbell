#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: pic.py
import RPi.GPIO as GPIO
import time



import sys, os, glob, time
from boto.s3.connection import S3Connection
from boto.s3.key import Key

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)



AWS_ACCESS ='AKIAJVAP3ASQHYTSOA7A'
AWS_SECRET ='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'

conn = S3Connection(AWS_ACCESS,AWS_SECRET)
bucket = conn.get_bucket('imagesfrompi')
directory = '/home/pi/'

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


API_KEY = '332bee223735a8f34a37e2b428260c48'
API_SECRET = 'lgZP0QBuv0g4MXUuThPWMMWbvf6WdOC1'

# Import system libraries and define helper functions
# 导入系统库并定义辅助函数
from pprint import pformat
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

# First import the API class from the SDK
# 首先，导入SDK中的API类
from facepp import API

api = API(API_KEY, API_SECRET)



TARGET_IMAGE = 'https://imagesfrompi.s3.amazonaws.com/image2.jpg'


while True:
    input_state = GPIO.input(18)
    if input_state == False:
        print('Button Pressed')
	from subprocess import call
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
		print 'The person with highest confidence:', \
        	result['face'][0]['candidate'][0]['person_name']
	
