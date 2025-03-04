import database
import experiment_data
import sqlite3

database.create_db()

def add_websites(websites, cursor):
    """Add websites to sqlite table"""
    for website in websites:
        # Check if the website already exists in the database
        cursor.execute("SELECT 1 FROM Websites WHERE website = ?", (website,))
        if cursor.fetchone():  # If a record exists, skip inserting
            continue

        # Insert the website if it does not exist
        cursor.execute("INSERT INTO Websites (website) VALUES (?)", (website,))
    
    cursor.connection.commit()

def get_website_id(website_url, cursor):
    """Return website id from sqlite table"""

    cursor.execute('''SELECT website_id FROM Websites WHERE website = ?''', (website_url,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        return None 

websites = ["https://www.anker.com/", "https://www.tonal.com/","https://www.rugsusa.com/","https://www.humnutrition.com/",
            "https://www.bragg.com/","https://flyingtiger.com/","https://vessi.com/","https://wineracksamerica.com/","https://onecountry.com/"]

conn = sqlite3.connect('experiments.db')
cursor = conn.cursor()

#Add website to db
add_websites(websites,cursor)

#For each website extract experiment data and add to database
for site in websites:
    exp_data = experiment_data.get_exp_data(site)
    experiment_data.insert_experiments(exp_data,cursor,get_website_id(site, cursor))

conn.commit()
conn.close()