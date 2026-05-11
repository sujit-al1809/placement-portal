<script setup>
import MatchScoreWidget from '../components/MatchScoreWidget.vue'
</script>

<template>
  <section class="hero">
    <div class="hero-grid">
      <div class="hero-copy surface">
        <div class="kicker">Placement portal</div>
        <h1>Connect students, recruiters, and admins in one flow.</h1>
        <p>
          Browse jobs, apply with one click, shortlist candidates, and surface AI-driven match scores instantly.
          The portal is designed for placement teams that need speed without losing control.
        </p>
        <div class="hero-actions">
          <router-link class="btn btn-primary" to="/register">Create account</router-link>
          <router-link class="btn btn-light" to="/login">Sign in</router-link>
          <router-link class="btn btn-accent" to="/match-score">Try the match widget</router-link>
        </div>

        <div class="grid grid-3" style="margin-top: 24px">
          <div class="hero-metric">
            <span class="muted">Student flow</span>
            <strong>Jobs, applications, scores</strong>
          </div>
          <div class="hero-metric">
            <span class="muted">HR flow</span>
            <strong>Post jobs, review talent</strong>
          </div>
          <div class="hero-metric">
            <span class="muted">Admin flow</span>
            <strong>Users and companies</strong>
          </div>
        </div>
      </div>

      <div class="stack">
        <div class="surface card">
          <div class="kicker">Core stack</div>
          <h3 style="margin: 8px 0">Flask API + Vue client</h3>
          <p class="muted" style="line-height: 1.7">
            Flask-Security handles token auth and role checks. SQLAlchemy persists users, companies, jobs,
            and applications. Celery can notify matching students when new jobs are posted.
          </p>
        </div>
        <div class="surface card">
          <div class="kicker">AI feature</div>
          <h3 style="margin: 8px 0">TF-IDF match scoring</h3>
          <p class="muted" style="line-height: 1.7">
            Paste a skills string and a job description to calculate a live compatibility score on the fly.
          </p>
        </div>
      </div>
    </div>
  </section>

  <div class="grid" style="gap: 22px; padding-bottom: 24px">
    <MatchScoreWidget />
  </div>
</template>
