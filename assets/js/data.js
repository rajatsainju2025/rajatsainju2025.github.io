// ---------------------------------------------------------------------------
// All site content lives in this file. Edit it and push; no build step needed.
// Empty strings ("") hide the corresponding link or item.
// ---------------------------------------------------------------------------

const SITE = {
  name: "Rajat Sainju",
  title: "AI/ML Scientist at Argonne National Laboratory",
  photo: "https://avatars.githubusercontent.com/u/202970519?v=4&s=560",

  email: "sainju73@gmail.com",
  location: "Chicago, IL",
  cv: "",                // e.g. "assets/cv.pdf" (upload the PDF to assets/)
  cvNote: "",            // e.g. "as of 2026"

  links: {
    github: "https://github.com/rajatsainju2025",
    scholar: "https://scholar.google.com/citations?user=c1UCRoEAAAAJ&hl=en",
    linkedin: "https://www.linkedin.com/in/rajat-sainju-a3435812a",
    twitter: "",         // e.g. "https://x.com/yourhandle"
  },

  // Your name as it appears in author lists (highlighted in bold).
  me: "Rajat Sainju",

  bio: `I'm an AI/ML scientist at the <a href="https://www.aps.anl.gov/">Advanced Photon Source</a>
    at Argonne National Laboratory. I build production LLM systems, including retrieval-augmented
    generation and agents, that help run a large accelerator facility, and I develop machine learning
    for accelerators and materials science. Before Argonne, I was a Ph.D. student in Materials Science
    and Engineering at the University of Connecticut, advised by Prof. Yuanyuan Zhu, where I used deep
    learning to analyze in-situ electron microscopy images and videos. I studied Engineering Physics at
    Ramapo College.`,
};

// News: newest first. `image` is a picture; otherwise `emoji` + `tint` make a tile.
const NEWS = [
  {
    date: "Sep, 2026", image: "assets/img/news_agents.jpg",
    text: `New perspective on <a href="https://arxiv.org/abs/2609.36362">deploying AI agents in production</a>
      at scientific user facilities, drawing on agents running at the APS.`,
  },
  {
    date: "Jul, 2026", image: "assets/img/news_apsrag.jpg",
    text: `<a href="https://arxiv.org/abs/2607.24663">APS-RAG</a> is on arXiv, and the
      <a href="https://github.com/rajatsainju2025/aps-rag">code</a> is open source! 🚀`,
  },
  {
    date: "Oct, 2025", image: "assets/img/news_gasification.jpg",
    text: `Our study of carbon gasification on a spent Ni/CeO₂ catalyst is out in
      <a href="https://doi.org/10.1021/acscatal.5c02824">ACS Catalysis</a>.`,
  },
  {
    date: "Jun, 2025", image: "assets/img/news_reduction.jpg",
    text: `Operando reduction of hollow NiO and Ni redispersion published in
      <a href="https://doi.org/10.1021/acs.nanolett.5c02133">Nano Letters</a>.`,
  },
  {
    date: "Oct, 2024", image: "assets/img/news_tungsten.jpg",
    text: `Tungsten nanofuzz oxidation, seen in situ at atmospheric pressure, published in
      <a href="https://doi.org/10.1016/j.actamat.2024.120282">Acta Materialia</a>.`,
  },
  {
    date: "Sep, 2022", image: "assets/img/news_defecttrack.jpg",
    text: `<a href="https://doi.org/10.1038/s41598-022-19697-1">DefectTrack</a>, real-time tracking of
      defects in in-situ TEM videos, published in Scientific Reports.`,
  },
  {
    date: "Apr, 2022", image: "assets/img/news_oxidation.jpg",
    text: `Single-nanoparticle Ni oxidation, from nucleation to thickening, published in
      <a href="https://doi.org/10.1021/acsnano.2c00742">ACS Nano</a>.`,
  },
  {
    date: "Sep, 2019", image: "assets/img/news_segmentation.jpg",
    text: `<a href="https://doi.org/10.1038/s41598-019-49105-0">DefectSegNet</a>, deep learning
      segmentation of defects in steel, published in Scientific Reports.`,
  },
];

