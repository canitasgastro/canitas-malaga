(function () {
  "use strict";

  var header = document.getElementById("site-header");
  var menuToggle = document.getElementById("menu-toggle");
  var siteMenu = document.getElementById("site-menu");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Mobile / dropdown menu ---------- */
  function closeMenu() {
    menuToggle.setAttribute("aria-expanded", "false");
    siteMenu.setAttribute("data-open", "false");
  }
  function openMenu() {
    menuToggle.setAttribute("aria-expanded", "true");
    siteMenu.setAttribute("data-open", "true");
  }
  if (menuToggle && siteMenu) {
    menuToggle.addEventListener("click", function () {
      var isOpen = siteMenu.getAttribute("data-open") === "true";
      if (isOpen) { closeMenu(); } else { openMenu(); }
    });
    siteMenu.querySelectorAll("[data-close-menu]").forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });
    document.addEventListener("click", function (e) {
      if (!siteMenu.contains(e.target) && !menuToggle.contains(e.target)) {
        closeMenu();
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });
  }

  /* ---------- Header background on scroll ---------- */
  function updateHeader() {
    if (window.scrollY > 40) {
      header.setAttribute("data-scrolled", "true");
    } else {
      header.setAttribute("data-scrolled", "false");
    }
  }

  /* ---------- Subtle parallax on the three-space backgrounds ---------- */
  var layers = Array.prototype.slice.call(document.querySelectorAll("[data-parallax-layer]"));

  function updateParallax() {
    if (reduceMotion || layers.length === 0) return;
    var viewportH = window.innerHeight;
    layers.forEach(function (layer) {
      var rect = layer.parentElement.getBoundingClientRect();
      var progress = (rect.top) / viewportH; /* -1 (above) .. 1 (below) */
      var offset = progress * 40; /* px of drift */
      layer.style.transform = "translateY(" + offset.toFixed(1) + "px)";
    });
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      updateHeader();
      updateParallax();
      ticking = false;
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  updateHeader();
  updateParallax();

  /* ---------- Single open accordion item at a time ---------- */
  var accordionItems = document.querySelectorAll(".accordion-item");
  accordionItems.forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (item.open) {
        accordionItems.forEach(function (other) {
          if (other !== item) other.removeAttribute("open");
        });
      }
    });
  });

  /* ---------- Photo galleries (e.g. "El hotel") ---------- */
  document.querySelectorAll(".hotel-gallery").forEach(function (gallery) {
    var track = gallery.querySelector(".hotel-gallery-track");
    var dotsWrap = gallery.querySelector(".hotel-gallery-dots");
    var prevBtn = gallery.querySelector('[data-dir="-1"]');
    var nextBtn = gallery.querySelector('[data-dir="1"]');
    var slides = Array.prototype.slice.call(track.children);
    if (!slides.length) return;

    var dots = slides.map(function (_, i) {
      var dot = document.createElement("span");
      if (i === 0) dot.classList.add("is-active");
      dot.addEventListener("click", function () { goTo(i); });
      dotsWrap.appendChild(dot);
      return dot;
    });

    function goTo(index) {
      index = Math.max(0, Math.min(slides.length - 1, index));
      track.scrollTo({ left: slides[index].offsetLeft, behavior: reduceMotion ? "auto" : "smooth" });
    }
    function currentIndex() {
      var trackLeft = track.scrollLeft;
      var closest = 0;
      var closestDist = Infinity;
      slides.forEach(function (slide, i) {
        var dist = Math.abs(slide.offsetLeft - trackLeft);
        if (dist < closestDist) { closestDist = dist; closest = i; }
      });
      return closest;
    }
    function syncDots() {
      var idx = currentIndex();
      dots.forEach(function (dot, i) { dot.classList.toggle("is-active", i === idx); });
    }

    if (prevBtn) prevBtn.addEventListener("click", function () { goTo(currentIndex() - 1); });
    if (nextBtn) nextBtn.addEventListener("click", function () { goTo(currentIndex() + 1); });

    var scrollTicking = false;
    track.addEventListener("scroll", function () {
      if (scrollTicking) return;
      scrollTicking = true;
      requestAnimationFrame(function () { syncDots(); scrollTicking = false; });
    }, { passive: true });
  });
})();
