/* Pula Rental – kalendar, izračun cijene i slanje upita (bez online plaćanja) */
(function () {
  var P = window.PR_PRICES, WA = window.PR_WA, MAIL = window.PR_MAIL;
  var ITEMS = P.items, ORDER = ['bike', 'ebike', 'escooter', 'kids', 'sup', 'kayak'];
  var SHORT = ['30m', '1h', '2h', '3h', '1d'];
  var LBL = { '30m': '30 min', '1h': '1 hour', '2h': '2 hours', '3h': '3 hours', '1d': '1 day' };
  var MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var $ = function (id) { return document.getElementById(id); };

  var today = new Date(); today.setHours(0, 0, 0, 0);
  var S = { mode: 'rent', start: null, end: null, view: new Date(today.getFullYear(), today.getMonth(), 1),
            qty: {}, ex: {}, tour: P.tours[0].id, tourN: 2 };
  ORDER.forEach(function (k) { S.qty[k] = 0; });
  P.extras.forEach(function (e) { S.ex[e.id] = 0; });

  // URL parametri: ?i=ebike  ?tour=kamenjak
  var q = new URLSearchParams(location.search);
  if (q.get('i') && ITEMS[q.get('i')]) S.qty[q.get('i')] = 1;
  if (q.get('tour')) { S.mode = 'tour'; if (P.tours.some(function (t) { return t.id === q.get('tour'); })) S.tour = q.get('tour'); }

  function eur(v) { return (Math.round(v * 100) / 100).toLocaleString('de-DE', { minimumFractionDigits: v % 1 ? 2 : 0, maximumFractionDigits: 2 }) + ' €'; }
  function dstr(d) { return d.getDate() + '.' + (d.getMonth() + 1) + '.' + d.getFullYear(); }
  function days() { if (!S.start) return 0; var e = S.end || S.start; return Math.round((e - S.start) / 864e5) + 1; }
  function single() { return S.start && (!S.end || +S.end === +S.start); }

  function itemPrice(k) {
    var c = ITEMS[k].calc, n = days();
    if (!n) return null;
    if (single()) {
      var want = SHORT.indexOf($('dur').value);
      for (var i = want; i < SHORT.length; i++) if (c[SHORT[i]] != null) return { p: c[SHORT[i]], t: LBL[SHORT[i]] };
      return null;
    }
    if (n === 2 && c['2d'] != null) return { p: c['2d'], t: '2 days' };
    if (n === 3 && c['3d'] != null) return { p: c['3d'], t: '3 days' };
    if (n >= 4 && c['4d'] != null) return { p: c['4d'] * n, t: n + ' days' };
    return { p: null, t: n + ' days – price on request' };
  }

  // ---------- kalendar ----------
  function renderCal() {
    var box = $('cal'), h = '', M = window.matchMedia('(max-width:640px)').matches ? 1 : 2;
    for (var m = 0; m < M; m++) {
      var first = new Date(S.view.getFullYear(), S.view.getMonth() + m, 1);
      var off = (first.getDay() + 6) % 7, dim = new Date(first.getFullYear(), first.getMonth() + 1, 0).getDate();
      h += '<div class="mo"><div class="mo-h">' + (m === 0 ? '<button type="button" class="nav-b" data-nav="-1" aria-label="Previous month">‹</button>' : '<span></span>') +
        '<b>' + MON[first.getMonth()] + ' ' + first.getFullYear() + '</b>' +
        (m === M - 1 ? '<button type="button" class="nav-b" data-nav="1" aria-label="Next month">›</button>' : '<span></span>') + '</div>' +
        '<div class="dw"><span>Mo</span><span>Tu</span><span>We</span><span>Th</span><span>Fr</span><span>Sa</span><span>Su</span></div><div class="dg">';
      for (var i = 0; i < off; i++) h += '<span></span>';
      for (var d = 1; d <= dim; d++) {
        var dt = new Date(first.getFullYear(), first.getMonth(), d), cls = 'd', dis = dt < today;
        var e = S.end || S.start;
        if (S.start && +dt === +S.start) cls += ' sel s';
        if (S.end && +dt === +S.end) cls += ' sel e';
        if (S.start && S.end && dt > S.start && dt < S.end) cls += ' in';
        if (+dt === +today) cls += ' td';
        h += '<button type="button" class="' + cls + '" data-d="' + dt.getTime() + '"' + (dis ? ' disabled' : '') + ' aria-label="' + dstr(dt) + '">' + d + '</button>';
      }
      h += '</div></div>';
    }
    box.innerHTML = h;
  }
  $('cal').addEventListener('click', function (ev) {
    var b = ev.target.closest('button'); if (!b) return;
    if (b.dataset.nav) {
      var nv = new Date(S.view.getFullYear(), S.view.getMonth() + (+b.dataset.nav), 1);
      if (nv >= new Date(today.getFullYear(), today.getMonth(), 1)) S.view = nv;
      return renderCal();
    }
    var dt = new Date(+b.dataset.d);
    if (S.mode === 'tour') { S.start = dt; S.end = null; }
    else if (!S.start || S.end) { S.start = dt; S.end = null; }
    else if (dt < S.start) { S.start = dt; }
    else { S.end = dt; }
    renderCal(); update();
  });

  // ---------- stavke ----------
  function row(id, name, sub, val, kind) {
    return '<div class="row" data-k="' + id + '" data-kind="' + kind + '"><div><b>' + name + '</b><small>' + sub + '</small></div>' +
      '<div class="qty"><button type="button" data-q="-" aria-label="Less">−</button><output>' + val + '</output><button type="button" data-q="+" aria-label="More">+</button></div></div>';
  }
  function renderItems() {
    var loc = $('loc').value;
    $('items').innerHTML = ORDER.map(function (k) {
      var it = ITEMS[k], c = it.calc, from = c['1d'] != null ? 'Day ' + eur(c['1d']) : '';
      var sub = (c['3h'] != null ? '3 h ' + eur(c['3h']) + ' · ' : (c['1h'] != null ? '1 h ' + eur(c['1h']) + ' · ' : '')) + from + (it.only ? ' · Camp Stoja only' : '');
      return row(k, it.name, sub, S.qty[k], 'i');
    }).join('');
    $('extras').innerHTML = P.extras.map(function (e) { return row(e.id, e.name, eur(e.price) + ' per day' + (e.multiFree ? ' · free for 2+ days' : ''), S.ex[e.id], 'x'); }).join('');
    ORDER.forEach(function (k) {
      var r = document.querySelector('.row[data-k="' + k + '"]');
      var off = ITEMS[k].only && ITEMS[k].only !== loc;
      r.classList.toggle('off', !!off);
      if (off && S.qty[k]) S.qty[k] = 0, r.querySelector('output').textContent = 0;
    });
    $('locHint').textContent = (loc === 'stoja') ? 'SUP boards and kayaks are available here.' : '';
  }
  function onQty(ev) {
    var b = ev.target.closest('button[data-q]'); if (!b) return;
    var r = b.closest('.row'), k = r.dataset.k, isI = r.dataset.kind === 'i';
    if (r.classList.contains('off')) return;
    var o = isI ? S.qty : S.ex;
    o[k] = Math.max(0, Math.min(20, o[k] + (b.dataset.q === '+' ? 1 : -1)));
    r.querySelector('output').textContent = o[k];
    update();
  }
  $('items').addEventListener('click', onQty);
  $('extras').addEventListener('click', onQty);
  $('loc').addEventListener('change', function () { renderItems(); update(); });
  $('dur').addEventListener('change', update);

  // ---------- ture ----------
  $('tours').innerHTML = P.tours.map(function (t) {
    return '<label class="topt"><input type="radio" name="tour" value="' + t.id + '"' + (t.id === S.tour ? ' checked' : '') + '><span>' + t.name + '</span></label>';
  }).join('');
  $('tours').addEventListener('change', function (e) { S.tour = e.target.value; update(); });
  document.querySelector('#tourStep .qty').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    S.tourN = Math.max(1, Math.min(40, S.tourN + (b.dataset.t === '+' ? 1 : -1))); $('tourN').textContent = S.tourN; update();
  });
  $('tourE').addEventListener('change', update);

  function setMode(m) {
    S.mode = m;
    document.querySelectorAll('.tab').forEach(function (t) { var on = t.dataset.mode === m; t.classList.toggle('on', on); t.setAttribute('aria-selected', on); });
    $('itemsStep').hidden = m !== 'rent'; $('tourStep').hidden = m !== 'tour';
    $('calTitle').textContent = m === 'rent' ? 'Select your days' : 'Select the tour date';
    $('calHint').textContent = m === 'rent' ? 'Click the first day and the last day you need the equipment. For a few hours, click one day twice.' : 'Click the day you would like to join the tour.';
    if (m === 'tour' && S.end) { S.end = null; renderCal(); }
    update();
  }
  document.querySelectorAll('.tab').forEach(function (t) { t.addEventListener('click', function () { setMode(t.dataset.mode); }); });

  // ---------- sažetak ----------
  var lines = [], total = 0;
  function update() {
    lines = []; total = 0;
    var n = days(), body = '';
    $('durBox').hidden = !(S.mode === 'rent' && single());
    if (S.mode === 'rent') {
      var vehicles = 0, longDel = false, onReq = false;
      ORDER.forEach(function (k) {
        if (!S.qty[k]) return;
        var pr = itemPrice(k);
        if (!pr) return;
        if (ITEMS[k].delivery) vehicles += S.qty[k];
        if (ITEMS[k].delivery && n >= 2) longDel = true;
        if (pr.p == null) { onReq = true; lines.push(S.qty[k] + '× ' + ITEMS[k].name + ' – ' + pr.t); return; }
        var sum = pr.p * S.qty[k]; total += sum;
        lines.push(S.qty[k] + '× ' + ITEMS[k].name + ' – ' + pr.t + ' = ' + eur(sum));
      });
      P.extras.forEach(function (e) {
        if (!S.ex[e.id]) return;
        var multi = n >= 2 && !single();
        if (multi && e.multiFree) { lines.push(S.ex[e.id] + '× ' + e.name + ' – free for ' + n + ' days'); return; }
        var dd = multi ? n : 1, sum = e.price * S.ex[e.id] * dd; total += sum;
        lines.push(S.ex[e.id] + '× ' + e.name + (multi ? ' – ' + n + ' days' : '') + ' = ' + eur(sum));
      });
      var when = S.start ? (single() ? dstr(S.start) + ' · ' + LBL[$('dur').value] : dstr(S.start) + ' – ' + dstr(S.end) + ' · ' + n + ' days') : 'No dates selected';
      body = '<p class="when">' + when + '</p>';
      body += lines.length ? '<ul>' + lines.map(function (l) { return '<li>' + l + '</li>'; }).join('') + '</ul>' : '<p class="muted">' + (S.start ? 'Add equipment with the + buttons.' : 'Select dates in the calendar.') + '</p>';
      if (lines.length && (longDel || vehicles >= 4)) body += '<p class="del">🚚 Free delivery applies to this booking.</p>';
      var tt = eur(total) + (onReq ? ' + on request' : '');
      $('tot').textContent = tt;
      if (mb) mb.querySelector('b').textContent = tt;
    } else {
      if (mb) mb.querySelector('b').textContent = 'on request';
      var t = P.tours.filter(function (x) { return x.id === S.tour; })[0];
      body = '<p class="when">' + (S.start ? dstr(S.start) : 'No date selected') + '</p><ul><li>' + t.name + ' – ' + S.tourN + ' ' + (S.tourN === 1 ? 'person' : 'people') + ($('tourE').checked ? ' (e-bikes)' : '') + '</li></ul>';
      $('tot').textContent = 'on request';
    }
    body += '<p class="loc-s">Pick-up: ' + $('loc').options[$('loc').selectedIndex].text + ' · ' + $('time').value + '</p>';
    $('sumBody').innerHTML = body;
    $('err').textContent = '';
  }
  $('time').addEventListener('change', update);

  function message() {
    var L = [];
    L.push(S.mode === 'rent' ? 'Booking request – Pula Rental' : 'Tour request – Pula Rental');
    L.push('Location: ' + $('loc').options[$('loc').selectedIndex].text);
    if (S.mode === 'rent') {
      L.push('Dates: ' + (single() ? dstr(S.start) + ' (' + LBL[$('dur').value] + ')' : dstr(S.start) + ' – ' + dstr(S.end) + ' (' + days() + ' days)'));
      L.push('Pick-up time: ' + $('time').value);
      lines.forEach(function (l) { L.push('• ' + l); });
      L.push('Total: ' + $('tot').textContent + ' (pay on arrival)');
    } else {
      var t = P.tours.filter(function (x) { return x.id === S.tour; })[0];
      L.push('Tour: ' + t.name + ($('tourE').checked ? ' (e-bikes)' : ''));
      L.push('Date: ' + dstr(S.start) + ', ' + $('time').value);
      L.push('People: ' + S.tourN);
    }
    if ($('dlv').checked) L.push('Delivery to accommodation: yes');
    if ($('acc').value.trim()) L.push('Accommodation: ' + $('acc').value.trim());
    L.push('Name: ' + $('nm').value.trim());
    if ($('ph').value.trim()) L.push('Phone: ' + $('ph').value.trim());
    if ($('em').value.trim()) L.push('E-mail: ' + $('em').value.trim());
    if ($('msg').value.trim()) L.push('Message: ' + $('msg').value.trim());
    return L.join('\n');
  }
  function check(needContact) {
    var e = '';
    if (!S.start) e = 'Please select the date(s) in the calendar.';
    else if (S.mode === 'rent' && !lines.length) e = 'Please choose at least one item.';
    else if (!$('nm').value.trim()) e = 'Please enter your name.';
    else if (needContact && !$('em').value.trim() && !$('ph').value.trim()) e = 'Please enter your e-mail or phone so we can reply.';
    else if (needContact && $('em').value.trim() && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test($('em').value.trim())) e = 'Please check your e-mail address.';
    $('err').textContent = e;
    if (e) { $('sum').scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
    return !e;
  }
  function track(kind) { try { if (window.gtag) gtag('event', 'booking_request', { method: kind, value: total, currency: 'EUR' }); } catch (x) {} }

  $('sendWa').addEventListener('click', function () {
    if (!check(false)) return;
    track('whatsapp');
    window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(message()), '_blank', 'noopener');
  });
  $('sendEm').addEventListener('click', function () {
    if (!check(true)) return;
    var btn = this; btn.disabled = true; btn.textContent = 'Sending…';
    var data = { _subject: (S.mode === 'rent' ? 'Booking request ' : 'Tour request ') + (S.start ? dstr(S.start) : '') + ' – ' + $('nm').value.trim(),
                 _template: 'box', _captcha: 'false', name: $('nm').value.trim(), email: $('em').value.trim(), phone: $('ph').value.trim(), request: message() };
    if ($('em').value.trim()) data._replyto = $('em').value.trim();
    fetch('https://formsubmit.co/ajax/' + MAIL, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (String(j.success) !== 'true') throw new Error(j.message || 'error');
        track('email');
        $('ok').hidden = false; $('ok').textContent = 'Thank you! Your request has been sent. We will reply with availability as soon as possible.';
        btn.textContent = 'Request sent';
      })
      .catch(function () {
        btn.disabled = false; btn.textContent = 'Send request by e-mail';
        $('err').innerHTML = 'Sending failed. Please use WhatsApp or write to <a href="mailto:' + MAIL + '">' + MAIL + '</a>.';
      });
  });

  var mb = document.querySelector('.mbar');
  if (mb) {
    mb.innerHTML = '<div class="mtot"><span>Total</span><b>0 €</b></div><a class="btn btn-main" href="#sum">Review &amp; send</a>';
  }
  renderItems(); renderCal(); setMode(S.mode);
  window.matchMedia('(max-width:640px)').addEventListener('change', renderCal);
})();
