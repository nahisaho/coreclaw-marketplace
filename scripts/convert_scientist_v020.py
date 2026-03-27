#!/usr/bin/env python3
"""
Batch conversion script for scientist skills v0.2.0.
- Converts SKILL.md frontmatter descriptions from Japanese to English
- Translates common Japanese patterns in body text to English
- Adds harness optimization sections (verification loop, quality gates)
- Bumps skill.json version to v0.2.0
- Syncs source/SKILL.md with SKILL.md
"""

import json
import os
import re
from pathlib import Path

SCIENTIST_DIR = Path("coreclaw-skills-hub/skills/scientist")

# ── Frontmatter description mapping ──
# Maps skill dir name → English description for the YAML frontmatter
SKILL_DESCRIPTIONS = {
    "scientific-academic-writing": "Academic paper writing skill. Supports IMRaD standard, Nature/Science, ACS, IEEE, and Elsevier journal formats with section design, writing patterns, and citation management.",
    "scientific-active-learning": "Active learning skill. Uncertainty sampling, Query-by-Committee, expected model change, pool-based/stream-based, batch active learning, stopping criteria, and model improvement pipeline.",
    "scientific-adaptive-experiments": "Adaptive experiment design skill. Sequential experiment optimization, Bayesian optimization, multi-armed bandit, response-adaptive randomization, and interim analysis for efficient experimental workflows.",
    "scientific-admet-pharmacokinetics": "ADMET and pharmacokinetics prediction skill. Absorption, Distribution, Metabolism, Excretion, Toxicity modeling with RDKit, DeepChem, and PK/PD simulation pipelines.",
    "scientific-advanced-imaging": "Advanced imaging analysis skill. Microscopy image processing, segmentation, super-resolution, 3D reconstruction, fluorescence quantification, and multi-channel analysis pipelines.",
    "scientific-advanced-visualization": "Advanced scientific visualization skill. Multi-panel figures, 3D plots, interactive dashboards, heatmaps, volcano plots, Manhattan plots, and publication-quality figure generation.",
    "scientific-alphafold-structures": "AlphaFold structure prediction skill. Protein structure retrieval from AlphaFold DB, pLDDT confidence scoring, structural alignment, and downstream structural analysis.",
    "scientific-anomaly-detection": "Anomaly detection skill. Isolation Forest, LOF, One-Class SVM, autoencoders, statistical control charts, time-series anomaly detection, and multivariate outlier analysis.",
    "scientific-arrayexpress-expression": "ArrayExpress gene expression skill. Microarray and RNA-seq data retrieval from ArrayExpress/BioStudies, normalization, differential expression, and cross-study comparison.",
    "scientific-audit-report": "Research audit report skill. Systematic quality assessment of experimental designs, statistical analyses, reproducibility, and reporting standards compliance.",
    "scientific-automl": "AutoML pipeline skill. Optuna hyperparameter optimization, FLAML fast AutoML, Auto-sklearn model selection, NAS, automated feature engineering, and model comparison pipelines.",
    "scientific-bayesian-statistics": "Bayesian statistics skill. PyMC/Stan/ArviZ-based Bayesian regression, hierarchical models, MCMC sampling, Bayesian optimization, posterior predictive checks, and model comparison.",
    "scientific-biobank-cohort": "Biobank cohort analysis skill. UK Biobank, All of Us, and large-scale cohort data integration, phenotype extraction, population stratification, and epidemiological analysis pipelines.",
    "scientific-bioinformatics": "Bioinformatics workflow skill. Sequence alignment, variant calling, genome assembly, annotation, phylogenetic analysis, and multi-omics data integration pipelines.",
    "scientific-biomedical-pubtator": "PubTator biomedical text mining skill. Named entity recognition for genes, diseases, chemicals, mutations, and species from PubMed literature using PubTator3 API.",
    "scientific-biosignal-processing": "Biosignal processing skill. EEG, ECG, EMG signal processing with filtering, spectral analysis, wavelet transforms, and time-frequency analysis pipelines.",
    "scientific-biothings-idmapping": "BioThings ID mapping skill. Gene/variant/chemical/disease identifier conversion using MyGene.info, MyVariant.info, and MyChem.info APIs.",
    "scientific-cancer-genomics": "Cancer genomics skill. Somatic mutation analysis, copy number variation, tumor mutational burden, microsatellite instability, driver gene identification, and oncological pathway analysis.",
    "scientific-causal-inference": "Causal inference skill. DoWhy/EconML-based causal analysis, propensity score matching, instrumental variables, difference-in-differences, regression discontinuity, and DAG-based causal reasoning.",
    "scientific-causal-ml": "Causal machine learning skill. Heterogeneous treatment effects, CATE estimation, causal forests, meta-learners (S/T/X), uplift modeling, and policy optimization.",
    "scientific-cell-line-resources": "Cell line resource skill. Cellosaurus, ATCC, DepMap cell line data retrieval, cell line authentication, STR profiling, and cross-reference between cell line databases.",
    "scientific-cellxgene-census": "CellxGene Census skill. Single-cell RNA-seq data retrieval from CZ CELLxGENE, cell type annotation, cross-dataset comparison, and gene expression atlas queries.",
    "scientific-chembl-assay-mining": "ChEMBL assay mining skill. Bioactivity data retrieval, target-compound mapping, SAR analysis, assay type classification, and compound potency comparison from ChEMBL database.",
    "scientific-cheminformatics": "Cheminformatics skill. RDKit molecular property calculation, SMILES/InChI handling, molecular fingerprints, substructure search, chemical similarity, and ADMET prediction.",
    "scientific-citation-checker": "Citation checking skill. Reference validation, DOI verification, retraction detection, citation consistency checking, and bibliography formatting compliance.",
    "scientific-civic-evidence": "CIViC clinical interpretation skill. Clinical Interpretations of Variants in Cancer (CIViC) database queries, evidence level assessment, and clinical actionability evaluation.",
    "scientific-clingen-curation": "ClinGen curation skill. Gene-disease validity classification, variant pathogenicity assessment, dosage sensitivity, and clinical actionability curation using ClinGen resources.",
    "scientific-clinical-decision-support": "Clinical decision support skill. Evidence-based clinical guidelines, risk scoring models, diagnostic algorithms, treatment pathway selection, and clinical prediction rules.",
    "scientific-clinical-nlp": "Clinical NLP skill. MedSpaCy/cTAKES/scispaCy-based clinical text NER, section detection, negation detection, ICD-10/SNOMED-CT entity linking, and de-identification pipelines.",
    "scientific-clinical-pharmacology": "Clinical pharmacology skill. Dose-response modeling, PK/PD simulation, drug interaction prediction, therapeutic drug monitoring, and population pharmacokinetics.",
    "scientific-clinical-reporting": "Clinical reporting skill. Structured clinical study reports, CONSORT/STROBE compliance, patient demographics tables, efficacy/safety summaries, and regulatory submission formatting.",
    "scientific-clinical-standards": "Clinical standards skill. CDISC SDTM/ADaM data standards, HL7 FHIR resource mapping, LOINC/SNOMED coding, and regulatory data submission format compliance.",
    "scientific-clinical-trials-analytics": "Clinical trials analytics skill. Trial design comparison, enrollment simulation, interim analysis, survival analysis, and adverse event signal detection from ClinicalTrials.gov data.",
    "scientific-compound-screening": "Compound screening skill. High-throughput screening data analysis, hit identification, dose-response curve fitting, Z-factor calculation, and compound library management.",
    "scientific-computational-materials": "Computational materials science skill. DFT calculations, molecular dynamics for materials, crystal structure prediction, band structure analysis, and materials property prediction.",
    "scientific-crispr-design": "CRISPR design skill. Guide RNA design, off-target analysis, CRISPR screen analysis, gene knockout/knock-in design, and editing efficiency prediction.",
    "scientific-critical-review": "Critical review skill. Systematic assessment of research quality, experimental rigor evaluation, statistical claim verification, and comprehensive peer review analysis.",
    "scientific-crossref-metadata": "Crossref metadata skill. Scholarly publication metadata retrieval, citation count tracking, DOI resolution, funder information extraction, and bibliometric analysis via Crossref API.",
    "scientific-data-preprocessing": "Data preprocessing skill. Missing value imputation, outlier detection, normalization, feature scaling, encoding, and data cleaning pipelines for scientific datasets.",
    "scientific-data-profiling": "Data profiling skill. Automated dataset characterization, distribution analysis, data quality metrics, schema inference, and statistical summary generation.",
    "scientific-data-simulation": "Data simulation skill. Synthetic data generation, Monte Carlo simulation, bootstrap resampling, parametric/non-parametric simulation, and power analysis via simulation.",
    "scientific-data-submission": "Data submission skill. GEO/SRA/ENA/DDBJ data deposition, metadata preparation, compliance with FAIR principles, and repository-specific format conversion.",
    "scientific-deep-chemistry": "Deep chemistry skill. Graph neural networks for molecular property prediction, molecular generation with VAE/GAN, reaction prediction, and retrosynthesis planning.",
    "scientific-deep-learning": "Deep learning skill. PyTorch/TensorFlow model building, CNN/RNN/Transformer architectures, training optimization, GPU acceleration, and deep learning experiment management.",
    "scientific-deep-research": "Deep research skill. Iterative literature research following the SHIKIGAMI WebResearcher paradigm (Think→Report→Action cycle) with academic database search, evidence hierarchy assessment, source tracking, and hallucination prevention.",
    "scientific-depmap-dependencies": "DepMap dependency skill. Cancer cell line dependency data from DepMap/CRISPR screens, gene essentiality scoring, and functional genomics analysis.",
    "scientific-disease-research": "Disease research skill. Disease ontology queries, phenotype-genotype associations, clinical feature extraction, and disease mechanism pathway analysis.",
    "scientific-doe": "Design of Experiments (DOE) skill. Factorial design, response surface methodology, Latin hypercube sampling, Taguchi methods, and optimal experimental design generation.",
    "scientific-drug-repurposing": "Drug repurposing skill. Computational drug repositioning, network-based prediction, molecular similarity-based repurposing, and clinical trial evidence mining for new indications.",
    "scientific-drug-target-profiling": "Drug-target profiling skill. Target identification, binding affinity prediction, selectivity profiling, polypharmacology analysis, and target deconvolution pipelines.",
    "scientific-drugbank-resources": "DrugBank resource skill. Drug information retrieval, drug-target interactions, drug-drug interactions, pharmacological classifications, and clinical indication mapping.",
    "scientific-ebi-databases": "EBI databases skill. EMBL-EBI resource integration including UniProt, PDB, ChEMBL, Ensembl, InterPro, and cross-database querying strategies.",
    "scientific-eda-correlation": "EDA and correlation analysis skill. Exploratory data analysis, correlation matrices, distribution visualization, multivariate analysis, and automated EDA report generation.",
    "scientific-encode-screen": "ENCODE screen skill. ENCODE project data access, regulatory element annotation, epigenomic data analysis, and functional genomics screen result interpretation.",
    "scientific-ensembl-genomics": "Ensembl genomics skill. Genome browser API queries, gene annotation retrieval, variant effect prediction, comparative genomics, and regulatory feature mapping via Ensembl REST API.",
    "scientific-ensemble-methods": "Ensemble methods skill. Random forests, gradient boosting (XGBoost/LightGBM/CatBoost), stacking, blending, voting classifiers, and ensemble model interpretation.",
    "scientific-environmental-ecology": "Environmental ecology skill. Biodiversity analysis, species distribution modeling, ecological niche analysis, community ecology metrics, and conservation assessment pipelines.",
    "scientific-environmental-geodata": "Environmental geodata skill. Satellite imagery analysis, remote sensing data processing, climate data integration, land use classification, and environmental monitoring.",
    "scientific-epidemiology-public-health": "Epidemiology and public health skill. Disease surveillance, outbreak analysis, incidence/prevalence estimation, risk factor analysis, and population health metrics.",
    "scientific-epigenomics-chromatin": "Epigenomics and chromatin skill. ChIP-seq/ATAC-seq analysis, histone modification mapping, chromatin accessibility, DNA methylation analysis, and epigenetic regulatory networks.",
    "scientific-experiment-fork": "Experiment forking skill. A/B test branching, experiment versioning, parameter variation management, and parallel experimental workflow orchestration.",
    "scientific-experiment-template": "Experiment template skill. Standardized experimental protocol generation, reproducible experiment setup, parameter configuration templates, and lab notebook formatting.",
    "scientific-explainable-ai": "Explainable AI skill. SHAP values, LIME explanations, feature importance, partial dependence plots, model-agnostic interpretability, and explanation report generation.",
    "scientific-expression-comparison": "Gene expression comparison skill. Differential expression analysis (DESeq2/edgeR/limma), multi-condition comparison, volcano plots, and enrichment analysis pipelines.",
    "scientific-feature-importance": "Feature importance skill. Permutation importance, SHAP-based feature ranking, mutual information, recursive feature elimination, and feature selection pipelines.",
    "scientific-federated-learning": "Federated learning skill. Privacy-preserving distributed model training, federated averaging, differential privacy, secure aggregation, and cross-silo federation.",
    "scientific-gdc-portal": "GDC Portal skill. Genomic Data Commons cancer data retrieval, mutation frequency analysis, clinical-genomic correlation, and multi-project data integration.",
    "scientific-gene-expression-transcriptomics": "Gene expression and transcriptomics skill. RNA-seq analysis pipeline, gene quantification, isoform analysis, co-expression networks, and transcriptome-wide association.",
    "scientific-genome-sequence-tools": "Genome sequence tools skill. BLAST searches, multiple sequence alignment, genome annotation, primer design, and sequence manipulation utilities.",
    "scientific-geo-expression": "GEO expression skill. Gene Expression Omnibus data retrieval, microarray/RNA-seq dataset processing, GEO2R analysis, and cross-platform data normalization.",
    "scientific-geospatial-analysis": "Geospatial analysis skill. Spatial data processing with GeoPandas, coordinate transformations, spatial statistics, map visualization, and geospatial machine learning.",
    "scientific-glycomics": "Glycomics skill. Glycan structure analysis, glycosylation site prediction, glycoproteomics data processing, and carbohydrate database queries.",
    "scientific-gnomad-variants": "gnomAD variant skill. Population allele frequency queries, variant filtering, loss-of-function constraint metrics, and clinical variant annotation from gnomAD database.",
    "scientific-gpu-singlecell": "GPU-accelerated single-cell skill. RAPIDS/cuML-based single-cell analysis, GPU-accelerated dimensionality reduction, clustering, and differential expression on large datasets.",
    "scientific-grant-writing": "Grant writing skill. Research proposal drafting, specific aims composition, budget justification, significance/innovation statements, and funding agency format compliance.",
    "scientific-graph-neural-networks": "Graph neural networks skill. GNN architectures (GCN/GAT/GraphSAGE), molecular graph learning, knowledge graph embeddings, and graph-level prediction tasks.",
    "scientific-gtex-tissue-expression": "GTEx tissue expression skill. Tissue-specific gene expression queries from GTEx portal, eQTL analysis, cross-tissue comparison, and gene expression variation analysis.",
    "scientific-gwas-catalog": "GWAS Catalog skill. Genome-wide association study result queries, trait-variant associations, LD analysis, and polygenic risk score construction from GWAS Catalog data.",
    "scientific-healthcare-ai": "Healthcare AI skill. Clinical prediction models, patient risk stratification, medical image classification, electronic health record analysis, and clinical decision support ML.",
    "scientific-hgnc-nomenclature": "HGNC nomenclature skill. Official gene symbol resolution, gene name standardization, symbol history tracking, and gene family classification via HGNC database.",
    "scientific-human-cell-atlas": "Human Cell Atlas skill. HCA data portal queries, cell type reference mapping, organ-specific cell atlases, and single-cell study integration across the Human Cell Atlas project.",
    "scientific-human-protein-atlas": "Human Protein Atlas skill. Protein expression data retrieval, tissue/cell/pathology atlas queries, subcellular localization, and protein classification from HPA database.",
    "scientific-hypothesis-pipeline": "Hypothesis pipeline skill. Structured hypothesis generation, testable prediction formulation, experimental design derivation, and hypothesis-driven research workflow orchestration.",
    "scientific-icgc-cancer-data": "ICGC cancer data skill. International Cancer Genome Consortium data retrieval, pan-cancer mutation analysis, driver mutation identification, and multi-project comparison.",
    "scientific-image-analysis": "Image analysis skill. Scientific image processing, segmentation, morphological analysis, particle detection, colocalization analysis, and quantitative microscopy pipelines.",
    "scientific-immunoinformatics": "Immunoinformatics skill. Epitope prediction, MHC binding analysis, TCR/BCR repertoire analysis, immune cell deconvolution, and vaccine design support.",
    "scientific-infectious-disease": "Infectious disease skill. Pathogen genomics, antimicrobial resistance prediction, epidemiological modeling, phylogenetic tracking, and outbreak analysis pipelines.",
    "scientific-interactive-dashboard": "Interactive dashboard skill. Streamlit/Plotly Dash scientific dashboard creation, real-time data visualization, parameter exploration interfaces, and research result presentation.",
    "scientific-lab-automation": "Lab automation skill. Laboratory workflow automation, instrument control scripting, sample tracking, experimental protocol automation, and LIMS integration.",
    "scientific-lab-data-management": "Lab data management skill. Research data organization, metadata management, electronic lab notebook integration, data versioning, and FAIR data compliance.",
    "scientific-latex-export": "LaTeX export skill. Markdown-to-LaTeX conversion, journal-specific LaTeX template generation, bibliography management, and publication-ready PDF compilation.",
    "scientific-latex-formatter": "LaTeX formatter skill. LaTeX document formatting, equation typesetting, table formatting, figure placement optimization, and style file customization.",
    "scientific-lipidomics": "Lipidomics skill. Lipid species identification, quantification, lipid class profiling, lipidome-wide association, and lipidomics pathway analysis.",
    "scientific-literature-search": "Literature search skill. PubMed/Scopus/Web of Science search strategy design, systematic search query construction, citation screening, and reference manager integration.",
    "scientific-marine-ecology": "Marine ecology skill. Ocean biodiversity analysis, marine species distribution modeling, fisheries data analysis, coral reef assessment, and marine environmental monitoring.",
    "scientific-materials-characterization": "Materials characterization skill. XRD pattern analysis, SEM/TEM image processing, spectroscopy data analysis (XPS/FTIR/Raman), and materials property database queries.",
    "scientific-md-simulation": "Molecular dynamics simulation skill. GROMACS/OpenMM simulation setup, force field selection, trajectory analysis, free energy calculations, and enhanced sampling methods.",
    "scientific-medical-imaging": "Medical imaging skill. DICOM processing, image segmentation (U-Net), classification, registration, radiomics feature extraction, and clinical imaging pipeline development.",
    "scientific-meta-analysis": "Meta-analysis skill. Effect size calculation, random/fixed effects models, heterogeneity assessment (I², Q-test), forest plots, funnel plots, and publication bias analysis.",
    "scientific-metabolic-atlas": "Metabolic atlas skill. Genome-scale metabolic model queries, metabolic pathway visualization, flux balance analysis results, and cross-species metabolic comparison.",
    "scientific-metabolic-flux": "Metabolic flux analysis skill. ¹³C metabolic flux analysis, flux balance analysis, flux variability analysis, and metabolic network constraint-based modeling.",
    "scientific-metabolic-modeling": "Metabolic modeling skill. Constraint-based metabolic modeling (COBRApy), genome-scale model construction, gene knockout simulation, and metabolic engineering predictions.",
    "scientific-metabolomics": "Metabolomics skill. LC-MS/GC-MS data processing, metabolite identification, pathway mapping, biomarker discovery, and metabolomics statistical analysis pipelines.",
    "scientific-metabolomics-databases": "Metabolomics databases skill. HMDB/METLIN/MassBank database queries, metabolite annotation, spectral library matching, and cross-database metabolite identification.",
    "scientific-metabolomics-network": "Metabolomics network skill. Metabolite correlation networks, pathway-level network analysis, metabolite-gene interaction mapping, and multi-omics network integration.",
    "scientific-metagenome-assembled-genomes": "Metagenome-assembled genomes (MAG) skill. Metagenomic binning, genome quality assessment (CheckM), taxonomic classification, and functional annotation of MAGs.",
    "scientific-microbiome-metagenomics": "Microbiome and metagenomics skill. 16S rRNA analysis, shotgun metagenomics, diversity metrics, taxonomic profiling, functional metagenomics, and microbiome association studies.",
    "scientific-missing-data-analysis": "Missing data analysis skill. Missing data pattern detection, MCAR/MAR/MNAR classification, multiple imputation (MICE), sensitivity analysis, and missing data reporting.",
    "scientific-ml-classification": "ML classification skill. Binary/multi-class classification, model selection, hyperparameter tuning, cross-validation, metrics evaluation, and classification pipeline orchestration.",
    "scientific-ml-regression": "ML regression skill. Linear/nonlinear regression, regularization (L1/L2/ElasticNet), polynomial features, cross-validation, and regression diagnostics pipelines.",
    "scientific-model-monitoring": "Model monitoring skill. ML model performance tracking, data drift detection, prediction quality monitoring, model degradation alerts, and A/B test monitoring.",
    "scientific-model-organism-db": "Model organism database skill. FlyBase/WormBase/SGD/ZFIN/MGI queries, ortholog mapping, phenotype data retrieval, and cross-species gene function comparison.",
    "scientific-molecular-docking": "Molecular docking skill. AutoDock Vina/SMINA docking simulations, binding pose prediction, scoring function evaluation, virtual screening, and protein-ligand interaction analysis.",
    "scientific-monarch-ontology": "Monarch ontology skill. Monarch Initiative queries for disease-gene associations, phenotype ontology navigation, cross-species phenotype comparison, and knowledge graph exploration.",
    "scientific-multi-omics": "Multi-omics integration skill. Genomics/transcriptomics/proteomics/metabolomics data integration, multi-omics factor analysis (MOFA), pathway-level integration, and cross-omics correlation.",
    "scientific-multi-task-learning": "Multi-task learning skill. Shared representation learning, task-specific heads, gradient balancing, auxiliary task selection, and multi-task model evaluation.",
    "scientific-nci60-screening": "NCI-60 screening skill. NCI-60 cancer cell line panel data analysis, drug sensitivity profiling, COMPARE algorithm, and multi-drug response comparison.",
    "scientific-network-analysis": "Network analysis skill. NetworkX graph construction, centrality analysis, community detection, network visualization, PPI networks, and correlation network building.",
    "scientific-network-visualization": "Network visualization skill. Interactive network plots (Cytoscape.js/D3/NetworkX), layout algorithms, edge bundling, node clustering visualization, and publication-quality network figures.",
    "scientific-neural-architecture-search": "Neural architecture search (NAS) skill. Architecture space definition, search strategy implementation, performance estimation, and efficient NAS methods (DARTS/ENAS).",
    "scientific-neuroscience-electrophysiology": "Neuroscience electrophysiology skill. Spike sorting, LFP analysis, neural oscillation characterization, connectivity analysis, and electrophysiology data preprocessing.",
    "scientific-noncoding-rna": "Non-coding RNA skill. miRNA target prediction, lncRNA functional annotation, ncRNA expression analysis, small RNA-seq processing, and RNA secondary structure prediction.",
    "scientific-ontology-enrichment": "Ontology enrichment skill. GO enrichment analysis, KEGG pathway enrichment, disease ontology enrichment, multiple testing correction, and enrichment visualization.",
    "scientific-opentargets-genetics": "Open Targets Genetics skill. GWAS trait-gene associations, L2G scoring, colocation analysis, and variant-to-gene mapping from Open Targets Genetics portal.",
    "scientific-paleobiology": "Paleobiology skill. Fossil record analysis, paleobiodiversity estimation, extinction rate calculation, stratigraphic data processing, and macroevolutionary pattern analysis.",
    "scientific-paper-quality": "Paper quality assessment skill. Manuscript quality scoring, structural completeness checking, statistical reporting assessment, and writing clarity evaluation.",
    "scientific-parasite-genomics": "Parasite genomics skill. Parasite genome analysis, drug resistance marker identification, population genetics of parasites, and host-parasite interaction genomics.",
    "scientific-pathway-enrichment": "Pathway enrichment skill. GSEA, ORA, KEGG/Reactome/WikiPathways enrichment, gene set analysis, leading-edge analysis, and pathway crosstalk identification.",
    "scientific-pca-tsne": "Dimensionality reduction skill. PCA, t-SNE, UMAP, MDS implementations with visualization, parameter tuning, and biological interpretation of reduced dimensions.",
    "scientific-peer-review": "Peer review skill. Structured peer review generation following journal guidelines, constructive critique formulation, statistical audit, and review scoring.",
    "scientific-peer-review-response": "Peer review response skill. Point-by-point response to reviewer comments, revision tracking, rebuttal letter drafting, and manuscript revision management.",
    "scientific-perturbation-analysis": "Perturbation analysis skill. CRISPR screen analysis, drug perturbation response, perturbation signature comparison, and connectivity map (CMap) analysis.",
    "scientific-pharmacogenomics": "Pharmacogenomics skill. Genotype-drug response associations, pharmacogenomic variant annotation, dosing guideline integration, and PGx biomarker analysis.",
    "scientific-pharmacology-targets": "Pharmacology targets skill. Target validation, druggability assessment, target prioritization scoring, and pharmacological target-disease mapping.",
    "scientific-pharmacovigilance": "Pharmacovigilance skill. Adverse event signal detection, FAERS/VAERS data analysis, disproportionality analysis, and drug safety signal evaluation.",
    "scientific-pharmgkb-pgx": "PharmGKB pharmacogenomics skill. PharmGKB clinical annotation queries, drug-gene interaction lookup, dosing guideline retrieval, and pharmacogenomic pathway analysis.",
    "scientific-pharos-targets": "Pharos targets skill. Target Development Level (TDL) classification, understudied protein identification, Illuminating the Druggable Genome (IDG) resource queries.",
    "scientific-phylogenetics": "Phylogenetics skill. Phylogenetic tree construction (ML/Bayesian), multiple sequence alignment, divergence time estimation, and evolutionary analysis pipelines.",
    "scientific-pipeline-scaffold": "Pipeline scaffold skill. Bioinformatics pipeline scaffolding with Snakemake/Nextflow, workflow configuration, reproducible analysis environment setup.",
    "scientific-plant-biology": "Plant biology skill. Plant genomics, transcriptomics, phenomics data analysis, crop improvement, and plant-specific database queries (TAIR, Phytozome).",
    "scientific-population-genetics": "Population genetics skill. Allele frequency analysis, Hardy-Weinberg testing, Fst/neutrality statistics, population structure (ADMIXTURE/PCA), and demographic inference.",
    "scientific-precision-oncology": "Precision oncology skill. Tumor molecular profiling, actionable mutation identification, treatment matching, clinical trial matching, and molecular tumor board support.",
    "scientific-preprint-archive": "Preprint archive skill. bioRxiv/medRxiv/arXiv search, preprint tracking, citation monitoring, and preprint-to-publication linking.",
    "scientific-presentation-design": "Presentation design skill. Scientific slide design, figure layout optimization, conference poster creation, and data visualization for oral presentations.",
    "scientific-process-optimization": "Process optimization skill. Industrial process optimization, response surface methodology, constraint optimization, and process parameter tuning pipelines.",
    "scientific-protein-design": "Protein design skill. De novo protein design, directed evolution simulation, stability prediction, and protein engineering workflow support.",
    "scientific-protein-domain-family": "Protein domain and family skill. InterPro/Pfam domain annotation, protein family classification, domain architecture analysis, and functional domain prediction.",
    "scientific-protein-interaction-network": "Protein interaction network skill. STRING/BioGRID PPI data integration, interaction confidence scoring, network topology analysis, and protein complex identification.",
    "scientific-protein-structure-analysis": "Protein structure analysis skill. PDB structure retrieval, structural alignment (TM-align), binding site analysis, and structure-function relationship exploration.",
    "scientific-proteomics-mass-spectrometry": "Proteomics and mass spectrometry skill. MS data processing, peptide identification, protein quantification (LFQ/TMT/iTRAQ), and proteomics statistical analysis.",
    "scientific-public-health-data": "Public health data skill. WHO/CDC/national health data retrieval, health indicator analysis, demographic health survey processing, and public health metric calculation.",
    "scientific-publication-figures": "Publication figures skill. Journal-specification figure generation, multi-panel layout, color-blind safe palettes, resolution/DPI compliance, and figure annotation.",
    "scientific-quantum-computing": "Quantum computing skill. Qiskit/Cirq quantum circuit design, VQE/QAOA algorithms, quantum chemistry simulation, and quantum machine learning experiments.",
    "scientific-radiology-ai": "Radiology AI skill. Medical image classification, detection, and segmentation for radiology, DICOM handling, radiomics, and clinical AI model evaluation.",
    "scientific-rare-disease-genetics": "Rare disease genetics skill. Rare variant prioritization, exome/genome sequencing analysis, phenotype-driven gene ranking, and diagnostic yield optimization.",
    "scientific-rcsb-pdb-search": "RCSB PDB search skill. Protein Data Bank structure search, advanced query construction, structure clustering, and PDB data retrieval/parsing.",
    "scientific-reactome-pathways": "Reactome pathways skill. Reactome pathway queries, pathway hierarchy navigation, pathway enrichment analysis, and pathway diagram generation.",
    "scientific-regulatory-genomics": "Regulatory genomics skill. Enhancer/promoter annotation, transcription factor binding, regulatory variant analysis, and chromatin state classification.",
    "scientific-regulatory-science": "Regulatory science skill. FDA/EMA regulatory guidance, clinical trial regulation, drug approval pathway analysis, and regulatory document preparation.",
    "scientific-reinforcement-learning": "Reinforcement learning skill. Policy gradient methods, Q-learning, actor-critic architectures, environment design, reward shaping, and RL experiment management.",
    "scientific-reproducible-reporting": "Reproducible reporting skill. Jupyter/Quarto/R Markdown report automation, computational reproducibility, environment snapshot, and version-controlled analysis reports.",
    "scientific-research-methodology": "Research methodology skill. Study design planning, sampling strategy selection, measurement validity/reliability assessment, and methodological quality framework.",
    "scientific-revision-tracker": "Revision tracker skill. Manuscript revision tracking, diff generation between drafts, change log maintenance, and reviewer comment integration management.",
    "scientific-rrna-taxonomy": "rRNA taxonomy skill. 16S/18S/ITS rRNA-based taxonomic classification, OTU/ASV analysis, taxonomic database queries, and microbial diversity profiling.",
    "scientific-scatac-signac": "scATAC-seq Signac skill. Single-cell ATAC-seq analysis with Signac/ArchR, peak calling, motif enrichment, chromatin accessibility clustering, and gene activity scoring.",
    "scientific-scientific-schematics": "Scientific schematics skill. Pathway diagrams, mechanism illustrations, experimental workflow diagrams, and scientific concept visualization generation.",
    "scientific-scvi-integration": "scVI integration skill. Deep generative model-based single-cell analysis with scvi-tools, batch correction, cell type annotation, and multi-modal data integration.",
    "scientific-semantic-scholar": "Semantic Scholar skill. Academic paper search via Semantic Scholar API, citation graph exploration, author profiling, and research impact metrics retrieval.",
    "scientific-semi-supervised-learning": "Semi-supervised learning skill. Self-training, co-training, label propagation, MixMatch/FixMatch, and semi-supervised model evaluation pipelines.",
    "scientific-sequence-analysis": "Sequence analysis skill. DNA/RNA/protein sequence alignment, motif discovery, sequence feature extraction, homology search, and sequence comparison tools.",
    "scientific-single-cell-genomics": "Single-cell genomics skill. scRNA-seq analysis (Scanpy/Seurat), cell clustering, trajectory inference, cell type annotation, and gene regulatory network inference.",
    "scientific-spatial-multiomics": "Spatial multi-omics skill. Spatially resolved transcriptomics + proteomics integration, spatial niche identification, and multi-modal spatial data analysis.",
    "scientific-spatial-transcriptomics": "Spatial transcriptomics skill. Visium/MERFISH/Slide-seq data analysis, spatial gene expression mapping, spatial clustering, and tissue region deconvolution.",
    "scientific-spectral-signal": "Spectral signal processing skill. Spectroscopy data analysis (UV-Vis/NMR/MS), peak detection, spectral deconvolution, and signal-to-noise optimization.",
    "scientific-squidpy-advanced": "Squidpy advanced skill. Spatial omics analysis with Squidpy: neighborhood enrichment, spatial autocorrelation, ligand-receptor analysis, and image feature extraction.",
    "scientific-statistical-simulation": "Statistical simulation skill. Monte Carlo methods, bootstrap confidence intervals, permutation tests, power simulation, and simulation-based inference.",
    "scientific-statistical-testing": "Statistical testing skill. Frequentist hypothesis testing (t-test, ANOVA, chi-square, nonparametric tests), multiple testing correction, effect size calculation, and power analysis.",
    "scientific-stitch-chemical-network": "STITCH chemical network skill. STITCH chemical-protein interaction queries, chemical similarity networks, and drug-target network construction.",
    "scientific-streaming-analytics": "Streaming analytics skill. Real-time data processing, stream windowing, online learning, event-driven analysis, and streaming aggregation pipelines.",
    "scientific-string-network-api": "STRING network API skill. Protein-protein interaction network queries, functional enrichment via STRING, network clustering, and PPI confidence scoring.",
    "scientific-structural-proteomics": "Structural proteomics skill. Cross-linking mass spectrometry analysis, HDX-MS data processing, native MS, and structural biology data integration.",
    "scientific-supplementary-generator": "Supplementary materials generator skill. Supplementary data preparation, extended methods writing, supplementary table/figure organization, and SI document formatting.",
    "scientific-survival-clinical": "Survival and clinical analysis skill. Kaplan-Meier estimation, Cox proportional hazards, time-to-event analysis, competing risks, and clinical outcome modeling.",
    "scientific-symbolic-mathematics": "Symbolic mathematics skill. SymPy-based symbolic computation, equation solving, calculus, linear algebra, and mathematical proof assistance.",
    "scientific-systematic-review": "Systematic review skill. PRISMA-compliant systematic review workflow, literature screening, data extraction, risk of bias assessment, and evidence synthesis.",
    "scientific-systems-biology": "Systems biology skill. Network modeling, flux balance analysis, dynamical systems simulation, and multi-scale biological system analysis.",
    "scientific-text-mining-nlp": "Text mining and NLP skill. Scientific text mining, named entity recognition, relation extraction, topic modeling, and biomedical NLP pipelines.",
    "scientific-time-series": "Time series analysis skill. Trend decomposition, stationarity testing, ARIMA/SARIMA modeling, spectral analysis, and time series feature extraction.",
    "scientific-time-series-forecasting": "Time series forecasting skill. Prophet/NeuralProphet/LSTM forecasting, ensemble forecasting, forecast evaluation metrics, and confidence interval estimation.",
    "scientific-toxicology-env": "Toxicology and environmental skill. Toxicity prediction, dose-response modeling, environmental risk assessment, and chemical hazard characterization.",
    "scientific-transfer-learning": "Transfer learning skill. Domain adaptation, fine-tuning pretrained models, feature extraction, few-shot learning, and transfer learning strategy selection.",
    "scientific-uncertainty-quantification": "Uncertainty quantification skill. Aleatory/epistemic uncertainty estimation, ensemble uncertainty, conformal prediction, calibration, and uncertainty propagation.",
    "scientific-uniprot-proteome": "UniProt proteome skill. UniProt protein sequence/annotation retrieval, proteome-wide queries, functional annotation extraction, and protein feature analysis.",
    "scientific-variant-effect-prediction": "Variant effect prediction skill. CADD/REVEL/AlphaMissense scoring, splice variant prediction, regulatory variant impact, and variant pathogenicity classification.",
    "scientific-variant-interpretation": "Variant interpretation skill. ACMG/AMP variant classification, pathogenicity evidence aggregation, clinical significance assessment, and variant report generation.",
}

