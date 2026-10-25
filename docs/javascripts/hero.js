// Home page hero: a sphere of "training data" in the brand blue. A small yellow cluster (Carol's rows)
// drifts out and fades, and the sphere keeps its shape. Three.js is loaded only on the home page.
(function () {
  var THREE_URL = "https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js";
  var loading = null;

  function loadThree() {
    if (window.THREE) return Promise.resolve();
    if (!loading) {
      loading = new Promise(function (resolve, reject) {
        var s = document.createElement("script");
        s.src = THREE_URL; s.async = true; s.onload = resolve; s.onerror = reject;
        document.head.appendChild(s);
      });
    }
    return loading;
  }

  function cssColour(name, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || fallback;
  }

  function dotTexture() {
    var c = document.createElement("canvas"); c.width = c.height = 64;
    var g = c.getContext("2d");
    var grad = g.createRadialGradient(32, 32, 0, 32, 32, 30);
    grad.addColorStop(0, "rgba(255,255,255,1)"); grad.addColorStop(.55, "rgba(255,255,255,1)"); grad.addColorStop(1, "rgba(255,255,255,0)");
    g.fillStyle = grad; g.beginPath(); g.arc(32, 32, 30, 0, Math.PI * 2); g.fill();
    return new THREE.CanvasTexture(c);
  }

  function start(canvas) {
    var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(40, 1, .1, 50);
    camera.position.z = 7;
    var stage = new THREE.Group(); scene.add(stage);
    var sphere = new THREE.Group(); stage.add(sphere);
    var dot = dotTexture();

    // Points spread evenly over a sphere (Fibonacci spiral).
    var N = 950, R = 1.6, golden = Math.PI * (3 - Math.sqrt(5));
    var cap = new THREE.Vector3(.55, .35, .76).normalize();
    var blue = [], carol = [];
    for (var i = 0; i < N; i++) {
      var y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), t = i * golden;
      var p = new THREE.Vector3(Math.cos(t) * r, y, Math.sin(t) * r);
      (p.dot(cap) > .93 ? carol : blue).push(p);
    }
    function build(list) {
      var a = new Float32Array(list.length * 3);
      list.forEach(function (p, k) { a[k * 3] = p.x * R; a[k * 3 + 1] = p.y * R; a[k * 3 + 2] = p.z * R; });
      var g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(a, 3));
      return g;
    }
    var blueMat = new THREE.PointsMaterial({ size: .14, map: dot, transparent: true, depthWrite: false, opacity: .9 });
    var carolMat = new THREE.PointsMaterial({ size: .2, map: dot, transparent: true, depthWrite: false });
    var bluePts = new THREE.Points(build(blue), blueMat); sphere.add(bluePts);
    var carolGeo = build(carol), carolPts = new THREE.Points(carolGeo, carolMat); sphere.add(carolPts);
    var carolBase = carolGeo.attributes.position.array.slice();

    // Two faint orbit rings.
    var ringMat = new THREE.LineBasicMaterial({ transparent: true, opacity: .22 });
    function ring(rad, tilt) {
      var pts = []; for (var k = 0; k <= 96; k++) { var a = k / 96 * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(a) * rad, 0, Math.sin(a) * rad)); }
      var l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), ringMat); l.rotation.x = tilt; stage.add(l);
    }
    ring(2.15, .5); ring(2.4, -.35);

    function colours() {
      var b = new THREE.Color(cssColour("--mul-blue", "#3D5AFE")), y = new THREE.Color(cssColour("--mul-yellow", "#FFC300"));
      blueMat.color.copy(b); ringMat.color.copy(b); carolMat.color.copy(y);
    }
    colours();
    var observer = new MutationObserver(colours);
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
    observer.observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });

    var mx = 0, my = 0;
    function onMove(e) {
      var b = canvas.getBoundingClientRect();
      mx = ((e.clientX - b.left) / b.width - .5); my = ((e.clientY - b.top) / b.height - .5);
    }
    window.addEventListener("pointermove", onMove, { passive: true });

    function resize() {
      var w = canvas.clientWidth, h = canvas.clientHeight;
      if (!w || !h) return;
      renderer.setSize(w, h, false);
      camera.aspect = w / h; camera.updateProjectionMatrix();
      stage.position.set(0, 0, 0);
      stage.scale.setScalar(Math.min(1, camera.aspect * .8));
    }
    resize();
    var ro = window.ResizeObserver ? new ResizeObserver(resize) : null;
    if (ro) ro.observe(canvas);

    var CYCLE = 11, ease = function (x) { return x * x * (3 - 2 * x); };
    function frame(sec) {
      // 0-3 s: the data sits in the model. 3-5.5 s: Carol's rows leave. 5.5-8 s: the model settles without them. 8-10 s: they return.
      var c = sec % CYCLE, away = 0;
      if (c > 3 && c <= 5.5) away = ease((c - 3) / 2.5);
      else if (c > 5.5 && c <= 8) away = 1;
      else if (c > 8 && c <= 10) away = 1 - ease((c - 8) / 2);
      var pos = carolGeo.attributes.position.array;
      for (var k = 0; k < pos.length; k += 3) {
        var k2 = k / 3, wob = Math.sin(sec * 2 + k2) * .02;
        var push = 1 + away * (.32 + .14 * Math.sin(k2 * 1.7)) + wob;
        pos[k] = carolBase[k] * push; pos[k + 1] = carolBase[k + 1] * push + away * .2; pos[k + 2] = carolBase[k + 2] * push;
      }
      carolGeo.attributes.position.needsUpdate = true;
      carolMat.opacity = 1 - away * .96;
      var settle = (c > 5.5 && c < 7) ? Math.sin((c - 5.5) / 1.5 * Math.PI) * .05 : 0;
      bluePts.scale.setScalar(1 + settle); 
      sphere.rotation.y = sec * .22 + mx * .6; sphere.rotation.x = .25 + my * .4;
      stage.children[1].rotation.z = sec * .05; 
      renderer.render(scene, camera);
    }

    var raf = 0, t0 = performance.now();
    function loop(now) {
      if (!canvas.isConnected) { cleanup(); return; }
      frame((now - t0) / 1000);
      raf = requestAnimationFrame(loop);
    }
    function cleanup() {
      cancelAnimationFrame(raf); observer.disconnect(); if (ro) ro.disconnect();
      window.removeEventListener("pointermove", onMove); renderer.dispose();
    }
    if (reduced) { frame(1.5); } else { raf = requestAnimationFrame(loop); }
  }

  function init() {
    var canvas = document.getElementById("hero-canvas");
    if (!canvas || canvas.dataset.ready) return;
    canvas.dataset.ready = "1";
    loadThree().then(function () { start(canvas); }).catch(function () { canvas.classList.add("is-off"); });
  }

  if (typeof document$ !== "undefined") document$.subscribe(init); else document.addEventListener("DOMContentLoaded", init);
})();
