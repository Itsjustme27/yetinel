use std::io::{Read};
use std::net::TcpStream;
use std::str::FromStr;

use crate::models::{LogEvent, LogEventInput};
// use crate::handlers::handle_logs;
use crate::utils::http_response;
use mongodb::Database;
use mongodb::bson::DateTime;
use chrono::{DateTime as ChronoDT, Utc};


pub async fn handle_connection(mut stream: TcpStream, db: Database) {
    let mut buffer = [0; 4096];
    
    let bytes_read = match stream.read(&mut buffer) {
        Ok(n) if n > 0 => n,
        _ => return,  // Connection close or error
    };


    let request = String::from_utf8_lossy(&buffer[..bytes_read]);

    if request.starts_with("POST /logs") {
        let body = request
            .split("\r\n\r\n")
            .nth(1)
            .unwrap_or("")
            .trim_matches(char::from(0));

        let input: LogEventInput = match serde_json::from_str(body) {
            Ok(data) => data,
            Err(e) => {
                eprintln!("JSON Parsing Error: {}", e);
                http_response(&mut stream, "400 Bad Request", "Invalid JSON format");
                return;
            }
        };

        let bson_timestamp = match ChronoDT::<Utc>::from_str(&input.timestamp) {
            Ok(chrono_dt) => DateTime::from(chrono_dt),
            Err(_) => {
                eprintln!("Invalid date format received: {}", input.timestamp);
                DateTime::now()
            }
        };
       
        let log_to_store = LogEvent {
            timestamp: bson_timestamp,
            source: input.source,
            level: input.level,
            event: input.event,
            message: input.message,
            source_ip: input.source_ip,
        };

        println!("Parsed log with ISODate: {:?}", log_to_store);

        let collection = db.collection::<LogEvent>("logs");

        match collection.insert_one(&log_to_store, None).await {
            Ok(_) => {
                println!("Log successfully stored in MongoDB");
                http_response(&mut stream, "200 OK", "Log received and stored");
            }
            Err(e) => {
                eprintln!("Mongo insert failed: {}", e);
                http_response(&mut stream, "500 Internal Server Error", "Database insertion failed");
            } 
        }
     
    } else {
        http_response(&mut stream, "404 Not Found", "Endpoint not found");
    }

}
