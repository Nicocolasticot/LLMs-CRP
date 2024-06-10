# List of countries 

countries = ["France, Italy, Spain"]


# This function remove countries from the trip
# (used in trip_cities cause both countries and cities are labeled GPE by the NER model)
def remove_countries(countries, trip):
    no_country_trip = trip
    for word in countries:
        no_country_trip = no_country_trip.replace(word, '')

    return no_country_trip


# This function returns the list of cities in a trip
async def trip_cities(trip, countries, nlp):
    no_country_trip = remove_countries(countries, trip)

    cities = []
    doc = nlp(no_country_trip)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            cities.append(str(ent.text))

    cities = list(set(cities))
    return cities


async def trip_activities(trip, nlp):
    activities = []
    doc = nlp(trip)
    for ent in doc.ents:
        if ent.label_ == "ORG" or "FAC":
            activities.append(str(ent.text))

    activities = list(set(activities))

    return activities


# Function to find month names in a text
def trip_months(text):
    # Dictionary of months with their variations
    months_with_variations = {
        "January": ["Jan", "Jan.", "January"],
        "February": ["Feb", "Feb.", "February"],
        "March": ["Mar", "Mar.", "March"],
        "April": ["Apr", "Apr.", "April"],
        "May": ["May"],
        "June": ["Jun", "Jun.", "June"],
        "July": ["Jul", "Jul.", "July"],
        "August": ["Aug", "Aug.", "August"],
        "September": ["Sep", "Sept", "Sep.", "Sept.", "September"],
        "October": ["Oct", "Oct.", "October"],
        "November": ["Nov", "Nov.", "November"],
        "December": ["Dec", "Dec.", "December"]
    }

    months = []  # This list will hold the canonical names of the months found in the text
    words = text.split()  # Split the text into words

    # Iterate over each word in the text
    for word in words:
        # Remove punctuation from the word for a clean comparison
        clean_word = ''.join(char for char in word if char.isalnum())

        # Check each month and its variations
        for month, variations in months_with_variations.items():
            if clean_word in variations:
                months.append(month)  # Append the canonical month name to the list
                break  # Stop checking once a match is found to avoid duplicates from the same word

    return months


def trip_dates(trip, nlp):
    dates = []
    doc = nlp(trip)
    for ent in doc.ents:
        if ent.label_ == "DATE":
            dates.append(str(ent.text))

    dates = list(set(dates))

    return dates
