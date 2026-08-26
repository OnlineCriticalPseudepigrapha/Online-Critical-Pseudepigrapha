/**
 * OCP Digital Critical Edition Reader Controller
 * Manages multi-pane parallel alignment, synchronized navigation, unit selection, and critical apparatus.
 */

const OCP_DOCUMENTS = [
  { filename: '1En.xml', title: '1 Enoch', lang: 'Ethiopic' },
  { filename: '2Bar.xml', title: '2 (Syriac Apocalypse of) Baruch', lang: 'Syriac' },
  { filename: '2Bar-Syr.xml', title: '2 Baruch (Syriac Text)', lang: 'Syriac' },
  { filename: '3Bar.xml', title: '3 (Greek Apocalypse of) Baruch', lang: 'Greek' },
  { filename: '4Bar.xml', title: '4 Baruch (Paraleipomena Ieremiou)', lang: 'Greek' },
  { filename: '4Ezra.xml', title: '4 Ezra (Syriac)', lang: 'Syriac' },
  { filename: '4Macc.xml', title: '4 Maccabees', lang: 'Greek' },
  { filename: '4Q548.xml', title: '4Q548 (Dead Sea Scrolls)', lang: 'Aramaic' },
  { filename: 'AdamEve.xml', title: 'Life of Adam and Eve', lang: 'Greek' },
  { filename: 'Amram.xml', title: 'Visions of Amram', lang: 'Aramaic' },
  { filename: 'ApocrEzek.xml', title: 'Apocryphon of Ezekiel', lang: 'Greek' },
  { filename: 'ArisEx.xml', title: 'Aristeas the Exegete', lang: 'Greek' },
  { filename: 'Aristob.xml', title: 'Aristobulus', lang: 'Greek' },
  { filename: 'Artap.xml', title: 'Artapanus', lang: 'Greek' },
  { filename: 'ClMal.xml', title: 'Cleodemus Malchus', lang: 'Greek' },
  { filename: 'ElMod.xml', title: 'Eldad and Modad', lang: 'Greek' },
  { filename: 'Esdl.xml', title: 'Vision of Ezra (Latin)', lang: 'Latin' },
  { filename: 'Esdr.xml', title: '4 Ezra (Latin)', lang: 'Latin' },
  { filename: 'Eup.xml', title: 'Eupolemus', lang: 'Greek' },
  { filename: 'EzekTrag.xml', title: 'Ezekiel the Tragedian', lang: 'Greek' },
  { filename: 'HistRech.xml', title: 'History of the Rechabites', lang: 'Greek' },
  { filename: 'JosAsen.xml', title: 'Joseph and Aseneth', lang: 'Greek' },
  { filename: 'Jub.xml', title: 'Jubilees (Greek & Latin Fragments)', lang: 'Greek' },
  { filename: 'Jubi.xml', title: 'Jubilees (Latin Version)', lang: 'Latin' },
  { filename: 'LetAris.xml', title: 'Letter of Aristeas to Philocrates', lang: 'Greek' },
  { filename: 'LivPro.xml', title: 'Lives of the Prophets', lang: 'Greek' },
  { filename: 'Mois.xml', title: 'Assumption of Moses', lang: 'Latin' },
  { filename: 'PhEPoet.xml', title: 'Philo the Epic Poet', lang: 'Greek' },
  { filename: 'Ps-Eup.xml', title: 'Pseudo-Eupolemus', lang: 'Greek' },
  { filename: 'PssSol.xml', title: 'Psalms of Solomon', lang: 'Greek' },
  { filename: 'SibOr.xml', title: 'Sibylline Oracles', lang: 'Greek' },
  { filename: 'TAbA.xml', title: 'Testament of Abraham (Recension A)', lang: 'Greek' },
  { filename: 'TAbB.xml', title: 'Testament of Abraham (Recension B)', lang: 'Greek' },
  { filename: 'TAbr.xml', title: 'Testament of Abraham (Combined)', lang: 'Greek' },
  { filename: 'TAdam.xml', title: 'Testament of Adam', lang: 'Syriac' },
  { filename: 'TJob.xml', title: 'Testament of Job', lang: 'Greek' },
  { filename: 'TSol.xml', title: 'Testament of Solomon', lang: 'Greek' },
  { filename: 'Theod.xml', title: 'Theodotus', lang: 'Greek' }
];

