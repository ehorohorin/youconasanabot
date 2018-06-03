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
	last_used_token = 0
	head = {}

	def getRequest(self, URL):
		head = {'Authorization': '{}'.format(ASANA_TOKEN)}
		response = requests.get(URL, headers=head)
		return response

	def updateProjectList(self):
		myUrl = 'https://app.asana.com/api/1.0/projects/'
		response = self.getRequest(myUrl)
		
		for project in response.json()['data']:
			myUrl = 'https://app.asana.com/api/1.0/projects/{}'.format(project['id'])
			project_response = self.getRequest(myUrl)
			if project_response.json()['data']['archived'] == False:
				self.getUpdatesOnProject(project['id'])
			else:
				print('{} is archived'.format(project['id']))


		
	def getSyncToken(self, projectId):
		self.last_used_token = self.sync_tokens.get(projectId, self.last_used_token)
		print("Project {}, sync_token {}".format(projectId, self.last_used_token))
		return self.last_used_token

	def updateSyncToken(self, projectId, token):
		self.last_used_token=token
		self.sync_tokens[projectId]=self.last_used_token

	def getEvents(self, projectId):
		sync_token=self.getSyncToken(projectId)
		myUrl = 'https://app.asana.com/api/1.0/projects/{}/events?sync={}'.format(projectId,sync_token)
		print(myUrl)
		response = self.getRequest(myUrl)


		if response.status_code == 412:
			print("Status code: 412 (Token is expired)")	
			self.updateSyncToken(projectId,response.json()['sync'])
			myUrl = 'https://app.asana.com/api/1.0/projects/{}/events?sync={}'.format(projectId,self.sync_tokens[projectId])
			response = self.getRequest(myUrl)
			print('new token is: {}'.format(response.json()['sync']))
		
		self.updateSyncToken(projectId,response.json()['sync'])
		return response

	def getUpdatesOnProject(self, projectId):
		response = self.getEvents(projectId)
		return response.json().get('data', [])


	def getUpdates(self):
		print(self.sync_tokens)
		value = {}
		
		for p in self.sync_tokens.keys():
			for v in self.getUpdatesOnProject(p):
				value.update(v)
		return value
		#return {}
		

	def __init__(self):
		self.__init__(ASANA_TOKEN)
		print("ASANA_TOKEN is not defined, use environmental one")

	def __init__(self, TOKEN):
		self.head = {'Authorization': '{}'.format(TOKEN)}

		self.updateProjectList()


TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_TARGET = os.environ['TELEGRAM_TARGET']
ASANA_TOKEN = os.environ['ASANA_TOKEN']


def main():
	VERBOSE_MODE = os.environ.get('VERBOSE', '0')

	if VERBOSE_MODE=='1':
		print("Verbose mode is enabled")
	
		print('TELEGRAM_TOKEN: {}'.format(TELEGRAM_TOKEN))
		print('TELEGRAM_TARGET: {}'.format(TELEGRAM_TARGET))
		print('ASANA_TOKEN: {}'.format(ASANA_TOKEN))

	telegram_bot = Bot(TELEGRAM_TOKEN)
	ap = AsanaProjects(ASANA_TOKEN)

	print('Go wild!')
	while True:
		print(ap.getUpdates())
		time.sleep(60)


if __name__ == "__main__":
    main()

