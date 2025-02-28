import database
import experiment_data
import sqlite3

database.create_db()

def add_websites(websites, cursor):
    # Prepare data for bulk insertion
    website_values = [(website,) for website in websites]  # Convert list of websites into a list of tuples
    
    # Insert multiple websites at once
    cursor.executemany('''INSERT INTO Websites (website) VALUES (?)''', website_values)


def get_website_id(website_url, cursor):
    cursor.execute('''SELECT website_id FROM Websites WHERE website = ?''', (website_url,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        return None 

# websites = ["https://www.anker.com/", "https://www.tonal.com/","https://www.rugsusa.com/","https://www.humnutrition.com/",
#             "https://www.bragg.com/","https://flyingtiger.com/","https://vessi.com/","https://wineracksamerica.com/","https://onecountry.com/"]

websites = ["https://www.tonal.com/","https://www.humnutrition.com/","https://flyingtiger.com/","https://vessi.com/","https://wineracksamerica.com/","https://onecountry.com/"]


conn = sqlite3.connect('experiments.db')
cursor = conn.cursor()

add_websites(websites,cursor)

for site in websites:
    exp_data = experiment_data.get_exp_data(site)
    experiment_data.insert_experiments(exp_data,cursor,get_website_id(site, cursor))

conn.commit()
conn.close()