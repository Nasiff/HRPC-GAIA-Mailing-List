import re
import csv
import sys

filename = 'archives/gaia.csv'
listA = []

if sys.version_info[0] < 3: 
	infile = open(filename, 'rb')
else:
	infile = open(filename, 'r', newline='', encoding='utf8')

# Convert the CSV file into a list of lists for easier manipulation.
with infile as csvfile:
	csv_reader = csv.reader(csvfile)
	listA = list(csv_reader)
	print("Converted csv to list of lists. Size: " + str(len(listA)))

body = 6
listB = []

# Take only the body column of the previous list and append it to a
# new list for further analysis.
print("Extracting the body column...")
for items in listA:
	listB.append(items[body])

listC = []

# Find the words before and after the word infrastructure and append it to listC
print("Finding the words before and after infrastructure...")
for texts in listB:
	clean = texts.replace("\r\n", "")
	clean = clean.replace(">", "")
	clean = clean.replace("=", "")
	clean = clean.replace("<", "")
	clean = clean.replace("A0", " ")
	clean = clean.replace("*", " ")
	clean = clean.replace("\r", " ")
	clean = clean.strip()
	infrastructure = re.findall(r"(?:[a-zA-Z'-]+[^a-zA-Z'-]+){0,10}infrastructure(?:[^a-zA-Z'-]+[a-zA-Z'-]+){0,10}", clean)
	if len(infrastructure) > 1:
		listC.append(infrastructure)

print("Outputting to a CSV file: before_after...")

# Export the list into a CSV for viewing
with open('archives/before_after.csv', mode='w') as file:
	csv_writer = csv.writer(file, delimiter='|')

	for items in listC:
		try:
			csv_writer.writerow([items])
		except:
			pass
		

	# employee_writer.writerow(['John Smith', 'Accounting', 'November'])
	# employee_writer.writerow(['Erica Meyers', 'IT', 'March'])

print("Script Completed. Size: " + str(len(listC)))
