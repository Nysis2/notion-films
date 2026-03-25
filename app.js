// ─────────────────────────────────────────────
//  Configuration
// ─────────────────────────────────────────────

const PER_PAGE = 20; // Nombre de films affichés par page

// État global de l'application
let currentPage = 1;
let allMovies  = []; // Liste complète chargée depuis movies.json
let filtered   = []; // Liste après application des filtres et du tri


// ─────────────────────────────────────────────
//  Mode standalone (hors iframe)
//  Active le fond sombre et le titre quand le
//  site est ouvert directement dans le navigateur
// ─────────────────────────────────────────────

if (window.self === window.top) {
  document.body.classList.add("standalone");
}


// ─────────────────────────────────────────────
//  Composant dropdown personnalisé
//  Remplace les <select> natifs pour correspondre
//  au style sombre du site.
//
//  Utilisation : initSelect(ids..., callback)
//  Le callback reçoit la valeur sélectionnée.
// ─────────────────────────────────────────────

function initSelect(selectId, triggerId, menuId, labelId, onChange) {
  const select  = document.getElementById(selectId);
  const trigger = document.getElementById(triggerId);
  const menu    = document.getElementById(menuId);
  const label   = document.getElementById(labelId);

  // Ouvrir / fermer au clic sur le bouton
  trigger.addEventListener("click", (e) => {
    e.stopPropagation();
    // Fermer les autres dropdowns ouverts
    document.querySelectorAll(".custom-select.open").forEach(s => {
      if (s !== select) s.classList.remove("open");
    });
    select.classList.toggle("open");
  });

  // Sélectionner une option
  menu.addEventListener("click", (e) => {
    const opt = e.target.closest(".custom-select-option");
    if (!opt) return;

    menu.querySelectorAll(".custom-select-option").forEach(o => o.classList.remove("selected"));
    opt.classList.add("selected");
    label.textContent = opt.textContent.trim();
    select.classList.remove("open");
    onChange(opt.dataset.value);
  });
}

// Fermer tous les dropdowns si on clique ailleurs sur la page
document.addEventListener("click", () => {
  document.querySelectorAll(".custom-select.open").forEach(s => s.classList.remove("open"));
});


// ─────────────────────────────────────────────
//  Initialisation des dropdowns
// ─────────────────────────────────────────────

let currentSort  = "default"; // Valeur du tri sélectionné
let currentGenre = "";        // Genre sélectionné ("" = tous)

// Dropdown de tri
initSelect("sort-select", "sort-trigger", "sort-menu", "sort-label", (val) => {
  currentSort = val;
  applyFilters();
});

// Dropdown de genre (les options sont peuplées dynamiquement après le chargement)
initSelect("genre-select", "genre-trigger", "genre-menu", "genre-label", (val) => {
  currentGenre = val;
  applyFilters();
});


// ─────────────────────────────────────────────
//  Filtres et tri
//  Appelé à chaque changement de recherche,
//  de genre ou de tri.
// ─────────────────────────────────────────────

function applyFilters() {
  const query = document.getElementById("search").value.trim().toLowerCase();

  // Filtrage : texte libre (titre ou genre) + genre sélectionné
  filtered = allMovies.filter(movie => {
    const matchQuery = !query
      || movie.title.toLowerCase().includes(query)
      || movie.genre.toLowerCase().includes(query);

    // Un film peut avoir plusieurs genres séparés par " / "
    const matchGenre = !currentGenre
      || movie.genre.split(" / ").includes(currentGenre);

    return matchQuery && matchGenre;
  });

  // Tri
  filtered.sort((a, b) => {
    switch (currentSort) {
      case "rating-desc": return (b.rating || 0) - (a.rating || 0);
      case "rating-asc":  return (a.rating || 0) - (b.rating || 0);
      case "title-asc":   return a.title.localeCompare(b.title, "fr");
      case "title-desc":  return b.title.localeCompare(a.title, "fr");
      case "date-desc":   return (b.release_date || "").localeCompare(a.release_date || "");
      case "date-asc":    return (a.release_date || "").localeCompare(b.release_date || "");
      default:            return 0;
    }
  });

  currentPage = 1;
  renderPage(currentPage);
}

// Déclencher les filtres à chaque frappe dans la barre de recherche
document.getElementById("search").addEventListener("input", applyFilters);


// ─────────────────────────────────────────────
//  Affichage des cards
// ─────────────────────────────────────────────

