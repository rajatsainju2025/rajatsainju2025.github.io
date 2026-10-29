// ---------------------------------------------------------------------------
// Numbers behind the story's charts. Every value is copied from a paper;
// the source is noted next to each block. Profile, papers and links stay in
// data.js.
// ---------------------------------------------------------------------------

// Theme of each paper, keyed by its Semantic Scholar id in data.js.
const THEMES = {
  vision:    { label: "Computer vision for microscopy", short: "Vision",    color: "#1F6F6B" },
  materials: { label: "In-situ materials science",      short: "Materials", color: "#B4532A" },
  language:  { label: "Language models, agents and accelerator AI", short: "AI for accelerators", color: "#2E4A87" },
};

const PAPER_THEME = {
  "6dadbf288ecf359d43a45960d4e962f46c11e762": "language",   // APS-RAG
  "20b48cdbfc7030a69799439d2c8264a3b8349add": "language",   // Agents at user facilities
  "18dc0f899b48fb5387514a67bfc8fd82175ff5e0": "materials",  // NiO reduction
  "d19916428af24c32501704a731dd656bf2c1e9d0": "materials",  // Carbon gasification
  "dc2a192d30a60e1b700acc9d409935fc9ca5b014": "materials",  // Tungsten nanofuzz
  "4c95de79ed256c1bbcb51e8d51195fc85cf2f033": "vision",     // DefectTrack
  "7b8d7b2fede25f75cd5ea3d7a7768bd83ca3845e": "materials",  // Ni oxidation
  "4de06cf3a055f2835ede8e4fe76ba7652dfe8706": "materials",  // Tungsten oxidation
  "6dbbc49afcac5830ca4aac05c577a3fca404694d": "language",   // Gender bias in BERT
  "d1bc2bc7e00178969a1d0b43c4f137e69e0688ab": "vision",     // DefectSegNet
};

// Which energy system a paper serves. Only fission and fusion are shown as tags.
const FIELDS = {
  fusion:  { label: "Fusion" },
  fission: { label: "Fission" },
};
const PAPER_FIELD = {
  "dc2a192d30a60e1b700acc9d409935fc9ca5b014": "fusion",   // W nanofuzz, plasma-facing material
  "4de06cf3a055f2835ede8e4fe76ba7652dfe8706": "fusion",   // W oxidation, ITER divertor material
  "4c95de79ed256c1bbcb51e8d51195fc85cf2f033": "fission",  // DefectTrack, ion irradiation of Ni
  "d1bc2bc7e00178969a1d0b43c4f137e69e0688ab": "fission",  // DefectSegNet, neutron-irradiated HT-9
};
// Conference abstracts on fission or fusion materials, matched by title.
const NUCLEAR_ABSTRACT = /irradiat|radiation|fusion|tungsten|HT-9|nuclear|reactor/i;

// Short labels for the timeline and the co-author network.
const PAPER_SHORT = {
  "6dadbf288ecf359d43a45960d4e962f46c11e762": "APS-RAG",
  "20b48cdbfc7030a69799439d2c8264a3b8349add": "Agents in production",
  "18dc0f899b48fb5387514a67bfc8fd82175ff5e0": "NiO reduction",
  "d19916428af24c32501704a731dd656bf2c1e9d0": "Carbon gasification",
  "dc2a192d30a60e1b700acc9d409935fc9ca5b014": "W nanofuzz",
  "4c95de79ed256c1bbcb51e8d51195fc85cf2f033": "DefectTrack",
  "7b8d7b2fede25f75cd5ea3d7a7768bd83ca3845e": "Ni oxidation",
  "4de06cf3a055f2835ede8e4fe76ba7652dfe8706": "W oxidation",
  "6dbbc49afcac5830ca4aac05c577a3fca404694d": "Bias in BERT",
  "d1bc2bc7e00178969a1d0b43c4f137e69e0688ab": "DefectSegNet",
};

// Sainju et al., ACS Nano 2022 (Ni nanoparticle oxidation at 600 °C).
const NI_OXIDATION = {
  criticalNm: 5.52,          // retracted Ni thickness at the end of stage 1
  criticalErrNm: 1.45,
  particles: 207,
  ensembleSeconds: 80,       // collective (SAED) oxidation duration, approximate
  smallDuration: "1.1 ± 0.5 s",
  mediumVoids: "2.7 ± 1.1 s",
  largeVoids: "3.5 ± 1.0 s",
  largeDiameterNm: 43.8,
};

