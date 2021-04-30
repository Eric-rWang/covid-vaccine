import csv

with open('owid-covid-data.csv', 'r') as csv_in:
	csv_file = csv.reader(csv_in, delimiter=',')
	data = []
	for line in csv_file:
		location = str(line[2])
		vaccinated = line[36]

		if location == "United States" and vaccinated != "":
			line_data = []
			line_data.append(line[2])
			line_data.append(line[3])
			line_data.append(line[36])
			
			data.append(line_data)
	
	#print(data)

	us_vaccine_data = "us_vaccine_data.csv"
	field = ['Location','Date','Fully Vaccinated']

	with open(us_vaccine_data, 'w') as csv_out:
		csv_writer = csv.writer(csv_out)
		csv_writer.writerow(field)
		csv_writer.writerows(data)