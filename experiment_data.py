from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def get_exp_data(website):

    #Connect to chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Open the website
    driver.get(website)

    # Wait for the page to load completely
    time.sleep(5)  

    # Extract window._vwo_exp data by executing JavaScript
    vwo_exp_data = driver.execute_script("return window._vwo_exp;")

    # Close the browser session
    driver.quit()

    # Return the extracted experiment data
    return vwo_exp_data

def insert_experiments(experiments_data, cursor, website_id):
    #need to call for each website
    # inserts for all the experiments for a particular website
    if experiments_data is not None:
        experiment_values = []
        
        for experiment_id, experiment in experiments_data.items():

            cursor.execute("SELECT 1 FROM Experiments WHERE website_id = ? AND experiment_id = ?", 
                           (website_id, experiment_id))
            if cursor.fetchone():  # If a record exists, skip inserting
                continue

            # Flatten the experiment data and provide defaults if necessary
            name = experiment.get('name', 'Unnamed Experiment')
            type_ = experiment.get('type', 'UNKNOWN')
            status = experiment.get('status', 'UNKNOWN')
            version = experiment.get('version', 1)
            pc_traffic = experiment.get('pc_traffic', 0)
            comb_n = json.dumps(experiment.get('comb_n', {}))  # Convert nested dict to JSON string
            combs = json.dumps(experiment.get('combs', {}))    # Convert nested dict to JSON string
            globalCode = json.dumps(experiment.get('globalCode', {}))  # Convert nested dict to JSON string
            segment_code = experiment.get('segment_code', None)
            segment_eligble = experiment.get('segment_eligble', False)
            multiple_domains = experiment.get('multiple_domains', False)
            clickmap = experiment.get('clickmap', 0)
            exclude_url = experiment.get('exclude_url', None)
            exec_flag = experiment.get('exec', False)
            isEventMigrated = experiment.get('isEventMigrated', False)
            manual = experiment.get('manual', False)
            ready = experiment.get('ready', False)
            varSegAllowed = experiment.get('varSegAllowed', False)
            metrics = json.dumps(experiment.get('metrics', {}))  # Convert nested list to JSON string
            ep = experiment.get('ep', None)
            ss = json.dumps(experiment.get('ss', {}))  # Convert nested dict to JSON string
            shouldHideElement = experiment.get('shouldHideElement', False)
            isTriggerValidated = experiment.get('isTriggerValidated', False)
            metrics = json.dumps(experiment.get('metrics', ''))
            pg_config = json.dumps(experiment.get('pg_config', ''))
            triggers = json.dumps(experiment.get('triggers', ''))
            mt = json.dumps(experiment.get('mt', ''))
            muts = json.dumps(experiment.get('muts', ''))
            sections = json.dumps(experiment.get('sections', ''))
            
            # Append the data tuple for this experiment
            experiment_values.append((
                website_id, experiment_id, name, type_, status, version, pc_traffic, comb_n, combs, 
                globalCode, segment_code, segment_eligble, multiple_domains, 
                clickmap, exclude_url, exec_flag, isEventMigrated,  manual,ready, varSegAllowed, metrics,
                ep, ss, shouldHideElement, isTriggerValidated, metrics, pg_config, triggers, 
                mt, muts, sections
            ))
    
        # Insert all experiments at once into the database
        cursor.executemany('''INSERT INTO Experiments (
            website_id, experiment_id, name, type, status, version, pc_traffic, comb_n, combs, 
            globalCode, segment_code, segment_eligble, multiple_domains, 
            clickmap, exclude_url, exec, isEventMigrated, manual, ready, varSegAllowed, metrics, ep, ss, 
            shouldHideElement, isTriggerValidated, metrics, pg_config, triggers, mt, muts, sections
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?)''', 
        experiment_values)
        
        # Commit the changes after insertion
        cursor.connection.commit()



    





