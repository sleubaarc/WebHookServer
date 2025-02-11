import mysql.connector

# Connexion à MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin"  # Remplacez par votre mot de passe MySQL
)

cursor = conn.cursor()

# Création de la base de données
cursor.execute("CREATE DATABASE webhook;")
print("Base de données 'webhook' créée avec succès.")

# Vérification
cursor.execute("SHOW DATABASES;")
for db in cursor:
    print(db)

# Fermeture de la connexion
cursor.close()
conn.close()