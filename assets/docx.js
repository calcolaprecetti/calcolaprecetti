/* Generatore .docx minimo, senza librerie esterne (ZIP non compresso). */
var Docx = (function () {
  var TABLE = (function () {
    var t = new Uint32Array(256);
    for (var n = 0; n < 256; n++) {
      var c = n;
      for (var k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1;
      t[n] = c >>> 0;
    }
    return t;
  })();
  function crc32(b) {
    var c = 0xFFFFFFFF;
    for (var i = 0; i < b.length; i++) c = TABLE[(c ^ b[i]) & 0xFF] ^ (c >>> 8);
    return (c ^ 0xFFFFFFFF) >>> 0;
  }
  function utf8(s) { return new TextEncoder().encode(s); }
  function zip(files, mime) {
    var parts = [], central = [], offset = 0, d = new Date();
    var time = (d.getHours() << 11) | (d.getMinutes() << 5) | Math.floor(d.getSeconds() / 2);
    var date = ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
    files.forEach(function (f) {
      var name = utf8(f.name), data = utf8(f.text), crc = crc32(data);
      var lh = new DataView(new ArrayBuffer(30));
      lh.setUint32(0, 0x04034b50, true); lh.setUint16(4, 20, true); lh.setUint16(6, 0x0800, true);
      lh.setUint16(8, 0, true); lh.setUint16(10, time, true); lh.setUint16(12, date, true);
      lh.setUint32(14, crc, true); lh.setUint32(18, data.length, true); lh.setUint32(22, data.length, true);
      lh.setUint16(26, name.length, true); lh.setUint16(28, 0, true);
      parts.push(new Uint8Array(lh.buffer), name, data);
      var ch = new DataView(new ArrayBuffer(46));
      ch.setUint32(0, 0x02014b50, true); ch.setUint16(4, 20, true); ch.setUint16(6, 20, true);
      ch.setUint16(8, 0x0800, true); ch.setUint16(10, 0, true); ch.setUint16(12, time, true);
      ch.setUint16(14, date, true); ch.setUint32(16, crc, true); ch.setUint32(20, data.length, true);
      ch.setUint32(24, data.length, true); ch.setUint16(28, name.length, true); ch.setUint16(30, 0, true);
      ch.setUint16(32, 0, true); ch.setUint16(34, 0, true); ch.setUint16(36, 0, true);
      ch.setUint32(38, 0, true); ch.setUint32(42, offset, true);
      central.push(new Uint8Array(ch.buffer), name);
      offset += 30 + name.length + data.length;
    });
    var size = central.reduce(function (s, a) { return s + a.length; }, 0);
    var end = new DataView(new ArrayBuffer(22));
    end.setUint32(0, 0x06054b50, true); end.setUint16(4, 0, true); end.setUint16(6, 0, true);
    end.setUint16(8, files.length, true); end.setUint16(10, files.length, true);
    end.setUint32(12, size, true); end.setUint32(16, offset, true); end.setUint16(20, 0, true);
    return new Blob(parts.concat(central, [new Uint8Array(end.buffer)]), { type: mime });
  }
  function x(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function run(t, bold, sz) {
    sz = sz || 24;
    return '<w:r><w:rPr><w:rFonts w:ascii="Garamond" w:hAnsi="Garamond" w:cs="Garamond"/>' + (bold ? '<w:b/><w:bCs/>' : '') +
      '<w:sz w:val="' + sz + '"/><w:szCs w:val="' + sz + '"/></w:rPr><w:t xml:space="preserve">' + x(t) + '</w:t></w:r>';
  }
  function cell(w, t, right, bold) {
    return '<w:tc><w:tcPr><w:tcW w:w="' + w + '" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr><w:p><w:pPr><w:spacing w:before="40" w:after="40"/>' +
      (right ? '<w:jc w:val="right"/>' : '') + '</w:pPr>' + run(t, bold) + '</w:p></w:tc>';
  }
  // rows: [{label, amount}] con importi già formattati; total: stringa;
  // notes: stringa oppure elenco di {text, small} (paragrafi sotto la tabella)
  function build(rows, total, title, notes) {
    var b = 'w:val="single" w:sz="4" w:space="0" w:color="000000"';
    var tbl = '<w:tbl><w:tblPr><w:tblW w:w="9638" w:type="dxa"/><w:tblBorders><w:top ' + b + '/><w:left ' + b + '/><w:bottom ' + b + '/><w:right ' + b +
      '/><w:insideH ' + b + '/><w:insideV ' + b + '/></w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="108" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr>' +
      '<w:tblGrid><w:gridCol w:w="7200"/><w:gridCol w:w="2438"/></w:tblGrid>';
    rows.forEach(function (r) { tbl += '<w:tr><w:trPr><w:cantSplit/></w:trPr>' + cell(7200, r.label) + cell(2438, r.amount, true) + '</w:tr>'; });
    tbl += '<w:tr><w:trPr><w:cantSplit/></w:trPr>' + cell(7200, 'TOTALE COMPLESSIVO', false, true) + cell(2438, total, true, true) + '</w:tr></w:tbl>';
    var p = function (t, bold, after) { return '<w:p><w:pPr><w:spacing w:before="0" w:after="' + (after || 0) + '"/></w:pPr>' + run(t, bold) + '</w:p>'; };
    if (typeof notes === 'string') notes = [{ text: notes }];
    var tail = (notes || []).map(function (n, i) {
      return '<w:p><w:pPr><w:spacing w:before="' + (i === 0 ? 160 : 60) + '" w:after="0"/></w:pPr>' + run(n.text, false, n.small ? 20 : 24) + '</w:p>';
    }).join('');
    var body = (title ? p(title, true, 160) : '') + tbl + (tail || '<w:p/>');
    var doc = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' + body +
      '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1417" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>';
    var ct = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>';
    var rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>';
    return zip([{ name: '[Content_Types].xml', text: ct }, { name: '_rels/.rels', text: rels }, { name: 'word/document.xml', text: doc }],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document');
  }
  return { build: build };
})();
