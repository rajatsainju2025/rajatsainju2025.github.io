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

  bio: `<p>I'm an AI/ML scientist at the <a href="https://www.aps.anl.gov/">Advanced Photon Source</a>
    at Argonne National Laboratory. I build production LLM systems, including
    <a href="https://arxiv.org/abs/2607.24663">agentic RAG</a> and
    <a href="https://arxiv.org/abs/2609.36362">AI harnesses</a>, that help run a large accelerator facility, and I develop machine learning
    for accelerators and materials science.</p>
    <p>My postdoctoral advisors at Argonne are
    <a href="https://www.anl.gov/profile/michael-david-borland">Dr. Michael Borland</a> and
    <a href="https://www.anl.gov/profile/yine-sun">Dr. Yine Sun</a>. I did my Ph.D. in Materials Science
    and Engineering at UConn with <a href="https://zhu.mse.uconn.edu">Prof. Yuanyuan Zhu</a>, where I
    developed deep learning tools, like <a href="https://github.com/rajatsainju2025/DefectTrack">DefectTrack</a>,
    that analyze in-situ electron microscopy videos in real time. Before that, I studied Engineering
    Physics at Ramapo College.</p>`,
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
    date: "Apr, 2026", image: "assets/img/news_seminar.jpg",
    text: `Invited by the Argonne Accelerator Institute (AAI) to give a
      <a href="https://www.anl.gov/aai/beams-and-applications-seminar">Beams and Applications Seminar</a>
      on AI and ML for accelerator operations.`,
  },
  {
    date: "Oct, 2025", image: "assets/img/news_gasification.jpg",
    text: `Our study of carbon gasification on a spent Ni/CeO₂ catalyst is out in
      <a href="https://doi.org/10.1021/acscatal.5c02824">ACS Catalysis</a>.`,
  },
  {
    date: "Jul, 2025", image: "assets/img/news_tpc.jpg",
    text: `Talk at <a href="https://tpc25.org">TPC25</a> in San Jose on augmenting Advanced Photon
      Source search with retrieval-augmented generation.`,
  },
  {
    date: "Jul, 2025", image: "assets/img/news_biscuit.jpg",
    text: `Talk on large language model operations for the APS at BISCUIT, the X-ray Science
      Division seminar at Argonne. 🍪`,
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
    date: "Apr, 2023", image: "assets/img/news_speaker.jpg",
    text: `Named the Spring 2023 Outstanding Graduate Student Speaker in
      <a href="https://mse.engr.uconn.edu/">Materials Science and Engineering</a> at UConn. 🎤`,
  },
  {
    date: "Feb, 2023", image: "assets/img/news_feature.jpg",
    text: `DefectTrack featured in Argonne's story
      <a href="https://www.anl.gov/article/artificial-intelligence-reframes-nuclear-material-studies">Artificial
      intelligence reframes nuclear material studies</a>.`,
  },
  {
    date: "Sep, 2022", image: "assets/img/news_defecttrack.jpg",
    text: `<a href="https://doi.org/10.1038/s41598-022-19697-1">DefectTrack</a>, real-time tracking of
      defects in in-situ TEM videos, published in Scientific Reports.`,
  },
  {
    date: "Aug, 2022", image: "assets/img/news_scholar.jpg",
    text: `Won an <a href="https://microscopy.org/2022-M-M-Student-Scholars">M&amp;M 2022 Student Scholar
      Award</a> for real-time tracking of irradiation defects in in-situ TEM videos. 🏆`,
  },
  {
    date: "Apr, 2022", image: "assets/img/news_oxidation.jpg",
    text: `Single-nanoparticle Ni oxidation, from nucleation to thickening, published in
      <a href="https://doi.org/10.1021/acsnano.2c00742">ACS Nano</a>.`,
  },
  {
    date: "Aug, 2021", image: "assets/img/news_mm2021.jpg",
    text: `Presented deep learning-assisted in-situ ETEM of
      <a href="https://doi.org/10.1017/S1431927621007984">nanocatalyst sintering and regeneration</a>
      at M&amp;M 2021.`,
  },
  {
    date: "Mar, 2021", image: "assets/img/news_matchar.jpg",
    text: `Tungsten oxidation watched in situ by environmental TEM, led by Maanas Togaru, published in
      <a href="https://doi.org/10.1016/j.matchar.2021.111016">Materials Characterization</a>.`,
  },
  {
    date: "Sep, 2020", image: "assets/img/news_doe.jpg",
    text: `DefectSegNet featured by the DOE Office of Science:
      <a href="https://www.energy.gov/science/fes/articles/ai-helps-scientists-quantify-irradiation-effects">AI
      helps scientists quantify irradiation effects</a>.`,
  },
  {
    date: "Mar, 2020", image: "assets/img/news_top100.jpg",
    text: `DefectSegNet made the Scientific Reports
      <a href="https://www.nature.com/collections/ecjehiebic">Top 100 in Materials Science</a> of 2019. 🎉`,
  },
  {
    date: "Sep, 2019", image: "assets/img/news_segmentation.jpg",
    text: `<a href="https://doi.org/10.1038/s41598-019-49105-0">DefectSegNet</a>, deep learning
      segmentation of defects in steel, published in Scientific Reports.`,
  },
];

