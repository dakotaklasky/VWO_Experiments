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
            goal_id INTEGER,                            -- Goal ID
            goal_type TEXT,                             -- Goal Type (REVENUE_TRACKING, CUSTOM_GOAL)
            pUrl TEXT,                                  -- Goal URL Pattern
            excludeUrl TEXT,                            -- Excluded Goal URL Pattern
            pExcludeUrl TEXT,                           -- Pre-excluded Goal URL Pattern
            js TEXT,                                    -- JavaScript Code for Variations/Redirection
            globalCode TEXT,                            -- Global Code (for the experiment)
            section_path TEXT,                          -- Section Path for Experiment
            variation_names TEXT,                      -- Variation Names in Sections
            segment_code TEXT,                          -- Segment Code Expression
            segment_eligble BOOLEAN,                    -- Segment Eligibility Flag (True/False)
            multiple_domains BOOLEAN,                   -- Multiple Domains Flag (True/False)
            clickmap INTEGER,                           -- Clickmap Tracking (Enabled/Disabled)
            exclude_url TEXT,                           -- URL to Exclude from Experiment
            exec BOOLEAN,                               -- Execution Flag (True/False)
            isEventMigrated BOOLEAN,                    -- Event Migration Flag (True/False)
            isSpaRevertFeatureEnabled BOOLEAN,          -- SPA Revert Feature Flag (True/False)
            manual BOOLEAN,                             -- Manual Trigger Flag (True/False)
            post_mutations_enabled BOOLEAN,             -- Post Mutations Enabled Flag (True/False)
            pre_mutations TEXT,                         -- Pre Mutations Data
            ready BOOLEAN,                              -- Experiment Ready Flag (True/False)
            varSegAllowed BOOLEAN,                      -- Variable Segmentation Allowed (True/False)
            metrics TEXT,                               -- Metrics for Tracking
            ep INTEGER,                                 -- Epoch Time (Experiment Start Time)
            ss TEXT,                                    -- Session Tracking (Optional)
            shouldHideElement BOOLEAN,                  -- Flag to Hide Element (True/False)
            isTriggerValidated BOOLEAN,                 -- Trigger Validation Flag (True/False)
            custom_goal_flags TEXT,                     -- Custom Goal Flags (e.g., mca, revenueProp)
            segmentObj TEXT,                            -- Segment Object (Optional)
            segment TEXT,                                 -- Segment Data (Optional)
            FOREIGN KEY(website_id) REFERENCES Websites(website_id)
        )''')
    


    # Close the connection
    conn.commit()
    conn.close()