function renderPage(page) {
  const container = document.getElementById("movies");
  container.innerHTML = "";

  // Mise à jour du compteur de résultats
  document.getElementById("count").textContent =
    filtered.length === allMovies.length
      ? `${allMovies.length} films`
      : `${filtered.length} / ${allMovies.length} films`;

  // Aucun résultat
  if (filtered.length === 0) {
    container.innerHTML = '<div class="no-results">Aucun film trouvé</div>';
    document.getElementById("pagination").innerHTML = "";
    return;
  }

  // Découper la liste selon la page courante
  const start = (page - 1) * PER_PAGE;
  filtered.slice(start, start + PER_PAGE).forEach((movie) => {
    const card = document.createElement("div");
    card.classList.add("card");

    // Badge de note (étoile + chiffre, ou "À venir" si pas de note)
    const rating = movie.rating && movie.rating > 0 ? movie.rating.toFixed(1) : null;
    const ratingBadge = rating
      ? `<span class="rating-badge">
           <svg width="10" height="10" viewBox="0 0 24 24" fill="#f0c060"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
           ${rating}
         </span>`
      : `<span class="rating-badge na">À venir</span>`;

    card.innerHTML = `
      <div class="poster-wrapper">
        <img src="${movie.poster}" alt="${movie.title}" loading="lazy"
             onerror="this.src='https://www.consultingmc.info/wp-content/uploads/2024/01/No-Image-Placeholder.svg_.png'">
        ${ratingBadge}
      </div>
      <div class="card-body">
        <h3>${movie.title}</h3>
        <span class="genre-tag">${movie.genre}</span>
        <a class="trailer-btn" href="${movie.trailer}" target="_blank" onclick="event.stopPropagation()">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
          Bande-annonce
        </a>
      </div>
    `;

    // Ouvrir la modale au clic sur la card
    card.addEventListener("click", () => openModal(movie));
    container.appendChild(card);
  });

  renderPagination(page);
}


// ─────────────────────────────────────────────
//  Pagination
// ─────────────────────────────────────────────

function renderPagination(page) {
  const totalPages = Math.ceil(filtered.length / PER_PAGE);
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  // Inutile d'afficher la pagination s'il n'y a qu'une page
  if (totalPages <= 1) return;

  // Aller à une page et remonter en haut
  const goTo = (p) => {
    currentPage = p;
    renderPage(p);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Créer un bouton de page
  const btn = (label, p, disabled = false, active = false) => {
    const b = document.createElement("button");
    b.innerHTML = label;
    if (active)   b.classList.add("active");
    if (disabled) b.disabled = true;
    b.addEventListener("click", () => { if (!disabled) goTo(p); });
    return b;
  };

  // Créer les "..." entre les pages non contiguës
  const dots = () => {
    const s = document.createElement("span");
    s.className = "dots";
    s.textContent = "…";
    return s;
  };

  // Bouton précédent
  pagination.appendChild(btn("&#8592;", page - 1, page === 1));

  // Pages visibles : toujours afficher la 1ère, la dernière, et les voisines de la page courante
  const visible = new Set(
    [1, totalPages, page - 1, page, page + 1].filter(p => p >= 1 && p <= totalPages)
  );

  let prev = 0;
  [...visible].sort((a, b) => a - b).forEach(p => {
    if (p - prev > 1) pagination.appendChild(dots());
    pagination.appendChild(btn(p, p, false, p === page));
    prev = p;
  });

  // Bouton suivant
  pagination.appendChild(btn("&#8594;", page + 1, page === totalPages));
}


// ─────────────────────────────────────────────
//  Chargement des données
//  Lit movies.json généré par fetch_movies.py
// ─────────────────────────────────────────────

fetch("movies.json")
  .then(r => r.json())
  .then(movies => {
    allMovies = movies;
    filtered  = [...movies];

    // Construire la liste des genres uniques à partir des films
    // Chaque film peut avoir plusieurs genres séparés par " / "
    const genres = [
      ...new Set(movies.flatMap(m => m.genre ? m.genre.split(" / ") : []))
    ].sort((a, b) => a.localeCompare(b, "fr"));

    // Peupler le dropdown des genres
    const genreMenu = document.getElementById("genre-menu");
    genres.forEach(genre => {
      const opt = document.createElement("div");
      opt.className     = "custom-select-option";
      opt.dataset.value = genre;
      opt.textContent   = genre;
      genreMenu.appendChild(opt);
    });

    renderPage(currentPage);
    document.getElementById("count").textContent = `${movies.length} films`;
  })
  .catch(() => {
    document.getElementById("movies").innerHTML =
      '<div class="loading">Impossible de charger les films.</div>';
  });
