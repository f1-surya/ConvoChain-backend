package handlers

import (
	"log"
	"net/http"
	"os"

	"github.com/f1-surya/ConvoChain-backend/db"
	"github.com/f1-surya/ConvoChain-backend/models"
	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"github.com/golang-jwt/jwt/v5"
	"github.com/joho/godotenv"
)

func Signup(c *gin.Context) {
	database, e := db.GetDB()
	if e != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"message": e.Error()})
		log.Print(e.Error())
		return
	}
	var newUser models.User

	if err := c.BindJSON(&newUser); err != nil {
		c.JSON(500, gin.H{"message": err.Error()})
		log.Println(err)
		return
	}

	validate := validator.New()

	if e = validate.Struct(newUser); e != nil {
		c.JSON(400, gin.H{"message": e.Error()})
		log.Println(e)
		return
	}

	newUser.HashPassword()

	_, err := database.Exec("INSERT INTO users (name, email, bio, username, profile_pic, password) VALUES (?, ?, ?, ?, ?, ?)", newUser.Name, newUser.Email, newUser.Bio, newUser.Username, newUser.ProfilePic, newUser.Password)
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusInternalServerError, gin.H{"message": err.Error()})
		return
	}

	token, err := generateToken(newUser.Email)
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusInternalServerError, gin.H{"message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "User created successfully", "token": token})
}

type LoginCredentials struct {
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required"`
}

func Login(c *gin.Context) {
	database, e := db.GetDB()
	if e != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"message": e.Error()})
		log.Print(e.Error())
		return
	}
	var credentials LoginCredentials
	if err := c.BindJSON(&credentials); err != nil {
		c.JSON(400, gin.H{"message": err.Error()})
		return
	}
	validate := validator.New()

	if e = validate.Struct(credentials); e != nil {
		c.JSON(400, gin.H{"message": e.Error()})
		log.Println(e)
		return
	}
	var user models.User
	err := database.QueryRow("SELECT * FROM users WHERE email = ?", credentials.Email).Scan(&user.Id, &user.Name, &user.Email, &user.Bio, &user.Username, &user.ProfilePic, &user.Password, &user.CreatedAt, &user.UpdatedAt)
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusUnauthorized, gin.H{"message": "Invalid credentials"})
		return
	}
	err = user.VerifyPassword(credentials.Password)
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusUnauthorized, gin.H{"message": "Invalid credentials"})
		return
	}
	token, err := generateToken(user.Email)
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusInternalServerError, gin.H{"message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "Login successful", "token": token})
}

func generateToken(email string) (string, error) {
	godotenv.Load()
	var jwtKey = []byte(os.Getenv("JWTKEY"))

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"email": email,
	})
	return token.SignedString(jwtKey)
}
