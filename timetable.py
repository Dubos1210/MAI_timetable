group = "М4О-114Б-20"
week = 11

try:
	import requests
except ModuleNotFoundError:
	import pip
	pip.main(['install', 'requests'])
	import requests

try:
	from bs4 import BeautifulSoup
except ModuleNotFoundError:
	import pip
	pip.main(['install', 'bs4'])
	from bs4 import BeautifulSoup

from datetime import datetime

wday = {"Пн": 1, "Вт": 2, "Ср": 3, "Чт": 4, "Пт": 5, "Сб": 6, "Вс": 7}
time = {"09:00 – 10:30": 1, "10:45 – 12:15": 2, "13:00 – 14:30": 3, "14:45 – 16:15": 4, "16:30 – 18:00": 5, "18:15 – 19:45": 6}
tim2 = ["09:00<br>10:30", "10:45<br>12:15", "13:00<br>14:30", "14:45<br>16:15", "16:30<br>18:00", "18:15	<br>19:45"]

def getTimetable(group, week):
	print("Downloading timetable for "+group+" (week "+str(week)+")")
	timetable = [["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""]]
	data_group = requests.get("https://mai.ru/education/schedule/detail.php?group="+group+"&week="+str(week)).text
	soup = BeautifulSoup(data_group, 'html.parser')
	days = soup.find('div', {'id': 'schedule-content'}).find_all('div', {'class': 'sc-container'})
	for day in days:
		curr_day = wday[day.find('span', {'class': 'sc-day'}).text]
		lessons = day.find('div', {'class': 'sc-table-detail'}).find_all('div', {'class': 'sc-table-row'})
		for lesson in lessons:
			ltime = time[lesson.find('div', {'class': 'sc-item-time'}).text]
			ltype = lesson.find('div', {'class': 'sc-item-type'}).text.replace(' ', '')
			ltitle = lesson.find('span', {'class': 'sc-title'}).text
			llocation = lesson.find_all('div', {'class': 'sc-table-col sc-item-location'})[1].text.replace('\n', '').replace('\t', '').replace('\xa0', '')
			#print(str(curr_day)+": "+str(ltime)+"\t"+llocation+"\t"+ltitle+" ("+ltype+")")
			timetable[curr_day-1][ltime-1] = ltitle+" <i>("+ltype+"/"+llocation+")</i>"
	return timetable

timetable1 = getTimetable(group, week)
timetable2 = getTimetable(group, week+1)

print("Creating file '"+"timetable_"+group+"_"+str(week)+".html"+"'")

html = open("timetable_"+group+"_"+str(week)+".html", 'w')
html.write("<!DOCTYPE html>" + '\n')
html.write("<html>" + '\n')
html.write("\t<head>" + '\n')
html.write("\t\t<META charset=\"windows-1251\">" + '\n')
html.write("\t\t<LINK rel=\"stylesheet\" href=\"style.css\" type=\"text/css\">" + '\n')
html.write("\t</head>" + '\n')
html.write("\t<body>" + '\n')
html.write("\t\t<h1>Расписание занятий <b>"+group+" [недели "+str(week)+"-"+str(week+1)+"]</b></h1>" + '\n')
html.write("\t\t<p class='subheading'>Сформировано скриптом <a href='mailto:dubos1210@yandex.ru'>Владимира Дубишкина</a> "+datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")+"</p>" + '\n')
html.write("\t\t<table>" + '\n')
html.write("\t\t\t<tr class='heading'>" + '\n')
html.write("\t\t\t\t<td></td>" + '\n')
html.write("\t\t\t\t<td>ПН</td>" + '\n')
html.write("\t\t\t\t<td>ВТ</td>" + '\n')
html.write("\t\t\t\t<td>СР</td>" + '\n')
html.write("\t\t\t\t<td>ЧТ</td>" + '\n')
html.write("\t\t\t\t<td>ПТ</td>" + '\n')
html.write("\t\t\t\t<td>СБ</td>" + '\n')
html.write("\t\t\t</tr>" + '\n')
for j in range(6):
	html.write("\t\t\t<tr>" + '\n')
	html.write("\t\t\t\t<td rowspan='2' style='text-align: center;'><span style='font-weight: bold; font-size: 1.5em'>"+str(j+1)+"</span><br><i>"+tim2[j]+"</i></td>" + '\n')
	for i in range(6):
		html.write("\t\t\t\t<td")
		if(timetable1[i][j] == timetable2[i][j]):
			if(timetable1[i][j] != ""):
				html.write(" style='background: #FFE4C4'")				
			html.write(" rowspan='2'")
		else:
			html.write(" style='background: #7FFFD4'")
		html.write(">"+timetable1[i][j]+"</td>" + '\n')
	html.write("\t\t\t</tr>" + '\n')

	html.write("\t\t\t<tr>" + '\n')
	for i in range(6):
		if(timetable1[i][j] != timetable2[i][j]):
			html.write("\t\t\t\t<td style='background: #87CEFA'>"+timetable2[i][j]+"</td>" + '\n')
	html.write("\t\t\t</tr>" + '\n')
html.write("\t\t</table>" + '\n')
html.write("\t\t<p class='info'>Для печати вызовите окно печати (Ctrl+P), выберите необходимую ориентацию листа и масштаб, отключите поля.</p>" + '\n')
html.write("\t</body>" + '\n')
html.write("</html>" + '\n')
html.close()

print("Done")