// Display labels for the database body fields exported to
// static/docs/intros.json (mirrors DISPLAY_FIELDS in controllers/docs.py)
const INTRO_FIELD_TITLES = {
  introduction: 'Introduction',
  provenance: 'Provenance and Cultural Setting',
  themes: 'Major Themes',
  status: 'Current State of the OCP Text',
  manuscripts: 'Manuscripts',
  bibliography: 'Bibliography',
  corrections: 'Corrections',
  sigla: 'Sigla Used in the Text',
  copyright: 'Copyright Information'
};

class OcpReaderApp {
  constructor() {
    this.activeDoc = 'TJob.xml';
    this.book = null;
    this.panes = [];
    this.nextPaneId = 1;
    this.currentFromRef = null;
    this.currentToRef = null;
    this.activePassage = null;
    this.currentFontSize = 18;

    this.initElements();
    this.initEvents();
    this.loadInitialState();
  }

  initElements() {
    this.docSelect = document.getElementById('docSelect');
    this.addPaneBtn = document.getElementById('addPaneBtn');
    this.themeToggle = document.getElementById('themeToggle');
    this.zoomInBtn = document.getElementById('zoomInBtn');
    this.zoomOutBtn = document.getElementById('zoomOutBtn');
    this.infoDrawerBtn = document.getElementById('infoDrawerBtn');
    this.closeDrawerBtn = document.getElementById('closeDrawerBtn');
    this.infoDrawerBackdrop = document.getElementById('infoDrawerBackdrop');
    
    this.fromRefSelect = document.getElementById('fromRefSelect');
    this.toRefSelect = document.getElementById('toRefSelect');
    this.prevBtn = document.getElementById('prevBtn');
    this.nextBtn = document.getElementById('nextBtn');
    this.activeRangeBadge = document.getElementById('activeRangeBadge');
    this.panesContainer = document.getElementById('panesContainer');
    this.msPopover = document.getElementById('msPopover');

    // Populate Document Switcher
    this.docSelect.innerHTML = OCP_DOCUMENTS.map(d => {
      return `<option value="${d.filename}">${d.title} (${d.lang})</option>`;
    }).join('');
  }

