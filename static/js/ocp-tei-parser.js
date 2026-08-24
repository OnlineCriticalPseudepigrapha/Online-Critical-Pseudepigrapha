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

          renderedUnits.push({
            id: u.id,
            ref: u.ref,
            divPath: u.divPath,
            readingText: chosenReading ? chosenReading.text : '',
            chosenOption: chosenReading ? chosenReading.option : '0',
            chosenMss: chosenReading ? chosenReading.mss : [],
            linebreak: chosenReading ? chosenReading.linebreak : false,
            indent: chosenReading ? chosenReading.indent : false,
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
      // Node.js fallback using xmldom or lightweight DOM
      try {
        const { DOMParser: NodeDOMParser } = require('@xmldom/xmldom');
        doc = new NodeDOMParser().parseFromString(xmlString, 'text/xml');
      } catch (e) {
        throw new Error('DOMParser is required to parse XML. In Node.js, install @xmldom/xmldom.');
      }
    }

    const parserError = doc.querySelector('parsererror');
    if (parserError) {
      throw new Error('XML Parse Error: ' + parserError.textContent);
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
        const lb = r.getAttribute('linebreak') === 'yes';
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

  return {
    parseBook: parseXmlDoc,
    OcpBook: OcpBook
  };
}));
