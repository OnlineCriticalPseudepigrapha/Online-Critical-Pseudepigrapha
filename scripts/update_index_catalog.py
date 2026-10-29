#!/usr/bin/env python3
"""
Updates index.html to render all 299 texts from CANON.md (via static/data/catalog.json).
Adds Corpus / Status tabs (All Texts, Live Editions, Clavis Records / Gaps),
Section/Genre filters, Crosswalk concordance cards, and enriched modal previews.
Ensures Bibliography & Editions section is rendered in the modal.
"""
import json
import re

with open('static/data/catalog.json', 'r', encoding='utf-8') as f:
    catalog_items = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS if needed for tabs, badges, crosswalk pills
custom_css = """
    /* Status Badges */
    .badge-live { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; font-weight: 700; }
    .badge-staged { background: #fef9c3; color: #854d0e; border: 1px solid #fef08a; font-weight: 600; }
    .badge-gap { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; font-weight: 500; }
    [data-theme="dark"] .badge-live { background: #052e16; color: #86efac; border-color: #14532d; }
    [data-theme="dark"] .badge-staged { background: #422006; color: #fde047; border-color: #713f12; }
    [data-theme="dark"] .badge-gap { background: #1e293b; color: #94a3b8; border-color: #334155; }

    /* Crosswalk Concordance Pill Grid */
    .concordance-box {
      margin-top: 10px;
      padding: 8px 10px;
      background: var(--bg-secondary);
      border-radius: var(--radius-sm);
      font-size: 0.76rem;
      color: var(--text-secondary);
      display: flex;
      flex-direction: column;
      gap: 4px;
      border: 1px dashed var(--border-color);
    }
    .concordance-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
    }
    .crosswalk-chip {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      padding: 1px 6px;
      border-radius: 4px;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      white-space: nowrap;
    }

    /* Status Tab Switcher */
    .status-tabs {
      display: flex;
      gap: 6px;
      background: var(--bg-secondary);
      padding: 4px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
      width: fit-content;
      margin-bottom: 8px;
    }
    .status-tab {
      padding: 6px 14px;
      border-radius: var(--radius-sm);
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-secondary);
      background: transparent;
      border: none;
      cursor: pointer;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .status-tab:hover {
      color: var(--text-primary);
    }
    .status-tab.active {
      background: var(--bg-card);
      color: var(--accent-gold-dark);
      box-shadow: var(--shadow-sm);
    }
    [data-theme="dark"] .status-tab.active {
      color: var(--accent-gold);
    }

    /* Modal Tabs */
    .modal-tab-bar {
      display: flex;
      border-bottom: 1px solid var(--border-color);
      background: var(--bg-secondary);
      padding: 0 24px;
      gap: 8px;
    }
    .modal-tab-btn {
      padding: 10px 16px;
      background: transparent;
      border: none;
      border-bottom: 2px solid transparent;
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
    }
    .modal-tab-btn.active {
      color: var(--accent-gold);
      border-bottom-color: var(--accent-gold);
    }
"""

if '.badge-live' not in html:
    html = html.replace('/* Modal / Drawer */', custom_css + '\n    /* Modal / Drawer */')

