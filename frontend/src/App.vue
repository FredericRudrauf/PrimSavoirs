<template>
  <div id="app">
    <!-- BARRE DE NAVIGATION -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-custom fixed-top px-3">
      <div class="container-fluid">
        <!-- Logo + Nom -->
        <router-link class="navbar-brand d-flex align-items-center me-4" to="/"style="font-size: 1.5rem; font-weight: bold;">
          <img src="/icons/web-app-manifest-192x192.png" alt="Logo" width="56" height="56" class="me-2" />
          <span>PrimSavoirs</span>
        </router-link>

        <!-- BOUTON BURGER -->
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- LIENS DE NAVIGATION -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav" style="font-size: 1.2rem;">
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.path === '/' }" to="/">Mathématiques</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.path === '/about' }" to="/about">À propos</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Décalage pour contenu -->
    <div style="margin-top: 70px;">
      <router-view />
    </div>
  </div>
</template>

<style>
.bg-custom {
  background-color: #4DBA87 !important;
}

.nav-link.active {
  font-weight: bold;
  color: white !important;
}
</style>
