# Entity Relationship Diagram (ERD)
## AEP Hourly Energy Consumption Database

## Entities and Relationships

    +------------------+       +------------------+       +---------------------+
    |     regions      |       |  energy_readings  |       |   time_dimension    |
    +------------------+       +------------------+       +---------------------+
    | PK region_id     |1    N | PK reading_id    | N    1| PK time_id          |
    |    region_name   |-------| FK region_id     |-------| datetime            |
    |    country       |       | FK time_id       |       | hour                |
    |    timezone      |       |    consumption   |       | day                 |
    |    created_at    |       +------------------+       | month               |
    +------------------+                                   | year                |
                                                           | day_of_week         |
                                                           | season              |
                                                           | is_weekend          |
                                                           +---------------------+

## Relationships
- One region can have many energy readings (1 to N)
- One time dimension entry can have many energy readings (1 to N)
- energy_readings is the central fact table linking regions and time

## Design Decisions
- time_dimension is separated from readings to avoid repeating time data in every row
- regions table allows the schema to support more energy regions beyond AEP in future
- consumption is stored as DECIMAL to preserve precision for energy values