# 2. Replace Controls Bar to include Status Tabs & Section Select
new_controls = """<div class="controls-card">
        <!-- Status Filter Tabs -->
        <div class="status-tabs" id="statusTabs" role="tablist">
          <button class="status-tab active" data-status="all" role="tab" aria-selected="true">
            All Canon Texts <span class="pill-count" id="countStatusAll">299</span>
          </button>
          <button class="status-tab" data-status="live" role="tab" aria-selected="false">
            Live Editions <span class="pill-count" id="countStatusLive">51</span>
          </button>
          <button class="status-tab" data-status="gap" role="tab" aria-selected="false">
            Clavis Records / Gaps <span class="pill-count" id="countStatusGap">248</span>
          </button>
        </div>

        <div class="controls-row-top">
          <div class="search-box">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" id="searchInput" class="search-input" placeholder="Search 299 texts by English/Latin title, CAVT ID, language, figure, or OTP/APOT ref..." aria-label="Search documents" />
          </div>

          <div class="select-wrapper">
            <select id="sectionSelect" class="custom-select" aria-label="Filter by Corpus Section">
              <option value="all">All Corpus Sections (27)</option>
              <option value="ADAM">Adam Literature</option>
              <option value="POSTERI ADAE">Posteri Adae (Enoch, Noah, Shem)</option>
              <option value="ABRAHAM">Abraham, Isaac, Jacob</option>
              <option value="XII PATRIARCHAE">Twelve Patriarchs</option>
              <option value="MOYSES">Moses Traditions</option>
              <option value="JOSUE - JUDICES">Joshua &amp; Judges</option>
              <option value="I-II SAMUEL">Samuel, Kings, Chronicles</option>
              <option value="PSALMI">Psalms, Job, Wisdom</option>
              <option value="XII PROPHETAE">Prophets (Isaiah, Jeremiah, Ezekiel)</option>
              <option value="DANIEL">Daniel Traditions &amp; Apocalypses</option>
              <option value="ESDRAS">Ezra, Esther, Tobit, Maccabees</option>
              <option value="HISTORIA">Judaeo-Hellenistic Historians</option>
              <option value="POESIS">Judaeo-Hellenistic Poets &amp; Drama</option>
              <option value="PHILOSOPHIA">Judaeo-Hellenistic Philosophers</option>
              <option value="QUMRAN">Qumran &amp; Sectarian Works</option>
              <option value="APOCALYPSIS">Other Apocalypses &amp; Varia</option>
            </select>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </div>

          <div class="select-wrapper">
            <select id="sortSelect" class="custom-select" aria-label="Sort documents">
              <option value="canon-asc">Sort: OCP Canon ID (CAVT-001 &rarr; 277, JH)</option>
              <option value="title-asc">Sort: Title (A &rarr; Z)</option>
              <option value="title-desc">Sort: Title (Z &rarr; A)</option>
              <option value="lang">Sort: Language</option>
              <option value="status">Sort: Live Editions First</option>
            </select>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </div>
        </div>

        <div class="filter-pills">
          <span class="filter-label">Language:</span>
          <button class="pill-btn active" data-lang="all">All <span class="pill-count" id="countAll">299</span></button>
          <button class="pill-btn" data-lang="Greek">Greek <span class="pill-count" id="countGreek">0</span></button>
          <button class="pill-btn" data-lang="Latin">Latin <span class="pill-count" id="countLatin">0</span></button>
          <button class="pill-btn" data-lang="Syriac">Syriac <span class="pill-count" id="countSyriac">0</span></button>
          <button class="pill-btn" data-lang="Hebrew">Hebrew <span class="pill-count" id="countHebrew">0</span></button>
          <button class="pill-btn" data-lang="Aramaic">Aramaic <span class="pill-count" id="countAramaic">0</span></button>
          <button class="pill-btn" data-lang="Ethiopic">Ethiopic <span class="pill-count" id="countEthiopic">0</span></button>
          <button class="pill-btn" data-lang="Armenian">Armenian <span class="pill-count" id="countArmenian">0</span></button>
          <button class="pill-btn" data-lang="Coptic">Coptic <span class="pill-count" id="countCoptic">0</span></button>
          <button class="pill-btn" data-lang="Slavonic">Slavonic <span class="pill-count" id="countSlavonic">0</span></button>
        </div>

        <div class="results-meta">
          <span id="resultsCounter">Showing 299 texts</span>
          <span style="font-size:0.8rem;">Click <strong>Read Text</strong> for live editions or <strong>Dossier / Concordance</strong> for clavis profiles.</span>
        </div>
      </div>"""

old_controls_pattern = re.compile(r'<div class="controls-card">.*?</div>\s*<!-- Cards Grid -->', re.DOTALL)
html = old_controls_pattern.sub(new_controls + '\n\n      <!-- Cards Grid -->', html)

