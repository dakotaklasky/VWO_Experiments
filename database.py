import sqlite3

def create_db():
    # Connect to the database (or create it)
    conn = sqlite3.connect('experiments.db')
    cursor = conn.cursor()

    # Create a table

    cursor.execute('''CREATE TABLE IF NOT EXISTS Websites (
            website_id INTEGER PRIMARY KEY,
            website TEXT
        )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER,
            experiment_id INTEGER,          -- Experiment ID
            name TEXT,                                  -- Experiment Name
            type TEXT,                                  -- Experiment Type
            status TEXT,                                -- Experiment Status
            version INTEGER,                            -- Experiment Version
            pc_traffic INTEGER,                        -- Traffic Percentage
            comb_n TEXT,                                -- Combination Names (Control, Variation)
            combs TEXT,                                 -- Traffic Distribution (Combinations)
            globalCode TEXT,                            -- Global Code (for the experiment)
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
            metrics TEXT,                               -- Metrics for Tracking
            ep INTEGER,                                 -- Epoch Time (Experiment Start Time)
            ss TEXT,                                    -- Session Tracking (Optional)
            shouldHideElement BOOLEAN,                  -- Flag to Hide Element (True/False)
            isTriggerValidated BOOLEAN,                 -- Trigger Validation Flag (True/False)
            pg_config TEXT,                             -- List of Experiment Configurations (complex)
            triggers TEXT,                              -- List of Triggers (complex structure)
            mt TEXT,                                    -- mt Data (complex structure)
            muts TEXT,                                  -- Post-mutation Data (complex structure)
            sections TEXT,                              -- Sections (complex structure)
            FOREIGN KEY(website_id) REFERENCES Websites(website_id)
        )''')
    


    # Close the connection
    conn.commit()
    conn.close()