// Sainju et al., Acta Materialia 2024 (W nanofuzz in 1 bar dry air).
const W_NANOFUZZ = {
  kp400: "0.31 ± 0.07",      // µg² cm⁻⁴ min⁻¹
  kp500: "6.10 ± 0.12",
  slowerAt500: 7,            // "about seven times slower" than pristine bulk W
};

// Sainju et al., Scientific Reports 2022, Table 3: two-sample KS test of each
// lifetime distribution against the ground truth.
const DEFECTTRACK_KS = [
  { who: "DefectTrack, all tracks", n: 4378, d: 0.018, p: 0.488, model: true },
  { who: "DefectTrack, 150 sampled", n: 150, d: 0.065, p: 0.541, model: true },
  { who: "DefectTrack, 150 sampled", n: 150, d: 0.065, p: 0.547, model: true },
  { who: "Expert 1", n: 150, d: 0.077, p: 0.336 },
  { who: "Expert 2", n: 150, d: 0.141, p: 0.005 },
  { who: "Expert 3", n: 150, d: 0.056, p: 0.725 },
  { who: "Expert 4", n: 150, d: 0.150, p: 0.002 },
];

// Same paper: the video, the labelling effort and the speed comparison.
const DEFECTTRACK_FACTS = {
  frames: 1200, msPerFrame: 9.7, nmPerPixel: 0.38, defectPx: 20,
  labelWeeks: 20, detections: 243052, uniqueDefects: 4279,
  modelSeconds: 57.14, expertHoursForTenth: 5.25,
  shortestMs: 19.4, longestMs: 6411.7,
};

// Roberts, Haile, Sainju et al., Scientific Reports 2019, Tables 2 and 3.
// Values are the measurement itself; errors are computed against `truth`.
// Expert 4 did not measure precipitates or voids.
const DEFECTSEGNET = [
  { what: "Dislocation density, image 1", truth: 8.91e14, model: 8.58e14, experts: [9.96e14, 9.50e14, 1.26e15, 8.45e14, 5.20e14, 1.03e15] },
  { what: "Dislocation density, image 2", truth: 9.19e14, model: 8.78e14, experts: [8.61e14, 1.01e15, 1.66e15, 4.81e14, 6.92e14, 1.02e15] },
  { what: "Precipitate density, image 1", truth: 6.56e21, model: 7.46e21, experts: [7.04e21, 5.09e21, 2.08e22, 4.10e21, 6.10e21] },
  { what: "Precipitate density, image 2", truth: 8.42e21, model: 8.87e21, experts: [4.86e21, 4.68e21, 8.36e21, 3.78e21, 5.70e21] },
  { what: "Void density, image 1",        truth: 5.25e20, model: 4.20e20, experts: [4.73e20, 5.25e20, 6.88e20, 5.25e20, 5.30e20] },
  { what: "Void density, image 2",        truth: 1.04e21, model: 9.00e20, experts: [7.20e20, 8.55e20, 9.90e20, 8.56e20, 9.00e20] },
  { what: "Precipitate size, image 1",    truth: 10.17,   model: 10.32,   experts: [9.65, 11.70, 9.00, 9.86, 9.70] },
  { what: "Precipitate size, image 2",    truth: 10.83,   model: 11.04,   experts: [12.35, 12.80, 13.00, 13.12, 12.40] },
  { what: "Void size, image 1",           truth: 22.64,   model: 25.77,   experts: [23.56, 22.30, 27.00, 23.71, 23.80] },
  { what: "Void size, image 2",           truth: 20.26,   model: 21.09,   experts: [22.41, 22.10, 23.00, 21.45, 21.80] },
];

// The APS-RAG pipeline as described in the paper's abstract (data.js TLDR).
const RAG_STEPS = [
  { name: "Ask", text: "A staff member asks a question in plain language, the way they would ask a colleague." },
  { name: "Retrieve", text: "Three searches run at once: dense (meaning), keyword (exact terms) and a knowledge graph (how things connect). Their results are fused." },
  { name: "Check", text: "The agent grades the evidence. If it is weak or off-topic, it rewrites the question and searches again. This corrective loop is what keeps answers grounded." },
  { name: "Answer", text: "An answer is written from the retrieved evidence only." },
  { name: "Cite", text: "Each claim links back to the logbook entry, document, work request, chat message or live reading it came from." },
];
const RAG_SOURCES = ["Logbooks", "Technical documents", "Work requests", "Chat", "Live control-system data"];
