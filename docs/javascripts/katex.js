/* ============================================
   Tutor Inteligente - KaTeX Auto-Render Setup
   ============================================ */

function renderMath() {
  if (typeof renderMathInElement !== "undefined") {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "$$",  right: "$$",  display: true },
        { left: "$",   right: "$",   display: false },
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
      ],
      throwOnError: false
    });
  }
}

if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    setTimeout(renderMath, 50);
  });
} else {
  document.addEventListener("DOMContentLoaded", renderMath);
}
