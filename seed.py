"""Seed script - Populates the database with test data via the API."""
import requests
import random

BASE_URL = "https://dweb-proyecto-production.up.railway.app/api"

USERS = [
    {"username": "M3ssi", "email": "m3ssi@test.com", "password": "HolaHola123?"},
    {"username": "W3stcol", "email": "w3stcol@test.com", "password": "HolaHola123?"},
    {"username": "F3id", "email": "f3id@test.com", "password": "HolaHola123?"},
    {"username": "G0ku", "email": "g0ku@test.com", "password": "HolaHola123?"},
    {"username": "S3nk", "email": "s3nk@test.com", "password": "HolaHola123?"},
]

POSTS = [
    {"name": "Pagoda Chureito", "location": "Yamanashi, Japón", "review": "Un lugar mágico donde puedes ver el Monte Fuji de fondo con la pagoda tradicional japonesa. La subida de escaleras vale totalmente la pena por la vista espectacular.", "rating": 9, "imageUrl": "https://res.klook.com/klook-brand/image/upload/fl_lossy.progressive,w_1200,h_630,c_fill,q_85/v1684410166/1-%20IMAGES/Countries/Japan/Yamanashi%20Prefecture/Fujiyoshida%20City/_Vertical%20Generic/_Experiences:%20Local%20Leisure/Chureito%20Pagoda/Chureito%20Pagoda_Fujiyoshida_Yamanashi_Japan_AdobeStock_265237090.jpg"},
    {"name": "Pirámides de Egipto", "location": "Guiza, Egipto", "review": "Las pirámides son impresionantes en persona, mucho más grandes de lo que imaginas. Una maravilla del mundo antiguo que te deja sin palabras.", "rating": 10, "imageUrl": "https://www.taranna.com/wp-content/uploads/2026/01/piramides-de-egipto-scaled.webp"},
    {"name": "Malecón del Río", "location": "Barranquilla, Colombia", "review": "Un paseo increíble junto al río Magdalena. Perfecto para caminar al atardecer con la brisa caribeña y disfrutar de la gastronomía local.", "rating": 8, "imageUrl": "https://barranquilla.gov.co/wp-content/uploads/2025/02/gran-malecon.jpg"},
    {"name": "Islas Lofoten", "location": "Nordland, Noruega", "review": "Paisajes de otro mundo con montañas que emergen del mar ártico. Las auroras boreales aquí son un espectáculo inolvidable.", "rating": 10, "imageUrl": "https://media.traveler.es/photos/668bee1f96cc25fd7b8e029f/16:9/w_2560%2Cc_limit/2BNN3MR%2520(1).jpg"},
    {"name": "Torre Eiffel", "location": "París, Francia", "review": "El ícono de París no decepciona. La vista desde la cima al atardecer es romántica y espectacular. Recomiendo subir por las escaleras para disfrutar cada nivel.", "rating": 9, "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Eiffelturm.JPG/960px-Eiffelturm.JPG"},
    {"name": "Ciudad Perdida", "location": "Santa Marta, Colombia", "review": "Una caminata exigente de 4 días por la selva que te lleva a ruinas ancestrales de los Tayrona. La experiencia cultural y natural es incomparable.", "rating": 9, "imageUrl": "https://ecoglobalexpeditions.com/wp-content/uploads/2016/12/paginaciudadperdida-720x800.jpg"},
    {"name": "Santuario de Las Lajas", "location": "Pasto, Colombia", "review": "Una iglesia construida sobre un cañón que parece sacada de un cuento de hadas. La arquitectura gótica en medio de la naturaleza es impresionante.", "rating": 9, "imageUrl": "https://i.pinimg.com/736x/b5/9c/6e/b59c6e3c4c408614b4a5612558d8f67e.jpg"},
    {"name": "Muralla China", "location": "Pekín, China", "review": "Caminar sobre la muralla te hace sentir parte de la historia. La sección de Mutianyu es menos concurrida y tiene vistas espectaculares.", "rating": 10, "imageUrl": "https://i.blogs.es/2df33e/20090529_great_wall_8185/450_1000.jpeg"},
    {"name": "Salar de Uyuni", "location": "Potosí, Bolivia", "review": "El desierto de sal más grande del mundo es surrealista. En temporada de lluvias se convierte en un espejo gigante que refleja el cielo.", "rating": 10, "imageUrl": "https://www.lorenzoexpeditions.com/wp-content/uploads/2025/01/Salar-de-Uyuni-11-1.jpg"},
    {"name": "Cataratas del Niágara", "location": "Ontario, Canadá", "review": "El poder del agua es sobrecogedor. El paseo en barco Maid of the Mist te acerca tanto que sientes la fuerza de la naturaleza en la piel.", "rating": 8, "imageUrl": "https://cdn.britannica.com/30/94430-050-D0FC51CD/Niagara-Falls.jpg"},
    {"name": "Monte Saint-Michel", "location": "Normandía, Francia", "review": "Una abadía medieval sobre una isla rocosa que parece flotar durante la marea alta. Pasear por sus callejuelas es viajar en el tiempo.", "rating": 9, "imageUrl": "https://media.traveler.es/photos/64f745b00cb606d22d6ef3b7/3:2/w_5100,h_3400,c_limit/TTNP70.jpg"},
    {"name": "Interlaken", "location": "Berna, Suiza", "review": "Rodeado de los Alpes suizos entre dos lagos cristalinos. Perfecto para deportes extremos o simplemente contemplar la naturaleza en su máxima expresión.", "rating": 9, "imageUrl": "https://www.planetware.com/img/gallery/interlaken-switzerlands-13-must-see-destinations-for-first-time-visitors/intro-1764257628.jpg"},
    {"name": "Acrópolis de Atenas", "location": "Atenas, Grecia", "review": "El Partenón es majestuoso y te transporta a la antigua Grecia. La vista de la ciudad desde arriba es un bonus increíble.", "rating": 8, "imageUrl": "https://media.cntraveler.com/photos/551dc0d196bfd1f1482d850e/16:9/w_2560,c_limit/acropolis-athens-greece.jpg"},
    {"name": "Machu Picchu", "location": "Cusco, Perú", "review": "La ciudadela inca entre las nubes es una experiencia espiritual. Llegar por el Camino Inca hace que la recompensa sea aún mayor.", "rating": 10, "imageUrl": "https://www.ytuqueplanes.com/imagenes//fotos/novedades/b-Macchupicchu-todo-lo-que-debes-conocer-antes-de-visitarlo.webp"},
    {"name": "Chichén Itzá", "location": "Yucatán, México", "review": "La pirámide de Kukulcán es una obra maestra de la astronomía maya. El efecto de la serpiente durante los equinoccios es fascinante.", "rating": 9, "imageUrl": "https://cdn1.matadornetwork.com/blogs/2/2018/03/Chichen-Itza-Mexico.jpeg"},
    {"name": "Coliseo Romano", "location": "Roma, Italia", "review": "Estar dentro del Coliseo te hace imaginar los gladiadores y la antigua Roma. La historia que guardan esas paredes es impresionante.", "rating": 9, "imageUrl": "https://img2.rtve.es/n/16553427?w=1600"},
    {"name": "Cristo Redentor", "location": "Río de Janeiro, Brasil", "review": "La estatua es imponente y la vista panorámica de Río desde el Corcovado es de las mejores del mundo. Mejor ir temprano para evitar multitudes.", "rating": 8, "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Christ_the_Redeemer_-_Cristo_Redentor.jpg"},
    {"name": "Isla de Pascua", "location": "Valparaíso, Chile", "review": "Los moáis son misteriosos y la isla tiene una energía especial. Está aislada en medio del Pacífico pero eso la hace única.", "rating": 10, "imageUrl": "https://static.nationalgeographicla.com/files/styles/image_3200/public/28019.webp?w=1600&h=900"},
    {"name": "Ciudad del Vaticano", "location": "Ciudad del Vaticano, Italia", "review": "La Capilla Sixtina y la Basílica de San Pedro son obras maestras del arte. Cada rincón tiene siglos de historia y belleza.", "rating": 9, "imageUrl": "https://www.omnesmag.com/wp-content/uploads/2022/10/ACT_JUL.jpg"},
    {"name": "Stonehenge", "location": "Wiltshire, Inglaterra", "review": "El misterio de cómo se construyó sigue vigente. Verlo al amanecer con la niebla es una experiencia mística que te conecta con el pasado.", "rating": 8, "imageUrl": "https://ingeoexpert.com/wp-content/uploads/2022/11/pexels-john-nail-1448136-scaled.webp"},
]

