BEGIN;
CREATE TABLE IF NOT EXISTS live_prediction_sync(
  dataset character(100),
  pid int,
  start_time TIMESTAMP,
PRIMARY KEY(dataset));
COMMIT;

BEGIN;
CREATE TABLE IF NOT EXISTS predictions(
  dataset character(100),
  record_id INT,
  model_id INT,
  epoch INT,
  angle float8,
PRIMARY KEY(dataset, record_id, model_id, epoch));
COMMIT;

BEGIN;
CREATE TABLE IF NOT EXISTS epochs(
  model_id INT,
  epoch INT,
  train float8,
  validation float8,
PRIMARY KEY(epoch));
COMMIT;

BEGIN;
CREATE TABLE IF NOT EXISTS deploy(
  model_id INT,
  epoch INT,
  timestamp TIMESTAMP
);
COMMIT;

BEGIN;
CREATE TABLE IF NOT EXISTS records(
    dataset character(100),
    record_id INT,
    label_path character(300),
    image_path character(300),
    angle float8,
    throttle float8,
    is_flagged BOOLEAN DEFAULT FALSE,
PRIMARY KEY(dataset, record_id));
COMMIT;

BEGIN;
CREATE TABLE IF NOT EXISTS toggles(
    event_ts TIMESTAMP,
    web_page VARCHAR(100),
    name VARCHAR(100),
    detail VARCHAR(100),
    is_on BOOLEAN,
PRIMARY KEY(event_ts, web_page, name, detail));
COMMIT;
