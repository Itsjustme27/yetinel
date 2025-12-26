use serde::{Deserialize, Serialize};
use mongodb::bson::DateTime;
use std::str::FromStr;
use chrono::{DateTime as ChronoDT, Utc};


#[derive(Debug, Serialize, Deserialize)]
pub struct LogEvent {
    pub timestamp: DateTime, 
    pub source: String,
    pub level: String,
    pub event: String,
    pub message: String,
    pub source_ip: String,
}

#[derive(Debug, Deserialize)]
pub struct LogEventInput {
    pub timestamp: String,
    pub source: String,
    pub level: String,
    pub event: String,
    pub message: String,
    pub source_ip: String,
}
