import sqlite3

def create_db():
    # Connect to the database (or create it)
    conn = sqlite3.connect('experiments.db')
    cursor = conn.cursor()

    # Create a Website table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Websites (
            website_id INTEGER PRIMARY KEY,
            website TEXT
        )''')
    
    #Create Experiments table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Experiments (
            experiment_uid TEXT PRIMARY KEY,
            website_id INTEGER,
            vwo_id INTEGER,                             -- Experiment ID
            name TEXT,                                  -- Experiment Name
            type TEXT,                                  -- Experiment Type
            status TEXT,                                -- Experiment Status
            version INTEGER,                            -- Experiment Version
            pc_traffic INTEGER,                        -- Traffic Percentage
            segment_code TEXT,                          -- Segment Code Expression
            segment_eligble BOOLEAN,                    -- Segment Eligibility Flag (True/False)
            multiple_domains BOOLEAN,                   -- Multiple Domains Flag (True/False)
            clickmap INTEGER,                           -- Clickmap Tracking (Enabled/Disabled)
            exclude_url TEXT,                           -- URL to Exclude from Experiment
            exec BOOLEAN,                               -- Execution Flag (True/False)
            isEventMigrated BOOLEAN,                    -- Event Migration Flag (True/False)
            manual BOOLEAN,                             -- Manual Trigger Flag (True/False)
            ready BOOLEAN,                              -- Experiment Ready Flag (True/False)
            varSegAllowed BOOLEAN,                      -- Variable Segmentation Allowed (True/False)
            ep INTEGER,                                 -- Epoch Time (Experiment Start Time)
            shouldHideElement BOOLEAN,                  -- Flag to Hide Element (True/False)
            isTriggerValidated BOOLEAN,                 -- Trigger Validation Flag (True/False)
            pg_config TEXT,                             -- List of Experiment Configurations (complex)
            triggers TEXT,                              -- List of Triggers (complex structure)
            FOREIGN KEY(website_id) REFERENCES Websites(website_id)
        )''')
    
    #Experiment Combinations Table (Stores 'comb_n' and 'combs' Dict)
    cursor.execute('''CREATE TABLE IF NOT EXISTS ExperimentCombinations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        experiment_uid TEXT,
        combination_key TEXT,
        combination_value TEXT,
        traffic INTEGER,
        FOREIGN KEY(experiment_uid) REFERENCES Experiments(experiment_uid)
    )''')

    #Experiment Global Code Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS ExperimentGlobalCode (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        experiment_uid TEXT,
        code_type TEXT, -- 'pre' or 'post'
        code TEXT,
        FOREIGN KEY(experiment_uid) REFERENCES Experiments(experiment_uid)
    )''')

    #Experiment Metrics Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS ExperimentMetrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        experiment_uid TEXT,
        metric_id INTEGER,
        metric_type TEXT, -- 'm' for main metric, 'g' for goal metric
        FOREIGN KEY(experiment_uid) REFERENCES Experiments(experiment_uid)
    )''')

    #Experiment Mutations Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS ExperimentMutations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        experiment_uid TEXT,
        mutation_type TEXT, -- 'post' mutation settings
        enabled BOOLEAN,
        refresh BOOLEAN,
        FOREIGN KEY(experiment_uid) REFERENCES Experiments(experiment_uid)
    )''')
    
    # Close the connection
    conn.commit()
    conn.close()