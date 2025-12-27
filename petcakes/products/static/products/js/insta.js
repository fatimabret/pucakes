const BEHOLD_URL = 'TU_URL_DE_BEHOLD_AQUI';

async function loadInstagram() {
    try {
        const response = await fetch(BEHOLD_URL);
        const data = await response.json();

        // 1. Mostrar Perfil (Nombre y Botón)
        const header = document.getElementById('insta-profile-header');
        const username = data[0].username; // Behold devuelve un array de posts
        
        header.innerHTML = `
            <div class="profile-info">
                <h3>@${username}</h3>
                <a href="https://instagram.com/${username}" target="_blank" class="follow-button">Seguir</a>
            </div>
        `;

        // 2. Mostrar las 6 publicaciones
        const gallery = document.getElementById('insta-gallery');
        // Usamos slice(0, 6) para asegurar que solo se muestren 6
        data.slice(0, 6).forEach(post => {
            const imgElement = `
                <a href="${post.permalink}" target="_blank">
                    <img src="${post.mediaUrl}" alt="Post de Instagram">
                </a>
            `;
            gallery.innerHTML += imgElement;
        });

    } catch (error) {
        console.error("Error al cargar Instagram:", error);
    }
}

loadInstagram();