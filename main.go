package main

import (
	"github.com/f1-surya/ConvoChain-backend/handlers"
	"github.com/gin-gonic/gin"
)

func main() {
	app := gin.Default()
	app.POST("/signup", handlers.Signup)
	app.POST("/login", handlers.Login)

	app.Run()
}