// Projects / publications, newest first.
// `s2` is the Semantic Scholar paper id; it is used to show a live citation count.
const PROJECTS = [
  {
    title: "APS-RAG: A Corrective Agentic Hybrid RAG and an Operations-Grounded Evaluation for a Scientific Facility",
    image: "assets/img/apsrag.jpg",
    authors: ["Rajat Sainju", "Dariusz Jarosz", "Hairong Shang", "Michael Prince", "Ryan M. Aydelott",
              "Mathew J. Cherukara", "Yine Sun", "Michael Borland"],
    venue: "arXiv 2026",
    tldr: `A deployed platform that lets Advanced Photon Source staff ask plain-language questions over
      logbooks, technical documents, work requests, chat and live control-system data, with cited answers.
      It fuses dense, keyword and knowledge-graph retrieval with a corrective agentic loop, and is
      evaluated on APS-Bench, an operations-grounded benchmark.`,
    s2: "6dadbf288ecf359d43a45960d4e962f46c11e762",
    links: { pdf: "https://arxiv.org/pdf/2607.24663", arxiv: "https://arxiv.org/abs/2607.24663",
             github: "https://github.com/rajatsainju2025/aps-rag" },
  },
  {
    title: "Strategies for Deploying AI Agents in Production at Scientific User Facilities",
    card: { line1: "Perspective", line2: "AI Agents at User Facilities", tint: "violet" },
    authors: ["Ming Du", "Xiang-Yu Yin", "Michael H. Prince", "Yi Jiang", "Rajat Sainju", "Tekin Bicer",
              "Yan-Qi Luo", "Eric Codrea", "P. Myint", "Nina Andrejevic", "Juan-Juan Huang",
              "Trupti Mohanty", "Pawan K. Tripathi", "D. Beniwal", "Hemant Sharma", "D. Gursoy",
              "Ai-Shan Luo", "Tao Zhou", "Chen-Ran Xu", "J. Ilavsky", "M. Dearing", "Ryan Chard",
              "Ho-Young Seo", "Dariusz Jarosz", "Elaine A. Chandler", "T. Fors", "Hairong Shang",
              "P. Jemian", "Xue Wu", "Madeline Miller", "Ryan M. Aydelott", "Nicholas Schwarz",
              "F. De Carlo", "Byeongdu Lee", "Yine Sun", "M. Smart", "Philippe Piot",
              "Joe H. Sullivan", "Mathew J. Cherukara", "Alec Sandy", "S. Vogt", "J.-A. Lang",
              "Laurent C. Chapon"],
    venue: "arXiv 2026",
    tldr: `A perspective, drawn from LLM-driven agents deployed at the APS, on practical strategies for
      running agents in production at light sources and other user facilities, from beamline control to
      knowledge retrieval and data analysis.`,
    s2: "20b48cdbfc7030a69799439d2c8264a3b8349add",
    links: { arxiv: "https://arxiv.org/abs/2609.36362" },
  },
  {
    title: "Operando Spatially and Time-Resolved Reduction of Hollow Polycrystalline NiO: How to Promote Ni Nanoparticle Redispersion",
    card: { line1: "Nano Letters", line2: "Operando NiO Reduction", tint: "teal" },
    authors: ["Rajat Sainju", "Tianyu Li", "M. Nielsen", "Yuanyuan Zhu"],
    venue: "Nano Letters 2025",
    tldr: `Watches hollow, polycrystalline NiO reduce in an environmental TEM and uses semantic segmentation
      to extract grain-by-grain kinetics, showing how the reduction temperature can promote Ni
      nanoparticle redispersion.`,
    s2: "18dc0f899b48fb5387514a67bfc8fd82175ff5e0",
    links: { paper: "https://doi.org/10.1021/acs.nanolett.5c02133" },
  },
  {
    title: "Operando Elucidation of Filamentous Carbon Gasification Kinetics and Mechanisms on a Spent Ni/CeO₂ Catalyst",
    card: { line1: "ACS Catalysis", line2: "Carbon Gasification", tint: "amber" },
    authors: ["M. Nielsen", "Tianyu Li", "Rajat Sainju", "Seth March", "Chun-Xiang Zhu", "Pu-Xian Gao",
              "S. Suib", "Yuanyuan Zhu"],
    venue: "ACS Catalysis 2025",
    tldr: `Follows, operando in the TEM, how carbon filaments on a spent Ni/CeO₂ catalyst are gasified,
      to measure the kinetics and identify the mechanisms involved.`,
    s2: "d19916428af24c32501704a731dd656bf2c1e9d0",
    links: { paper: "https://doi.org/10.1021/acscatal.5c02824" },
  },
  {
    title: "In-situ ETEM Study of Plasma-Facing Tungsten Nanofuzz Oxidation at Atmospheric Pressure: Microstructure Evolution and Substrate-Free Oxidation Kinetics",
    card: { line1: "Acta Materialia", line2: "Tungsten Nanofuzz Oxidation", tint: "rose" },
    authors: ["Rajat Sainju", "Marlene Patino", "Matthew Baldwin", "O. El-Atwani", "R. Kolasinski",
              "Yuanyuan Zhu"],
    venue: "Acta Materialia 2024",
    tldr: `Uses in-situ environmental TEM at atmospheric pressure to follow the oxidation of tungsten
      nanofuzz, a plasma-facing fusion material, tracking its microstructure and measuring oxidation
      kinetics free of substrate effects.`,
    s2: "dc2a192d30a60e1b700acc9d409935fc9ca5b014",
    links: { paper: "https://doi.org/10.1016/j.actamat.2024.120282" },
  },
  {
    title: "DefectTrack: A Deep Learning-Based Multi-Object Tracking Algorithm for Quantitative Defect Analysis of In-situ TEM Videos in Real-Time",
    image: "assets/img/defecttrack.jpg",
    authors: ["Rajat Sainju", "Wei-Ying Chen", "Samuel Schaefer", "Qian Yang", "Caiwen Ding", "Meimei Li",
              "Yuanyuan Zhu"],
    venue: "Scientific Reports 2022",
    tldr: `The first deep-learning multi-object tracker for defect clusters in in-situ irradiation TEM
      videos. It runs in real time and measured defect lifetimes more accurately and faster than four
      human experts.`,
    s2: "4c95de79ed256c1bbcb51e8d51195fc85cf2f033",
    links: { paper: "https://doi.org/10.1038/s41598-022-19697-1",
             pdf: "https://www.nature.com/articles/s41598-022-19697-1.pdf",
             github: "https://github.com/rajatsainju2025/DefectTrack",
             data: "https://figshare.com/s/9e7f6c0870e828dbc1a2" },
  },
  {
    title: "In Situ Studies of Single-Nanoparticle-Level Nickel Thermal Oxidation: From Early Oxide Nucleation to Diffusion-Balanced Oxide Thickening",
    card: { line1: "ACS Nano", line2: "Single-Nanoparticle Oxidation", tint: "sky" },
    authors: ["Rajat Sainju", "D. Rathnayake", "Haiyan Tan", "George Bollas", "A. Dongare",
              "S. Suib", "Yuanyuan Zhu"],
    venue: "ACS Nano 2022",
    tldr: `Follows the oxidation of individual 4–50 nm Ni nanoparticles in situ at 600 °C and shows how
      particle size changes the oxidation pathway, from early oxide nucleation to diffusion-balanced
      oxide thickening.`,
    s2: "7b8d7b2fede25f75cd5ea3d7a7768bd83ca3845e",
    links: { paper: "https://doi.org/10.1021/acsnano.2c00742" },
  },
  {
    title: "Direct Observation of Tungsten Oxidation Studied by In Situ Environmental TEM",
    card: { line1: "Materials Characterization", line2: "Tungsten Oxidation", tint: "slate" },
    authors: ["Maanas Togaru", "Rajat Sainju", "Lichun Zhang", "Weilin Jiang", "Yuanyuan Zhu"],
    venue: "Materials Characterization 2021",
    tldr: `The first in-situ environmental TEM study of tungsten thermal oxidation, at 500–900 °C,
      revealing two distinct oxide microstructures on pristine and ion-irradiated tungsten.`,
    s2: "4de06cf3a055f2835ede8e4fe76ba7652dfe8706",
    links: { paper: "https://doi.org/10.1016/j.matchar.2021.111016" },
  },
  {
    title: "Detecting Gender Bias in Transformer-Based Models: A Case Study on BERT",
    card: { line1: "Case Study", line2: "Gender Bias in BERT", tint: "lime" },
    authors: ["Bingbing Li", "Hongwu Peng", "Rajat Sainju", "Jun-Huan Yang", "Lei Yang", "Yue-Ying Liang",
              "Wei-Wen Jiang", "Binghui Wang", "Hang Liu", "Caiwen Ding"],
    venue: "arXiv 2021",
    tldr: `Detects gender bias in transformer models through their attention maps, and traces where
      inside BERT the bias comes from.`,
    s2: "6dbbc49afcac5830ca4aac05c577a3fca404694d",
    links: { arxiv: "https://arxiv.org/abs/2110.15733" },
  },
  {
    title: "Deep Learning for Semantic Segmentation of Defects in Advanced STEM Images of Steels",
    image: "assets/img/defectsegnet.jpg",
    authors: ["Graham Roberts", "Simon Y. Haile", "Rajat Sainju", "Danny J. Edwards", "Brian Hutchinson",
              "Yuanyuan Zhu"],
    venue: "Scientific Reports 2019",
    tldr: `DefectSegNet, a CNN that segments dislocations, precipitates and voids in DCI STEM images of
      steel, reaching 91.6–98.9% pixel accuracy from a small set of training images.`,
    s2: "d1bc2bc7e00178969a1d0b43c4f137e69e0688ab",
    links: { paper: "https://doi.org/10.1038/s41598-019-49105-0",
             github: "https://github.com/rajatsainju2025/DefectSegNet" },
  },
];

