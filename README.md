# time-series-energy-analysis

A complete time series data analysis and forecasting project using the AEP Hourly Energy Consumption dataset from PJM Interconnection LLC. This project covers exploratory data analysis, database design, REST API development, and machine learning prediction.
Dataset

Source: AEP Hourly Energy Consumption (PJM Interconnection LLC)
Time Range: October 2004 to August 2018
Frequency: Hourly
Target Variable: AEP_MW (energy consumption in megawatts)
No download needed. The dataset is loaded directly from a public URL in the notebook.

Team Members and Contributions
MemberTaskMember 1Task 1: EDA, analytical questions, model trainingMember 2Task 2: SQL schema, MongoDB design, ERDMember 3Task 3: Flask REST API with CRUD endpointsMember 4Task 4: Prediction and forecast script
Task 1: EDA and Modeling
Open task1_eda/task1_eda.ipynb in Google Colab. The notebook runs without downloading any files. Covers time range analysis, missing value handling, statistical distribution, 5 analytical questions including lag features and moving averages, and Random Forest model training with 2 experiments.
Experimentn_estimatorsmax_depthMAE (MW)RMSE (MW)R2 ScoreExperiment 1 Baseline5010219.10291.760.9858Experiment 2 Tuned20020146.82201.240.9932
Task 2: Database Design
MySQL Setup
Run the following to set up the database: sudo mysql -u root < task2_databases/schema.sql
Three tables are created: regions, time_dimension, and energy_readings. See task2_databases/schema.sql for the full schema and task2_databases/erd.md for the ERD.
MongoDB
Hosted on MongoDB Atlas free tier. See task2_databases/mongo_design.md for collection structure and sample documents.
Task 3: REST API
Setup
cd task3_api && python3 -m venv venv && source venv/bin/activate && pip install flask pymongo mysql-connector-python python-dotenv
Create a .env file inside task3_api/ with these values:
MONGO_URI=your_mongodb_atlas_connection_string
MONGO_DB=energy_consumption
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=energy_consumption
Run
python app.py — runs on http://127.0.0.1:5000
Endpoints
MethodEndpointDescriptionGET/mysql/readingsGet all MySQL readingsGET/mysql/readings/latestGet latest MySQL readingGET/mysql/readings/range?start=...&end=...Get MySQL readings by date rangePOST/mysql/readingsCreate a new MySQL readingPUT/mysql/readings/idUpdate a MySQL readingDELETE/mysql/readings/idDelete a MySQL readingGET/mongo/readingsGet all MongoDB readingsGET/mongo/readings/latestGet latest MongoDB readingGET/mongo/readings/range?start=...&end=...Get MongoDB readings by date rangePOST/mongo/readingsCreate a new MongoDB readingPUT/mongo/readings/datetimeUpdate a MongoDB readingDELETE/mongo/readings/datetimeDelete a MongoDB reading
Task 4: Prediction Script
Setup
cd task4_prediction && python3 -m venv venv && source venv/bin/activate && pip install requests pandas numpy scikit-learn
Run
Make sure the API is running first, then run: python predict.py
The script fetches data from the API, preprocesses it, trains the Random Forest model using the best hyperparameters from Task 1, and makes a prediction.
Example Output
Input datetime: 2018-08-03 00:00:00 — Actual: 14,809.00 MW — Predicted: 14,706.18 MW — Accuracy: 99.31%
Requirements

Python 3.12
MySQL 8.0
MongoDB Atlas free tier account
All libraries installed per task using pip inside a virtual environment


