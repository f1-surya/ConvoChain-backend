package models

import (
	"strings"
	"testing"
)

func TestHashPassword(t *testing.T) {
	user := &User{Password: "mysecretpassword"}
	user.HashPassword()

	// Test if password was hashed
	if user.Password == "mysecretpassword" {
		t.Error("Password was not hashed")
	}

	// Test if hashed password contains a colon
	if !strings.Contains(user.Password, ":") {
		t.Error("Hashed password does not contain a colon separator")
	}

	// Test if hashed password has two parts (hashed password and salt)
	parts := strings.Split(user.Password, ":")
	if len(parts) != 2 {
		t.Errorf("Hashed password does not contain two parts, got %d parts", len(parts))
	}

	// Test if each part is of the correct length
	hashedPassword, salt := parts[0], parts[1]
	if len(hashedPassword) != 64 {
		t.Errorf("Hashed password part is not 64 characters long, got %d characters", len(hashedPassword))
	}

	if len(salt) != 32 {
		t.Errorf("Salt part is not 32 characters long, got %d characters", len(salt))
	}
}
