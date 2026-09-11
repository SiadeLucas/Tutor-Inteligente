/**
 * Motor de cor — Tutor Inteligente (RN-INT-001 revisada)
 *
 * Fonte da verdade: `disciplinas.cor_tema` (um único hex por disciplina).
 * Toda a escala é DERIVADA matematicamente em OKLCH, garantindo:
 *  - Escala perceptualmente uniforme entre disciplinas (trocar o laranja da
 *    Matemática pelo azul da Física não "achata" a identidade visual).
 *  - Acessibilidade por construção: alvos de claridade fixos por step.
 *
 * Sem dependências externas. Conversões portadas do CSS Color 4 spec
 * (Björn Ottosson, domínio público) com gamut-mapping simplificado.
 */

const clamp01 = (x: number) => Math.min(1, Math.max(0, x));

const srgbToLinear = (c: number) => (c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
const linearToSrgb = (c: number) => (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055);

// ---------------------------------------------------------------------------
// Conversões sRGB <-> OKLab/OKLCH
// ---------------------------------------------------------------------------

export function hexToRgb(hex: string): { r: number; g: number; b: number } {
  const h = hex.replace("#", "").trim();
  const full = h.length === 3 ? h.split("").map((c) => c + c).join("") : h;
  const int = parseInt(full, 16);
  if (Number.isNaN(int)) return { r: 0, g: 0, b: 0 };
  return { r: (int >> 16) & 255, g: (int >> 8) & 255, b: int & 255 };
}

export function rgbToHex(r: number, g: number, b: number): string {
  const toHex = (n: number) => Math.round(clamp01(n / 255) * 255).toString(16).padStart(2, "0");
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}

function oklchFromRgb(r: number, g: number, b: number): { l: number; c: number; h: number } {
  const lr = srgbToLinear(r / 255);
  const lg = srgbToLinear(g / 255);
  const lb = srgbToLinear(b / 255);

  const l = Math.cbrt(0.4122214708 * lr + 0.5363325363 * lg + 0.0514459929 * lb);
  const m = Math.cbrt(0.2119034982 * lr + 0.6806995451 * lg + 0.1073969566 * lb);
  const s = Math.cbrt(0.0883024619 * lr + 0.2817188376 * lg + 0.6299787005 * lb);

  return {
    l: 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
    c: 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s,
    h:
      (Math.atan2(
        0.0259040425 * l + 0.7827717124 * m - 0.8086757549 * s,
        1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s
      ) *
        180) /
      Math.PI,
  };
}

function rgbFromOklchRaw(l: number, c: number, hDeg: number): { r: number; g: number; b: number } {
  const hr = (hDeg * Math.PI) / 180;
  const a = c * Math.cos(hr);
  const b2 = c * Math.sin(hr);

  const l_ = l + 0.3963377774 * a + 0.2158037573 * b2;
  const m_ = l - 0.1055613458 * a - 0.0638541728 * b2;
  const s_ = l - 0.0894841775 * a - 1.291485548 * b2;

  const l3 = l_ * l_ * l_;
  const m3 = m_ * m_ * m_;
  const s3 = s_ * s_ * s_;

  return {
    r: +4.0767416621 * l3 - 3.3077115913 * m3 + 0.2309699292 * s3,
    g: -1.2684380046 * l3 + 2.6097574011 * m3 - 0.3413193965 * s3,
    b: -0.0041960863 * l3 - 0.7034186147 * m3 + 1.707614701 * s3,
  };
}

/** Converte OKLCH -> hex com gamut mapping (reduz croma e ajusta L até caber em sRGB). */
export function oklchToHex(l: number, c: number, h: number): string {
  let cc = Math.max(0, c);
  let ll = clamp01(l);
  for (let i = 0; i < 32; i++) {
    const raw = rgbFromOklchRaw(ll, cc, h);
    const inGamut = raw.r >= -0.002 && raw.r <= 1.002 && raw.g >= -0.002 && raw.g <= 1.002 && raw.b >= -0.002 && raw.b <= 1.002;
    if (inGamut) break;
    cc *= 0.9;
    ll += (clamp01(0.5 + (ll - 0.5) * 0.9) - ll) * 0.25;
  }
  const { r, g, b } = rgbFromOklchRaw(ll, cc, h);
  return rgbToHex(
    Math.round(linearToSrgb(clamp01(r)) * 255),
    Math.round(linearToSrgb(clamp01(g)) * 255),
    Math.round(linearToSrgb(clamp01(b)) * 255)
  );
}

export function hexToOklch(hex: string): { l: number; c: number; h: number } {
  const { r, g, b } = hexToRgb(hex);
  return oklchFromRgb(r, g, b);
}

// ---------------------------------------------------------------------------
// Escala semântica derivada
// ---------------------------------------------------------------------------

export interface SubjectPalette {
  /** hex original de disciplinas.cor_tema */
  base: string;
  /** 50..900 — 100/200 substituem tint/accent; 500 é o primary; 600/700 hovers */
  scale: Record<50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900, string>;
}

/** Chroma por step: identidade forte no meio da escala, neutra nos extremos. */
const STEP_CHROMA: Record<number, number> = {
  50: 0.018, 100: 0.038, 200: 0.08, 300: 0.115,
  400: 0.148, 500: 0.165, 600: 0.15, 700: 0.125,
  800: 0.09, 900: 0.055,
};

/** Lightness alvo por step (idêntico entre disciplinas => contraste estável). */
const STEP_LIGHTNESS: Record<number, number> = {
  50: 0.977, 100: 0.955, 200: 0.916, 300: 0.85,
  400: 0.76, 500: 0.68, 600: 0.6, 700: 0.51,
  800: 0.42, 900: 0.33,
};

const STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900] as const;

