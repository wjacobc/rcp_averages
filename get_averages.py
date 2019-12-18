from bs4 import BeautifulSoup
import requests

html_doc = requests.get("https://www.realclearpolitics.com/epolls/2020/president/us/2020_democratic_presidential_nomination-6730.html")

soup = BeautifulSoup(html_doc.text, 'html.parser')

candidates = []
averages = []

for row in soup.table:
    if "header" in row["class"]:
       candidates = row.text.split(" ")

       # Remove the "PollDate" from the first candidate
       candidates[0] = candidates[0][8:]
       # Remove the "Spread" category
       candidates.remove("Spread")

    # Find the RCP Average row
    if "RCP" in row.text:
        for data in row:
            if " " not in data.text and "RCP" not in data.text:
                averages.append(float(data.text))

# Create a tuple of the candidate and their average
candidates_and_averages = zip(candidates, averages)

# Find the length of the longest name, we will use this to make
# the data tabular when we print
longest_str_length = len(max(candidates, key=len))

for entry in candidates_and_averages:
    candidate_name, candidate_average = entry

    # Create a whitespace buffer to make the print tabular
    # The buffer is made based on the longest candidate's name
    # from earlier
    buf = " " * (longest_str_length - len(candidate_name))

    # Add one extra whitespace if the average is less than
    # ten, so that it's right aligned
    if candidate_average < 10:
        buf += " "

    print(candidate_name + ": " + buf + str(candidate_average))
