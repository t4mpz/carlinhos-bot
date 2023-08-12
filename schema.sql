CREATE SCHEMA carlinhos;

CREATE TABLE IF NOT EXISTS carlinhos.user_server_map(
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    server_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS carlinhos.user_server_log(
    id SERIAL PRIMARY KEY,
    map_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    sending_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_code INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS carlinhos.account_watchlist(
    id SERIAL PRIMARY KEY,
    account_name TEXT NOT NULL,
    account_url TEXT NOT NULL,
    created_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NULL,
    options TEXT NOT NULL DEFAULT '{}'
);