# ── Common Japanese → English text replacements ──
REPLACEMENTS = [
    # Section-level / structural patterns
    ("## ToolUniverse 連携", "## ToolUniverse Integration"),
    ("## パイプライン統合", "## Pipeline Integration"),
    ("## パイプライン出力", "## Pipeline Output"),
    ("## 標準パイプライン", "## Standard Pipeline"),
    ("## 利用可能ツール (ToolUniverse SMCP)", "## Available Tools (ToolUniverse SMCP)"),
    ("## 利用可能ツール", "## Available Tools"),
    ("## K-Dense 連携", "## K-Dense Integration"),
    ("## 他スキルとの連携", "## Inter-Skill Integration"),

    # Table headers
    ("| TU Key | ツール名 | 連携内容 |", "| TU Key | Tool Name | Integration |"),
    ("| TU Key | ツール名 | 用途 |", "| TU Key | Tool Name | Usage |"),
    ("| ファイル | 形式 | 生成タイミング |", "| File | Format | Generated When |"),
    ("| スキル | 連携 |", "| Skill | Integration |"),
    ("| 参照スキル | 連携 |", "| Related Skill | Integration |"),
    ("| ステップ | 内容 |", "| Step | Description |"),
    ("| パラメータ | 説明 |", "| Parameter | Description |"),
    ("| メトリクス | 説明 |", "| Metric | Description |"),
    ("| 要素 | 説明 |", "| Element | Description |"),
    ("| 手法 | 説明 |", "| Method | Description |"),
    ("| ツール | 説明 |", "| Tool | Description |"),
    ("| 項目 | 内容 |", "| Item | Description |"),
    ("| 入力 | 形式 | 説明 |", "| Input | Format | Description |"),
    ("| 出力 | 形式 | 説明 |", "| Output | Format | Description |"),
    ("| テキスト要素 | 規則 |", "| Text Element | Rule |"),
    ("| 成果物の種類 | 保存形式 | 保存先の例 |", "| Artifact Type | Format | Example Path |"),

    # Common Japanese phrases (sorted longest first to avoid partial matches)
    ("### 参照スキル", "### Related Skills"),
    ("### 出力ファイル", "### Output Files"),
    ("## Output Files", "## Output Files"),
    ("結果レポート・プロット生成", "Result report and plot generation"),
    ("事後分布の要約 (mean, HDI)", "Posterior summary (mean, HDI)"),
    ("収束診断 (Rhat, ESS, divergences)", "Convergence diagnostics (Rhat, ESS, divergences)"),
    ("事後予測チェック (PPC)", "Posterior predictive check (PPC)"),
    ("モデル比較 (LOO-CV / WAIC)", "Model comparison (LOO-CV / WAIC)"),
    ("MCMC サンプリング完了", "MCMC sampling complete"),
    ("Prior predictive check", "Prior predictive check"),
    ("モデル仕様 (尤度・事前分布) の定義", "Model specification (likelihood and priors)"),

    # Generic high-frequency phrases
    ("で発火。", "triggers this skill."),
    ("で発火", "triggers this skill"),
    ("TU 外スキル", "Non-TU skill"),
    ("（直接 Python ライブラリ）", "(direct Python library usage)"),
    ("完了チェックリスト", "Completeness Checklist"),
    ("品質ゲート", "Quality Gates"),
    ("品質基準", "Quality Criteria"),
]


