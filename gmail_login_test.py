import smtplib

email = "supporthub.mail1@gmail.com"
password = "yjgrjjdzgvymyrak"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(email, password)

print("LOGIN SUCCESS")
print("EMAIL:", repr("supporthub.mail1@gmail.com"))