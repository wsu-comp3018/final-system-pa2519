import argon2

password = "MySecurePassword"

# Create a password hasher object
ph = argon2.PasswordHasher()

# Hash the password
hashed_password = ph.hash(password)

print("Hashed Password: ", hashed_password)

input_password = input("Enter Password: ")

try:
    ph.verify(hashed_password, input_password)
    print("Verified Succesfully!")
except:
    print("Password verification failed.")