/**
 * Deriva a paleta completa de uma disciplina a partir de UM hex.
 * Mesma L em cada step para todas as disciplinas => tokens com contraste
 * garantido independentemente da cor cadastrada no banco.
 */
export function buildPalette(baseHex: string): SubjectPalette {
  const { h } = hexToOklch(baseHex);
  const scale = {} as SubjectPalette["scale"];
  for (const step of STEPS) {
    scale[step] = oklchToHex(STEP_LIGHTNESS[step], STEP_CHROMA[step], h);
  }
  return { base: rgbToHex(...Object.values(hexToRgb(baseHex)) as [number, number, number]), scale };
}

// ---------------------------------------------------------------------------
// Tokens estruturais (superfície, tinta, borda) — independentes de disciplina
// ---------------------------------------------------------------------------

export function neutralPalette(hueDeg: number, dark: boolean) {
  // Neutros levemente matizados pelo hue da disciplina (0.004-0.012 de croma):
  // coesão sutil sem "sujar" o tema de outra matéria.
  if (dark) {
    return {
      bg: oklchToHex(0.145, 0.008, hueDeg),
      card: oklchToHex(0.205, 0.01, hueDeg),
      elevated: oklchToHex(0.25, 0.012, hueDeg),
      text: oklchToHex(0.93, 0.006, hueDeg),
      textMuted: oklchToHex(0.68, 0.008, hueDeg),
      textFaint: oklchToHex(0.52, 0.008, hueDeg),
      border: oklchToHex(0.28, 0.012, hueDeg),
      borderStrong: oklchToHex(0.35, 0.014, hueDeg),
    };
  }
  return {
    bg: oklchToHex(0.985, 0.004, hueDeg),
    card: oklchToHex(1.0, 0.0, hueDeg),
    elevated: oklchToHex(0.975, 0.006, hueDeg),
    text: oklchToHex(0.21, 0.012, hueDeg),
    textMuted: oklchToHex(0.48, 0.012, hueDeg),
    textFaint: oklchToHex(0.62, 0.01, hueDeg),
    border: oklchToHex(0.915, 0.008, hueDeg),
    borderStrong: oklchToHex(0.84, 0.012, hueDeg),
  };
}
