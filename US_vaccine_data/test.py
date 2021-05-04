import uuid, json, os, csv, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
from numpy import arange
from scipy.optimize import curve_fit
from datetime import date

def objective(x, a, b, c, d):
	return a * x**3 + b * x**2 + c * x + d

with open('us_vaccine_data.csv', 'r') as csv_in:
	csv_file = csv.reader(csv_in, delimiter=',')
	data = {"vaccine_data":[]}
	header = next(csv_file, None)

	for line in csv_file:
	    data['vaccine_data'].append({
	        'location': str(line[0]),
	        'date': str(line[1]),
	        'vaccinated': float(line[2])
	})

	dates = []
	fully_vaccinated = []

	for i in range(len(data['vaccine_data'])):
	    dates.append(data['vaccine_data'][i]['date'])
	    fully_vaccinated.append(data['vaccine_data'][i]['vaccinated'])

	x_values = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in dates]

	'''
	plt.plot(x_values, fully_vaccinated)
	plt.xlabel("Date")
	plt.ylabel("Fully Vaccinated")
	plt.title("Number of Fully Vaccinated People in the US")
	plt.ylim(1342086.0, 96747454.0)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
	plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
	plt.gcf().autofmt_xdate()
	#plt.savefig('vaccinated_graph.png')
	plt.show()
	'''

	x = list(range(len(dates)))
	popt, _ = curve_fit(objective, x, fully_vaccinated)
	a, b, c, d = popt
	print('y = %.5f * x^3 + %.5f * x^2 + %.5f * x + %.5f' % (a, b, c, d))

	plt.scatter(x,fully_vaccinated, s=1)
	x_line = arange(min(x), max(x), 1)
	y_line = objective(x_line, a, b, c, d)
	plt.plot(x_line, y_line, '--', color='green')
	plt.show()

	dates2 = "2021-05-03"
	date1 = dates[0].split('-')
	date2 = dates2.split('-')
	f_date = date(int(date1[0]), int(date1[1]), int(date1[2]))
	l_date = date(int(date2[0]), int(date2[1]), int(date2[2]))
	delta = l_date - f_date
	print(type(delta.days))

	print(objective(delta.days, a, b, c, d))