// Conference abstracts (shown in a collapsed list under Projects).
const ABSTRACTS = [
  { year: 2026, title: "Quantifying Size- and Reaction Mode-dependent Oxidation of Individual Carbon Nanotube Filaments by Spatially-resolved Operando ETEM and AI", url: "https://doi.org/10.1093/mam/ozag053.712" },
  { year: 2024, title: "Tracking Metal/Oxide Interface Evolution and Reaction Kinetics of Fusion Energy Nanostructured Tungsten Material Using In Situ ETEM", url: "https://doi.org/10.1093/mam/ozae044.856" },
  { year: 2023, title: "Deep Learning for Automated Quantification of Irradiation Defects in TEM Data: Relating Pixel-level Errors to Defect Properties", url: "https://doi.org/10.1093/micmic/ozad067.802" },
  { year: 2023, title: "In-situ Thermal Oxidation of Fusion PFM Tungsten Using Atmospheric Environmental TEM", url: "https://doi.org/10.1093/micmic/ozad067.751" },
  { year: 2023, title: "In-situ ETEM Observation of Competing Mechanisms for Filamentous Carbon Gasification", url: "https://doi.org/10.1093/micmic/ozad067.663" },
  { year: 2022, title: "Real-time Multi-Object Tracking of Ion-irradiation Induced Defects in in situ TEM Videos", url: "https://doi.org/10.1017/S1431927622007966" },
  { year: 2022, title: "Beyond In Situ ETEM Imaging: Unveiling the Size-dependent Oxidation Mechanism of Metallic Nanoparticles by Individual Nanoparticle-level Oxidation Kinetic Analysis", url: "https://doi.org/10.1017/S1431927622001532" },
  { year: 2021, title: "Deep Learning-based Computer Vision for Radiation Defect Analysis: from Static Defect Segmentation to Dynamic Defect Tracking", url: "https://doi.org/10.1017/S1431927621005419" },
  { year: 2021, title: "Tracking and Understanding Nanocatalyst Sintering and Regeneration using Deep Learning-assisted In Situ Environmental TEM", url: "https://doi.org/10.1017/S1431927621007984" },
  { year: 2020, title: "Towards an End-to-end Radiation Defect Quantitative Characterization Workflow Using Advanced Microscopy Images", url: "https://doi.org/10.1017/S1431927620016980" },
  { year: 2019, title: "DefectNet – A Deep Convolutional Neural Network for Semantic Segmentation of Crystallographic Defects in Advanced Microscopy Images", url: "https://doi.org/10.1017/S1431927619001557" },
  { year: 2019, title: "Automated Quantitative Analysis of Extended Irradiation Defects: Dislocations, Voids and Precipitates in Neutron Irradiated HT-9 Steel", url: "https://doi.org/10.1017/S1431927619008559" },
];

// Software. Star and fork counts are fetched live from GitHub (numbers here are fallbacks).
const SOFTWARE = [
  { repo: "rajatsainju2025/aps-rag", tag: "Framework", lang: "Python",
    desc: "🔎 Corrective agentic hybrid RAG for facility knowledge", stars: 1, forks: 0 },
  { repo: "rajatsainju2025/DefectTrack", tag: "Model", lang: "PyTorch",
    desc: "🎯 Real-time tracking of defects in in-situ TEM videos", stars: 0, forks: 0 },
  { repo: "rajatsainju2025/DefectSegNet", tag: "Model", lang: "TensorFlow",
    desc: "🧩 Semantic segmentation of defects in STEM images of steel", stars: 0, forks: 0 },
  { repo: "rajatsainju2025/ml-tutorial", tag: "Tutorial", lang: "Jupyter",
    desc: "📚 Beginner-friendly notebooks that build core ML step by step", stars: 0, forks: 0 },
  { repo: "rajatsainju2025/volatility-forecasting", tag: "Research", lang: "Jupyter",
    desc: "📈 Can LightGBM beat HAR and GARCH at forecasting SPY volatility?", stars: 0, forks: 0 },
];
