# MongoDB Collection Design
## Database: energy_consumption
## Collection: energy_readings

This collection stores hourly energy consumption readings.
Each document represents one hourly reading with all its
time components embedded directly in the document.
This is more efficient for time series queries than joins.

---

## Sample Documents

### Document 1
```json
{
  "_id": "ObjectId('...')",
  "datetime": "2004-10-01T01:00:00Z",
  "consumption_mw": 12379.0,
  "region": "AEP",
  "time_components": {
    "hour": 1,
    "day": 1,
    "month": 10,
    "year": 2004,
    "day_of_week": 4,
    "season": "Autumn",
    "is_weekend": false
  }
}
```

### Document 2
```json
{
  "_id": "ObjectId('...')",
  "datetime": "2004-10-01T02:00:00Z",
  "consumption_mw": 11935.0,
  "region": "AEP",
  "time_components": {
    "hour": 2,
    "day": 1,
    "month": 10,
    "year": 2004,
    "day_of_week": 4,
    "season": "Autumn",
    "is_weekend": false
  }
}
```

### Document 3
```json
{
  "_id": "ObjectId('...')",
  "datetime": "2007-01-15T19:00:00Z",
  "consumption_mw": 21500.0,
  "region": "AEP",
  "time_components": {
    "hour": 19,
    "day": 15,
    "month": 1,
    "year": 2007,
    "day_of_week": 0,
    "season": "Winter",
    "is_weekend": false
  }
}
```

---

## Queries

### Query 1: Get the latest energy reading
```javascript
db.energy_readings.find().sort({ datetime: -1 }).limit(1)
```

### Query 2: Get all readings within a date range
```javascript
db.energy_readings.find({
  datetime: {
    $gte: ISODate("2010-01-01T00:00:00Z"),
    $lte: ISODate("2010-01-31T23:00:00Z")
  }
})
```

### Query 3: Average consumption per season
```javascript
db.energy_readings.aggregate([
  {
    $group: {
      _id: "$time_components.season",
      avg_consumption: { $avg: "$consumption_mw" }
    }
  },
  { $sort: { avg_consumption: -1 } }
])
```