COMMENTS = [
    "¡Increíble lugar! Definitivamente está en mi lista de viajes pendientes.",
    "Las fotos no le hacen justicia, debe ser mucho mejor en persona.",
    "Fui el año pasado y puedo confirmar que es espectacular.",
    "¿Cuánto tiempo recomiendas para visitarlo?",
    "Me encanta este destino, lo tengo en mi bucket list.",
    "La naturaleza en su máxima expresión, qué belleza.",
    "Excelente reseña, muy completa y útil para planificar el viaje.",
    "Ese lugar se ve increíble, necesito ir ya.",
    "Hermoso destino, gracias por compartir la experiencia.",
    "¡Qué envidia! Espero poder ir algún día.",
    "La arquitectura es impresionante, se nota la historia.",
    "Muy buen rating, coincido totalmente con la calificación.",
    "Este es de esos lugares que hay que ver antes de morir.",
    "Gracias por la recomendación, no conocía este lugar.",
    "Las vistas deben ser espectaculares desde ahí.",
    "Un destino que no decepciona, lo recomiendo al 100%.",
    "Me gustaría saber más sobre cómo llegar y dónde hospedarse.",
    "Impresionante fotografía, captura muy bien la esencia del lugar.",
    "Definitivamente un lugar para visitar con calma y sin prisas.",
    "¡Wow! No sabía que existía un lugar así, increíble.",
]

