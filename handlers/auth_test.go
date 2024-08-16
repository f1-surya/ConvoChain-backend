package handlers

import (
	"bytes"
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/DATA-DOG/go-sqlmock"
	"github.com/f1-surya/ConvoChain-backend/db"
	"github.com/f1-surya/ConvoChain-backend/models"
	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func TestSignup(t *testing.T) {
	// Set Gin to test mode
	gin.SetMode(gin.TestMode)

	// Create a new Gin router
	router := gin.Default()

	// Define the endpoint we want to test
	router.POST("/signup", Signup)

	// Create mock database
	mockDB, mock, err := sqlmock.New()
	assert.NoError(t, err)
	defer mockDB.Close()

	// Replace the GetDB function with a function that returns the mock DB
	db.SetDB(mockDB, nil)

	// Define test cases
	tests := []struct {
		name             string
		requestBody      models.User
		mockSetup        func()
		expectedStatus   int
		expectedResponse string
	}{
		{
			name: "Successful Signup",
			requestBody: models.User{
				Name:       "John Doe",
				Email:      "john@example.com",
				Bio:        "A short bio",
				Username:   "johndoe",
				ProfilePic: "path/to/profile/pic",
				Password:   "password123",
			},
			mockSetup: func() {
				mock.ExpectExec("INSERT INTO users").
					WithArgs("John Doe", "john@example.com", "A short bio", "johndoe", "path/to/profile/pic", sqlmock.AnyArg()).
					WillReturnResult(sqlmock.NewResult(1, 1))
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "JSON Binding Failure",
			requestBody: models.User{
				Name:       "John Doe",
				Email:      "invalid-email",
				Bio:        "A short bio",
				Username:   "johndoe",
				ProfilePic: "path/to/profile/pic",
				Password:   "password123",
			},
			mockSetup:      func() {},
			expectedStatus: http.StatusBadRequest,
		},
		{
			name: "Database Insertion Failure",
			requestBody: models.User{
				Name:       "John Doe",
				Email:      "john@example.com",
				Bio:        "A short bio",
				Username:   "johndoe",
				ProfilePic: "path/to/profile/pic",
				Password:   "password123",
			},
			mockSetup: func() {
				mock.ExpectExec("INSERT INTO users").
					WithArgs("John Doe", "john@example.com", "A short bio", "johndoe", "path/to/profile/pic", sqlmock.AnyArg()).
					WillReturnError(errors.New("insertion error"))
			},
			expectedStatus: http.StatusInternalServerError,
		},
		{
			name: "Database Connection Failure",
			requestBody: models.User{
				Name:       "John Doe",
				Email:      "john@example.com",
				Bio:        "A short bio",
				Username:   "johndoe",
				ProfilePic: "path/to/profile/pic",
				Password:   "password123",
			},
			mockSetup: func() {
				db.SetDB(nil, errors.New("database connection error"))
			},
			expectedStatus: http.StatusInternalServerError,
		},
	}

	// Execute test cases
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Set up mock behavior
			tt.mockSetup()

			// Create request body
			body, err := json.Marshal(tt.requestBody)
			assert.NoError(t, err)

			// Create a new HTTP request
			req, err := http.NewRequest(http.MethodPost, "/signup", bytes.NewBuffer(body))
			assert.NoError(t, err)

			// Create a response recorder
			w := httptest.NewRecorder()

			// Perform the request
			router.ServeHTTP(w, req)

			// Assert the status code
			assert.Equal(t, tt.expectedStatus, w.Code)
		})
	}
}

func TestLogin(t *testing.T) {
	// Set Gin to test mode
	gin.SetMode(gin.TestMode)

	// Create a new Gin router
	router := gin.Default()
	router.POST("/login", Login)

	// Create mock database
	mockDB, mock, err := sqlmock.New()
	assert.NoError(t, err)
	defer mockDB.Close()

	// Replace the GetDB function with a function that returns the mock DB
	db.SetDB(mockDB, nil)

	// Write tests to check valid and invalid credentials

	// Define test cases
	tests := []struct {
		name           string
		requestBody    models.User
		mockSetup      func()
		expectedStatus int
	}{
		{
			name: "Successful Login",
			requestBody: models.User{
				Email:    "john@example.com",
				Password: "password",
			},
			mockSetup: func() {
				mock.ExpectQuery("SELECT * FROM users WHERE email = ?").
					WithArgs("john@example.com").
					WillReturnRows(sqlmock.NewRows([]string{"id", "name", "email", "bio", "username", "profile_pic", "password"}).
						AddRow(1, "John Doe", "john@example.com", "A short bio", "johndoe", "path/to/profile/pic", "$2a$10$iJBYriKv0N5B5sUhiPs4nOeT4UtZ7nYTi9gQfg.VnF/wKJjnl52Ya"))
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Invalid Email",
			requestBody: models.User{
				Email:    "invalid-email",
				Password: "password123",
			},
			mockSetup: func() {
				mock.ExpectQuery("SELECT * FROM users WHERE email = ?").
					WithArgs("invalid-email").
					WillReturnError(errors.New("invalid email"))
			},
			expectedStatus: http.StatusBadRequest,
		},
		{
			name: "Invalid Password",
			requestBody: models.User{
				Email:    "john@example.com",
				Password: "invalid-password",
			},
			mockSetup: func() {
				mock.ExpectQuery("SELECT * FROM users WHERE email = ?").
					WithArgs("john@example.com").
					WillReturnRows(sqlmock.NewRows([]string{"id", "name", "email", "bio", "username", "profile_pic", "password"}).
						AddRow(1, "John Doe", "john@example.com", "A short bio", "johndoe", "path/to/profile/pic", "$2a$10$iJBYriKv0N5B5sUhiPs4nOeT4UtZ7nYTi9gQfg.VnF/wKJjnl52Ya"))
			},
			expectedStatus: http.StatusUnauthorized,
		},
	}

	// Execute test cases
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Set up mock behavior
			tt.mockSetup()

			// Create request body
			body, err := json.Marshal(tt.requestBody)
			assert.NoError(t, err)

			// Create a new HTTP request
			req, err := http.NewRequest(http.MethodPost, "/login", bytes.NewBuffer(body))
			assert.NoError(t, err)

			// Create a response recorder
			w := httptest.NewRecorder()

			// Perform the request
			router.ServeHTTP(w, req)

			// Assert the status code
			assert.Equal(t, tt.expectedStatus, w.Code)
		})
	}
}
