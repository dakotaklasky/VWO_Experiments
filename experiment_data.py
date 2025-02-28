from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import sqlite3

def get_exp_data(website):
    # Set up options for headless browser 
    chrome_options = Options()
    chrome_options.add_argument("--headless") 

    # Set the path to the ChromeDriver
    service = Service('/Users/dakotaklasky/Desktop/chromedriver-mac-x64/chromedriver')  # Specify the correct path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the website
    driver.get(website)

    # Wait for the page to load completely (
    time.sleep(5)  

    # Extract window._vwo_exp data by executing JavaScript
    vwo_exp_data = driver.execute_script("return window._vwo_exp;")

    # Close the browser session
    driver.quit()

    # Return the extracted experiment data
    return vwo_exp_data

def insert_experiments(experiments_data, cursor, website_id):
    #need to call this for each website but this inserts for all the experiments for a particular website
    experiment_values = []
    
    for experiment_id, experiment in experiments_data.items():
        # Flatten the experiment data and provide defaults if necessary
        name = experiment.get('name', 'Unnamed Experiment')
        type_ = experiment.get('type', 'UNKNOWN')
        status = experiment.get('status', 'UNKNOWN')
        version = experiment.get('version', 1)
        pc_traffic = experiment.get('pc_traffic', 0)
        comb_n = json.dumps(experiment.get('comb_n', {}))  # Convert nested dict to JSON string
        combs = json.dumps(experiment.get('combs', {}))    # Convert nested dict to JSON string
        goal_id = experiment.get('goal_id', None)
        goal_type = experiment.get('goal_type', None)
        pUrl = experiment.get('pUrl', None)
        excludeUrl = experiment.get('excludeUrl', None)
        pExcludeUrl = experiment.get('pExcludeUrl', None)
        js = json.dumps(experiment.get('js', {}))         # Convert nested dict to JSON string
        globalCode = json.dumps(experiment.get('globalCode', {}))  # Convert nested dict to JSON string
        section_path = experiment.get('section_path', None)
        variation_names = json.dumps(experiment.get('variation_names', {}))  # Convert nested dict to JSON string
        segment_code = experiment.get('segment_code', None)
        segment_eligble = experiment.get('segment_eligble', False)
        multiple_domains = experiment.get('multiple_domains', False)
        clickmap = experiment.get('clickmap', 0)
        exclude_url = experiment.get('exclude_url', None)
        exec_flag = experiment.get('exec', False)
        isEventMigrated = experiment.get('isEventMigrated', False)
        isSpaRevertFeatureEnabled = experiment.get('isSpaRevertFeatureEnabled', False)
        manual = experiment.get('manual', False)
        post_mutations_enabled = experiment.get('post_mutations_enabled', False)
        pre_mutations = json.dumps(experiment.get('pre_mutations', {}))  # Convert nested dict to JSON string
        ready = experiment.get('ready', False)
        varSegAllowed = experiment.get('varSegAllowed', False)
        metrics = json.dumps(experiment.get('metrics', {}))  # Convert nested list to JSON string
        ep = experiment.get('ep', None)
        ss = json.dumps(experiment.get('ss', {}))  # Convert nested dict to JSON string
        shouldHideElement = experiment.get('shouldHideElement', False)
        isTriggerValidated = experiment.get('isTriggerValidated', False)
        custom_goal_flags = json.dumps(experiment.get('custom_goal_flags', {}))  # Convert nested dict to JSON string
        segmentObj = json.dumps(experiment.get('segmentObj', {}))  # Convert nested dict to JSON string
        segment = json.dumps(experiment.get('segment', {}))  # Convert nested dict to JSON string
        
        # Append the data tuple for this experiment
        experiment_values.append((
            website_id, experiment_id, name, type_, status, version, pc_traffic, comb_n, combs, 
            goal_id, goal_type, pUrl, excludeUrl, pExcludeUrl, js, globalCode, section_path, 
            variation_names, segment_code, segment_eligble, multiple_domains, clickmap, exclude_url, 
            exec_flag, isEventMigrated, isSpaRevertFeatureEnabled, manual, post_mutations_enabled, 
            pre_mutations, ready, varSegAllowed, metrics, ep, ss, shouldHideElement, 
            isTriggerValidated, custom_goal_flags, segmentObj, segment
        ))
    
    # Insert all experiments at once into the database
    cursor.executemany('''INSERT INTO Experiments (
        website_id, experiment_id, name, type, status, version, pc_traffic, comb_n, combs, 
        goal_id, goal_type, pUrl, excludeUrl, pExcludeUrl, js, globalCode, section_path, 
        variation_names, segment_code, segment_eligble, multiple_domains, clickmap, exclude_url, 
        exec, isEventMigrated, isSpaRevertFeatureEnabled, manual, post_mutations_enabled, 
        pre_mutations, ready, varSegAllowed, metrics, ep, ss, shouldHideElement, 
        isTriggerValidated, custom_goal_flags, segmentObj, segment
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
    experiment_values)
    
    # Commit the changes after insertion
    cursor.connection.commit()



    