// Projects / publications, newest first.
// image:  thumbnail shown in the list (assets/img/thumbs/)
// figure: full figure opened on click (assets/img/figs/), with figCaption
// s2:     Semantic Scholar paper id or "DOI:..." — used for the live citation count
const PROJECTS = [
  {
    title: "Strategies for Deploying AI Agents in Production at Scientific User Facilities",
    more: true,   // listed only after "Show all"
    image: "assets/img/thumbs/ai_agents.jpg", figure: "assets/img/figs/ai_agents.jpg",
    figCaption: "Agent harnesses (general, data analysis, experiment control) call tools and skills through the APS Tool/Skill Hub.",
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
    title: "APS-RAG: A Corrective Agentic Hybrid RAG and an Operations-Grounded Evaluation for a Scientific Facility",
    image: "assets/img/thumbs/apsrag.jpg", figure: "assets/img/figs/apsrag.png", figCaption: "Fig. 1: APS-RAG deployment overview.",
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
    title: "A Domain-Aware Hybrid Retrieval Augmented Generation System for Accelerator Operations and Knowledge Synthesis",
    image: "assets/img/thumbs/ipac26_apsrag_v2.jpg", figure: "assets/img/figs/ipac26_apsrag_v2.jpg",
    figCaption: "Illustration based on the paper: four APS sources indexed for dense and BM25 search, fused with RRF, reranked, and synthesized into a cited answer.",
    authors: ["Rajat Sainju", "Dariusz Jarosz", "Hairong Shang", "Michael Prince", "Ryan M. Aydelott",
              "Mathew J. Cherukara", "Yine Sun", "Michael Borland"],
    venue: "IPAC'26",
    tldr: `The production version of APS-RAG at the Advanced Photon Source: hybrid dense and BM25 retrieval
      with reciprocal-rank fusion and cross-encoder reranking over more than 10,000 documents from the
      BELY logbook, Teams operations chats, ICMS and work requests, with every answer linked back to its
      source records.`,
    s2: "",
    links: { pdf: "https://indico.jacow.org/event/95/contributions/14256/attachments/2311/8525/MOP6302_edited_version.pdf",
             github: "https://github.com/rajatsainju2025/aps-rag" },
  },
  {
    title: "Leveraging Low-Cost Sensors and Machine Learning for Pump Anomaly Detection in Accelerator Facilities",
    image: "assets/img/thumbs/ipac26_pumps_v2.jpg", figure: "assets/img/figs/ipac26_pumps_v2.jpg",
    figCaption: "Illustration based on the paper: a vibration sensor on a cooling pump streams to an edge node; an autoencoder scores anomalies shown on a web dashboard.",
    authors: ["Rajat Sainju", "O. Mohsen", "J. Ackley", "J. Fuerst", "R. Wright", "Yine Sun", "Michael Borland"],
    venue: "IPAC'26",
    tldr: `Low-cost vibration sensors on a helium pump and storage-ring cooling-water pumps stream data to
      Linux edge nodes; an autoencoder flags anomalies every hour and a web dashboard shows trends,
      spectrograms and spectra. In the pilot at the APS, rolling weekly baselines and consistent sensor
      mounting mattered more than model tweaks.`,
    s2: "",
    links: { pdf: "https://indico.jacow.org/event/95/contributions/14437/attachments/2279/8431/MOP6303_edited_version.pdf" },
  },
  {
    title: "Operando Elucidation of Filamentous Carbon Gasification Kinetics and Mechanisms on a Spent Ni/CeO₂ Catalyst",
    more: true,   // listed only after "Show all"
    image: "assets/img/thumbs/gasification.jpg", figure: "assets/img/figs/gasification.jpg",
    figCaption: "Fig. 1: Filamentous carbon evolution and gasification kinetics in operando ETEM, revealing three gasification modes.",
    authors: ["Monia R. Nielsen", "Tianyu Li", "Rajat Sainju", "Seth March", "Chunxiang Zhu", "Pu-Xian Gao",
              "Steven L. Suib", "Yuanyuan Zhu"],
    venue: "ACS Catalysis 2025",
    tldr: `Watches a spent Ni/CeO₂ catalyst being regenerated in air inside an environmental TEM and, with
      semantic segmentation, separates three ways its carbon filaments burn off: catalytic, noncatalytic
      and cooperative. The last two turn out to be more common than expected, and catalytic gasification
      is limited by carbon diffusion through Ni(−Cₓ) rather than the usual bulk-diffusion model.`,
    s2: "d19916428af24c32501704a731dd656bf2c1e9d0",
    links: { paper: "https://doi.org/10.1021/acscatal.5c02824" },
  },
  {
    title: "Application of Low-Cost Sensors and Deep Autoencoders for Monitoring Water Pumps in Particle Accelerators",
    image: "assets/img/thumbs/napac2025_art.jpg", figure: "assets/img/figs/napac2025_pumps.jpg",
    figCaption: "Fig. 4a: Transformer-based autoencoder for real-time vibration monitoring.",
    authors: ["Rajat Sainju", "O. Mohsen", "Michael Borland", "Yine Sun"],
    venue: "NAPAC 2025",
    tldr: `A low-cost vibration sensor and a Raspberry Pi stream cooling-water pump vibrations to a
      transformer autoencoder that learns each pump's normal behaviour and flags anomalies. Trained with
      physics-based synthetic faults, it aims to catch pump failures before they cause downtime at the APS.`,
    s2: "",
    links: { paper: "https://doi.org/10.18429/JACoW-NAPAC2025-WEP006" },
  },
  {
    title: "Advanced Ex-situ and In-situ Electron Microscopy Characterization of Fusion Plasma-Facing Tungsten Oxidation",
    image: "assets/img/thumbs/mm2025_tungsten.jpg", figure: "assets/img/figs/mm2025_tungsten.jpg",
    figCaption: "Fig. 1: Ex-situ SEM, AFM and TEM characterization of orientation-dependent W oxidation.",
    authors: ["Rajat Sainju", "Amutheesan Jeyaveerasigamani", "Marlene Patino", "Adanma Akoma", "Bryan Huey",
              "Matthew Baldwin", "Osman El Atwani", "Robert Kolasinski", "Yuanyuan Zhu"],
    venue: "Microscopy & Microanalysis 2025",
    tldr: `Combines SEM, AFM, EBSD and TEM with in-situ ETEM to show that tungsten oxidation depends on grain
      orientation, and that He-plasma nanofuzz oxidizes more slowly than bulk W because a durable
      amorphous surface oxide passivates it.`,
    s2: "DOI:10.1093/mam/ozaf048.775",
    links: { paper: "https://doi.org/10.1093/mam/ozaf048.775" },
  },
  {
    title: "Operando Spatially and Time-Resolved Reduction of Hollow Polycrystalline NiO: How to Promote Ni Nanoparticle Redispersion",
    image: "assets/img/thumbs/ni_redispersion.jpg", figure: "assets/img/figs/ni_redispersion.jpg",
    figCaption: "Fig. 2: A lower reduction temperature of 450 °C enhances the redispersion of hollow NiO.",
    authors: ["Rajat Sainju", "Tianyu Li", "Monia R. Nielsen", "Yuanyuan Zhu"],
    venue: "Nano Letters 2025",
    tldr: `Follows hollow NiO grains being reduced in an environmental TEM and measures their kinetics with
      semantic segmentation. A milder 450 °C reduction slows and desynchronizes neighbouring grains, which
      breaks the oxide into more, smaller Ni particles: redispersion needs both a hollow oxide and slow,
      asynchronous reduction.`,
    s2: "18dc0f899b48fb5387514a67bfc8fd82175ff5e0",
    links: { paper: "https://doi.org/10.1021/acs.nanolett.5c02133" },
  },
  {
    title: "In-situ ETEM Study of Plasma-Facing Tungsten Nanofuzz Oxidation at Atmospheric Pressure: Microstructure Evolution and Substrate-Free Oxidation Kinetics",
    image: "assets/img/thumbs/acta_nanofuzz.jpg", figure: "assets/img/figs/acta_nanofuzz.jpg",
    figCaption: "Fig. 1: W nanofuzz and the in-situ environmental TEM gas cell used to oxidize it in 1 bar dry air.",
    authors: ["Rajat Sainju", "Marlene Patino", "Matthew J. Baldwin", "Osman El Atwani", "Robert Kolasinski",
              "Yuanyuan Zhu"],
    venue: "Acta Materialia 2024",
    tldr: `The first oxidation kinetics for substrate-free tungsten nanofuzz, measured in 1 bar dry air at
      400 and 500 °C inside an environmental TEM. Nanofuzz oxidizes more slowly than bulk W: a durable
      amorphous surface oxide, likely promoted by He-plasma surface damage, acts as a passivating layer.`,
    s2: "dc2a192d30a60e1b700acc9d409935fc9ca5b014",
    links: { paper: "https://doi.org/10.1016/j.actamat.2024.120282" },
  },
  {
    title: "Tracking Metal/Oxide Interface Evolution and Reaction Kinetics of Fusion Energy Nanostructured Tungsten Material Using In Situ ETEM",
    image: "assets/img/thumbs/mm2024_nanofuzz.jpg", figure: "assets/img/figs/mm2024_nanofuzz.jpg",
    figCaption: "Fig. 2: ETEM setup and analysis used to measure the oxidation kinetics of individual W nanofuzz.",
    authors: ["Rajat Sainju", "Marlene Patino", "Matthew Baldwin", "Osman El Atwani", "Yuanyuan Zhu"],
    venue: "Microscopy & Microanalysis 2024",
    tldr: `Conventional TGA can't separate a 1 µm nanofuzz layer from its 1 mm substrate, so we load single
      tungsten nanofuzz tendrils into an environmental TEM and segment metal, oxide and He bubbles to get
      the first nanofuzz-specific oxidation kinetics.`,
    s2: "DOI:10.1093/mam/ozae044.856",
    links: { paper: "https://doi.org/10.1093/mam/ozae044.856" },
  },
  {
    title: "Deep Learning for Automated Quantification of Irradiation Defects in TEM Data: Relating Pixel-level Errors to Defect Properties",
    image: "assets/img/thumbs/mm2023_defectquant.jpg", figure: "assets/img/figs/mm2023_defectquant.jpg",
    figCaption: "Fig. 1: Segmentation and quantification by DefectSegNet + DefectQuant, evaluated with computer-vision and defect-property metrics.",
    authors: ["Rajat Sainju", "Graham Roberts", "Wei-Ying Chen", "Brian Hutchinson", "Qian Yang", "Caiwen Ding",
              "Danny J. Edwards", "Meimei Li", "Yuanyuan Zhu"],
    venue: "Microscopy & Microanalysis 2023",
    tldr: `Evaluates DefectSegNet and DefectTrack with the materials-science numbers that matter (defect
      density, size and lifetime distributions) alongside standard pixel-level computer-vision metrics,
      and studies how the two kinds of metric relate.`,
    s2: "DOI:10.1093/micmic/ozad067.802",
    links: { paper: "https://doi.org/10.1093/micmic/ozad067.802" },
  },
  {
    title: "In-situ Thermal Oxidation of Fusion PFM Tungsten Using Atmospheric Environmental TEM",
    image: "assets/img/thumbs/mm2023_tungsten.jpg", figure: "assets/img/figs/mm2023_tungsten.jpg",
    figCaption: "Fig. 1: In-situ ETEM setup for tungsten oxidation and surface thickness mapped by EELS.",
    authors: ["Rajat Sainju", "Maanas Togaru", "Lichun Zhang", "Weilin Jiang", "Wahyu Setyawan", "Osman El Atwani",
              "Yuanyuan Zhu"],
    venue: "Microscopy & Microanalysis 2023",
    tldr: `In-situ ETEM oxidation of pristine and ion-irradiated fusion-grade tungsten at up to 1 bar.
      Thinner grains in the TEM foil did not oxidize faster, and in-situ diffraction caught the
      high-temperature orthorhombic WO₃ that post-mortem studies miss.`,
    s2: "DOI:10.1093/micmic/ozad067.751",
    links: { paper: "https://doi.org/10.1093/micmic/ozad067.751" },
  },
  {
    title: "In-situ ETEM Observation of Competing Mechanisms for Filamentous Carbon Gasification",
    image: "assets/img/thumbs/mm2023_gasification.jpg", figure: "assets/img/figs/mm2023_gasification.jpg",
    figCaption: "Fig. 2: In-situ ETEM filamentous carbon gasification, suggesting a new competing mechanism.",
    authors: ["Monia R. Nielsen", "Seth March", "Rajat Sainju", "Chunxiang Zhu", "Pu-Xian Gao", "Steven L. Suib",
              "Yuanyuan Zhu"],
    venue: "Microscopy & Microanalysis 2023",
    tldr: `Watching carbon filaments burn off a spent Ni-W/CeO₂ catalyst at 750 °C shows that carbon can
      gasify even without touching the catalyst, so several competing mechanisms are at play during
      catalyst regeneration.`,
    s2: "DOI:10.1093/micmic/ozad067.663",
    links: { paper: "https://doi.org/10.1093/micmic/ozad067.663" },
  },
  {
    title: "DefectTrack: A Deep Learning-Based Multi-Object Tracking Algorithm for Quantitative Defect Analysis of In-situ TEM Videos in Real-Time",
    image: "assets/img/thumbs/defecttrack.jpg", figure: "assets/img/figs/defecttrack.jpg",
    figCaption: "Fig. 3: Overview of the DefectTrack network: backbone, detection branch and tracking module.",
    authors: ["Rajat Sainju", "Wei-Ying Chen", "Samuel Schaefer", "Qian Yang", "Caiwen Ding", "Meimei Li",
              "Yuanyuan Zhu"],
    venue: "Scientific Reports 2022",
    tldr: `The first deep-learning multi-object tracker for defect clusters in in-situ irradiation TEM videos.
      It reaches a MOTA of 66.4%, runs in real time, and measured defect lifetimes more accurately and
      faster than four human experts.`,
    s2: "4c95de79ed256c1bbcb51e8d51195fc85cf2f033",
    links: { paper: "https://doi.org/10.1038/s41598-022-19697-1",
             pdf: "https://www.nature.com/articles/s41598-022-19697-1.pdf",
             github: "https://github.com/rajatsainju2025/DefectTrack",
             data: "https://figshare.com/s/9e7f6c0870e828dbc1a2" },
  },
  {
    title: "Real-time Multi-Object Tracking of Ion-irradiation Induced Defects in in situ TEM Videos",
    image: "assets/img/thumbs/mm2022_realtime.jpg", figure: "assets/img/figs/mm2022_realtime.jpg",
    figCaption: "Fig. 1: DefectTrack's tracked defect clusters and their lifetimes during irradiation of nickel.",
    authors: ["Rajat Sainju", "Wei-Ying Chen", "Samuel Schaefer", "Qian Yang", "Caiwen Ding", "Meimei Li",
              "Yuanyuan Zhu"],
    venue: "Microscopy & Microanalysis 2022",
    tldr: `DefectTrack follows ion-irradiation defect clusters at 28 frames per second. Compared with human
      experts it is about 100 times faster and analyzes 25 times more defect clusters, with a lifetime
      distribution that matches the ground truth.`,
    s2: "DOI:10.1017/S1431927622007966",
    links: { paper: "https://doi.org/10.1017/S1431927622007966" },
  },
  {
    title: "Beyond In Situ ETEM Imaging: Unveiling the Size-dependent Oxidation Mechanism of Metallic Nanoparticles by Individual Nanoparticle-level Oxidation Kinetic Analysis",
    image: "assets/img/thumbs/mm2022_ni.jpg", figure: "assets/img/figs/mm2022_ni.jpg",
    figCaption: "Fig. 1: Collective (diffraction-based) versus single-nanoparticle (image-based) oxidation kinetics.",
    authors: ["Rajat Sainju", "Dinithi Rathnayake", "Haiyan Tan", "George Bollas", "Avinash M. Dongare",
              "Steven L. Suib", "Yuanyuan Zhu"],
    venue: "Microscopy & Microanalysis 2022",
    tldr: `Compares collective and single-particle oxidation kinetics for 207 Ni nanoparticles, and shows
      that averaging over particles of different sizes can skew which kinetic model appears to fit.`,
    s2: "DOI:10.1017/S1431927622001532",
    links: { paper: "https://doi.org/10.1017/S1431927622001532" },
  },
  {
    title: "In Situ Studies of Single-Nanoparticle-Level Nickel Thermal Oxidation: From Early Oxide Nucleation to Diffusion-Balanced Oxide Thickening",
    image: "assets/img/thumbs/ni_oxidation.jpg", figure: "assets/img/figs/ni_oxidation.jpg",
    figCaption: "Fig. 2: Size-dependent Ni nanoparticle oxidation and the resulting NiO morphology.",
    authors: ["Rajat Sainju", "Dinithi Rathnayake", "Haiyan Tan", "George Bollas", "Avinash M. Dongare",
              "Steven L. Suib", "Yuanyuan Zhu"],
    venue: "ACS Nano 2022",
    tldr: `Tracks the oxidation of individual 4–50 nm Ni nanoparticles at 600 °C in an environmental TEM. A
      two-stage model explains the size dependence: NiO nucleation first, then diffusion-balanced shell
      thickening, which in larger particles leaves hollow NiO.`,
    s2: "7b8d7b2fede25f75cd5ea3d7a7768bd83ca3845e",
    links: { paper: "https://doi.org/10.1021/acsnano.2c00742" },
  },
  {
    title: "Detecting Gender Bias in Transformer-Based Models: A Case Study on BERT",
    more: true,   // listed only after "Show all"
    image: "assets/img/thumbs/bert.jpg", figure: "assets/img/figs/bert.jpg",
    figCaption: "Fig. 1: Gender-swapped sentences and the attention between pronouns and occupations.",
    authors: ["Bingbing Li", "Hongwu Peng", "Rajat Sainju", "Yueying Liang", "Junhuan Yang", "Lei Yang",
              "Weiwen Jiang", "Binghui Wang", "Hang Liu", "Caiwen Ding"],
    venue: "arXiv 2021",
    tldr: `Detects gender bias in BERT through its attention maps and traces where it comes from: the query
      and key matrices add the most bias, and the bias rises and falls periodically through the layers.`,
    s2: "6dbbc49afcac5830ca4aac05c577a3fca404694d",
    links: { arxiv: "https://arxiv.org/abs/2110.15733" },
  },
  {
    title: "Deep Learning-based Computer Vision for Radiation Defect Analysis: from Static Defect Segmentation to Dynamic Defect Tracking",
    image: "assets/img/thumbs/mm2021_defects.jpg", figure: "assets/img/figs/mm2021_defects.jpg",
    figCaption: "Fig. 1: Defect quantification by computer (DefectSegNet + DefectQuant) versus human experts.",
    authors: ["Rajat Sainju", "Wei-Ying Chen", "Samuel Schaefer", "Graham Roberts", "Mychailo Toloczko",
              "Danny Edwards", "Meimei Li", "Yuanyuan Zhu"],
    venue: "Microscopy & Microanalysis 2021",
    tldr: `Two studies: DefectSegNet quantifies static radiation defects in seconds, more reproducibly than
      human experts, and an annotation pipeline for in-situ TEM videos lays the groundwork for tracking how
      defect clusters evolve during irradiation.`,
    s2: "DOI:10.1017/S1431927621005419",
    links: { paper: "https://doi.org/10.1017/S1431927621005419" },
  },
  {
    title: "Direct Observation of Tungsten Oxidation Studied by In Situ Environmental TEM",
    more: true,   // listed only after "Show all"
    image: "assets/img/thumbs/matchar_tungsten.jpg", figure: "assets/img/figs/matchar_tungsten.jpg",
    figCaption: "Fig. 3: Two oxide scale regions on un-irradiated W{27-1} at 600–800 °C and their oxide phases.",
    authors: ["Maanas Togaru", "Rajat Sainju", "Lichun Zhang", "Weilin Jiang", "Yuanyuan Zhu"],
    venue: "Materials Characterization 2021",
    tldr: `The first in-situ environmental TEM observation of tungsten thermal oxidation, at 500–900 °C and
      1 bar. Both the oxide microstructure and how fast it grows depend strongly on the orientation of the
      tungsten surface.`,
    s2: "4de06cf3a055f2835ede8e4fe76ba7652dfe8706",
    links: { paper: "https://doi.org/10.1016/j.matchar.2021.111016" },
  },
  {
    title: "Towards an End-to-end Radiation Defect Quantitative Characterization Workflow Using Advanced Microscopy Images",
    image: "assets/img/thumbs/mm2020_workflow.jpg", figure: "assets/img/figs/mm2020_workflow.jpg",
    figCaption: "Fig. 1: End-to-end workflow: defect imaging, recognition and quantification.",
    authors: ["Rajat Sainju", "Graham Roberts", "Colin Ophus", "Brian Hutchinson", "Jing Wang",
              "Mychailo B. Toloczko", "Richard J. Kurtz", "Charles H. Henager Jr.", "Danny J. Edwards", "Yuanyuan Zhu"],
    venue: "Microscopy & Microanalysis 2020",
    tldr: `An end-to-end workflow for radiation-defect analysis: DCI STEM imaging, DefectSegNet segmentation
      and DefectQuant measurement. It is accurate, reproducible and at least two orders of magnitude faster
      than human experts.`,
    s2: "DOI:10.1017/S1431927620016980",
    links: { paper: "https://doi.org/10.1017/S1431927620016980" },
  },
  {
    title: "Deep Learning for Semantic Segmentation of Defects in Advanced STEM Images of Steels",
    image: "assets/img/thumbs/defectsegnet.jpg", figure: "assets/img/figs/defectsegnet.jpg",
    figCaption: "Fig. 4: The DefectSegNet architecture, with dense connections within and across encoder and decoder.",
    authors: ["Graham Roberts", "Simon Y. Haile", "Rajat Sainju", "Danny J. Edwards", "Brian Hutchinson",
              "Yuanyuan Zhu"],
    venue: "Scientific Reports 2019",
    tldr: `DefectSegNet, a CNN that segments dislocations, precipitates and voids in DCI STEM images of
      steel, reaching 91.6–98.9% pixel accuracy from a small set of training images. Defect measurements
      from its output beat the human-expert average.`,
    s2: "d1bc2bc7e00178969a1d0b43c4f137e69e0688ab",
    links: { paper: "https://doi.org/10.1038/s41598-019-49105-0",
             github: "https://github.com/rajatsainju2025/DefectSegNet" },
  },
  {
    title: "DefectNet – A Deep Convolutional Neural Network for Semantic Segmentation of Crystallographic Defects in Advanced Microscopy Images",
    image: "assets/img/thumbs/mm2019_defectnet.jpg", figure: "assets/img/figs/mm2019_defectnet.jpg",
    figCaption: "Fig. 1: DefectNet segmentation of dislocations, precipitates and voids.",
    authors: ["Graham Roberts", "Rajat Sainju", "Brian Hutchinson", "Mychailo B. Toloczko", "Danny J. Edwards",
              "Yuanyuan Zhu"],
    venue: "Microscopy & Microanalysis 2019",
    tldr: `The first version of DefectSegNet: a CNN that segments dislocations, precipitates and voids in
      DCI STEM images, reaching 94.6% average pixel accuracy from a small labelled set.`,
    s2: "DOI:10.1017/S1431927619001557",
    links: { paper: "https://doi.org/10.1017/S1431927619001557" },
  },
  {
    title: "Automated Quantitative Analysis of Extended Irradiation Defects: Dislocations, Voids and Precipitates in Neutron Irradiated HT-9 Steel",
    image: "assets/img/thumbs/mm2019_quant.jpg", figure: "assets/img/figs/mm2019_quant.jpg",
    figCaption: "Fig. 1: DCI STEM images of dislocations, voids and precipitates, with grain area and volume.",
    authors: ["Rajat Sainju", "Colin Ophus", "Mychailo B. Toloczko", "Danny J. Edwards", "Yuanyuan Zhu"],
    venue: "Microscopy & Microanalysis 2019",
    tldr: `MATLAB algorithms that automatically measure dislocation density (an optimized circular-grid
      method) and void and precipitate sizes (a modified Hough transform that separates overlapping
      particles) in neutron-irradiated HT-9 steel.`,
    s2: "DOI:10.1017/S1431927619008559",
    links: { paper: "https://doi.org/10.1017/S1431927619008559" },
  },
];

// Conference abstracts without a figure on the site (shown in a collapsed list under Projects).
const ABSTRACTS = [
  { year: 2026, title: "Quantifying Size- and Reaction Mode-dependent Oxidation of Individual Carbon Nanotube Filaments by Spatially-resolved Operando ETEM and AI", url: "https://doi.org/10.1093/mam/ozag053.712" },
  { year: 2021, title: "Tracking and Understanding Nanocatalyst Sintering and Regeneration using Deep Learning-assisted In Situ Environmental TEM", url: "https://doi.org/10.1017/S1431927621007984" },
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