# 3. Replace the Modal body with multi-tab structure (Dossier / Crosswalk / TEI XML)
new_modal_card = """<div class="modal-card">
      <div class="modal-header">
        <div class="modal-title">
          <h4 id="modalDocTitle">Document Details</h4>
        </div>
        <button class="modal-close" id="modalCloseBtn" aria-label="Close modal">&times;</button>
      </div>
      <div class="modal-tab-bar" id="modalTabBar">
        <button class="modal-tab-btn active" id="modalTabDossier" onclick="switchModalTab('dossier')">Overview &amp; Dossier</button>
        <button class="modal-tab-btn" id="modalTabConcordance" onclick="switchModalTab('concordance')">6-Way Concordance</button>
        <button class="modal-tab-btn" id="modalTabXml" onclick="switchModalTab('xml')">TEI XML Preview</button>
      </div>
      <div class="modal-body" id="modalBody">
        <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; align-items:center;">
          <div id="modalDocMeta" style="font-size:0.9rem; color:var(--text-secondary);"></div>
          <div id="modalDocBadges" class="doc-badges"></div>
        </div>

        <!-- Dossier Tab Content -->
        <div id="tabContentDossier" style="display:flex; flex-direction:column; gap:14px;">
          <div id="modalIntroContent" style="font-size:0.95rem; line-height:1.6; color:var(--text-primary);"></div>
          <div id="modalProvenanceSection" style="display:none;">
            <h5 style="margin-bottom:6px; color:var(--accent-gold-dark);">Provenance &amp; Date</h5>
            <div id="modalProvenanceContent" style="font-size:0.9rem; line-height:1.5;"></div>
          </div>
          <div id="modalMssSection" style="display:none;">
            <h5 style="margin-bottom:6px; color:var(--accent-gold-dark);">Manuscripts &amp; Witnesses</h5>
            <div id="modalMssContent" style="font-size:0.88rem; line-height:1.5; overflow-x:auto;"></div>
          </div>
          <div id="modalBiblioSection" style="display:none;">
            <h5 style="margin-bottom:6px; color:var(--accent-gold-dark);">Critical Editions &amp; Bibliography</h5>
            <div id="modalBiblioContent" style="font-size:0.88rem; line-height:1.5; overflow-x:auto;"></div>
          </div>
        </div>

        <!-- Concordance Tab Content -->
        <div id="tabContentConcordance" style="display:none; flex-direction:column; gap:12px;">
          <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:4px;">
            Cross-references across the six major reference corpora (CANON.md framework):
          </p>
          <table style="width:100%; border-collapse:collapse; font-size:0.88rem;">
            <tbody>
              <tr style="border-bottom:1px solid var(--border-color);">
                <td style="padding:6px 8px; font-weight:600; width:180px;">CAVT (Haelewyck 1998)</td>
                <td id="modalConfCavt" style="padding:6px 8px; font-family:var(--font-mono);"></td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-color);">
                <td style="padding:6px 8px; font-weight:600;">CANT Reference</td>
                <td id="modalConfCant" style="padding:6px 8px; font-family:var(--font-mono);"></td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-color);">
                <td style="padding:6px 8px; font-weight:600;">Denis (1970 / 2000)</td>
                <td id="modalConfDenis" style="padding:6px 8px;"></td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-color);">
                <td style="padding:6px 8px; font-weight:600;">DiTommaso (2001)</td>
                <td id="modalConfDiTommaso" style="padding:6px 8px;"></td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-color);">
                <td style="padding:6px 8px; font-weight:600;">Charlesworth (OTP 1 &amp; 2)</td>
                <td id="modalConfOtp" style="padding:6px 8px;"></td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-color);">
                <td style="padding:6px 8px; font-weight:600;">Charles (APOT 2)</td>
                <td id="modalConfApot" style="padding:6px 8px;"></td>
              </tr>
              <tr style="border-bottom:1px solid var(--border-color);">
                <td style="padding:6px 8px; font-weight:600;">Sparks (AOT 1984)</td>
                <td id="modalConfAot" style="padding:6px 8px;"></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- XML Tab Content -->
        <div id="tabContentXml" style="display:none; flex-direction:column; gap:10px;">
          <p style="font-size:0.88rem; color:var(--text-muted);" id="modalXmlDesc">TEI XML Source Snippet (First 60 lines):</p>
          <pre class="xml-preview-box"><code id="modalXmlContent">Select a document to view TEI XML.</code></pre>
        </div>
      </div>
      <div class="modal-footer">"""

old_modal_card = re.compile(r'<div class="modal-card">.*?<div class="modal-footer">', re.DOTALL)
html = old_modal_card.sub(new_modal_card, html)

# 4. Replace embedded DOCS_DATA and JavaScript engine
script_start_idx = html.find('const DOCS_DATA = [')
if script_start_idx == -1:
    script_start_idx = html.find('const DOCS_DATA = ')
script_end_idx = html.find('</script>', script_start_idx)

catalog_json_str = json.dumps(catalog_items, ensure_ascii=False)

