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


PERSONS = [
    ('Brad x', 'http://www.faceplusplus.com/static/img/demo/9.jpg'),
    ('Nicolas x', 'http://www.faceplusplus.com/static/img/demo/7.jpg'),
    ('Elizabeth x', 'https://imagesfrompi.s3.amazonaws.com/liz.jpg'), 
    ('Henry x', 'https://imagesfrompi.s3.amazonaws.com/henry.jpg'),
    ('Dave x', 'https://imagesfrompi.s3.amazonaws.com/dave.jpg'),
    ('Sara x', 'https://imagesfrompi.s3.amazonaws.com/sara.jpg'),
    ('Jackie x', 'http://www.faceplusplus.com/static/img/demo/6.jpg')
]

api.group.delete(group_name = 'test')
#api.person.delete(person_name = [i[0] for i in PERSONS])
# Here are the person names and their face images
# 人名及其脸部图片

TARGET_IMAGE = 'https://imagesfrompi.s3.amazonaws.com/image2.jpg'
# Step 1: Create a group to add these persons in
# 步骤1： 新建一个group用以添加person
api.group.create(group_name = 'test')

# Step 2: Detect faces from those three images and add them to the persons
# 步骤2：从三种图片中检测人脸并将其加入person中。 
for (name, url) in PERSONS:
    result = api.detection.detect(url = url, mode = 'oneface')
    print_result('Detection result for {}:'.format(name), result)

    face_id = result['face'][0]['face_id']

    # Create a person in the group, and add the face to the person
    # 在该group中新建一个person，并将face加入期中
    api.person.create(person_name = name, group_name = 'test',
            face_id = face_id)


# Step 3: Train the group.
# Note: this step is required before performing recognition in this group,
# since our system needs to pre-compute models for these persons
# 步骤3：训练这个group
# 注：在group中进行识别之前必须执行该步骤，以便我们的系统能为这些person建模
result = api.recognition.train(group_name = 'test', type = 'all')

# Because the train process is time-consuming, the operation is done
# asynchronously, so only a session ID would be returned.
# 由于训练过程比较耗时，所以操作必须异步完成，因此只有session ID会被返回
print_result('Train result:', result)

session_id = result['session_id']
# Now, wait before train completes
# 等待训练完成
while True:
    result = api.info.get_session(session_id = session_id)
    if result['status'] == u'SUCC':
        print_result('Async train result:', result)
        break
    time.sleep(1)

#也可以通过调用api.wait_async(session_id)函数完成以上功能



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
	print '=' * 60
	print 'The person with highest confidence:', \
        result['face'][0]['candidate'][0]['person_name']
	
