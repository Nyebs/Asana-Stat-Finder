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
from pprint import pprint
import numpy
#from jsondb.db import Database
from collections import Counter

#globals
global asana_key
global zoom_key
global zoom_secret
global project_input
global run_date

#address of the api
asana_api = "https://app.asana.com/api/1.0"
zoom_api = "https://api.zoom.us/v2"
asana_key = "FILLMEIN"

def get(path, raw=False, **params):
  res = requests.get("%s/%s" % (asana_api, path), auth=(asana_key, ""), params=params)
  return res.text if raw else res.json()

#def get2(path, raw=False, **params):
  #res = requests.get("%s/%s" % (asana_api, path), auth=(asana_key, ""), params=params)
  #return res.json() if raw else res.text

run_date = datetime.datetime.now().date()

if __name__ == "__main__":
    def asana_grabby():
      print('')
      custom_key = str(input('custom api key? (y/n): '))
      if 'y' in custom_key:
          print('')
          asana_key = input('plz input your api key!~')
      custom_date_yn = str(input('custom date? (y/n): '))
      if 'y' in custom_date_yn:
          custom_year = int(input('year: '))
          custom_month = int(input('month (as number): '))
      else:
          asana_key = "FILLMEIN"
      print('')
      print('--------------------')
      print('available projects: ')
      print('1. hr')
      print('2. office')
      print('3. it')
      print('4. sm-3rd party')
      print('5. sm-release')
      print('6. custom')
      print('7. print um')
      print('--------------------')
      print('')
      project_input = input('plz choose from the above!~: ')
      def printer():
          project_list = get("projects")['data']
          for proj in project_list:
              print(proj['name'])
      if 'hr' in project_input:
          project_input = 'FILLMEIN'
      elif 'it' in project_input:
          project_input = 'FILLMEIN'
      elif 'office' in project_input:
          project_input = 'FILLMEIN'
      elif 'sm-3rd party' in project_input:
          project_input = 'FILLMEIN'
      elif 'sm-release' in project_input:
          project_input = 'FILLMEIN'
      elif 'custom' in project_input:
          project_input = input('enter project id number~: ')
      elif 'print' or 'print um' in project_input:
          printer()
          project_input = input('please select a project!~: ')
      out = sys.stdout
      #if project_input in
      tasks = get("projects/%s/tasks" % project_input)['data']
      project = get("projects/%s" % project_input)['data']
      print('')
      print(project_input)
      print('--------------------')
      print('getting ready to help you~')
      print('--------------------')
      print('')
      time.sleep(2)
      print('')
      print('--------------------')
      print('creating file to write your data to~')
      print('--------------------')
      print('')
      time.sleep(2)
      project_name = project['name']
      if custom_date_yn == "y":
          time_frame = custom_month
      elif custom_date_yn == "n":
          time_frame = "Full"
      with open('%s_%s_%s_tixdata.csv' % (project_name,run_date,time_frame), mode='w', newline='') as data_file:
          data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
          print('')
          print('--------------------')
          print('writing initial row~')
          print('--------------------')
          print('')
          time.sleep(2)
          data_writer.writerow(['TASK','NOTES','CREATED: DATE','RESPONDED: DATE','COMPLETED: DATE','DAYS TO RESPOND:', 'DAYS TO COMPLETE','COMPLETED BY','URGENCY'])
          print('')
          print('--------------------')
          print('beginning task iteration sequence~')
          print('--------------------')
          print('')
          time.sleep(2)
          print('')
          print('--------------------')
          print('artificial time delays disabled~')
          print('')
          print('brace yourself~')
          print('--------------------')
          print('')
          n = 0
          days_to_complete_data = []
          days_to_respond_data = []
          completed_by_list = []
          standard_average_close_data = []
          standard_average_response_data = []
          low_average_close_data = []
          low_average_response_data = []
          urgent_average_close_data = []
          urgent_average_response_data = []
          longest_task = 0
          for task in tasks:
              task_data = get("tasks/%s" % task['id'])
              #print(task_data)
              task_name = task['name']
              #print(task_name)
              task_notes = get("tasks/%s" % task['id'])['data']
              json.dump(task_data, out, indent=True)
              task_notes = task_notes['notes']
              task_notes = str(task_notes).encode('utf-8')
              #task_notes = task_notes.split('b"',1)[1]
              task_completed = get("tasks/%s" % task['id'])['data']
              stories = get("tasks/%s/stories" % task['id'])['data']
              ##task_completed = get('projects')
              added_date = str('none')
              urgency_ofit = str('none')
              responded_date = str('none')
              completed_date = str('none')
              completed_by = str('none')
              ##json.dump(task_data, out, indent=True)
              n = n+1
              print('')
              print('--------------------')
              print('story iteration engage, round #%s~' % n)
              print('--------------------')
              print('')
              ##only complete tasks
              if True == task_completed['completed']:
                  response_time = None
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
                          completed_by_list.append(completed_by)
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
                      days_to_complete = days_to_complete.total_seconds()
                      days_to_complete = (((days_to_complete / 60) / 60) / 24)
                      if int(days_to_complete) > int(longest_task):
                        longest_task = int(days_to_complete)
                      if 'none' not in responded_date:
                          responded_date_year = responded_date[0:4]
                          responded_date_year = int(responded_date_year)
                          responded_date_month = responded_date[5:7]
                          responded_date_month = int(responded_date_month)
                          responded_date_day = responded_date[8:10]
                          responded_date_day = int(responded_date_day)
                          utc_responded = datetime.date(responded_date_year, responded_date_month, responded_date_day)
                          response_time4 = utc_responded - utc_added
                          response_time3 = response_time4.total_seconds()
                          response_time = (((response_time3 / 60) / 60) / 24)
                          days_to_respond_data.append(response_time)
                          #if isinstance(urgency_note, str):
                      try:
                          task_data2 = str((task_data["data"])["custom_fields"])
                          #urgency_note = [db_item["enum_value"] for db_item in task_data]
                          urgency_note = task_data2.split("enum_value",1)[1]

                      except KeyError:
                          task_urgency = int(0)

                      if custom_date_yn == 'y':
                          if completed_date_year == custom_year and completed_date_month == custom_month:
                              if 'Normal' in urgency_note:
                                  if 'none' not in completed_time:
                                      standard_average_close_data.append(int(days_to_complete))
                                  if 'none' not in responded_date:
                                      standard_average_response_data.append(int(response_time))
                                  urgency_ofit = str('Normal')
                              if 'LowPri' in urgency_note:
                                  if 'none' not in completed_time:
                                      low_average_close_data.append(int(days_to_complete))
                                  if 'none' not in responded_date:
                                      low_average_response_data.append(int(response_time))
                                  urgency_ofit = str('Low')
                              if 'Urgent' in urgency_note:
                                  if 'none' not in completed_time:
                                      urgent_average_close_data.append(int(days_to_complete))
                                  if 'none' not in responded_date:
                                      urgent_average_response_data.append(int(response_time))
                                  urgency_ofit = str('Urgent')
                                          ##stories_output.append(completed_date)
                                          ##stories_output.append(completed_by)
                                          #else:
                                              #stories_output.append('N/A')
                      elif custom_date_yn == 'n':
                          if 'Normal' in urgency_note:
                              if 'none' not in completed_time:
                                  standard_average_close_data.append(int(days_to_complete))
                              if 'none' not in responded_date:
                                  standard_average_response_data.append(int(response_time))
                              urgency_ofit = str('Normal')
                          if 'LowPri' in urgency_note:
                              if 'none' not in completed_time:
                                  low_average_close_data.append(int(days_to_complete))
                              if 'none' not in responded_date:
                                  low_average_response_data.append(int(response_time))
                              urgency_ofit = str('Low')
                          if 'Urgent' in urgency_note:
                              if 'none' not in completed_time:
                                  urgent_average_close_data.append(int(days_to_complete))
                              if 'none' not in responded_date:
                                  urgent_average_response_data.append(int(response_time))
                              urgency_ofit = str('Urgent')
                      #writeout
                      print('')
                      print('--------------------')
                      print("writing data to table~")
                      stories_output = [task_name, task_notes, added_date, responded_date, completed_date, response_time, days_to_complete, completed_by, urgency_ofit]
                      print('')
                      print('writing table to file~')
                      print('--------------------')
                      print('')
                      if custom_date_yn == 'y':
                          if completed_date_year == custom_year and completed_date_month == custom_month:
                              data_writer.writerows([stories_output])
                              days_to_complete_data.append(days_to_complete)
                      else:
                          data_writer.writerows([stories_output])
                          days_to_complete_data.append(days_to_complete)

          print('')
          print('--------------------')
          print('quick maths, one moment plz~')
          print('--------------------')
          print('')
          time.sleep(2)
          low_average_response = numpy.average(low_average_response_data)
          low_average_close = numpy.average(low_average_close_data)
          standard_average_response = numpy.average(standard_average_response_data)
          standard_average_close = numpy.average(standard_average_close_data)
          urgent_average_response = numpy.average(urgent_average_response_data)
          urgent_average_close = numpy.average(urgent_average_close_data)
          average_close = numpy.average(days_to_complete_data)
          average_response = numpy.average(days_to_respond_data)
          top_closer = Counter(completed_by_list)
          #top_closer = top_closer[2:]
          #top_closer = top_closer[:9]
          data_writer.writerow([])
          data_writer.writerow(['','','','','AVERAGE CLOSE TIME:',average_close])
          data_writer.writerow(['','','','','AVERAGE RESPONSE TIME:',average_response])
          data_writer.writerow(['','','','','TOP TICKET CLOSERS:',top_closer])
          data_writer.writerow(['','','','','LONGEST TASK TIME:',longest_task])
          data_writer.writerow(['','','','','AVERAGE RESPONSE: LOW',low_average_response])
          data_writer.writerow(['','','','','AVERAGE CLOSE: LOW',low_average_close])
          data_writer.writerow(['','','','','AVERAGE RESPONSE: STANDARD',standard_average_response])
          data_writer.writerow(['','','','','AVERAGE CLOSE: STANDARD',standard_average_close])
          data_writer.writerow(['','','','','AVERAGE RESPONSE: URGENT',urgent_average_response])
          data_writer.writerow(['','','','','AVERAGE CLOSE: URGENT',urgent_average_close])
          print('')
          print('--------------------')
          print('all done~')
          print('--------------------')
          print('')
          ran = ['plz praise me (`･ω･´)', 'i accept headpats as thank you ヽ(´ー｀)ノ', 'uwu~', 'remember to drink water today ʕᵔᴥᵔʔ!', 'i wuv u', 'whats your favorite anime?','please come hang out again soon~ (づ｡◕‿‿◕｡)づ', '御粗末! ヾ(-_- )ゞ', 'What a good workout! ᕙ(⇀‸↼‶)ᕗ']
          end_phrase = random.choice(ran)
          print('')
          print('--------------------')
          print(end_phrase)
          print('--------------------')
          print('')

    def zoom_grabby():
        zoom_key = 'FILLMEIN'
        zoom_secret = 'FILLMEIN'
        zoom_token = 'FILLMEIN'
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
            print('--------------------')
            print('writing initial row~')
            print('--------------------')
            print('')
            data_writer.writerow(['Meeting Minutes','Participants','Total Meetings'])
            time.sleep(2)
            start_date
            zoom_users = getz(client.report.get_account_report())['total_meetings']
            #zoom_users = str(zoom_users)
            for zoom_user in zoom_users:
                print('')
                print('--------------------')
                print('writing table to file~')
                print('--------------------')
                print('')
                data_writer.writerows([zoom_user])
            #zoom_data = getz("report/%s" % timeframe)
            #participants = getz("report/%s" % timeframe)['total_participants']
            #meetings = getz("reports/%s" % timeframe)['total_meetings']

    def slack_grabby():
        print('')
        print('--------------------')
        print('this section under development q.q~')
        print('--------------------')
        print('')

    #if user entered proj number as arguement, use that
    if len(sys.argv) == 2:
      if 'help' in sys.argv[1]:
          print('')
          print('--------------------')
          print('hello~!')
          print('')
          print('welcome to the data grabber! theres a few ways to use me...')
          print('')
          print('--------------------')
          print('')
      else:
          project_input = sys.argv[1]
          #api key
          asana_key = "FILLMEIN"
          asana_grabby()

    #if user did not enter project number, ask for one
    elif len(sys.argv) == 1:
      print()
      print('')
      print('--------------------')
      print('available services: ')
      print('1. asana')
      print('2. zoom')
      print('3. slack')
      print('--------------------')
      print('')
      service_choice = input('please type which you want to proceed with~: ')
      if service_choice == 'asana' or '1' or '1.':
          asana_grabby()
      elif service_choice == 'zoom' or '2' or '2.':
          zoom_grabby()
      elif service_choice == 'slack' or '3' or '3.':
          slack_grabby()
      elif service_choice == 'will is cute!':
          print('hauu~!')

#to-dos
#-add task notes
