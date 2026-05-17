"""Seed fix 2 - Retry remaining failed posts with reliable image URLs."""
import requests
import random

BASE_URL = "https://dweb-proyecto-production.up.railway.app/api"

USERS = [
    {"username_or_email": "m3ssi@test.com", "password": "HolaHola123?", "username": "M3ssi"},
    {"username_or_email": "w3stcol@test.com", "password": "HolaHola123?", "username": "W3stcol"},
    {"username_or_email": "f3id@test.com", "password": "HolaHola123?", "username": "F3id"},
    {"username_or_email": "g0ku@test.com", "password": "HolaHola123?", "username": "G0ku"},
    {"username_or_email": "s3nk@test.com", "password": "HolaHola123?", "username": "S3nk"},
]

FAILED_POSTS = [
    {"name": "Pagoda Chureito", "location": "Yamanashi, Japón", "review": "Un lugar mágico donde puedes ver el Monte Fuji de fondo con la pagoda tradicional japonesa. La subida de escaleras vale totalmente la pena por la vista espectacular.", "rating": 9, "imageUrl": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1200"},
    {"name": "Malecón del Río", "location": "Barranquilla, Colombia", "review": "Un paseo increíble junto al río Magdalena. Perfecto para caminar al atardecer con la brisa caribeña y disfrutar de la gastronomía local.", "rating": 8, "imageUrl": "https://images.unsplash.com/photo-1583508915901-b5f84c1dcde1?w=1200"},
    {"name": "Islas Lofoten", "location": "Nordland, Noruega", "review": "Paisajes de otro mundo con montañas que emergen del mar ártico. Las auroras boreales aquí son un espectáculo inolvidable.", "rating": 10, "imageUrl": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?w=1200"},
    {"name": "Monte Saint-Michel", "location": "Normandía, Francia", "review": "Una abadía medieval sobre una isla rocosa que parece flotar durante la marea alta. Pasear por sus callejuelas es viajar en el tiempo.", "rating": 9, "imageUrl": "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=1200"},
    {"name": "Cristo Redentor", "location": "Río de Janeiro, Brasil", "review": "La estatua es imponente y la vista panorámica de Río desde el Corcovado es de las mejores del mundo. Mejor ir temprano para evitar multitudes.", "rating": 8, "imageUrl": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=1200"},
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

def seed_fix2():
    sessions = {}

    print("Iniciando sesión...")
    for user in USERS:
        r = requests.post(f"{BASE_URL}/app/login", json={"username_or_email": user["username_or_email"], "password": user["password"]})
        if r.status_code == 200:
            token = r.cookies.get("token")
            sessions[user["username"]] = {"cookie": {"token": token}}
            print(f"  ✓ {user['username']}")
        else:
            print(f"  ✗ {user['username']} error: {r.text}")

    usernames = list(sessions.keys())

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

    print("\n¡Completado!")

if __name__ == "__main__":
    seed_fix2()
