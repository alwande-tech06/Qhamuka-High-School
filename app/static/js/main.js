/* =====================================================================
   Qhamuka High School — main.js
   Plain modern JavaScript only. No frameworks.
   ===================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  /* ---- Mobile burger menu ---- */
  const burger = document.querySelector("[data-burger]");
  const menu = document.querySelector("[data-mobile-menu]");
  if (burger && menu) {
    burger.addEventListener("click", () => {
      const open = menu.classList.toggle("hidden") === false;
      burger.setAttribute("aria-expanded", String(open));
    });
  }

  /* ---- Admin rail collapse ---- */
  const railToggle = document.querySelector("[data-rail-toggle]");
  const rail = document.querySelector("[data-rail]");
  if (railToggle && rail) {
    railToggle.addEventListener("click", () => rail.classList.toggle("-translate-x-full"));
  }

  /* ---- Scroll reveal ---- */
  const reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("shown"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("shown"));
  }

  /* ---- Animated stat counters ---- */
  const counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const el = e.target;
        const target = parseInt(el.dataset.count, 10);
        let cur = 0;
        const step = Math.max(1, Math.round(target / 40));
        const tick = () => {
          cur = Math.min(target, cur + step);
          el.textContent = cur.toLocaleString();
          if (cur < target) requestAnimationFrame(tick);
        };
        tick();
        io.unobserve(el);
      });
    }, { threshold: 0.5 });
    counters.forEach((c) => io.observe(c));
  }

  /* ---- Gallery filter tabs + lightbox ---- */
  const tabs = document.querySelectorAll("[data-filter]");
  const items = document.querySelectorAll("[data-category]");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("is-active"));
      tab.classList.add("is-active");
      const cat = tab.dataset.filter;
      items.forEach((item) => {
        const show = cat === "all" || item.dataset.category === cat;
        item.classList.toggle("hidden", !show);
      });
    });
  });

  const lightbox = document.querySelector("[data-lightbox]");
  if (lightbox) {
    const lbImg = lightbox.querySelector("img");
    const close = lightbox.querySelector("[data-lightbox-close]");
    document.querySelectorAll("[data-lightbox-src]").forEach((trigger) => {
      trigger.addEventListener("click", () => {
        lbImg.src = trigger.dataset.lightboxSrc;
        lbImg.alt = trigger.dataset.lightboxAlt || "Gallery image";
        lightbox.classList.add("open");
      });
    });
    const hide = () => lightbox.classList.remove("open");
    close.addEventListener("click", hide);
    lightbox.addEventListener("click", (e) => { if (e.target === lightbox) hide(); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") hide(); });
  }

  /* ---- Scroll-aware sticky header ---- */
  const header = document.querySelector("header");
  if (header) {
    if (document.querySelector(".hero")) header.classList.add("hero-mode");
    const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 80);
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---- Contact form client validation ---- */
  const form = document.querySelector("[data-contact-form]");
  if (form) {
    const setState = (field, valid, msg) => {
      field.classList.toggle("valid", valid);
      field.classList.toggle("invalid", !valid);
      const err = field.querySelector(".error-text");
      if (err && msg) err.textContent = msg;
    };
    const validators = {
      name: (v) => v.trim().length >= 2 || "Please enter your full name.",
      email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || "Enter a valid email address.",
      message: (v) => v.trim().length >= 10 || "Message should be at least 10 characters.",
    };
    form.querySelectorAll("[data-validate]").forEach((input) => {
      input.addEventListener("blur", () => {
        const rule = validators[input.dataset.validate];
        const res = rule(input.value);
        setState(input.closest(".field"), res === true, res === true ? "" : res);
      });
    });
    form.addEventListener("submit", (e) => {
      let ok = true;
      form.querySelectorAll("[data-validate]").forEach((input) => {
        const res = validators[input.dataset.validate](input.value);
        if (res !== true) ok = false;
        setState(input.closest(".field"), res === true, res === true ? "" : res);
      });
      if (!ok) e.preventDefault();
      // When the Flask backend is wired, allow normal POST submission on success.
    });
  }
});
