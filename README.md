# Time Series Energy Consumption Analysis

A complete time series data analysis and forecasting project using the AEP Hourly Energy Consumption dataset from PJM Interconnection LLC. This project covers exploratory data analysis, database design, REST API development, and machine learning prediction.

## Dataset

| Field | Details |
|---|---|
| Source | AEP Hourly Energy Consumption, PJM Interconnection LLC |
| Time Range | October 2004 to August 2018 |
| Frequency | Hourly |
| Target Variable | AEP_MW (energy consumption in megawatts) |
| Download | Not needed, loaded directly from a public URL |

## Team Members and Contributions

| Member | Task |
|---|---|
| Member 1 | Task 1: EDA, analytical questions, model training |
| Member 2 | Task 2: SQL schema, MongoDB design, ERD |
| Member 3 | Task 3: Flask REST API with CRUD endpoints |
| Member 4 | Task 4: Prediction and forecast script |

## How to Run the Full Project

Follow these steps in order to run everything from scratch.

### Step 1: Clone the repository

```bash
git clone https://github.com/hasby-umutoniwabo/time-series-energy-analysis.git
cd time-series-energy-analysis
```

### Step 2: Run Task 1 (EDA and Modeling)

Open `task1_eda/task1_eda.ipynb` in Google Colab and run all cells from top to bottom. No file downloads needed.

### Step 3: Set up the MySQL database

Make sure MySQL is installed and running on your machine, then run:

```bash
sudo mysql -u root < task2_databases/schema.sql
```

### Step 4: Set up and run the API

```bash
cd task3_api
python3 -m venv venv
source venv/bin/activate
pip install flask pymongo mysql-connector-python python-dotenv
```

Create a `.env` file inside `task3_api/` with these values:

MONGO_URI=your_mongodb_atlas_connection_string
MONGO_DB=energy_consumption
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=energy_consumption

Then start the API:

```bash
python app.py
```

The API runs on http://127.0.0.1:5000

### Step 5: Run the prediction script

Open a new terminal and run:

```bash
cd task4_prediction
python3 -m venv venv
source venv/bin/activate
pip install requests pandas numpy scikit-learn
python predict.py
```

## Task 1: EDA and Modeling

Open `task1_eda/task1_eda.ipynb` in Google Colab. The notebook runs without downloading any files. It covers time range analysis, missing value handling, statistical distribution, 5 analytical questions including lag features and moving averages, and Random Forest model training with 2 experiments.

| Experiment | n_estimators | max_depth | MAE (MW) | RMSE (MW) | R2 Score |
|---|---|---|---|---|---|
| Experiment 1 Baseline | 50 | 10 | 219.10 | 291.76 | 0.9858 |
| Experiment 2 Tuned | 200 | 20 | 146.82 | 201.24 | 0.9932 |

## Task 2: Database Design

### MySQL

Three tables are created: `regions`, `time_dimension`, and `energy_readings`. See `task2_databases/schema.sql` for the full schema and `task2_databases/erd.md` for the ERD.

### MongoDB

Hosted on MongoDB Atlas free tier. See `task2_databases/mongo_design.md` for the collection structure and sample documents.

## Task 3: REST API

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /mysql/readings | Get all MySQL readings |
| GET | /mysql/readings/latest | Get latest MySQL reading |
| GET | /mysql/readings/range?start=...&end=... | Get MySQL readings by date range |
| POST | /mysql/readings | Create a new MySQL reading |
| PUT | /mysql/readings/id | Update a MySQL reading |
| DELETE | /mysql/readings/id | Delete a MySQL reading |
| GET | /mongo/readings | Get all MongoDB readings |
| GET | /mongo/readings/latest | Get latest MongoDB reading |
| GET | /mongo/readings/range?start=...&end=... | Get MongoDB readings by date range |
| POST | /mongo/readings | Create a new MongoDB reading |
| PUT | /mongo/readings/datetime | Update a MongoDB reading |
| DELETE | /mongo/readings/datetime | Delete a MongoDB reading |

## Task 4: Prediction Script

### Example Output

Input datetime  : 2018-08-03 00:00:00
Actual value    : 14,809.00 MW
Predicted value : 14,706.18 MW
Difference      : 102.82 MW
Accuracy        : 99.31%

## Requirements

- Python 3.12
- MySQL 8.0
- MongoDB Atlas free tier account
- All libraries installed per task using pip inside a virtual environment
