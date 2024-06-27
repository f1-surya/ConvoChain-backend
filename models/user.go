package models

import (
	"time"

	"golang.org/x/crypto/bcrypt"
)

type User struct {
	Id         int64     `json:"id"`
	Name       string    `json:"name" validate:"required"`
	Username   string    `json:"username" validate:"required"`
	Email      string    `json:"email" validate:"required,email"`
	Bio        string    `json:"bio"`
	ProfilePic string    `json:"profile_pic"`
	Password   string    `json:"password" validate:"required"`
	CreatedAt  time.Time `json:"created_at"`
	UpdatedAt  time.Time `json:"updated_at"`
}

func (user *User) HashPassword() error {
	password, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	user.Password = string(password)
	return nil
}

func (user *User) VerifyPassword(password string) error {
	return bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password))
}
