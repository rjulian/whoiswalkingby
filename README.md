# WhoIsWalkingBy
A flask site to display airodump data from a Raspberry Pi in a dashboard.

## Requirements
* A sqlite database with airodump information (see: [airodump2sqlite](https://github.com/rjulian/airodump2sqlite/)).
* Environment variable `AIRODUMP_DB_FILE` pointing to the above database. 
* Environment variable `AIRODUMP_TABLE_NAME` pointing to the relevant table in the above database.

## Usage
`flask run`
