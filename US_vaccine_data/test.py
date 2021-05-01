import uuid, json, os, csv, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl

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

	plt.plot(x_values, fully_vaccinated)
	plt.xlabel("Date")
	plt.ylabel("Fully Vaccinated")
	plt.title("Number of Fully Vaccinated People in the US")
	plt.ylim(1342086.0, 96747454.0)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
	plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
	plt.gcf().autofmt_xdate()
	plt.show()
