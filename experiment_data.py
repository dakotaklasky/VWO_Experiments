from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def get_exp_data(website):
    """Extract vwo data by executing Javascript via Selenium"""

    #Connect to chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Open the website and wait to load
    driver.get(website)
    time.sleep(5)  

    # Extract window._vwo_exp data by executing JavaScript
    vwo_exp_data = driver.execute_script("return window._vwo_exp;")

    driver.quit()
    return vwo_exp_data

def insert_experiments(experiments_data, cursor, website_id):
    """Insert all experiments and their related structured data at once."""
    
    if not experiments_data:
        return  # Exit if no data

    experiment_values = []
    combination_values = []
    global_code_values = []
    metric_values = []
    mutation_values = []

    for vwo_id, experiment in experiments_data.items():

        experiment_uid = f"{website_id}_{vwo_id}"

        # Check if experiment already exists
        cursor.execute("SELECT 1 FROM Experiments WHERE experiment_uid = ? ", (experiment_uid,))
        if cursor.fetchone():
            continue

        # Flatten core experiment data
        experiment_values.append((
            experiment_uid,
            website_id,
            vwo_id,
            experiment.get('name', 'Unnamed Experiment'),
            experiment.get('type', 'UNKNOWN'),
            experiment.get('status', 'UNKNOWN'),
            experiment.get('version', 1),
            experiment.get('pc_traffic', 0),
            experiment.get('segment_code', None),
            experiment.get('segment_eligble', False),
            experiment.get('multiple_domains', False),
            experiment.get('clickmap', 0),
            experiment.get('exclude_url', None),
            experiment.get('exec', False),
            experiment.get('isEventMigrated', False),
            experiment.get('manual', False),
            experiment.get('ready', False),
            experiment.get('varSegAllowed', False),
            experiment.get('ep', None),
            experiment.get('shouldHideElement', False),
            experiment.get('isTriggerValidated', False),
            json.dumps(experiment.get('pg_config', '')),  
            json.dumps(experiment.get('triggers', '')),
            experiment.get('urlRegex',None)  
        ))


        # Handle combinations (comb_n and combs)
        comb_n = experiment.get('comb_n', {})
        combs = experiment.get('combs', {})
        for key, value in comb_n.items():
            combination_values.append((experiment_uid, key, value, combs.get(key, 0)))

        # Handle global code
        global_code = experiment.get('globalCode', {})
        if isinstance(global_code, dict):  # If it's a dict, process normally
            for code_type, code in global_code.items():
                global_code_values.append((experiment_uid, code_type, code))
        elif isinstance(global_code, list):  # If it's a list, store as list items
            for i, code in enumerate(global_code):
                global_code_values.append((experiment_uid, f'list_{i}', code))

        # Handle metrics
        metrics = experiment.get('metrics', [])
        for metric in metrics:
            metric_values.append((experiment_uid, metric.get('metricId', 0), metric.get('type', 'UNKNOWN')))

        # Handle mutations
        muts = experiment.get('muts', {}).get('post', {})
        mutation_values.append((experiment_uid, 'post', muts.get('enabled', False), muts.get('refresh', False)))

    # Insert into Experiments table
    cursor.executemany('''INSERT INTO Experiments (
    experiment_uid, website_id, vwo_id, name, type, status, version, pc_traffic,
    segment_code, segment_eligble, multiple_domains, 
    clickmap, exclude_url, exec, isEventMigrated, manual, ready, varSegAllowed, ep, 
    shouldHideElement, isTriggerValidated, pg_config, triggers, urlRegex
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
    experiment_values)

    # Insert into ExperimentCombinations table
    if combination_values:
        cursor.executemany('''INSERT INTO ExperimentCombinations (experiment_uid, combination_key, combination_value, traffic)
        VALUES (?, ?, ?, ?)''', combination_values)

    # Insert into ExperimentGlobalCode table
    if global_code_values:
        cursor.executemany('''INSERT INTO ExperimentGlobalCode (experiment_uid, code_type, code)
        VALUES (?, ?, ?)''', global_code_values)

    # Insert into ExperimentMetrics table
    if metric_values:
        cursor.executemany('''INSERT INTO ExperimentMetrics (experiment_uid, metric_id, metric_type)
        VALUES (?, ?, ?)''', metric_values)

    # Insert into ExperimentMutations table
    if mutation_values:
        cursor.executemany('''INSERT INTO ExperimentMutations (experiment_uid, mutation_type, enabled, refresh)
        VALUES (?, ?, ?, ?)''', mutation_values)

    cursor.connection.commit()



    





