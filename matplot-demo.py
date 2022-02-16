import json
from urllib.request import urlopen
import matplotlib.pyplot as plt

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

# Variables
dkk_results = []
eur_results = []
hour_results = []

print(f"\n{color.BOLD}{color.HEADER}Getting data from API: \n")
print("\n"*9)
print(color.ENDC)

url = "https://api.energidataservice.dk/datastore_search_sql?sql=SELECT%20%22HourDK%22,%20%22PriceArea%22,%20%22SpotPriceDKK%22,%20%22SpotPriceEUR%22%20FROM%20%22elspotprices%22%20WHERE%20%22PriceArea%22%20=%20%27DK2%27%20ORDER%20BY%20%22HourDK%22%20DESC%20LIMIT%2048"

response = urlopen(url)

json_data = json.loads(response.read())

data = json_data["result"]

records = data["records"]
for record in records:
    dkk_results.append(record["SpotPriceDKK"])
    eur_results.append(record["SpotPriceEUR"])
    hour_results.append(record["HourDK"].split("T")[1].split(":")[0])

dkk_results1 = dkk_results[:len(dkk_results)//2]
dkk_results2 = dkk_results[len(dkk_results)//2:]

eur_results1 = eur_results[:len(eur_results)//2]
eur_results2 = eur_results[len(eur_results)//2:]

hour_results = hour_results[:len(hour_results)//2]

dkk_results1 = dkk_results1[::-1]
eur_results1 = eur_results1[::-1]

dkk_results2 = dkk_results2[::-1]
eur_results2 = eur_results2[::-1]

hour_results = hour_results[::-1]


print(f"\n{color.BOLD}{color.HEADER}Generating curves: \n")
print("\n"*9)
print(color.ENDC)


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