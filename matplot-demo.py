import json
from urllib.request import urlopen
import matplotlib.pyplot as plt

# This is just an "enum" for colors in the console
class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Initialize all of the empty list's
dkk_results = []
eur_results = []
hour_results = []

# Print to console, using colors
print(f"{color.BOLD}{color.HEADER}Getting data from API: \n")
print("\n"*9)
print(color.ENDC)

# API Url
url = "https://api.energidataservice.dk/datastore_search_sql?sql=SELECT%20%22HourDK%22,%20%22PriceArea%22,%20%22SpotPriceDKK%22,%20%22SpotPriceEUR%22%20FROM%20%22elspotprices%22%20WHERE%20%22PriceArea%22%20=%20%27DK2%27%20ORDER%20BY%20%22HourDK%22%20DESC%20LIMIT%2048"

# Get the response from opening the url, and automatically close it again
response = urlopen(url)

# Deserialize from json text, to a python dictionary
json_data = json.loads(response.read())

# Parse through the json "object", get the "result"
data = json_data["result"]

# And from within the "result", get the records, this is where the data is.
records = data["records"]
for record in records:
    dkk_results.append(record["SpotPriceDKK"]) # Append / Add to list
    eur_results.append(record["SpotPriceEUR"]) # Append / Add to list
    hour_results.append(record["HourDK"].split("T")[1].split(":")[0]) # Append / Add to list | 2022-02-15T00:00:00

dkk_results1 = dkk_results[:len(dkk_results)//2] # Get the first half of the list
dkk_results2 = dkk_results[len(dkk_results)//2:] # Get the second half of the list

eur_results1 = eur_results[:len(eur_results)//2] # Get the first half of the list
eur_results2 = eur_results[len(eur_results)//2:] # Get the second half of the list

hour_results = hour_results[:len(hour_results)//2] # Get the first half of the list

dkk_results1 = dkk_results1[::-1] # Reverse the list
eur_results1 = eur_results1[::-1] # Reverse the list

dkk_results2 = dkk_results2[::-1] # Reverse the list
eur_results2 = eur_results2[::-1] # Reverse the list

hour_results = hour_results[::-1] # Reverse the list


# Print to console
print(f"\n{color.BOLD}{color.HEADER}Generating curves: \n")
print("\n"*9)
print(color.ENDC)


# Create the plot/graph
plt.title("Engery prices for today & tomorow")
plt.ylabel("Price (DKK & EUR)")
plt.xlabel("Time (HOUR)")
plt.plot(hour_results, dkk_results1, label="DKK TODAY", linestyle="-", color="green")
plt.plot(hour_results, eur_results1, label="EUR TODAY", linestyle="-", color="green")
plt.plot(hour_results, dkk_results2, label="DKK TOMOROW", linestyle="-", color="red")
plt.plot(hour_results, eur_results2, label="EUR TOMOROW", linestyle="-", color="red")

plt.legend(loc="upper left")

plt.show()
# plt.figure(1).savefig("test.png")