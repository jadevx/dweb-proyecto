"""Seed fix - Retry failed posts with alternative images."""
import requests
import random

BASE_URL = "https://dweb-proyecto-production.up.railway.app/api"

# Login existing users
USERS = [
    {"username_or_email": "m3ssi@test.com", "password": "HolaHola123?", "username": "M3ssi"},
    {"username_or_email": "w3stcol@test.com", "password": "HolaHola123?", "username": "W3stcol"},
    {"username_or_email": "f3id@test.com", "password": "HolaHola123?", "username": "F3id"},
    {"username_or_email": "g0ku@test.com", "password": "HolaHola123?", "username": "G0ku"},
    {"username_or_email": "s3nk@test.com", "password": "HolaHola123?", "username": "S3nk"},
]

FAILED_POSTS = [
    {"name": "Pagoda Chureito", "location": "Yamanashi, Japón", "review": "Un lugar mágico donde puedes ver el Monte Fuji de fondo con la pagoda tradicional japonesa. La subida de escaleras vale totalmente la pena por la vista espectacular.", "rating": 9, "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Chureito_Pagoda_and_Mount_Fuji.jpg/1280px-Chureito_Pagoda_and_Mount_Fuji.jpg"},
    {"name": "Pirámides de Egipto", "location": "Guiza, Egipto", "review": "Las pirámides son impresionantes en persona, mucho más grandes de lo que imaginas. Una maravilla del mundo antiguo que te deja sin palabras.", "rating": 10, "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Kheops-Pyramid.jpg/1280px-Kheops-Pyramid.jpg"},
    {"name": "Malecón del Río", "location": "Barranquilla, Colombia", "review": "Un paseo increíble junto al río Magdalena. Perfecto para caminar al atardecer con la brisa caribeña y disfrutar de la gastronomía local.", "rating": 8, "imageUrl": "https://barranquilla.gov.co/wp-content/uploads/2025/02/gran-malecon.jpg"},
    {"name": "Islas Lofoten", "location": "Nordland, Noruega", "review": "Paisajes de otro mundo con montañas que emergen del mar ártico. Las auroras boreales aquí son un espectáculo inolvidable.", "rating": 10, "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Lofoten_from_Reinebringen.jpg/1280px-Lofoten_from_Reinebringen.jpg"},
    {"name": "Monte Saint-Michel", "location": "Normandía, Francia", "review": "Una abadía medieval sobre una isla rocosa que parece flotar durante la marea alta. Pasear por sus callejuelas es viajar en el tiempo.", "rating": 9, "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Mont-Saint-Michel_Drone.jpg/1280px-Mont-Saint-Michel_Drone.jpg"},
    {"name": "Acrópolis de Atenas", "location": "Atenas, Grecia", "review": "El Partenón es majestuoso y te transporta a la antigua Grecia. La vista de la ciudad desde arriba es un bonus increíble.", "rating": 8, "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/1280px-Camponotus_flavomarginatus_ant.jpg"},
    {"name": "Cristo Redentor", "location": "Río de Janeiro, Brasil", "review": "La estatua es imponente y la vista panorámica de Río desde el Corcovado es de las mejores del mundo. Mejor ir temprano para evitar multitudes.", "rating": 8, "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Christ_the_Redeemer_-_Cristo_Redentor.jpg/800px-Christ_the_Redeemer_-_Cristo_Redentor.jpg"},
]

COMMENTS = [
    "¡Increíble lugar! Definitivamente está en mi lista de viajes pendientes.",
    "Las fotos no le hacen justicia, debe ser mucho mejor en persona.",
    "Fui el año pasado y puedo confirmar que es espectacular.",
    "Me encanta este destino, lo tengo en mi bucket list.",
    "Excelente reseña, muy completa y útil para planificar el viaje.",
    "Hermoso destino, gracias por compartir la experiencia.",
    "¡Qué envidia! Espero poder ir algún día.",
    "Un destino que no decepciona, lo recomiendo al 100%.",
]

def seed_fix():
    sessions = {}

    # Login users
    print("Iniciando sesión...")
    for user in USERS:
        r = requests.post(f"{BASE_URL}/app/login", json={"username_or_email": user["username_or_email"], "password": user["password"]})
        if r.status_code == 200:
            token = r.cookies.get("token")
            sessions[user["username"]] = {"cookie": {"token": token}}
            print(f"  ✓ {user['username']} logueado")
        else:
            print(f"  ✗ {user['username']} error: {r.text}")

    usernames = list(sessions.keys())

    # Create failed posts
    print("\nCreando posts faltantes...")
    post_owners = {}
    for i, post in enumerate(FAILED_POSTS):
        owner = usernames[i % len(usernames)]
        cookies = sessions[owner]["cookie"]
        r = requests.post(f"{BASE_URL}/post/create", json=post, cookies=cookies)
        if r.status_code == 200:
            post_id = r.json().get("data")
            post_owners[post_id] = owner
            print(f"  ✓ '{post['name']}' creado por {owner}")
        else:
            print(f"  ✗ '{post['name']}' error: {r.text}")

    # Add comments
    print("\nAgregando comentarios...")
    for post_id, owner in post_owners.items():
        commenters = [u for u in usernames if u != owner]
        num_comments = random.randint(2, 4)
        selected = random.sample(commenters, min(num_comments, len(commenters)))

        for commenter in selected:
            cookies = sessions[commenter]["cookie"]
            comment_data = {"content": random.choice(COMMENTS), "rating": random.randint(7, 10)}
            r = requests.put(f"{BASE_URL}/post/{post_id}/comment", json=comment_data, cookies=cookies)
            if r.status_code == 200:
                print(f"  ✓ {commenter} comentó en post {post_id[:8]}...")
            else:
                print(f"  ✗ {commenter} error: {r.text}")

    print("\n¡Seed fix completado!")

if __name__ == "__main__":
    seed_fix()