def seed():
    sessions = {}

    # Register users
    print("Registrando usuarios...")
    for user in USERS:
        r = requests.post(f"{BASE_URL}/app/register", json=user)
        if r.status_code in (200, 201):
            token = r.cookies.get("token")
            sessions[user["username"]] = {"cookie": {"token": token}}
            print(f"  ✓ {user['username']} registrado")
        else:
            print(f"  ✗ {user['username']} error: {r.text}")

    if not sessions:
        print("No se pudieron registrar usuarios. Abortando.")
        return

    # Distribute posts among users
    usernames = list(sessions.keys())
    print("\nCreando posts...")
    post_owners = {}
    for i, post in enumerate(POSTS):
        owner = usernames[i % len(usernames)]
        cookies = sessions[owner]["cookie"]
        r = requests.post(f"{BASE_URL}/post/create", json=post, cookies=cookies)
        if r.status_code == 200:
            post_id = r.json().get("data")
            post_owners[post_id] = owner
            print(f"  ✓ '{post['name']}' creado por {owner}")
        else:
            print(f"  ✗ '{post['name']}' error: {r.text}")

    # Add comments (2-4 per post, not by the post owner)
    print("\nAgregando comentarios...")
    for post_id, owner in post_owners.items():
        commenters = [u for u in usernames if u != owner]
        num_comments = random.randint(2, 4)
        selected = random.sample(commenters, min(num_comments, len(commenters)))

        for commenter in selected:
            cookies = sessions[commenter]["cookie"]
            comment_data = {
                "content": random.choice(COMMENTS),
                "rating": random.randint(7, 10)
            }
            r = requests.put(f"{BASE_URL}/post/{post_id}/comment", json=comment_data, cookies=cookies)
            if r.status_code == 200:
                print(f"  ✓ {commenter} comentó en post {post_id[:8]}...")
            else:
                print(f"  ✗ {commenter} error en post {post_id[:8]}: {r.text}")

    print("\n¡Seed completado!")

if __name__ == "__main__":
    seed()
