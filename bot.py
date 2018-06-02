import os
import sys
import time
import re
import requests
import sqlite3

from telegram.bot import Bot


class AsanaProjects:
	"""Class for projects/sync tokens sync"""
	sync_tokens = {}
	head = {}

	def getRequest(self, URL):
		head = {'Authorization': '{}'.format(ASANA_TOKEN)}
		response = requests.get(URL, headers=head)
		return response

	def getProjects(self):
		myUrl = 'https://app.asana.com/api/1.0/projects/'
		response = self.getRequest(myUrl)
		return response

	
	
		
	def getSyncToken(self, projectId):
		sync_token = self.sync_tokens.get(projectId, 0)
		print("Project {}, sync_token {}".format(projectId, sync_token))
		return sync_token

	def getEvents(self, projectId):
		sync_token=self.getSyncToken(projectId)
		myUrl = 'https://app.asana.com/api/1.0/events?resource={}&sync={}'.format(projectId,sync_token)
		print(myUrl)
		response = self.getRequest(myUrl)
		#response = requests.get(myUrl, headers=self.head)


		if response.status_code == 412:
			print("Status code: 412 (Token is expired)")	
			self.sync_tokens[projectId]=response.json()['sync']
			print(self.sync_tokens[projectId])
			response = self.getEvents(projectId)
		
		self.sync_tokens[projectId]=response.json()['sync']
		return response

	def getUpdatesOnProject(self, projectId):
		response = self.getEvents(projectId)
		return response.json().get('data', [])


	def getUpdates(self):
		value = {}
		
		print(self.sync_tokens)
		for p in self.sync_tokens.keys():
			print(self.getUpdatesOnProject(p))
			#for v in self.getUpdatesOnProject(p):
				#value.append(v)
		#return value
		return {}
		

	def __init__(self):
		self.__init__(ASANA_TOKEN)
		print("ASANA_TOKEN is not defined, use environmental one")

	def __init__(self, TOKEN):
		self.head = {'Authorization': '{}'.format(TOKEN)}

		projects = self.getProjects()
		print(projects)

		for project in projects.json()['data']:
			self.getUpdatesOnProject(project['id'])






TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_TARGET = os.environ['TELEGRAM_TARGET']
ASANA_TOKEN = os.environ['ASANA_TOKEN']

telegram_bot = Bot(TELEGRAM_TOKEN)


ap = AsanaProjects(ASANA_TOKEN)

VERBOSE_MODE = os.environ.get('VERBOSE', '0')

if VERBOSE_MODE=='1':
	print("Verbose mode is enabled")
	
	print('TELEGRAM_TOKEN: {}'.format(TELEGRAM_TOKEN))
	print('TELEGRAM_TARGET: {}'.format(TELEGRAM_TARGET))
	print('ASANA_TOKEN: {}'.format(ASANA_TOKEN))


while True:
	print(ap.getUpdates())
	time.sleep(60)


exit(0)

if (1==1):
        myUrl = 'https://app.asana.com/api/1.0/projects/' + str(id) + '/tasks'
        tasks = requests.get(myUrl, headers=head).json()
        for task in tasks['data']:
                task_id = task['id']

                myUrl = 'https://app.asana.com/api/1.0/tasks/' + str(task_id) 
                single_task = requests.get(myUrl, headers=head).json()
                print(single_task)

        print(i['name'])



response = requests.get('https://app.asana.com/api/1.0/projects', headers={'Authorization': ASANA_TOKEN})

print(response.json)



#telegram_bot.sendMessage(TELEGRAM_TARGET, msg_string)
