/**
 * OCP TEI XML Parser (Online Critical Pseudepigrapha)
 * Zero-dependency client-side parser for OCP multi-witness XML documents.
 * 
 * Supports:
 * - Structural Neutrality (Base-Text Invariance)
 * - Multi-version parallel alignment (Greek, Syriac, Latin, Ethiopic, Aramaic)
 * - Dynamic witness transcription generation from variant apparatus
 * - Hierarchical and Fragmentary reference schemes
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.OcpTeiParser = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  class OcpBook {
    constructor(data) {
      this.title = data.title || '';
      this.filename = data.filename || '';
      this.textStructure = data.textStructure || 'hierarchical';
      this.language = data.language || '';
      this.manuscripts = data.manuscripts || [];
      this.versions = data.versions || [];
      this.rawXml = data.rawXml || '';
    }

    getManuscriptMetadata(abbrev) {
      const clean = (abbrev || '').trim();
      const match = this.manuscripts.find(m => m.abbrev === clean);
      if (match) return match;

      for (const v of this.versions) {
        const vMatch = v.manuscripts && v.manuscripts.find(m => m.abbrev === clean);
        if (vMatch) return vMatch;
      }
      return { abbrev: clean, name: clean, language: '', bibliography: '' };
    }

    getPassage(versionIdx = 0, fromRef = null, toRef = null, selectedMs = null) {
      const version = this.versions[versionIdx] || this.versions[0];
      if (!version) return { refRange: '', sections: [] };

      const allRefs = version.references || [];
      if (allRefs.length === 0) return { refRange: '', sections: [] };

      let startIndex = 0;
      let endIndex = allRefs.length - 1;

      if (fromRef) {
        const fIdx = allRefs.indexOf(fromRef);
        if (fIdx !== -1) startIndex = fIdx;
      }

      if (toRef) {
        const tIdx = allRefs.indexOf(toRef);
        if (tIdx !== -1) endIndex = tIdx;
      }

      if (startIndex > endIndex) {
        const temp = startIndex;
        startIndex = endIndex;
        endIndex = temp;
      }

      // Default chunk size if no range provided: first 5 reference units
      if (!fromRef && !toRef && allRefs.length > 5) {
        endIndex = Math.min(allRefs.length - 1, 4);
      }

      const activeRefs = allRefs.slice(startIndex, endIndex + 1);
      const sections = [];

      for (const ref of activeRefs) {
        const unitsInRef = (version.unitsByRef && version.unitsByRef[ref]) || [];
        const renderedUnits = [];

        for (const u of unitsInRef) {
          let chosenReading = null;

          if (selectedMs && selectedMs !== '__eclectic__' && selectedMs !== 'Default') {
            // Find reading supported by selected manuscript
            chosenReading = u.readings.find(r => r.mss && r.mss.includes(selectedMs));
          }

          if (!chosenReading) {
            // Default to option 0 or first available reading
            chosenReading = u.readings.find(r => r.option === '0' || r.option === 0) || u.readings[0];
          }

          const hasVariants = u.readings.length > 1;
          const isOmitted = !chosenReading || !chosenReading.text || chosenReading.text.trim() === '';

          const unitLinebreak = (chosenReading && chosenReading.linebreak) || (u.readings.find(r => r.linebreak) ? u.readings.find(r => r.linebreak).linebreak : false);
          const unitIndent = (chosenReading && chosenReading.indent) || (u.readings.find(r => r.indent) ? u.readings.find(r => r.indent).indent : false);

          renderedUnits.push({
            id: u.id,
            ref: u.ref,
            divPath: u.divPath,
            readingText: chosenReading ? chosenReading.text : '',
            chosenOption: chosenReading ? chosenReading.option : '0',
            chosenMss: chosenReading ? chosenReading.mss : [],
            linebreak: unitLinebreak,
            indent: unitIndent,
            hasVariants: hasVariants,
            isOmitted: isOmitted,
            allReadings: u.readings
          });
        }

        sections.push({
          ref: ref,
          units: renderedUnits
        });
      }

      return {
        refRange: `${activeRefs[0] || ''}${activeRefs.length > 1 ? '–' + activeRefs[activeRefs.length - 1] : ''}`,
        firstRef: activeRefs[0] || '',
        lastRef: activeRefs[activeRefs.length - 1] || '',
        startIndex: startIndex,
        endIndex: endIndex,
        totalRefsCount: allRefs.length,
        hasPrev: startIndex > 0,
        hasNext: endIndex < allRefs.length - 1,
        prevRef: startIndex > 0 ? allRefs[Math.max(0, startIndex - (endIndex - startIndex + 1))] : null,
        nextRef: endIndex < allRefs.length - 1 ? allRefs[endIndex + 1] : null,
        sections: sections
      };
    }

    getApparatus(versionIdx = 0, unitId) {
      const version = this.versions[versionIdx] || this.versions[0];
      if (!version) return null;

      const unit = version.unitsById && version.unitsById[unitId];
      if (!unit) return null;

      const manuscriptMeta = {};
      const allKnownMss = new Set();

      (version.manuscripts || this.manuscripts || []).forEach(m => {
        if (m.abbrev) {
          allKnownMss.add(m.abbrev);
          manuscriptMeta[m.abbrev] = m;
        }
      });

      const readings = unit.readings.map(r => {
        r.mss.forEach(ms => {
          if (!manuscriptMeta[ms]) {
            manuscriptMeta[ms] = this.getManuscriptMetadata(ms);
          }
        });

        return {
          option: r.option,
          mss: r.mss,
          text: r.text,
          words: r.words,
          linebreak: r.linebreak,
          indent: r.indent,
          isOmission: !r.text || r.text.trim() === ''
        };
      });

      // Find witnesses not accounted for in any explicit reading
      const attestedMss = new Set();
      readings.forEach(r => r.mss.forEach(m => attestedMss.add(m)));
      const omittedMss = Array.from(allKnownMss).filter(m => !attestedMss.has(m));

      return {
        unitId: unit.id,
        ref: unit.ref,
        versionTitle: version.title,
        versionLanguage: version.language,
        readings: readings,
        omittedMss: omittedMss,
        manuscriptMeta: manuscriptMeta
      };
    }
  }

  function parseXmlDoc(xmlString) {
    let doc;
    if (typeof DOMParser !== 'undefined') {
      const parser = new DOMParser();
      doc = parser.parseFromString(xmlString, 'text/xml');
    } else {
      // Node.js fallback using linkedom, jsdom, or xmldom
      try {
        const { DOMParser: LinkeDOMParser } = require('linkedom');
        doc = new LinkeDOMParser().parseFromString(xmlString, 'text/xml');
      } catch (e1) {
        try {
          const { JSDOM } = require('jsdom');
          doc = new JSDOM(xmlString, { contentType: 'text/xml' }).window.document;
        } catch (e2) {
          try {
            const { DOMParser: NodeDOMParser } = require('@xmldom/xmldom');
            doc = new NodeDOMParser().parseFromString(xmlString, 'text/xml');
          } catch (e3) {
            throw new Error('DOMParser is required to parse XML. In browser, DOMParser is built-in; in Node.js, install linkedom or jsdom.');
          }
        }
      }
    }

    const parserError = doc.querySelector('parsererror');
    if (parserError) {
      throw new Error('XML Parse Error: ' + parserError.textContent);
    }

    const root = doc.documentElement;
    const isTei = root && (
      (root.localName || root.tagName).toUpperCase() === 'TEI' ||
      doc.querySelector('TEI') !== null ||
      doc.querySelector('teiHeader') !== null
    );

    if (isTei) {
      return parseTeiDoc(doc, xmlString);
    }

    const bookElem = doc.querySelector('book') || doc.documentElement;
    const bookTitle = bookElem.getAttribute('title') || bookElem.getAttribute('name') || '';
    const bookFilename = bookElem.getAttribute('filename') || '';
    const textStructure = bookElem.getAttribute('textStructure') || 'hierarchical';
    const bookLang = bookElem.getAttribute('language') || '';

    // Global manuscripts under <book>
    const globalMss = parseManuscripts(bookElem.querySelector('manuscripts'));

    // Versions
    let versionElems = Array.from(bookElem.querySelectorAll(':scope > version'));
    if (versionElems.length === 0) {
      // Direct structure without <version> (e.g. Esdr.xml)
      versionElems = [bookElem];
    }

    const versions = versionElems.map((vElem, vIdx) => {
      const vTitle = vElem.getAttribute('title') || (vElem.tagName === 'book' ? bookTitle : `Version ${vIdx + 1}`);
      const vLang = vElem.getAttribute('language') || bookLang || '';
      const vAuthor = vElem.getAttribute('author') || '';
      const vFragment = vElem.getAttribute('fragment') || '';

      // Divisions
      const divLabels = [];
      const divDelims = [];
      const divElems = vElem.querySelectorAll('divisions > division');
      divElems.forEach(d => {
        divLabels.push(d.getAttribute('label') || '');
        divDelims.push(d.getAttribute('delimiter') || '');
      });

      // Manuscript list for version
      const vMssElem = vElem.querySelector(':scope > manuscripts');
      const vMss = vMssElem ? parseManuscripts(vMssElem) : globalMss;

      // Extract text units and hierarchy
      const textElem = vElem.querySelector(':scope > text') || vElem.querySelector('text');
      const { units, unitsById, unitsByRef, references } = parseTextHierarchy(textElem, divDelims, divLabels, vTitle);

      return {
        title: vTitle,
        language: vLang,
        author: vAuthor,
        fragment: vFragment,
        divisionLabels: divLabels,
        divisionDelimiters: divDelims,
        manuscripts: vMss,
        units: units,
        unitsById: unitsById,
        unitsByRef: unitsByRef,
        references: references
      };
    });

    return new OcpBook({
      title: bookTitle,
      filename: bookFilename,
      textStructure: textStructure,
      language: bookLang || (versions[0] ? versions[0].language : ''),
      manuscripts: globalMss.length > 0 ? globalMss : (versions[0] ? versions[0].manuscripts : []),
      versions: versions,
      rawXml: xmlString
    });
  }

  function parseManuscripts(mssContainer) {
    if (!mssContainer) return [];
    const msElems = mssContainer.querySelectorAll('ms');
    const list = [];

    msElems.forEach(ms => {
      const abbrev = (ms.getAttribute('abbrev') || '').trim();
      const language = ms.getAttribute('language') || '';
      const show = ms.getAttribute('show') || 'yes';
      const nameElem = ms.querySelector('name');
      const name = nameElem ? nameElem.textContent.trim() : abbrev;
      const bibElem = ms.querySelector('bibliography');
      const biblio = bibElem ? bibElem.textContent.trim() : '';

      list.push({
        abbrev: abbrev,
        name: name,
        language: language,
        show: show,
        bibliography: biblio
      });
    });

    return list;
  }

  function parseTextHierarchy(textElem, delims, labels, versionTitle) {
    const units = [];
    const unitsById = {};
    const unitsByRef = {};
    const referencesSet = new Set();
    const references = [];

    if (!textElem) return { units, unitsById, unitsByRef, references };

    function traverseDiv(elem, path) {
      const children = Array.from(elem.children);
      for (const child of children) {
        if (child.tagName.toLowerCase() === 'div') {
          const num = child.getAttribute('number') || child.getAttribute('n') || (path.length + 1).toString();
          traverseDiv(child, path.concat(num));
        } else if (child.tagName.toLowerCase() === 'unit') {
          processUnit(child, path);
        }
      }
    }

    function processUnit(unitElem, path) {
      const unitId = unitElem.getAttribute('id') || (units.length + 1).toString();
      
      // Build standard reference string using delimiters
      let refStr = '';
      if (path.length === 0) {
        refStr = '1';
      } else {
        const parts = [];
        for (let i = 0; i < path.length; i++) {
          parts.push(path[i]);
          if (i < path.length - 1) {
            const delim = (delims && delims[i] !== undefined && delims[i] !== '') ? delims[i] : ':';
            parts.push(delim);
          }
        }
        refStr = parts.join('');
      }

      if (!referencesSet.has(refStr)) {
        referencesSet.add(refStr);
        references.push(refStr);
      }

      // Readings
      const readingElems = unitElem.querySelectorAll(':scope > reading');
      const readings = [];

      readingElems.forEach((r, rIdx) => {
        const opt = r.getAttribute('option') !== null ? r.getAttribute('option') : rIdx.toString();
        const mssStr = r.getAttribute('mss') || '';
        const mss = mssStr.trim().split(/\s+/).filter(Boolean);
        const lbAttr = (r.getAttribute('linebreak') || '').trim();
        const lb = (lbAttr && lbAttr !== 'no') ? (lbAttr === 'yes' ? 'following' : lbAttr) : false;
        const ind = r.getAttribute('indent') === 'yes';

        // Words / Tokens if present
        const wElems = r.querySelectorAll('w');
        const words = [];
        if (wElems.length > 0) {
          wElems.forEach(w => {
            words.push({
              text: w.textContent,
              lex: w.getAttribute('lex') || '',
              morph: w.getAttribute('morph') || '',
              style: w.getAttribute('style') || '',
              lang: w.getAttribute('lang') || ''
            });
          });
        }

        readings.push({
          option: opt,
          mss: mss,
          text: r.textContent,
          words: words,
          linebreak: lb,
          indent: ind
        });
      });

      const unitObj = {
        id: unitId,
        ref: refStr,
        divPath: path,
        readings: readings
      };

      units.push(unitObj);
      unitsById[unitId] = unitObj;

      if (!unitsByRef[refStr]) {
        unitsByRef[refStr] = [];
      }
      unitsByRef[refStr].push(unitObj);
    }

    traverseDiv(textElem, []);

    return { units, unitsById, unitsByRef, references };
  }

  function parseTeiDoc(doc, xmlString) {
    const teiElem = doc.querySelector('TEI') || doc.documentElement;
    const titleStmt = doc.querySelector('teiHeader fileDesc titleStmt');
    const bookTitle = (titleStmt && titleStmt.querySelector('title') ? titleStmt.querySelector('title').textContent : (teiElem.getAttribute('xml:id') || teiElem.getAttribute('id') || '')).trim();
    const bookFilename = teiElem.getAttribute('xml:id') || teiElem.getAttribute('id') || '';
    const textStructure = 'hierarchical';

    // Language
    const textElem = doc.querySelector('text');
    let bookLang = '';
    if (textElem) {
      bookLang = textElem.getAttribute('xml:lang') || textElem.getAttribute('lang') || '';
    }
    if (!bookLang) {
      const langElem = doc.querySelector('teiHeader profileDesc langUsage language');
      bookLang = langElem ? (langElem.getAttribute('ident') || langElem.textContent.trim()) : '';
    }

    // Manuscripts from <sourceDesc> <listWit> <witness>
    const globalMss = [];
    const witnessMap = new Map();
    const witElems = Array.from(doc.querySelectorAll('sourceDesc listWit witness'));
    witElems.forEach(w => {
      const wId = w.getAttribute('xml:id') || w.getAttribute('id') || '';
      const abbrElem = w.querySelector('abbr');
      const abbrev = (abbrElem ? abbrElem.textContent : (wId.startsWith('wit-') ? wId.slice(4) : wId)).trim();
      const nameElem = w.querySelector('name');
      const name = nameElem ? nameElem.textContent.trim() : abbrev;
      const biblElem = w.querySelector('bibl');
      const biblio = biblElem ? biblElem.textContent.trim() : '';
      const lang = w.getAttribute('xml:lang') || w.getAttribute('lang') || '';
      const show = w.getAttribute('show') || 'yes';

      globalMss.push({
        abbrev: abbrev,
        name: name,
        language: lang,
        show: show,
        bibliography: biblio
      });

      if (wId) {
        witnessMap.set(wId, abbrev);
        witnessMap.set('#' + wId, abbrev);
      }
      witnessMap.set(abbrev, abbrev);
      witnessMap.set('#' + abbrev, abbrev);
    });

    // Body & Versions
    const bodyElem = doc.querySelector('text > body') || doc.querySelector('body') || doc.documentElement;
    let versionElems = Array.from(bodyElem.children).filter(c => c.tagName && c.tagName.toLowerCase() === 'div');
    const hasVersionDivs = versionElems.some(d => {
      const t = (d.getAttribute('type') || '').toLowerCase();
      return t === 'edition' || t === 'translation' || t === 'version' || t === 'pseudepigraphon';
    });

    if (!hasVersionDivs || versionElems.length === 0) {
      versionElems = [bodyElem];
    }

    // Read any <refsDecl> in teiHeader
    const refsDecls = Array.from(doc.querySelectorAll('teiHeader encodingDesc refsDecl'));

    const versions = versionElems.map((vElem, vIdx) => {
      const headElem = vElem.querySelector(':scope > head');
      let vTitle = headElem ? headElem.textContent.trim() : '';
      if (!vTitle) {
        vTitle = vElem.getAttribute('n') || vElem.getAttribute('title') || (vElem.tagName.toLowerCase() === 'body' ? bookTitle : (versionElems.length > 1 ? `Version ${vIdx + 1}` : bookTitle));
      }
      const vLang = vElem.getAttribute('xml:lang') || vElem.getAttribute('lang') || bookLang || '';
      const vAuthor = vElem.getAttribute('author') || '';
      const vFragment = vElem.getAttribute('fragment') || '';
      const vId = vElem.getAttribute('xml:id') || vElem.getAttribute('id') || '';

      // Match refsDecl for this version
      const vRefsDecl = refsDecls.find(rd => {
        const corresp = rd.getAttribute('corresp') || '';
        return vId && (corresp === '#' + vId || corresp === vId);
      }) || refsDecls[vIdx] || refsDecls[0];

      const divLabels = [];
      const divDelims = [];
      if (vRefsDecl) {
        const refStates = Array.from(vRefsDecl.querySelectorAll('refState'));
        refStates.forEach(rs => {
          divLabels.push(rs.getAttribute('unit') || '');
          divDelims.push(rs.getAttribute('delim') || '');
        });
      }

      // Manuscripts for version
      let vMss = globalMss;
      const vWitElems = Array.from(vElem.querySelectorAll(':scope > listWit witness'));
      if (vWitElems.length > 0) {
        vMss = [];
        vWitElems.forEach(w => {
          const wId = w.getAttribute('xml:id') || w.getAttribute('id') || '';
          const abbrElem = w.querySelector('abbr');
          const abbrev = (abbrElem ? abbrElem.textContent : (wId.startsWith('wit-') ? wId.slice(4) : wId)).trim();
          const nameElem = w.querySelector('name');
          const name = nameElem ? nameElem.textContent.trim() : abbrev;
          const biblElem = w.querySelector('bibl');
          const biblio = biblElem ? biblElem.textContent.trim() : '';
          const lang = w.getAttribute('xml:lang') || w.getAttribute('lang') || '';
          const show = w.getAttribute('show') || 'yes';
          vMss.push({ abbrev, name, language: lang, show, bibliography: biblio });
          if (wId) {
            witnessMap.set(wId, abbrev);
            witnessMap.set('#' + wId, abbrev);
          }
          witnessMap.set(abbrev, abbrev);
          witnessMap.set('#' + abbrev, abbrev);
        });
      }

      // Extract text units and hierarchy
      const { units, unitsById, unitsByRef, references } = parseTeiTextHierarchy(
        vElem, divDelims, divLabels, witnessMap, vMss
      );

      return {
        title: vTitle,
        language: vLang,
        author: vAuthor,
        fragment: vFragment,
        divisionLabels: divLabels,
        divisionDelimiters: divDelims,
        manuscripts: vMss,
        units: units,
        unitsById: unitsById,
        unitsByRef: unitsByRef,
        references: references
      };
    });

    return new OcpBook({
      title: bookTitle,
      filename: bookFilename,
      textStructure: textStructure,
      language: bookLang || (versions[0] ? versions[0].language : ''),
      manuscripts: globalMss.length > 0 ? globalMss : (versions[0] ? versions[0].manuscripts : []),
      versions: versions,
      rawXml: xmlString
    });
  }

  function parseTeiTextHierarchy(rootElem, delims, labels, witnessMap, manuscripts) {
    const units = [];
    const unitsById = {};
    const unitsByRef = {};
    const referencesSet = new Set();
    const references = [];

    if (!rootElem) return { units, unitsById, unitsByRef, references };

    function getRefStr(path) {
      if (path.length === 0) return '1';
      const parts = [];
      for (let i = 0; i < path.length; i++) {
        parts.push(path[i]);
        if (i < path.length - 1) {
          let delim = (delims && delims[i] !== undefined && delims[i] !== '') ? delims[i] : null;
          if (delim === null) {
            if (i === 0 && isNaN(Number(path[i]))) {
              delim = ' ';
            } else {
              delim = ':';
            }
          }
          parts.push(delim);
        }
      }
      return parts.join('');
    }

    function addReference(refStr) {
      if (!referencesSet.has(refStr)) {
        referencesSet.add(refStr);
        references.push(refStr);
      }
    }

    function traverse(elem, path) {
      const children = Array.from(elem.children);
      for (const child of children) {
        const tag = child.tagName.toLowerCase();
        if (tag === 'head') {
          continue;
        } else if (tag === 'div') {
          const num = child.getAttribute('n') || child.getAttribute('number') || '';
          const nextPath = num ? path.concat(num) : path;
          traverse(child, nextPath);
        } else if (tag === 'ab') {
          processAb(child, path);
        } else if (tag === 'app') {
          processApp(child, path);
        }
      }
    }

    function processAb(abElem, path) {
      const num = abElem.getAttribute('n') || abElem.getAttribute('number') || '';
      let abPath = path;
      if (num) {
        if (path.length > 0 && (num.startsWith(path[path.length - 1] + '.') || num.startsWith(path[path.length - 1] + ':'))) {
          const sep = num.includes(':') ? ':' : '.';
          abPath = path.slice(0, -1).concat(num.split(sep));
        } else {
          abPath = path.concat(num);
        }
      }

      const refStr = getRefStr(abPath);
      addReference(refStr);

      const appChildren = Array.from(abElem.querySelectorAll('app'));
      if (appChildren.length > 0) {
        appChildren.forEach(app => {
          processApp(app, abPath, refStr);
        });
      } else {
        processDirectAb(abElem, abPath, refStr);
      }
    }

    function processApp(appElem, path, refStr) {
      if (!refStr) {
        refStr = getRefStr(path);
        addReference(refStr);
      }

      const rawId = appElem.getAttribute('xml:id') || appElem.getAttribute('id') || (units.length + 1).toString();
      const m = rawId.match(/^u(\d+)(?:_.*)?$/);
      const unitId = m ? m[1] : rawId;

      const readings = [];
      const childNodes = Array.from(appElem.children);
      const readingNodes = childNodes.filter(c => {
        const tag = c.tagName.toLowerCase();
        return tag === 'lem' || tag === 'rdg';
      });

      readingNodes.forEach((rElem, rIdx) => {
        const isLem = rElem.tagName.toLowerCase() === 'lem';
        const opt = rElem.getAttribute('n') !== null ? rElem.getAttribute('n') : (isLem ? '0' : rIdx.toString());
        const witAttr = (rElem.getAttribute('wit') || '').trim();
        const mss = witAttr ? witAttr.split(/\s+/).map(sig => {
          const cleanSig = sig.startsWith('#') ? sig.slice(1) : sig;
          return witnessMap.get(cleanSig) || witnessMap.get(sig) || (cleanSig.startsWith('wit-') ? cleanSig.slice(4) : cleanSig);
        }) : [];

        const hasLb = rElem.querySelector('lb') !== null;
        const lbAttr = rElem.getAttribute('linebreak') || (hasLb ? 'following' : false);
        const lb = (lbAttr && lbAttr !== 'no') ? (lbAttr === 'yes' ? 'following' : lbAttr) : false;
        const ind = rElem.getAttribute('rend') === 'indent' || rElem.getAttribute('indent') === 'yes';

        const wElems = Array.from(rElem.querySelectorAll('w'));
        const words = [];
        if (wElems.length > 0) {
          wElems.forEach(w => {
            words.push({
              text: w.textContent,
              lex: w.getAttribute('lemma') || w.getAttribute('lex') || '',
              morph: w.getAttribute('msd') || w.getAttribute('morph') || '',
              style: w.getAttribute('pos') || w.getAttribute('style') || '',
              lang: w.getAttribute('xml:lang') || w.getAttribute('lang') || ''
            });
          });
        }

        const isOmission = rElem.getAttribute('type') === 'omission';
        let readingText = '';
        if (!isOmission) {
          readingText = rElem.textContent.trim();
        }

        readings.push({
          option: opt,
          mss: mss,
          text: readingText,
          words: words,
          linebreak: lb,
          indent: ind
        });
      });

      if (readings.length === 0) {
        readings.push({
          option: '0',
          mss: [],
          text: appElem.textContent.trim(),
          words: [],
          linebreak: false,
          indent: false
        });
      }

      const unitObj = {
        id: unitId,
        ref: refStr,
        divPath: path,
        readings: readings
      };

      units.push(unitObj);
      unitsById[unitId] = unitObj;
      if (!unitsByRef[refStr]) {
        unitsByRef[refStr] = [];
      }
      unitsByRef[refStr].push(unitObj);
    }

    function processDirectAb(abElem, path, refStr) {
      const rawId = abElem.getAttribute('xml:id') || abElem.getAttribute('id') || (units.length + 1).toString();
      const m = rawId.match(/^u(\d+)(?:_.*)?$/);
      const unitId = m ? m[1] : rawId;

      const wElems = Array.from(abElem.querySelectorAll('w'));
      const words = [];
      if (wElems.length > 0) {
        wElems.forEach(w => {
          words.push({
            text: w.textContent,
            lex: w.getAttribute('lemma') || w.getAttribute('lex') || '',
            morph: w.getAttribute('msd') || w.getAttribute('morph') || '',
            style: w.getAttribute('pos') || w.getAttribute('style') || '',
            lang: w.getAttribute('xml:lang') || w.getAttribute('lang') || ''
          });
        });
      }

      let text = '';
      if (wElems.length > 0) {
        const tokens = [];
        Array.from(abElem.childNodes).forEach(node => {
          if (node.nodeType === 1) {
            tokens.push(node.textContent.trim());
          }
        });
        tokens.forEach((tok, idx) => {
          if (idx === 0 || /^[,.:;·?!]/.test(tok)) {
            text += tok;
          } else {
            text += ' ' + tok;
          }
        });
      } else {
        text = abElem.textContent.trim();
      }

      const defaultMss = manuscripts.map(m => m.abbrev);
      const readings = [{
        option: '0',
        mss: defaultMss,
        text: text,
        words: words,
        linebreak: 'following',
        indent: false
      }];

      const unitObj = {
        id: unitId,
        ref: refStr,
        divPath: path,
        readings: readings
      };

      units.push(unitObj);
      unitsById[unitId] = unitObj;
      if (!unitsByRef[refStr]) {
        unitsByRef[refStr] = [];
      }
      unitsByRef[refStr].push(unitObj);
    }

    traverse(rootElem, []);

    return { units, unitsById, unitsByRef, references };
  }

  return {
    parseBook: parseXmlDoc,
    OcpBook: OcpBook
  };
}));