  initEvents() {
    // Document Switcher
    this.docSelect.addEventListener('change', (e) => {
      this.loadDocument(e.target.value);
    });

    // Add Parallel Pane
    this.addPaneBtn.addEventListener('click', () => {
      this.addPane();
    });

    // Navigation Steppers
    this.prevBtn.addEventListener('click', () => this.navigateStep('prev'));
    this.nextBtn.addEventListener('click', () => this.navigateStep('next'));

    // Range Selectors
    this.fromRefSelect.addEventListener('change', (e) => {
      this.currentFromRef = e.target.value;
      this.refreshAllPanes();
    });
    this.toRefSelect.addEventListener('change', (e) => {
      this.currentToRef = e.target.value;
      this.refreshAllPanes();
    });

    // Text Zoom
    this.zoomInBtn.addEventListener('click', () => {
      this.currentFontSize = Math.min(32, this.currentFontSize + 1);
      this.updateFontSize();
    });
    this.zoomOutBtn.addEventListener('click', () => {
      this.currentFontSize = Math.max(12, this.currentFontSize - 1);
      this.updateFontSize();
    });

    // Info Drawer
    this.infoDrawerBtn.addEventListener('click', () => this.openInfoDrawer());
    this.closeDrawerBtn.addEventListener('click', () => this.closeInfoDrawer());
    this.infoDrawerBackdrop.addEventListener('click', (e) => {
      if (e.target === this.infoDrawerBackdrop) this.closeInfoDrawer();
    });

    // Theme Toggle
    this.themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const target = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', target);
      localStorage.setItem('ocp-theme', target);
    });

    // Close MS Popover on click outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.ms-chip') && !e.target.closest('.ms-popover')) {
        this.msPopover.classList.remove('open');
      }
    });

    // Handle Browser PopState (Back/Forward)
    window.addEventListener('popstate', () => {
      this.loadInitialState();
    });
  }

  loadInitialState() {
    const urlParams = new URLSearchParams(window.location.search);
    let doc = urlParams.get('doc') || 'TJob.xml';
    if (!doc.endsWith('.xml')) doc += '.xml';

    const match = OCP_DOCUMENTS.find(d => d.filename.toLowerCase() === doc.toLowerCase());
    if (match) {
      this.activeDoc = match.filename;
    } else {
      this.activeDoc = 'TJob.xml';
    }

    this.docSelect.value = this.activeDoc;
    this.loadDocument(this.activeDoc, urlParams.get('ref'));
  }

  async loadDocument(filename, targetRef = null) {
    this.activeDoc = filename;
    this.docSelect.value = filename;
    this.panesContainer.innerHTML = '<div style="padding:40px; text-align:center; width:100%; color:var(--text-muted);">Loading electronic critical edition...</div>';

    try {
      const res = await fetch(`static/docs/${filename}`);
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      const xmlText = await res.text();

      this.book = OcpTeiParser.parseBook(xmlText);

      // Populate navigation dropdowns
      const firstVersion = this.book.versions[0];
      const refs = (firstVersion && firstVersion.references) || [];

      this.fromRefSelect.innerHTML = refs.map(r => `<option value="${r}">${r}</option>`).join('');
      this.toRefSelect.innerHTML = refs.map(r => `<option value="${r}">${r}</option>`).join('');

      if (refs.length > 0) {
        if (targetRef && refs.includes(targetRef)) {
          this.currentFromRef = targetRef;
          this.currentToRef = targetRef;
        } else {
          this.currentFromRef = refs[0];
          this.currentToRef = refs[Math.min(refs.length - 1, 4)];
        }
        this.fromRefSelect.value = this.currentFromRef;
        this.toRefSelect.value = this.currentToRef;
      }

      // Initialize Panes
      this.panes = [];
      this.nextPaneId = 1;

      // Add primary pane
      this.panes.push({
        id: this.nextPaneId++,
        versionIdx: 0,
        selectedMs: '__eclectic__',
        activeUnitId: null
      });

      // If document has multiple language versions (e.g. TAbr, Jub, TAdam), automatically add second pane for comparison
      if (this.book.versions.length > 1) {
        this.panes.push({
          id: this.nextPaneId++,
          versionIdx: 1,
          selectedMs: '__eclectic__',
          activeUnitId: null
        });
      }

      this.refreshAllPanes();
      this.updateUrlState();
      this.populateInfoDrawer();

    } catch (err) {
      console.error('Error loading document:', err);
      this.panesContainer.innerHTML = `
        <div style="padding:40px; text-align:center; width:100%; color:#ef4444;">
          <h3>Failed to load document (${filename})</h3>
          <p>${err.message}</p>
        </div>
      `;
    }
  }

  addPane(versionIdx = 0) {
    if (!this.book) return;
    const vIdx = Math.min(versionIdx, this.book.versions.length - 1);
    this.panes.push({
      id: this.nextPaneId++,
      versionIdx: vIdx,
      selectedMs: '__eclectic__',
      activeUnitId: null
    });
    this.refreshAllPanes();
  }

  removePane(paneId) {
    if (this.panes.length <= 1) return; // Keep at least one pane open
    this.panes = this.panes.filter(p => p.id !== paneId);
    this.refreshAllPanes();
  }

  navigateStep(direction) {
    if (!this.activePassage) return;
    if (direction === 'prev' && this.activePassage.hasPrev) {
      const step = (this.activePassage.endIndex - this.activePassage.startIndex + 1);
      const newStart = Math.max(0, this.activePassage.startIndex - step);
      const refs = this.book.versions[0].references;
      this.currentFromRef = refs[newStart];
      this.currentToRef = refs[newStart + step - 1] || refs[refs.length - 1];
    } else if (direction === 'next' && this.activePassage.hasNext) {
      const step = (this.activePassage.endIndex - this.activePassage.startIndex + 1);
      const newStart = this.activePassage.endIndex + 1;
      const refs = this.book.versions[0].references;
      this.currentFromRef = refs[newStart];
      this.currentToRef = refs[Math.min(refs.length - 1, newStart + step - 1)];
    }

    this.fromRefSelect.value = this.currentFromRef;
    this.toRefSelect.value = this.currentToRef;
    this.refreshAllPanes();
  }

  refreshAllPanes() {
    if (!this.book) return;

    this.panesContainer.innerHTML = '';
    const firstVersionIdx = this.panes[0] ? this.panes[0].versionIdx : 0;
    this.activePassage = this.book.getPassage(firstVersionIdx, this.currentFromRef, this.currentToRef, '__eclectic__');

    this.activeRangeBadge.textContent = `${this.book.title} ${this.activePassage.refRange}`;
    this.prevBtn.disabled = !this.activePassage.hasPrev;
    this.nextBtn.disabled = !this.activePassage.hasNext;

    this.panes.forEach(pane => {
      const paneElem = this.createPaneElement(pane);
      this.panesContainer.appendChild(paneElem);
      this.renderPaneContent(pane, paneElem);
    });

    this.updateFontSize();
    this.updateUrlState();
  }

  createPaneElement(pane) {
    const version = this.book.versions[pane.versionIdx] || this.book.versions[0];
    const paneDiv = document.createElement('div');
    paneDiv.className = 'version-pane';
    paneDiv.id = `pane_${pane.id}`;

    const versionOptions = this.book.versions.map((v, idx) => {
      return `<option value="${idx}" ${idx === pane.versionIdx ? 'selected' : ''}>${v.title || 'Version ' + (idx + 1)} (${v.language || 'Original'})</option>`;
    }).join('');

    const availableMss = version.manuscripts || [];
    let msOptions = `<option value="__eclectic__">Base Text (Eclectic / Opt 0)</option>`;
    availableMss.forEach(m => {
      msOptions += `<option value="${m.abbrev}" ${pane.selectedMs === m.abbrev ? 'selected' : ''}>${m.abbrev} (${m.name || m.abbrev})</option>`;
    });

    paneDiv.innerHTML = `
      <div class="pane-header">
        <div class="pane-selectors">
          <select class="pane-select version-select" title="Switch Language Version">${versionOptions}</select>
          <select class="pane-select ms-select" title="Switch Base Manuscript">${msOptions}</select>
        </div>
        ${this.panes.length > 1 ? `<button class="pane-close-btn" title="Close column">&times;</button>` : ''}
      </div>
      <div class="pane-text-frame ${this.getScriptClass(version.language)}"></div>
      <div class="pane-apparatus-frame">
        <div class="apparatus-header">
          <span class="apparatus-title">Critical Apparatus</span>
          <span class="apparatus-unit-badge">Click any text unit</span>
        </div>
        <div class="apparatus-content">
          <p style="color:var(--text-muted); font-style:italic;">Select a word or unit above to inspect manuscript variants and readings.</p>
        </div>
      </div>
    `;

    // Pane Events
    const vSelect = paneDiv.querySelector('.version-select');
    vSelect.addEventListener('change', (e) => {
      pane.versionIdx = parseInt(e.target.value, 10);
      pane.selectedMs = '__eclectic__';
      this.refreshAllPanes();
    });

    const mSelect = paneDiv.querySelector('.ms-select');
    mSelect.addEventListener('change', (e) => {
      pane.selectedMs = e.target.value;
      this.renderPaneContent(pane, paneDiv);
    });

    const closeBtn = paneDiv.querySelector('.pane-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        this.removePane(pane.id);
      });
    }

    return paneDiv;
  }

  getScriptClass(language) {
    const l = (language || '').toLowerCase();
    if (l.includes('greek')) return 'script-greek';
    if (l.includes('syriac')) return 'script-syriac';
    if (l.includes('ethiopic')) return 'script-ethiopic';
    if (l.includes('latin')) return 'script-latin';
    if (l.includes('aramaic') || l.includes('hebrew')) return 'script-aramaic';
    return 'script-greek';
  }

  renderPaneContent(pane, paneElem) {
    const textFrame = paneElem.querySelector('.pane-text-frame');
    const apparatusContent = paneElem.querySelector('.apparatus-content');
    const apparatusUnitBadge = paneElem.querySelector('.apparatus-unit-badge');

    const passage = this.book.getPassage(pane.versionIdx, this.currentFromRef, this.currentToRef, pane.selectedMs);

    let html = '';
    let firstUnitWithVariants = null;

    passage.sections.forEach(sec => {
      html += `<div class="section-ref-heading">${sec.ref}</div> `;
      sec.units.forEach(u => {
        if (!firstUnitWithVariants && u.hasVariants) {
          firstUnitWithVariants = u.id;
        }
        const isActive = pane.activeUnitId === u.id;
        const classes = [
          'ocp-unit',
          u.hasVariants ? 'has-variants' : '',
          isActive ? 'active' : '',
          u.isOmitted ? 'is-omitted' : ''
        ].filter(Boolean).join(' ');

        const displayText = u.isOmitted ? '[omitted]' : u.readingText;
        html += `<span class="${classes}" data-unit="${u.id}" data-ref="${u.ref}">${displayText}</span> `;
        if (u.linebreak) html += `<br/>`;
      });
      html += `<br/>`;
    });

    textFrame.innerHTML = html;

    // Attach click events on units
    textFrame.querySelectorAll('.ocp-unit').forEach(unitSpan => {
      unitSpan.addEventListener('click', () => {
        const uId = unitSpan.getAttribute('data-unit');
        pane.activeUnitId = uId;
        textFrame.querySelectorAll('.ocp-unit').forEach(s => s.classList.remove('active'));
        unitSpan.classList.add('active');
        this.renderPaneApparatus(pane, paneElem, uId);
      });
    });

    // Default active unit
    const activeId = pane.activeUnitId || firstUnitWithVariants;
    if (activeId) {
      pane.activeUnitId = activeId;
      const targetSpan = textFrame.querySelector(`[data-unit="${activeId}"]`);
      if (targetSpan) targetSpan.classList.add('active');
      this.renderPaneApparatus(pane, paneElem, activeId);
    }
  }

  renderPaneApparatus(pane, paneElem, unitId) {
    const apparatusContent = paneElem.querySelector('.apparatus-content');
    const apparatusUnitBadge = paneElem.querySelector('.apparatus-unit-badge');
    const version = this.book.versions[pane.versionIdx];

    const appData = this.book.getApparatus(pane.versionIdx, unitId);
    if (!appData) return;

    apparatusUnitBadge.textContent = `Ref: ${appData.ref} (Unit ${appData.unitId})`;

    let tableHtml = `
      <table class="apparatus-table">
        <thead>
          <tr>
            <th class="col-mss">Witnesses</th>
            <th>Reading</th>
          </tr>
        </thead>
        <tbody>
    `;

    appData.readings.forEach(r => {
      const mssChips = r.mss.map(m => `<span class="ms-chip" data-ms="${m}">${m}</span>`).join(' ');
      const isBaseOption = r.option === '0' || r.option === 0;
      const readingText = r.isOmission ? '<span style="color:var(--text-muted); font-style:italic;">[omitted]</span>' : r.text;

      tableHtml += `
        <tr>
          <td class="col-mss">
            ${mssChips || '<span style="color:var(--text-muted); font-style:italic;">(all other mss)</span>'}
            ${isBaseOption ? ' <small style="color:var(--accent-gold-dark); font-weight:700;">[Base]</small>' : ''}
          </td>
          <td class="reading-text-cell ${this.getScriptClass(version.language)}">
            ${readingText}
          </td>
        </tr>
      `;
    });

    tableHtml += `</tbody></table>`;

    if (appData.omittedMss && appData.omittedMss.length > 0) {
      const omittedChips = appData.omittedMss.map(m => `<span class="ms-chip" data-ms="${m}">${m}</span>`).join(' ');
      tableHtml += `
        <div class="omission-notice">
          <strong>Not attested in:</strong> ${omittedChips}
        </div>
      `;
    }

    apparatusContent.innerHTML = tableHtml;

    // Attach MS Chip Click / Tooltip
    apparatusContent.querySelectorAll('.ms-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        const msAbbrev = chip.getAttribute('data-ms');
        const meta = appData.manuscriptMeta[msAbbrev] || this.book.getManuscriptMetadata(msAbbrev);
        this.showMsPopover(chip, meta);
        e.stopPropagation();
      });
    });
  }

  showMsPopover(targetElem, meta) {
    if (!meta) return;

    this.msPopover.innerHTML = `
      <h5>${meta.name || meta.abbrev} (${meta.abbrev})</h5>
      <div class="ms-popover-meta">Language: ${meta.language || 'N/A'} | Status: ${meta.show === 'no' ? 'Apparatus only' : 'Full witness'}</div>
      ${meta.bibliography ? `<div class="ms-popover-bib"><strong>Bibliography:</strong> ${meta.bibliography}</div>` : ''}
    `;

    const rect = targetElem.getBoundingClientRect();
    this.msPopover.style.top = `${rect.bottom + window.scrollY + 6}px`;
    this.msPopover.style.left = `${Math.min(window.innerWidth - 340, rect.left + window.scrollX)}px`;
    this.msPopover.classList.add('open');
  }

  updateFontSize() {
    document.querySelectorAll('.pane-text-frame').forEach(f => {
      f.style.fontSize = `${this.currentFontSize}px`;
    });
  }

  updateUrlState() {
    const url = new URL(window.location);
    url.searchParams.set('doc', this.activeDoc);
    if (this.currentFromRef) url.searchParams.set('ref', `${this.currentFromRef}-${this.currentToRef}`);
    window.history.replaceState({}, '', url);
  }

  openInfoDrawer() {
    this.infoDrawerBackdrop.classList.add('open');
  }

  closeInfoDrawer() {
    this.infoDrawerBackdrop.classList.remove('open');
  }

  // Fetch the document introductions exported from the SQLite db
  // (scripts/export_intros.py -> static/docs/intros.json). Fetched at most
  // once per page load; results are shared across documents.
  async loadIntros() {
    if (!this.introsPromise) {
      this.introsPromise = fetch('static/docs/intros.json')
        .then(res => res.ok ? res.json() : Promise.reject(new Error(`HTTP ${res.status}`)))
        .catch(err => {
          console.warn('Could not load document introductions:', err);
          this.introsPromise = null; // allow retry on next drawer open
          return null;
        });
    }
    return this.introsPromise;
  }

  async populateInfoDrawer() {
    if (!this.book) return;
    const drawerTitle = document.getElementById('drawerDocTitle');
    const drawerBody = document.getElementById('drawerDocBody');

    // Render everything except the intro immediately, then stream the
    // introduction/body fields in when the JSON arrives.
    drawerTitle.textContent = this.book.title;

    let mssListHtml = '';
    const allMss = this.book.manuscripts || [];
    if (allMss.length > 0) {
      mssListHtml = `
        <div class="drawer-section">
          <h4>Manuscript Witnesses (${allMss.length})</h4>
          <ul style="padding-left:18px; font-size:0.9rem; color:var(--text-muted);">
            ${allMss.map(m => `<li><strong>${m.abbrev}</strong>: ${m.name || m.abbrev} ${m.bibliography ? ' &mdash; <em>' + m.bibliography + '</em>' : ''}</li>`).join('')}
          </ul>
        </div>
      `;
    }

    const drawerHtml = () => {
      const introSections = this.introSectionsHtml();
      return `${introSections}
      <div class="drawer-section">
        <h4>Document Information</h4>
        <p><strong>Title:</strong> ${this.book.title}</p>
        <p><strong>Filename:</strong> <code>${this.activeDoc}</code></p>
        <p><strong>Text Structure:</strong> ${this.book.textStructure}</p>
        <p><strong>Versions:</strong> ${this.book.versions.map(v => v.title + ' (' + v.language + ')').join(', ')}</p>
      </div>
      ${mssListHtml}
      <div class="drawer-section">
        <h4>How to Cite This Edition</h4>
        <div style="background:var(--bg-panel-secondary); padding:12px; border-radius:6px; font-family:var(--font-body); font-style:italic; font-size:0.95rem;">
          Ian W. Scott and Ken M. Penner, eds. <em>The Online Critical Pseudepigrapha: ${this.book.title}</em>. Atlanta: Society of Biblical Literature / Online: pseudepigrapha.org.
        </div>
      </div>
      <div class="drawer-section">
        <h4>TEI XML Source</h4>
        <a href="static/docs/${this.activeDoc}" target="_blank" class="btn-header btn-primary-header" style="display:inline-flex;">View Raw TEI XML</a>
      </div>`;
    };

    drawerBody.innerHTML = drawerHtml();

    const intros = await this.loadIntros();
    // Re-render only if the user hasn't switched documents while we waited.
    if (intros && intros.documents[this.activeDoc]) {
      this.introData = Object.assign({_docKey: this.activeDoc}, intros.documents[this.activeDoc]);
      drawerBody.innerHTML = drawerHtml();
    } else if (!intros) {
      this.introData = null;
      drawerBody.innerHTML = drawerHtml(); // leaves "not available" placeholder in place
    }
  }

  // Build the introduction / provenance / themes ... HTML from data exported
  // out of the database by scripts/export_intros.py.
  introSectionsHtml() {
    const entry = this.introData && this.activeDoc === this.introData._docKey
      ? this.introData
      : null;
    if (!entry) {
      return `
      <div class="drawer-section">
        <h4>Introduction</h4>
        <p style="color:var(--text-muted); font-size:0.9rem;">Introduction text is not yet available for offline reading.</p>
      </div>`;
    }
    const sections = Object.entries(entry.fields).map(([key, html]) => `
      <div class="drawer-section intro-body-field" id="intro-${key}">
        <h4>${INTRO_FIELD_TITLES[key] || key}</h4>
        <div class="intro-body-content">${html}</div>
      </div>`).join('');
    return sections;
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  window.ocpReader = new OcpReaderApp();
});
