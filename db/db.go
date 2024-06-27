package db

import (
	"database/sql"
	"log"
	"os"

	"github.com/go-sql-driver/mysql"
	"github.com/joho/godotenv"
)

var (
	db  *sql.DB
	err error
)

func init() {
	log.Println("Initiating connection to the database")
	err := godotenv.Load()
	if err != nil {
		log.Println(err.Error())
	}
	cfg := mysql.Config{
		User:      os.Getenv("DBUSER"),
		Passwd:    os.Getenv("DBPASS"),
		Net:       "tcp",
		Addr:      "127.0.0.1:3306",
		DBName:    "ConvoChain",
		ParseTime: true,
	}
	db, err = sql.Open("mysql", cfg.FormatDSN())
	if err != nil {
		panic(err) // Handle connection failure more gracefully in production    }
	}
}

func GetDB() (*sql.DB, error) {
	return db, err
}

func SetDB(mockDB *sql.DB, mockErr error) {
	db = mockDB
	err = mockErr
}
