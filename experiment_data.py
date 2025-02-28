from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import database

database.create_db()

# Set up options for headless browser (optional, removes the browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (optional)
chrome_options.add_argument("--disable-gpu")  # Disable GPU (optional)

# Set the path to the ChromeDriver (replace with your path if needed)
service = Service('/Users/dakotaklasky/Desktop/chromedriver-mac-x64/chromedriver')  # Specify the correct path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# https://www.anker.com/
# https://www.tonal.com/
# https://www.rugsusa.com/
# https://www.humnutrition.com/
# https://www.bragg.com/
# https://flyingtiger.com/
# https://vessi.com/
# https://wineracksamerica.com/
# https://onecountry.com/

# Open the humnutrition website
driver.get('https://onecountry.com/')

# Wait for the page to load completely (adjust timing based on internet speed)
time.sleep(5)  # Wait for 5 seconds (could be more depending on page load time)

# Extract window._vwo_exp data by executing JavaScript
vwo_exp_data = driver.execute_script("return window._vwo_exp;")

# Print the extracted experiment data
# print(vwo_exp_data)
print(vwo_exp_data['144']['name']) #get name of experiment

# Close the browser session
driver.quit()