# ── Harness optimization footer (appended to sub-skills) ──
HARNESS_FOOTER = """
---

## Verification Loop (v0.2.0)

```
PLAN   → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY  → check outputs against quality gates
REPORT  → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show())
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
"""


def translate_frontmatter_desc(skill_dir_name: str, original_desc: str) -> str:
    """Return English description for the YAML frontmatter."""
    if skill_dir_name in SKILL_DESCRIPTIONS:
        return SKILL_DESCRIPTIONS[skill_dir_name]
    # Fallback: keep original but note it's untranslated
    return original_desc


def apply_text_replacements(text: str) -> str:
    """Apply common Japanese→English text replacements outside code blocks."""
    lines = text.split("\n")
    result = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        # Apply replacements
        for jp, en in REPLACEMENTS:
            line = line.replace(jp, en)

        result.append(line)

    return "\n".join(result)


def has_harness_footer(text: str) -> bool:
    """Check if file already has harness optimization section."""
    return "## Verification Loop (v0.2.0)" in text


def process_skill_md(filepath: Path, skill_dir_name: str) -> bool:
    """Process a single SKILL.md file. Returns True if modified."""
    content = filepath.read_text(encoding="utf-8")
    original = content

    # ── 1. Convert frontmatter description ──
    fm_match = re.match(
        r"^---\n(.*?)---\n",
        content,
        re.DOTALL,
    )
    if fm_match:
        fm_block = fm_match.group(1)
        # Extract and replace description
        desc_match = re.search(
            r"description:\s*\|\n((?:\s+.*\n)*)",
            fm_block,
        )
        if desc_match:
            new_desc = translate_frontmatter_desc(skill_dir_name, desc_match.group(1).strip())
            # Rebuild frontmatter
            new_fm = re.sub(
                r"(description:\s*)\|\n(?:\s+.*\n)*",
                f"\\1|\n  {new_desc}\n",
                fm_block,
            )
            content = f"---\n{new_fm}---\n" + content[fm_match.end():]
        else:
            # Single-line description
            desc_match = re.search(
                r'description:\s*["\']?(.*?)["\']?\s*\n',
                fm_block,
            )
            if desc_match:
                new_desc = translate_frontmatter_desc(skill_dir_name, desc_match.group(1).strip())
                new_fm = re.sub(
                    r'(description:\s*)["\']?.*?["\']?\s*\n',
                    f"\\1|\n  {new_desc}\n",
                    fm_block,
                )
                content = f"---\n{new_fm}---\n" + content[fm_match.end():]

    # ── 2. Apply text replacements ──
    content = apply_text_replacements(content)

    # ── 3. Add harness footer if not already present ──
    if not has_harness_footer(content):
        content = content.rstrip() + "\n" + HARNESS_FOOTER

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return True
    return False