new_script = f"""const DOCS_DATA = {catalog_json_str};

    // Theme Management
    const themeToggle = document.getElementById('themeToggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('ocp-theme') || (prefersDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', savedTheme);

    themeToggle.addEventListener('click', () => {{
      const current = document.documentElement.getAttribute('data-theme');
      const target = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', target);
      localStorage.setItem('ocp-theme', target);
    }});

    // Catalog Counts
    const statusCounts = {{
      all: DOCS_DATA.length,
      live: DOCS_DATA.filter(d => d.status === 'live').length,
      gap: DOCS_DATA.filter(d => d.status !== 'live').length
    }};
    document.getElementById('countStatusAll').textContent = statusCounts.all;
    document.getElementById('countStatusLive').textContent = statusCounts.live;
    document.getElementById('countStatusGap').textContent = statusCounts.gap;

    const langCounts = {{ all: DOCS_DATA.length }};
    DOCS_DATA.forEach(d => {{
      const l = d.lang || 'Other';
      langCounts[l] = (langCounts[l] || 0) + 1;
    }});
    document.getElementById('countAll').textContent = langCounts.all;
    const langBtnIds = {{
      Greek: 'countGreek',
      Latin: 'countLatin',
      Syriac: 'countSyriac',
      Hebrew: 'countHebrew',
      Aramaic: 'countAramaic',
      Ethiopic: 'countEthiopic',
      Armenian: 'countArmenian',
      Coptic: 'countCoptic',
      Slavonic: 'countSlavonic'
    }};
    for (const [lang, elemId] of Object.entries(langBtnIds)) {{
      const el = document.getElementById(elemId);
      if (el) el.textContent = langCounts[lang] || 0;
    }}

    // State Variables
    let currentStatus = 'all';
    let currentFilterLang = 'all';
    let currentSection = 'all';
    let currentSearch = '';
    let currentSort = 'canon-asc';
    let activeModalItem = null;

    const docsGrid = document.getElementById('docsGrid');
    const searchInput = document.getElementById('searchInput');
    const sectionSelect = document.getElementById('sectionSelect');
    const sortSelect = document.getElementById('sortSelect');
    const resultsCounter = document.getElementById('resultsCounter');
    const pillButtons = document.querySelectorAll('.pill-btn');
    const statusButtons = document.querySelectorAll('.status-tab');

    function getLanguageBadgeClass(lang) {{
      const l = (lang || '').toLowerCase();
      if (l.includes('greek')) return 'badge-greek';
      if (l.includes('syriac')) return 'badge-syriac';
      if (l.includes('latin')) return 'badge-latin';
      if (l.includes('ethiopic')) return 'badge-ethiopic';
      if (l.includes('aramaic')) return 'badge-aramaic';
      if (l.includes('hebrew')) return 'badge-aramaic';
      if (l.includes('armenian') || l.includes('georgian') || l.includes('coptic') || l.includes('slavonic')) return 'badge-neutral';
      return 'badge-neutral';
    }}

    function renderDocs() {{
      let filtered = DOCS_DATA.filter(doc => {{
        // Status filter
        if (currentStatus === 'live' && doc.status !== 'live') return false;
        if (currentStatus === 'gap' && doc.status === 'live') return false;

        // Language filter
        if (currentFilterLang !== 'all') {{
          if (doc.lang !== currentFilterLang && !doc.mss_langs.includes(currentFilterLang)) {{
            return false;
          }}
        }}

        // Section filter
        if (currentSection !== 'all') {{
          if (!doc.section.toLowerCase().includes(currentSection.toLowerCase())) {{
            return false;
          }}
        }}

        // Search query
        if (currentSearch.trim()) {{
          const q = currentSearch.toLowerCase().trim();
          const matchTitle = doc.title.toLowerCase().includes(q);
          const matchId = doc.id.toLowerCase().includes(q);
          const matchCavt = (doc.cavt ? 'cavt ' + doc.cavt : '').toLowerCase().includes(q);
          const matchFile = (doc.filename || '').toLowerCase().includes(q);
          const matchLang = (doc.lang || '').toLowerCase().includes(q);
          const matchSection = (doc.section || '').toLowerCase().includes(q);
          const matchOtp = (doc.concordance.otp || '').toLowerCase().includes(q);
          const matchApot = (doc.concordance.apot || '').toLowerCase().includes(q);
          const matchDenis = (doc.concordance.denis || '').toLowerCase().includes(q);
          const matchDiTommaso = (doc.concordance.ditommaso || '').toLowerCase().includes(q);

          if (!matchTitle && !matchId && !matchCavt && !matchFile && !matchLang &&
              !matchSection && !matchOtp && !matchApot && !matchDenis && !matchDiTommaso) {{
            return false;
          }}
        }}
        return true;
      }});

      // Sorting
      filtered.sort((a, b) => {{
        if (currentSort === 'canon-asc') return a.id.localeCompare(b.id, undefined, {{ numeric: true }});
        if (currentSort === 'title-asc') return a.title.localeCompare(b.title);
        if (currentSort === 'title-desc') return b.title.localeCompare(a.title);
        if (currentSort === 'lang') return a.lang.localeCompare(b.lang);
        if (currentSort === 'status') {{
          if (a.status === 'live' && b.status !== 'live') return -1;
          if (a.status !== 'live' && b.status === 'live') return 1;
          return a.id.localeCompare(b.id, undefined, {{ numeric: true }});
        }}
        return 0;
      }});

      resultsCounter.textContent = `Showing ${{filtered.length}} of ${{DOCS_DATA.length}} canonical texts`;

      if (filtered.length === 0) {{
        docsGrid.innerHTML = `
          <div class="empty-state">
            <h4>No texts found matching your filter</h4>
            <p>Try adjusting your search terms, changing the status tab, or clearing the language filter.</p>
          </div>
        `;
        return;
      }}

      docsGrid.innerHTML = filtered.map(doc => {{
        const isLive = (doc.status === 'live');
        const isStaged = (doc.status === 'staged');
        const langBadgeClass = getLanguageBadgeClass(doc.lang);

        const statusBadge = isLive
          ? `<span class="badge badge-live">&bull; Live Edition</span>`
          : isStaged
            ? `<span class="badge badge-staged">&bull; In Progress</span>`
            : `<span class="badge badge-gap">Clavis Record</span>`;

        // Crosswalk chip list
        let chips = [];
        if (doc.cavt) chips.push(`<span class="crosswalk-chip" title="Haelewyck CAVT">CAVT ${{doc.cavt}}</span>`);
        if (doc.cant) chips.push(`<span class="crosswalk-chip" title="Clavis CANT">${{doc.cant}}</span>`);
        if (doc.concordance.otp) chips.push(`<span class="crosswalk-chip" title="Charlesworth OTP">${{doc.concordance.otp.split(' ')[0]}}</span>`);
        if (doc.concordance.apot) chips.push(`<span class="crosswalk-chip" title="Charles APOT">${{doc.concordance.apot.split(' ')[0]}}</span>`);
        if (doc.concordance.aot) chips.push(`<span class="crosswalk-chip" title="Sparks AOT">${{doc.concordance.aot.split(' ')[0]}}</span>`);

        const actionButtons = isLive ? `
          <div class="doc-actions">
            <a href="reader.html?doc=${{doc.filename}}" class="btn-action btn-primary" title="Open in Parallel Digital Reader">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
              Read Text
            </a>
            <button onclick="openDocModal('${{doc.id}}')" class="btn-action btn-secondary" title="View text introduction and critical dossier">
              Dossier
            </button>
            <a href="static/docs/${{doc.filename}}" target="_blank" class="btn-action btn-outline" title="Open raw TEI XML">
              XML
            </a>
          </div>
        ` : `
          <div class="doc-actions">
            <button onclick="openDocModal('${{doc.id}}')" class="btn-action btn-secondary" style="flex:1;" title="View text overview, manuscripts, and 6-way crosswalk">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              Dossier &amp; Concordance
            </button>
          </div>
        `;

        return `
          <div class="doc-card" data-id="${{doc.id}}">
            <div class="doc-header">
              <div class="doc-badges">
                ${{statusBadge}}
                <span class="badge ${{langBadgeClass}}">${{doc.lang}}</span>
                <span class="badge badge-neutral">${{doc.id}}</span>
              </div>
              <h4 class="doc-title">${{doc.title}}</h4>
              <div class="doc-meta">
                <div class="doc-meta-row">
                  <strong>Section:</strong>
                  <span>${{doc.section}}</span>
                </div>
                ${{isLive ? `
                  <div class="doc-meta-row">
                    <strong>Witnesses:</strong>
                    <span>${{doc.mss_count > 0 ? doc.mss_count + ' witness' + (doc.mss_count > 1 ? 'es' : '') : 'Eclectic critical text'}}</span>
                  </div>
                  <div class="doc-meta-row">
                    <strong>File:</strong>
                    <span class="doc-filename">${{doc.filename}}</span>
                  </div>
                ` : `
                  <div class="doc-meta-row">
                    <strong>Status:</strong>
                    <span>Documented in CAVT / Denis / DiTommaso</span>
                  </div>
                `}}
              </div>
              <div class="concordance-box">
                <div class="concordance-row">
                  <strong style="font-size:0.75rem;">Concordance:</strong>
                  ${{chips.join(' ') || '<span style="color:var(--text-muted);">Clavis reference</span>'}}
                </div>
              </div>
            </div>
            ${{actionButtons}}
          </div>
        `;
      }}).join('');
    }}

    // Filter Listeners
    statusButtons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        statusButtons.forEach(b => {{
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        }});
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
        currentStatus = btn.getAttribute('data-status');
        renderDocs();
      }});
    }});

    searchInput.addEventListener('input', (e) => {{
      currentSearch = e.target.value;
      renderDocs();
    }});

    sectionSelect.addEventListener('change', (e) => {{
      currentSection = e.target.value;
      renderDocs();
    }});

    sortSelect.addEventListener('change', (e) => {{
      currentSort = e.target.value;
      renderDocs();
    }});

    pillButtons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        pillButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilterLang = btn.getAttribute('data-lang');
        renderDocs();
      }});
    }});

    // Modal & Tabs Logic
    const previewModal = document.getElementById('previewModal');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const modalDocTitle = document.getElementById('modalDocTitle');
    const modalDocMeta = document.getElementById('modalDocMeta');
    const modalDocBadges = document.getElementById('modalDocBadges');
    const modalFilename = document.getElementById('modalFilename');
    const modalReadBtn = document.getElementById('modalReadBtn');
    const modalRawBtn = document.getElementById('modalRawBtn');
    const modalDownloadBtn = document.getElementById('modalDownloadBtn');
    const modalTabXml = document.getElementById('modalTabXml');

    function switchModalTab(tab) {{
      document.querySelectorAll('.modal-tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('tabContentDossier').style.display = 'none';
      document.getElementById('tabContentConcordance').style.display = 'none';
      document.getElementById('tabContentXml').style.display = 'none';

      if (tab === 'dossier') {{
        document.getElementById('modalTabDossier').classList.add('active');
        document.getElementById('tabContentDossier').style.display = 'flex';
      }} else if (tab === 'concordance') {{
        document.getElementById('modalTabConcordance').classList.add('active');
        document.getElementById('tabContentConcordance').style.display = 'flex';
      }} else if (tab === 'xml') {{
        document.getElementById('modalTabXml').classList.add('active');
        document.getElementById('tabContentXml').style.display = 'flex';
        loadModalXml();
      }}
    }}

    function loadModalXml() {{
      const codeEl = document.getElementById('modalXmlContent');
      if (!activeModalItem || !activeModalItem.filename) {{
        codeEl.textContent = 'No TEI XML file yet available for this clavis entry.';
        return;
      }}
      codeEl.textContent = 'Fetching TEI XML source...';
      fetch('static/docs/' + activeModalItem.filename)
        .then(res => {{
          if (!res.ok) throw new Error('Network error');
          return res.text();
        }})
        .then(text => {{
          const lines = text.split('\\n').slice(0, 70).join('\\n');
          codeEl.textContent = lines + (text.split('\\n').length > 70 ? '\\n\\n<!-- ... [Remaining document content truncated for preview] ... -->' : '');
        }})
        .catch(err => {{
          codeEl.textContent = 'Preview unavailable via local file protocol. Click "Read in Reader" or "Open Full XML" below.';
        }});
    }}

    function openDocModal(docId) {{
      const doc = DOCS_DATA.find(d => d.id === docId);
      if (!doc) return;
      activeModalItem = doc;

      modalDocTitle.textContent = doc.title;
      modalDocMeta.textContent = `ID: ${{doc.id}} | Section: ${{doc.section}} | Language: ${{doc.lang}}`;

      const isLive = (doc.status === 'live');
      modalDocBadges.innerHTML = `
        <span class="badge ${{isLive ? 'badge-live' : 'badge-gap'}}">${{isLive ? 'Live Edition' : 'Clavis Record'}}</span>
        <span class="badge ${{getLanguageBadgeClass(doc.lang)}}">${{doc.lang}}</span>
        ${{doc.cavt ? `<span class="badge badge-neutral">CAVT ${{doc.cavt}}</span>` : ''}}
      `;

      // Set Concordance values
      document.getElementById('modalConfCavt').textContent = doc.cavt ? `CAVT ${{doc.cavt}}` : 'Excluded from CAVT remit';
      document.getElementById('modalConfCant').textContent = doc.cant || '—';
      document.getElementById('modalConfDenis').textContent = doc.concordance.denis || '—';
      document.getElementById('modalConfDiTommaso').textContent = doc.concordance.ditommaso || '—';
      document.getElementById('modalConfOtp').textContent = doc.concordance.otp || '—';
      document.getElementById('modalConfApot').textContent = doc.concordance.apot || '—';
      document.getElementById('modalConfAot').textContent = doc.concordance.aot || '—';

      // Set Dossier content
      const introEl = document.getElementById('modalIntroContent');
      if (doc.details && doc.details.intro) {{
        introEl.innerHTML = doc.details.intro;
      }} else {{
        introEl.innerHTML = `<p>This document is indexed in the canonical master concordance (<strong>${{doc.id}}</strong>). It is referenced in Haelewyck's <em>Clavis Apocryphorum Veteris Testamenti</em>, Denis' <em>Introduction</em>, and DiTommaso's <em>Bibliography</em>.</p>`;
      }}

      // Provenance, Manuscripts & Bibliography
      const provSec = document.getElementById('modalProvenanceSection');
      const provEl = document.getElementById('modalProvenanceContent');
      if (doc.details && doc.details.provenance) {{
        provSec.style.display = 'block';
        provEl.innerHTML = doc.details.provenance;
      }} else {{
        provSec.style.display = 'none';
      }}

      const mssSec = document.getElementById('modalMssSection');
      const mssEl = document.getElementById('modalMssContent');
      if (doc.details && doc.details.manuscripts) {{
        mssSec.style.display = 'block';
        mssEl.innerHTML = doc.details.manuscripts;
      }} else {{
        mssSec.style.display = 'none';
      }}

      const biblioSec = document.getElementById('modalBiblioSection');
      const biblioEl = document.getElementById('modalBiblioContent');
      if (doc.details && doc.details.bibliography) {{
        biblioSec.style.display = 'block';
        biblioEl.innerHTML = doc.details.bibliography;
      }} else {{
        biblioSec.style.display = 'none';
      }}

      // Footer action buttons
      if (isLive) {{
        modalFilename.textContent = doc.filename;
        modalReadBtn.style.display = 'inline-flex';
        modalReadBtn.href = 'reader.html?doc=' + doc.filename;
        modalRawBtn.style.display = 'inline-flex';
        modalRawBtn.href = 'static/docs/' + doc.filename;
        modalDownloadBtn.style.display = 'inline-flex';
        modalDownloadBtn.href = 'static/docs/' + doc.filename;
        modalDownloadBtn.setAttribute('download', doc.filename);
        modalTabXml.style.display = 'inline-block';
      }} else {{
        modalFilename.textContent = 'Clavis authority entry (' + doc.id + ')';
        modalReadBtn.style.display = 'none';
        modalRawBtn.style.display = 'none';
        modalDownloadBtn.style.display = 'none';
        modalTabXml.style.display = 'none';
      }}

      switchModalTab('dossier');
      previewModal.classList.add('open');
    }}

    // Backwards-compat
    window.openPreview = function(filename) {{
      const doc = DOCS_DATA.find(d => d.filename === filename);
      if (doc) openDocModal(doc.id);
    }};

    modalCloseBtn.addEventListener('click', () => {{
      previewModal.classList.remove('open');
    }});

    previewModal.addEventListener('click', (e) => {{
      if (e.target === previewModal) previewModal.classList.remove('open');
    }});

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape' && previewModal.classList.contains('open')) {{
        previewModal.classList.remove('open');
      }}
    }});

    // Initial render
    renderDocs();
"""

html = html[:script_start_idx] + new_script + html[script_end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully updated index.html with bibliography modal section and HTML rendering.")
