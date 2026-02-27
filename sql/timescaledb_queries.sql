-- ============================================================
-- TimescaleDB Setup for Wind Turbine Streaming Project
-- ============================================================
-- This script:
-- 1. Enables TimescaleDB extension
-- 2. Creates wind turbine time-series table
-- 3. Converts table to hypertable
-- 4. Creates continuous aggregate (5-min averages)
-- 5. Adds compression + retention policies
-- ============================================================
CREATE EXTENSION IF NOT EXISTS timescaledb; --This command enables the TimescaleDB extension in your PostgreSQL database if it’s not already enabled.
-- It adds time-series capabilities (like hypertables, continuous aggregates, compression).
-- PostgreSQL alone doesn't handle time-series data efficiently at large scale.

-- 1. Drop the table if it already exists, along with any dependent objects (like views or constraints)
-- This ensures a clean setup, especially useful during development or re-deployment.
DROP TABLE IF EXISTS wind_turbine_streamdata CASCADE;

-- 2. Create the main data table for wind turbine sensor readings.
-- Each column stores a specific type of sensor data.
-- 'timestamp' is the time when the data was recorded and is essential for time-series analysis.
CREATE TABLE wind_turbine_streamdata (
    id SERIAL,  -- Auto-incrementing ID for internal reference (not required for TimescaleDB but good for tracking)
    turbine_id TEXT NOT NULL,  -- Unique identifier for each turbine (e.g., Turbine_1)
    nacelle_position DOUBLE PRECISION,  -- Position of the nacelle (the rotating top part of the turbine)
    wind_direction DOUBLE PRECISION,  -- Direction of the wind in degrees
    ambient_air_temp DOUBLE PRECISION,  -- Temperature outside around the turbine
    bearing_temp DOUBLE PRECISION,  -- Temperature of the turbine's bearings (used to detect wear/overheating)
    blade_pitch_angle DOUBLE PRECISION,  -- Angle of the turbine blades to control rotation
    gearbox_sump_temp DOUBLE PRECISION,  -- Temperature of the gearbox sump (critical for maintenance)
    generator_speed DOUBLE PRECISION,  -- Speed at which the generator is spinning
    hub_speed DOUBLE PRECISION,  -- Speed of the hub (core connecting the blades)
    power DOUBLE PRECISION,  -- Power output from the turbine (in watts or kilowatts)
    wind_speed DOUBLE PRECISION,  -- Wind speed at turbine location
    gear_temp DOUBLE PRECISION,  -- Gearbox temperature (another critical component)
    generator_temp DOUBLE PRECISION,  -- Generator temperature
    timestamp TIMESTAMPTZ NOT NULL  -- Time of measurement, required for hypertable partitioning
);

-- 3. Convert the table into a TimescaleDB hypertable.
-- Hypertables allow time-based partitioning of large datasets automatically in the background.
--It looks and behaves like a normal PostgreSQL table, but under the hood, it is automatically partitioned by time (and optionally by space, like device ID).
--A Hypertable = A logical table that is internally split into many smaller chunks based on time intervals
-- The 'timestamp' column is used for time-based chunking.
SELECT create_hypertable('wind_turbine_streamdata', 'timestamp');

-- 4. Create a Continuous Aggregate Materialized View.
--A Materialized View is a database object that stores the results of a query physically on disk — like a precomputed table.
--Think of it as:
--A snapshot of a SELECT query stored as a real table.
--Unlike regular views, which are virtual (they run the query every time you access them), materialized views:
--Run the query once
--Store the results
--And allow fast reads from the stored data
-- This view computes 5-minute average values for selected metrics per turbine.
-- It uses time_bucket to group data into 5-minute intervals (also known as time-bucketing).
-- WITH (timescaledb.continuous) ensures automatic background refresh as new data arrives.
CREATE MATERIALIZED VIEW wind_turbine_5min_avg
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('5 minutes', timestamp) AS bucket,  -- Group readings into 5-minute windows
    turbine_id,
    AVG(power) AS avg_power,  -- Average power output in the bucket
    AVG(wind_speed) AS avg_wind_speed,  -- Average wind speed
    AVG(generator_speed) AS avg_generator_speed  -- Average generator speed
FROM wind_turbine_streamdata
GROUP BY bucket, turbine_id
WITH NO DATA;  -- Prevents initial refresh (use manual refresh next)

-- 5. Manually refresh the Continuous Aggregate to populate it with existing data.
-- Without this, the view remains empty until the background jobs run.
CALL refresh_continuous_aggregate('wind_turbine_5min_avg', NULL, NULL);

-- 6. Enable compression for the hypertable.
-- Compression saves storage space by compressing old chunks.
-- 'compress_segmentby = turbine_id' ensures data is grouped per turbine when compressing.
ALTER TABLE wind_turbine_streamdata
SET (timescaledb.compress, timescaledb.compress_segmentby = 'turbine_id');

-- 7. Define a policy to automatically compress data older than 30 days.
-- Helps save disk space without affecting recent real-time queries.
SELECT add_compression_policy('wind_turbine_streamdata', INTERVAL '30 days');

-- 8. (Optional) Add a retention policy to delete data older than 1 year.
-- Useful for long-term cleanup in systems that don't need historical data forever.
SELECT add_retention_policy('wind_turbine_streamdata', INTERVAL '365 days');