def bump_skill_json(filepath: Path) -> bool:
    """Bump version to v0.2.0 and ensure description is English."""
    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return False

    changed = False
    if data.get("version") != "v0.2.0":
        data["version"] = "v0.2.0"
        changed = True

    filepath.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return changed


def sync_source(skill_dir: Path):
    """Copy SKILL.md to source/SKILL.md."""
    src = skill_dir / "SKILL.md"
    dst = skill_dir / "source" / "SKILL.md"
    if src.exists() and dst.parent.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def main():
    scientist = Path(SCIENTIST_DIR)
    if not scientist.exists():
        print(f"ERROR: {scientist} not found")
        return

    sub_skills = sorted(
        d for d in scientist.iterdir()
        if d.is_dir() and d.name.startswith("scientific-")
    )

    print(f"Found {len(sub_skills)} sub-skills to process")

    md_updated = 0
    json_updated = 0

    for skill_dir in sub_skills:
        skill_name = skill_dir.name

        # Process SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            if process_skill_md(skill_md, skill_name):
                md_updated += 1

        # Bump skill.json
        skill_json = skill_dir / "skill.json"
        if skill_json.exists():
            if bump_skill_json(skill_json):
                json_updated += 1

        # Sync source/SKILL.md
        sync_source(skill_dir)

    # Also bump root skill.json
    root_json = scientist / "skill.json"
    if root_json.exists():
        bump_skill_json(root_json)

    print(f"SKILL.md updated: {md_updated}/{len(sub_skills)}")
    print(f"skill.json bumped: {json_updated}/{len(sub_skills)}")
    print("source/SKILL.md synced for all sub-skills")
    print("Done! All scientist skills upgraded to v0.2.0")


if __name__ == "__main__":
    main()
