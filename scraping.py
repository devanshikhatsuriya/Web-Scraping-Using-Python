import requests
from bs4 import BeautifulSoup
import html5lib
import os


with open('input.txt','tr') as input:
	lines = input.readlines()
	start = lines[0].split()
	end = lines[1].split()
	authors = lines[2].split()

year_dict = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08',
'September':'09', 'October':'10', 'November':'11', 'December':'12'}

month_values = list(year_dict.values())
month_names = list(year_dict.keys())

def make_timeline(start, end):
	'''
	returns a list of lists, each list consists of month_number(string) and year(string) between and including start and end
	start and end are lists having month_name and year(string) 
	'''
	nstart = []
	nstart.append(year_dict[start[0]])
	nstart.append(start[1])
	nend = []
	nend.append(year_dict[end[0]])
	nend.append(end[1])
	n = 12*(int(nend[1])-int(nstart[1])) + (int(nend[0])-int(nstart[0])) + 1
	array = [[None,None] for i in range(n)]
	current = nstart
	array[0] = current
	for i in range(1, n):
		if int(current[0]) <= 11:
			month_int = (int(current[0]))+1
			if month_int <= 9:
				month = '0'+ str(month_int)
			else:
				month = str(month_int)
			year = current[1]
		else:
			month = '01'
			year = str(int(current[1])+1)
		current = [month, year]
		array[i] = current
	return array

timeline = make_timeline(start, end)
print("Timeline: ", timeline)

for author in authors:

	for domain in timeline:

		print("For", author, "during", domain, ":")

		home = "http://explosm.net/comics/archive/" + domain[1] + '/' + domain[0] + '/' + author.lower()

		print("Going to:", home)

		response = requests.get(home)
		if response.status_code != 200:
			raise requests.ConnectionError("Expected status code 200, but got {}".format(response.status_code))

		soup = BeautifulSoup(response.content, 'html5lib')

		url_list = []
		for comic in soup.findAll('div', attrs = {'class':'small-3 medium-3 large-3 columns'}):
			url = "http://explosm.net" + comic.a['href']
			url_list.append(url)

		date_list = []
		for comic in soup.findAll('div', attrs = {'id':'comic-author'}):
			date = comic.contents[0]
			date_list.append(date)

		total = len(url_list)

		for index in range(total):

			print("Going to:", url_list[index])

			page = requests.get(url_list[index])
			if page.status_code != 200:
				raise requests.ConnectionError("Expected status code 200, but got {}".format(page.status_code))

			soup2 = BeautifulSoup(page.content, 'html5lib')
			image = soup2.find('img', id='main-comic')
			src = "http:" + image['src']
			
			month_name = month_names[month_values.index(domain[0])]
			directory = domain[1]+"\\"+month_name
			current_dir = os.getcwd()

			path = os.path.join(current_dir, directory)
			if not os.path.isdir(path):
				print("Making directory:", path)
				os.makedirs(path)

			date = date_list[index]
			file_name = date.strip()+"-"+author+".png"
			final_path = os.path.join(path, file_name)

			print("Preparing to download file", index+1, "out of", total, end="; ")

			with open(final_path, 'wb') as image:
				comic = requests.get(src)
				if comic.status_code != 200:
					raise requests.ConnectionError("Expected status code 200, but got {}".format(comic.status_code))
				image.write(comic.content)

			print("Downloaded")











