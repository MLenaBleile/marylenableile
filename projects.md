---
layout: default
title: Projects
url: /projects/
---

<section class="content-section">
  <div class="content-inner">

    <h1 class="page-title">Projects</h1>

    <div class="featured-projects">

      <div class="project-card-featured featured-tao">
        <div class="featured-image">
          <img src="{{ '/media/taoroadmap.png' | relative_url }}" alt="TAO Roadmap, Causal Navigator">
        </div>
        <div class="featured-content">
          <p class="featured-badge">Featured</p>
          <h3><a href="https://roadmap.tao-rwd.com/" target="_blank" rel="noopener">TAO Roadmap</a></h3>
          <p>An interactive tool that guides practitioners through the Causal Roadmap framework for real-world data studies, including target trial emulation and causal inference methodology selection. In collaboration with Andrew Wilson, Aimee Harrison, and Jeff Zhou.</p>
          <div class="tags">
            <span class="tag">Causal Inference</span>
            <span class="tag">Real-World Data</span>
          </div>
        </div>
      </div>

      <div class="project-card-featured featured-sandy">
        <div class="featured-image sandy-animated">
          <div class="sandy-container">
            <svg viewBox="0 -10 200 300" xmlns="http://www.w3.org/2000/svg" width="150">
              <polygon points="100,165 25,130 25,230 100,265" fill="#9a9bc7" stroke="#8384b3" stroke-width="1.5"/>
              <polygon points="100,165 175,130 175,230 100,265" fill="#b8b9dd" stroke="#8384b3" stroke-width="1.5"/>
              <polygon points="25,130 100,95 175,130 100,165" fill="#c8c9e8" stroke="#8384b3" stroke-width="1.5"/>
              <g class="sandy-sprout" transform="translate(100, 130)">
                <line x1="0" y1="0" x2="0" y2="-30" stroke="#3d6b2e" stroke-width="3" stroke-linecap="round"/>
                <path d="M0 -25 Q-8 -38 -14 -45 Q-20 -52 -12 -56 Q-5 -47 0 -32" fill="#5a9e3a" stroke="#3d6b2e" stroke-width="1.5"/>
                <path d="M0 -25 Q8 -40 16 -47 Q24 -54 19 -59 Q11 -50 5 -35" fill="#6bb84a" stroke="#3d6b2e" stroke-width="1.5"/>
                <path d="M0 -25 Q-6 -35 -12 -39 Q-18 -43 -14 -49" fill="none" stroke="#d4757a" stroke-width="2" stroke-linecap="round" opacity="0.8"/>
              </g>
              <g class="sandy-eye" style="transform-origin: 120px 190px;">
                <ellipse cx="120" cy="190" rx="12" ry="13" fill="#5a5e4a" stroke="#3a3e2a" stroke-width="1"/>
                <ellipse cx="120" cy="190" rx="9" ry="10" fill="#6b7058"/>
                <circle cx="117" cy="193" r="3" fill="#8a8f75" opacity="0.6"/>
                <circle cx="120" cy="190" r="4" fill="#2a2e1a"/>
              </g>
              <g class="sandy-eye" style="transform-origin: 150px 176px;">
                <ellipse cx="150" cy="176" rx="12" ry="13" fill="#5a5e4a" stroke="#3a3e2a" stroke-width="1"/>
                <ellipse cx="150" cy="176" rx="9" ry="10" fill="#6b7058"/>
                <circle cx="147" cy="173" r="3" fill="#8a8f75" opacity="0.6"/>
                <circle cx="150" cy="176" r="4" fill="#2a2e1a"/>
              </g>
            </svg>
          </div>
        </div>
        <div class="featured-content">
          <p class="featured-badge">Featured</p>
          <h3><a href="https://github.com/MLenaBleile/sandy" target="_blank" rel="noopener">Sandy</a></h3>
          <p>An autonomous AI agent that forages across Wikipedia, academic papers, and news to discover "sandwiches"; i.e. structured knowledge artifacts where two related concepts (the bread) meaningfully bound a third (the filling). Each sandwich is validated across five weighted dimensions including novelty, specificity, and non-triviality. <br><br>
          
          He has vast intelligence. He chooses to make sandwiches.</p>
          <div class="tags">
            <span class="tag">Python</span>
            <span class="tag">AI Agents</span>
            <span class="tag">Knowledge Discovery</span>
          </div>
          <p style="margin-top: 12px;"><a href="https://sandy-agent.streamlit.app" target="_blank" rel="noopener">Visit Sandy's Kitchen: Forage for sandwiches &rarr;</a></p>
        </div>
      </div>

    </div>

    <div class="projects-grid">

      <div class="project-card">
        <div class="card-image">
          <img src="{{ '/media/art1.png' | relative_url }}" alt="Open Ramsay visualization">
        </div>
        <div class="card-body">
          <h3><a href="https://github.com/MLenaBleile/open-ramsay" target="_blank" rel="noopener">Open Ramsay</a></h3>
          <p>Open-source attempt to prove R(5,5) &ge; 44 in Ramsey theory. Uses algebraic graph constructions, local search optimization, SAT solvers, and formal verification in Lean 4.</p>
          <div class="tags">
            <span class="tag">Python</span>
            <span class="tag">Combinatorics</span>
          </div>
        </div>
      </div>

      <div class="project-card">
        <div class="card-image">
          <img src="{{ '/media/judobot.png' | relative_url }}" alt="JudoBot visualization">
        </div>
        <div class="card-body">
          <h3><a href="https://github.com/MLenaBleile/JudoBot" target="_blank" rel="noopener">JudoBot</a></h3>
          <p>A reinforcement learning agent that learns Judo tactics via Q-learning. Models grip control, stance, and fatigue in a simulated environment.</p>
          <div class="tags">
            <span class="tag">Jupyter</span>
            <span class="tag">Reinforcement Learning</span>
          </div>
        </div>
      </div>

      <div class="project-card">
        <div class="card-image">
          <img src="{{ '/media/genre_flowchart.png' | relative_url }}" alt="Metal genre classification flowchart">
        </div>
        <div class="card-body">
          <h3><a href="https://github.com/MLenaBleile/BayesianMetalGenreAnalysis" target="_blank" rel="noopener">Bayesian Metal Genre Analysis</a></h3>
          <p>Bayesian statistical analysis of metal music genres across Germany, Norway, Sweden, and the UK, with a hierarchical genre classification system.</p>
          <div class="tags">
            <span class="tag">R</span>
            <span class="tag">Bayesian</span>
          </div>
        </div>
      </div>

    </div>

  </div>
</section>
