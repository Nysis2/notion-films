// ─────────────────────────────────────────────
//  Modale de détail d'un film
//  S'ouvre au clic sur une card.
//  Se ferme via la croix, Échap, ou clic sur le fond.
// ─────────────────────────────────────────────


// ── Ouverture ────────────────────────────────

function openModal(movie) {
  const content = document.getElementById("modal-content");

  // --- Badge de note ---
  const ratingHTML = movie.rating && movie.rating > 0
    ? `<span class="meta-pill rating">
         <svg width="11" height="11" viewBox="0 0 24 24" fill="#f0c060">
           <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
         </svg>
         ${movie.rating.toFixed(1)}
       </span>`
    : `<span class="meta-pill">À venir</span>`;

  // --- Durée (ex : "1h52") ---
  const runtimeHTML = movie.runtime
    ? `<span class="meta-pill">
         <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
           <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
         </svg>
         ${Math.floor(movie.runtime / 60)}h${String(movie.runtime % 60).padStart(2, "0")}
       </span>`
    : "";

  // --- Date de sortie formatée en français ---
  const dateHTML = movie.release_date
    ? `<span class="meta-pill">
         ${new Date(movie.release_date).toLocaleDateString("fr-FR", {
           day: "numeric", month: "long", year: "numeric"
         })}
       </span>`
    : "";

  // --- Bouton bande-annonce (affiché seulement si une URL YouTube existe) ---
  const trailerBtn = movie.trailer
    ? `<a class="modal-trailer-btn" href="${movie.trailer}" target="_blank">
         <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
         Voir la bande-annonce
       </a>`
    : "";

  // --- Boutons cinémas (liens fixes vers les pages des cinémas lyonnais) ---
  const cinemaBtns = `
    <a class="modal-cinema-btn" href="https://www.ugc.fr/cinema-ugc-cine-cite-part-dieu.html" target="_blank">
      <img src="https://www.google.com/s2/favicons?domain=ugc.fr&sz=16" width="13" height="13" alt=""
           style="background: #fff; border-radius: 3px; padding: 1px;">
      UGC Part-Dieu
    </a>
    <a class="modal-cinema-btn" href="https://www.pathe.fr/cinemas/cinema-pathe-carre-de-soie" target="_blank">
      <img src="https://www.google.com/s2/favicons?domain=pathe.fr&sz=16" width="13" height="13" alt="">
      Pathé Carré de Soie
    </a>
  `;

  // --- Image de fond (backdrop) avec fallback sur un dégradé ---
  const backdropHTML = movie.backdrop
    ? `<img class="modal-backdrop" src="${movie.backdrop}" alt=""
            onerror="this.style.display='none'; this.nextElementSibling.style.display='block'">
       <div class="modal-backdrop-placeholder" style="display:none"></div>`
    : `<div class="modal-backdrop-placeholder"></div>`;

  // --- Injection du HTML dans la modale ---
  content.innerHTML = `
    <div class="modal-header">
      ${backdropHTML}
      <div class="modal-backdrop-gradient"></div>
    </div>

    <div class="modal-body">
      <div class="modal-poster">
        <img src="${movie.poster}" alt="${movie.title}"
             onerror="this.src='https://www.consultingmc.info/wp-content/uploads/2024/01/No-Image-Placeholder.svg_.png'">
      </div>

      <div class="modal-info">
        <div class="modal-title">${movie.title}</div>

        ${movie.tagline ? `<div class="modal-tagline">"${movie.tagline}"</div>` : ""}

        <div class="modal-meta">
          ${ratingHTML}
          ${runtimeHTML}
          ${dateHTML}
          <span class="meta-pill">${movie.genre}</span>
        </div>

        ${movie.overview ? `<div class="modal-overview">${movie.overview}</div>` : ""}

        <div class="modal-actions">
          ${trailerBtn}
          ${cinemaBtns}
        </div>
      </div>
    </div>
  `;

  document.getElementById("modal-overlay").classList.add("open");
  document.body.style.overflow = "hidden"; // Bloquer le scroll de la page derrière
}


// ── Fermeture ─────────────────────────────────

function closeModal() {
  document.getElementById("modal-overlay").classList.remove("open");
  document.body.style.overflow = "";
}

// Fermer via la croix
document.getElementById("modal-close").addEventListener("click", closeModal);

// Fermer en cliquant sur le fond sombre (hors de la modale)
document.getElementById("modal-overlay").addEventListener("click", (e) => {
  if (e.target === document.getElementById("modal-overlay")) closeModal();
});

// Fermer avec la touche Échap
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeModal();
});
