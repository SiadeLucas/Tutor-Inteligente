/* ============================================
   Tutor Inteligente - UI Interactions
   ============================================ */

(function () {
  "use strict";

  function initScrollReveal() {
    var elements = document.querySelectorAll(".fade-in-up:not(.is-visible)");
    if (!elements.length) return;

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var el = entry.target;
            var siblings = el.parentElement ? el.parentElement.children : [];
            var index = Array.prototype.indexOf.call(siblings, el);
            el.style.transitionDelay = index * 0.08 + "s";
            el.classList.add("is-visible");
            observer.unobserve(el);
          }
        });
      },
      { threshold: 0.01, rootMargin: "80px 0px 80px 0px" }
    );

    elements.forEach(function (el) {
      observer.observe(el);
    });
  }

  function initHomepageClass() {
    if (document.querySelector(".ti-hero")) {
      document.body.classList.add("ti-homepage");
    } else {
      document.body.classList.remove("ti-homepage");
    }
  }

  function initAll() {
    initHomepageClass();
    initScrollReveal();
  }

  var contentObserver = new MutationObserver(function () {
    initAll();
  });

  function startObserving() {
    var target = document.querySelector(".md-content") || document.body;
    contentObserver.observe(target, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initAll();
      startObserving();
    });
  } else {
    initAll();
    startObserving();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      setTimeout(initAll, 100);
    });
  }
})();
