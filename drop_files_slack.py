#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import json
import datetime
import logging

logging.basicConfig(
    filename='slack.log',
    filemode='w',
    format='%(asctime)s || %(process)d || %(name)s || %(levelname)s - %(message)s',
    level=logging.DEBUG
)

token = '<<<TOKEN>>>'
days = 30
ts_to = int(time.time()) - days * 24 * 60 * 60
count = 1000
# types = 'all'
# types = 'doc'
# types = 'snippets,images,gdocs,zips,pdfs,videos,spreadsheets,presentations'
# docs,binary,docx,text,sql,javascript,xml,pdf,jpg,xls,png,vb,python,xlsx
types = 'images'

def list_files():
  params = {
    'token': token,
    'ts_to': ts_to,
    'count': count,
    'types': types
  }
  uri = 'https://slack.com/api/files.list'
  response = requests.get(uri, params=params)
  return json.loads(response.text)['files']


def info_user(user):
  params = {
    'token': token,
    'user': user,
  }
  uri = 'https://slack.com/api/users.profile.get'
  response = requests.get(uri, params=params)
  return json.loads(response.text)['profile']['real_name']


def delete_files(file_ids):
  count = 0
  num_files = len(file_ids)
  for file_id in file_ids:
    count = count + 1
    params = {
      'token': token,
      'file': file_id,
    }
    uri = 'https://slack.com/api/files.delete'
    response = requests.get(uri, params=params)
    print(str(count) + " of " + str(num_files) + " - " + str(file_id) + ' ' + response.text)


def file_ids(files):
  return [f['id'] for f in files]


def file_filter(files):
  return [f for f in files if f['filetype']!='space']


def file_info(files):
  for file in files:
    print('Name: ' + file['name'])
    print('Created: ' + datetime.datetime.utcfromtimestamp(file['created']).strftime('%B %d, %Y %H:%M:%S'))
    print('Size: ' + str(file['size'] / 1000000) + ' MB')
    print('Filetype: ' + file['filetype'])
    print('Download: ' + file['url_private'])
    print('User: ' + info_user(file['user']))
    print('Channels: ' + str(file['channels']))
    print()

    



if __name__ == '__main__':
  try:
    print ("[*] Fetching file list..")
    files = list_files()
    files = file_filter(files)
    files_array_id = file_ids(files)
    file_info(files)
    # print ("[*] Deleting files..")
    # delete_files(files_array_id)

    print ("[*] Done")
  except Exception as e:
    logging.error(str(e), exc_info=True)
    print ("\b\b[-] Aborted")
    exit(1)