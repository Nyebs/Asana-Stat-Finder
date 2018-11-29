#imports
import os
import sys
import time
import json
import csv
import requests
import random
import asana
import datetime
from zoomus import ZoomClient
import numpy

#globals
global asana_key
global zoom_key
global zoom_secret
global project_input
global run_date

#address of the api
asana_api = "https://app.asana.com/api/1.0"
zoom_api = "https://api.zoom.us/v2"
asana_key = "0/1d6bb7b9f13d37e61cb1e22a15a9182d"

def get(path, raw=False, **params):
  res = requests.get("%s/%s" % (asana_api, path), auth=(asana_key, ""), params=params)
  return res.text if raw else res.json()

run_date = datetime.datetime.now().date()

if __name__ == "__main__":
    def asana_grabby():
      print('')
      custom_key = str(input('custom api key? (y/n): '))
      if 'y' in custom_key:
          print('')
          asana_key = input('plz input your api key!~')
      else:
          asana_key = "0/1d6bb7b9f13d37e61cb1e22a15a9182d"
      print('')
      print('available projects: hr, office, it')
      print('')
      project_input = input('plz input project id, or choose from above!~: ')
      if 'hr' in project_input:
          project_input = '831207095409567'
      elif 'it' in project_input:
          project_input = '795311327897887'
      elif 'office' in project_input:
          project_input = '806230840501006'
      out = sys.stdout
      tasks = get("projects/%s/tasks" % project_input)['data']
      project = get("projects/%s" % project_input)['data']
      print('')
      print('getting ready to help you~')
      time.sleep(2)
      print('')
      print('creating file to write your data to~')
      time.sleep(2)
      project_name = project['name']
      with open('%s_%s_data.csv' % (project_name,run_date), mode='w', newline='') as data_file:
          data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
          print('')
          print('writing initial row~')
          time.sleep(2)
          data_writer.writerow(['Task','Notes','Created: Date','Responded: Date','Completed: Date','Days To Complete','Completed By'])
          print('')
          print('beginning task iteration sequence~')
          time.sleep(2)
          print('')
          print('artificial time delays disabled~')
          print('')
          print('brace yourself~')
          n = 0
          days_to_complete_data = []
          #longest_task = datetime.timedelta(-999999999)
          for task in tasks:
              task_data = get("tasks/%s" % task['id'])
              task_name = task['name']
              task_notes = get("tasks/%s" % task['id'])['data']
              task_notes = task_notes['notes']
              task_notes = str(task_notes).encode('utf-8')
              task_completed = get("tasks/%s" % task['id'])['data']
              stories = get("tasks/%s/stories" % task['id'])['data']
              ##task_completed = get('projects')
              added_date = str('none')
              responded_date = str('none')
              completed_date = str('none')
              completed_by = str('none')
              json.dump(task_data, out, indent=True)
              n = n+1
              print('')
              print('story iteration engage, round #%s~' % n)
              ##only complete tasks
              if True == task_completed['completed']:
                  for story in stories:
                      story['task_id'] = task['id']
                      if 'added_to_project' in str(story):
                          added_date_temp = story['created_at']
                          added_date = (added_date_temp[:10] + '') if len(added_date_temp) > 10 else added_date_temp
                          added_time = ('' + added_date_temp[10:]) if len(added_date_temp) > 10 else added_date_temp
                          ##stories_output.append(added_date)
                      elif 'comment_added' in str(story):
                          responded_date_temp = story['created_at']
                          responded_date = (responded_date_temp[:10] + '') if len(responded_date_temp) > 10 else responded_date_temp
                          responded_time = ('' + responded_date_temp[10:]) if len(responded_date_temp) > 10 else responded_date_temp
                          ##stories_output.append(responded_date)
                      elif 'marked_complete' in str(story):
                          completed_date_temp = story['created_at']
                          completed_date = (completed_date_temp[:10] + '') if len(completed_date_temp) > 10 else completed_date_temp
                          completed_time = ('' + completed_date_temp[10:]) if len(completed_date_temp) > 10 else completed_date_temp
                          completed_by = story['created_by']['name']
                          ##stories_output.append(completed_date)
                          ##stories_output.append(completed_by)
                          #else:
                              #stories_output.append('N/A')
                  if 'none' not in completed_date:
                      #math
                      #print(type(completed_date))
                      #time.sleep(15)
                      completed_date_year = completed_date[0:4]
                      completed_date_year = int(completed_date_year)
                      completed_date_month = completed_date[5:7]
                      completed_date_month = int(completed_date_month)
                      completed_date_day = completed_date[8:10]
                      completed_date_day = int(completed_date_day)
                      #print(completed_date_year)
                      #print(completed_date_month)
                      #print(completed_date_day)
                      utc_completed = datetime.date(completed_date_year, completed_date_month, completed_date_day)
                      added_date_year = added_date[0:4]
                      added_date_year = int(added_date_year)
                      added_date_month = added_date[5:7]
                      added_date_month = int(added_date_month)
                      added_date_day =  added_date[8:10]
                      added_date_day = int(added_date_day)
                      utc_added = datetime.date(added_date_year, added_date_month, added_date_day)
                      #print(utc_added)
                      #print(utc_completed)
                      days_to_complete = utc_completed - utc_added
                      #if days_to_complete > longest_task:
                        #longest_task = days_to_complete
                      days_to_complete = days_to_complete.total_seconds()
                      days_to_complete = (((days_to_complete / 60) / 60) / 24)

                      #writeout
                      #longest_task = (((int(longest_task.total_seconds()) / 60) / 60) / 24)
                      print('')
                      print("writing data to table~")
                      stories_output = [task_name, task_notes, added_date, responded_date, completed_date, days_to_complete, completed_by]
                      print('')
                      print('writing table to file~')
                      data_writer.writerows([stories_output])
                      days_to_complete_data.append(days_to_complete)

          average_response = numpy.average(days_to_complete_data)
          data_writer.writerow([])
          data_writer.writerow(['','','','','AVERAGE RESPONSE TIME:',average_response])
          #data_writer.writerow(['','','','','LONGEST TASK TIME:',average_response])
          print('')
          print('all done~')
          ran = ['plz praise me (`･ω･´)', 'i accept headpats as thank you ヽ(´ー｀)ノ', 'uwu~', 'remember to drink water today ʕᵔᴥᵔʔ!', 'i wuv u', 'whats your favorite anime?','please come hang out again soon~ (づ｡◕‿‿◕｡)づ', '御粗末! ヾ(-_- )ゞ', 'What a good workout! ᕙ(⇀‸↼‶)ᕗ']
          end_phrase = random.choice(ran)
          print('')
          print(end_phrase)

    def zoom_grabby():
        zoom_key = 'DA_JxFR_Szy3qJmBzii8HA'
        zoom_secret = 'bCq9IWruug9RkBJ5fRhXUOT6wctJn6pu'
        zoom_token = 'cVtWHKu-QyOXA7hnGw29ng'
        #DA_JxFR_Szy3qJmBzii8HA
        #bCq9IWruug9RkBJ5fRhXUOT6wctJn6pu
        def getz(path, raw=False, **params):
          res = requests.get("%s/%s" % (zoom_api, path), auth=(zoom_token, ""), params=params)
          return res.text if raw else res.json()
        custom_key = str(input('custom api key? (y/n): '))
        if 'y' in custom_key:
            print('')
            zoom_key = input('plz input your api key!~')
        timeframe = input('daily/monthly/yearly: ')
        client = ZoomClient(zoom_key, zoom_secret)
        with open('zoom_%s_%s_data.csv' % (run_date,timeframe), mode='w', newline='') as data_file:
            data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            print('')
            print('writing initial row~')
            data_writer.writerow(['Meeting Minutes','Participants','Total Meetings'])
            time.sleep(2)
            start_date
            zoom_users = getz(client.report.get_account_report())['total_meetings']
            #zoom_users = str(zoom_users)
            for zoom_user in zoom_users:
                print('')
                print('writing table to file~')
                data_writer.writerows([zoom_user])
            #zoom_data = getz("report/%s" % timeframe)
            #participants = getz("report/%s" % timeframe)['total_participants']
            #meetings = getz("reports/%s" % timeframe)['total_meetings']

    def slack_grabby():
        print('this section under development q.q~')

    #if user entered proj number as arguement, use that
    if len(sys.argv) == 2:
      if 'help' in sys.argv[1]:
          print('')
          print('hello~!')
          print('')
          print('welcome to the data grabber! theres a few ways to use me...')
          print('')
          print('')
      else:
          project_input = sys.argv[1]
          #api key
          asana_key = "0/1d6bb7b9f13d37e61cb1e22a15a9182d"
          asana_grabby()

    #if user did not enter project number, ask for one
    elif len(sys.argv) == 1:
      print('')
      print('available services: asana, zoom, slack')
      print('')
      service_choice = input('please type which you want to proceed with~: ')
      if service_choice == 'asana':
          asana_grabby()
      elif service_choice == 'zoom':
          zoom_grabby()
      elif service_choice == 'slack':
          slack_grabby()
      elif service_choice == 'will is cute!':
          print('hauu~!')

#to-dos
#-add task notes
