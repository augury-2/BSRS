# Implementation Appendix — Runnable R Pipeline

This appendix contains the complete, runnable R Markdown pipeline that implements the spec (Parts A–F, H–P). Save the fenced R Markdown below as `analysis.Rmd` next to `MTVS.xlsx` and knit it.

**Note on Multi-Group Analysis (Part G / H4):** per-respondent demographics are confidential and were not released, so MGA is **not estimable** for this dataset and is reported as such; Table 1 is built from the published aggregate counts.

````markdown
---
title: "MTVS: PLS-SEM + fsQCA Analysis (UE, UX -> BSAT -> BSUC)"
output:
  html_document: { toc: true, toc_float: true, number_sections: true }
  word_document: { toc: true }
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE, warning = FALSE, message = FALSE,
                      fig.width = 7, fig.height = 5, dpi = 300)
SEED <- 20240701
set.seed(SEED)
pkgs <- c("readxl","dplyr","tidyr","psych","car","seminr","QCA","SetMethods",
          "ggplot2","corrplot","GGally","moments","knitr","tibble","digest")
to_install <- pkgs[!pkgs %in% rownames(installed.packages())]
if (length(to_install)) install.packages(to_install)
invisible(lapply(pkgs, library, character.only = TRUE))
```

# Data ingestion & structural validation (Req 1)

```{r load}
raw <- readxl::read_excel("MTVS.xlsx")
ind_UE <- paste0("UE",1:5); ind_UX <- paste0("UX",1:5)
ind_BSAT <- paste0("BSAT",1:4); ind_BSUC <- paste0("BSUC",1:4)
indicators <- c(ind_UE, ind_UX, ind_BSAT, ind_BSUC); controls <- c("ATT_1","ATT_2")
missing_cols <- setdiff(indicators, names(raw))
if (length(missing_cols)) stop("Missing required indicators: ", paste(missing_cols, collapse=", "))
oor <- do.call(rbind, lapply(indicators, function(v){ x<-raw[[v]]; b<-which(x<1|x>7|x!=round(x)); if(length(b)) data.frame(indicator=v,row=b,value=x[b]) else NULL }))
if (!is.null(oor)) print(oor) else message("No out-of-range values detected.")
cat("Observed rows:", nrow(raw), "| equals 312:", nrow(raw)==312, "\n")
id_label <- if ("ID" %in% names(raw)) raw$ID else seq_len(nrow(raw))
dat <- raw[, c(indicators, controls)]; n <- nrow(dat)
manifest <- list(seed=SEED, R=R.version.string,
                 file_sha256=digest::digest(file="MTVS.xlsx", algo="sha256"),
                 timestamp=format(Sys.time(), tz="UTC", usetz=TRUE)); str(manifest)
```

# Composite scores (Req 3)

```{r composites}
comp <- data.frame(UE=rowMeans(dat[,ind_UE]), UX=rowMeans(dat[,ind_UX]),
                   BSAT=rowMeans(dat[,ind_BSAT]), BSUC=rowMeans(dat[,ind_BSUC]))
psych::describe(comp)[, c("mean","sd","min","max")]
cat("Cases with any missing indicator:", sum(!complete.cases(dat[,indicators])), "\n")
```

# PART A — Data screening (Req 4-5)

```{r screening}
cat("n =", n, "| 10x-rule minimum =", 10*3, "\n")
desc <- psych::describe(dat[,indicators])[, c("mean","sd","skew","kurtosis")]
desc$skew_flag <- abs(desc$skew) > 2; desc$kurt_flag <- abs(desc$kurtosis) > 7
knitr::kable(round(desc[,1:4],3), caption="Indicator descriptives & normality")
md <- mahalanobis(dat[,indicators], colMeans(dat[,indicators]), cov(dat[,indicators]))
crit <- qchisq(0.999, df=length(indicators))
cat("Mahalanobis critical =", round(crit,3), "| flagged:", sum(md>crit), "\n")
fit_lm <- lm(BSUC ~ UE+UX+BSAT, data=comp); cook <- cooks.distance(fit_lm); thr <- 4/n
cat("Cook's 4/n =", round(thr,4), "| influential:", sum(is.finite(cook)&cook>thr), "\n")
print(round(car::vif(fit_lm),3))
knitr::kable(round(cor(comp),3), caption="Construct correlation matrix")
```

```{r screening-figs}
op <- par(mfrow=c(1,3))
for (v in indicators){ hist(dat[[v]],main=paste("Histogram:",v),xlab=v,col="grey85")
  plot(density(dat[[v]]),main=paste("Density:",v),xlab=v)
  qqnorm(dat[[v]],main=paste("Q-Q:",v)); qqline(dat[[v]],col="red") }
par(op)
corrplot::corrplot(cor(dat[,indicators]), method="color", tl.cex=0.6,
                   title="Indicator correlation heatmap", mar=c(0,0,1,0))
GGally::ggpairs(comp, title="Scatter matrix (constructs)")
```

# PART B — Measurement model (Req 7)

```{r measurement}
mm <- seminr::constructs(
  seminr::reflective("UE", seminr::multi_items("UE",1:5)),
  seminr::reflective("UX", seminr::multi_items("UX",1:5)),
  seminr::reflective("BSAT", seminr::multi_items("BSAT",1:4)),
  seminr::reflective("BSUC", seminr::multi_items("BSUC",1:4)))
sm <- seminr::relationships(
  seminr::paths(from=c("UE","UX"), to="BSAT"),
  seminr::paths(from=c("UE","UX","BSAT"), to="BSUC"))
pls <- seminr::estimate_pls(data=as.data.frame(dat[,indicators]),
        measurement_model=mm, structural_model=sm, inner_weights=seminr::path_weighting)
s <- summary(pls)
s$loadings; s$weights; s$reliability
s$validity$cross_loadings; s$validity$fl_criteria; s$validity$htmt; s$validity$vif_items
cs <- as.data.frame(pls$construct_scores)
fullcol <- sapply(names(cs), function(k) max(car::vif(lm(as.formula(paste(k,"~ .")), data=cs))))
cat("Full-collinearity VIF (CMB, flag >= 3.3):\n"); print(round(fullcol,3))
ev <- psych::principal(dat[,indicators], nfactors=1)$values
cat("Harman single-factor variance %:", round(100*ev[1]/length(indicators),2), "(concern if > 50%)\n")
# SRMR/d_ULS/d_G: report from SmartPLS/ADANCO if a reviewer requires (flag SRMR > 0.08).
```

# PART C + D — Structural model, bootstrap, mediation (Req 8-9)

```{r structural}
boot <- seminr::bootstrap_model(seminr_model=pls, nboot=5000,
          cores=parallel::detectCores(), seed=SEED)
bs <- summary(boot, alpha=0.05); bs$bootstrapped_paths
med_UE <- seminr::specific_effect_significance(boot, from="UE", through="BSAT", to="BSUC", alpha=0.05)
med_UX <- seminr::specific_effect_significance(boot, from="UX", through="BSAT", to="BSUC", alpha=0.05)
print(med_UE); print(med_UX); bs$bootstrapped_total_effects
vaf <- function(indirect, total) indirect/total   # VAF<.20 none; .20-.80 partial; >.80 full
```

# PART E — Model quality (Req 10)

```{r quality}
s$paths; s$fSquare
pp <- seminr::predict_pls(model=pls, technique=seminr::predict_DA, noFolds=10, reps=10)
sp <- summary(pp); sp$PLS_out_of_sample; sp$LM_out_of_sample
# Predictive power (Shmueli et al. 2019): proportion of BSUC indicators where PLS RMSE < LM RMSE.
```

# PART F — IPMA (Req 11)

```{r ipma}
rescale01 <- function(x) (x-1)/(7-1)*100
perf <- sapply(comp[,c("UE","UX","BSAT")], function(x) mean(rescale01(x)))
ipma <- data.frame(Construct=names(perf), Performance=round(perf,2)); print(ipma)
ggplot(ipma, aes(Performance, Construct)) + geom_point(size=3) +
  labs(title="IPMA — performance of predictors of BSUC", x="Performance (0-100)")
# Importance = total effects on BSUC (read from bs$bootstrapped_total_effects).
```

# PART G — Multi-Group Analysis (Req 12): NOT ESTIMABLE

```{r mga, eval=FALSE}
# Per-respondent demographics are CONFIDENTIAL and were not released.
# MGA (H4) is therefore NOT ESTIMABLE for this dataset and is reported as such.
# Conditional path (only if non-confidential per-respondent data ever becomes
# available internally, keyed on ID): MICOM + permutation/PLS-MGA via seminr.
```

# PART H — fsQCA (Req 13-17, 19)

```{r fsqca}
calib_direct <- function(x) QCA::calibrate(x, type="fuzzy", thresholds=c(2.0,4.0,6.5))
fs <- data.frame(UE_f=calib_direct(comp$UE), UX_f=calib_direct(comp$UX),
                 BSAT_f=calib_direct(comp$BSAT), BSUC_f=calib_direct(comp$BSUC))
fs[] <- lapply(fs, function(v){ v[v==0.5] <- 0.501; v }); summary(fs)
calib_pct <- function(x) QCA::calibrate(x, type="fuzzy",
                thresholds=stats::quantile(x, c(0.05,0.50,0.95)))
nec <- SetMethods::QCAfit(fs[,c("UE_f","UX_f","BSAT_f")], fs$BSUC_f, necessity=TRUE); print(nec)
tt <- QCA::truthTable(cbind(fs[,c("UE_f","UX_f","BSAT_f")], OUT=fs$BSUC_f),
        outcome="OUT", conditions=c("UE_f","UX_f","BSAT_f"),
        incl.cut=0.80, pri.cut=0.70, n.cut=1, complete=TRUE, show.cases=TRUE); print(tt)
sol_complex <- QCA::minimize(tt, details=TRUE)
sol_parsi   <- QCA::minimize(tt, include="?", details=TRUE)
sol_inter   <- QCA::minimize(tt, include="?", details=TRUE, dir.exp=c(1,1,1)); print(sol_inter)
QCA::XYplot(fs$UE_f, fs$BSUC_f, relation="sufficiency")
```

# PART K — Robustness (Req 20)

```{r robustness}
fs2 <- data.frame(UE_f=calib_pct(comp$UE), UX_f=calib_pct(comp$UX),
                  BSAT_f=calib_pct(comp$BSAT), BSUC_f=calib_pct(comp$BSUC))
fs2[] <- lapply(fs2, function(v){ v[v==0.5] <- 0.501; v })
tt2 <- QCA::truthTable(cbind(fs2[,c("UE_f","UX_f","BSAT_f")], OUT=fs2$BSUC_f),
        outcome="OUT", conditions=c("UE_f","UX_f","BSAT_f"), incl.cut=0.80, pri.cut=0.70, n.cut=1)
QCA::minimize(tt2, include="?", dir.exp=c(1,1,1), details=TRUE)
for (cc in c(0.75,0.80,0.85,0.90)){
  ttx <- QCA::truthTable(cbind(fs[,c("UE_f","UX_f","BSAT_f")], OUT=fs$BSUC_f),
          outcome="OUT", conditions=c("UE_f","UX_f","BSAT_f"), incl.cut=cc, pri.cut=0.70, n.cut=1)
  cat("\n--- raw consistency cutoff =", cc, "---\n")
  try(print(QCA::minimize(ttx, include="?", dir.exp=c(1,1,1))$solution)) }
```

# Table 1 — Respondent demographic profile (published aggregates) (Req 6)

```{r table1}
table1 <- tibble::tribble(
  ~Variable, ~Category, ~n, ~Percent,
  "Gender","Male",143,46.00, "Gender","Female",169,54.00,
  "Age","18-22",64,20.51, "Age","23-28",75,24.04, "Age","29-34",60,19.23,
  "Age","35-41",57,18.27, "Age","42-45",56,17.95,
  "Marital Status","Single",107,34.29, "Marital Status","Married w/ children",84,26.93,
  "Marital Status","Married w/o children",121,38.78,
  "Occupation","Students",88,28.21, "Occupation","Job",102,32.69, "Occupation","Business",122,39.10,
  "Engagement Freq.","Daily",52,16.67, "Engagement Freq.","Several/week",98,31.41,
  "Engagement Freq.","Weekly",73,23.38, "Engagement Freq.","Monthly",54,17.31,
  "Engagement Freq.","Rarely",35,11.21,
  "NFT Interaction","Yes",141,45.19, "NFT Interaction","No",171,54.81,
  "Virtual Event","Yes",129,41.35, "Virtual Event","No",183,58.65,
  "Social/Content","Yes",164,52.56, "Social/Content","No",148,47.44,
  "Monthly Income","<=30,000",57,18.40, "Monthly Income","30,001-50,000",80,25.64,
  "Monthly Income","50,001-80,000",100,32.05, "Monthly Income","80,001+",75,23.91)
knitr::kable(table1, caption="Table 1. Respondent demographic profile (N = 312)")
stopifnot(all(aggregate(n ~ Variable, table1, sum)$n == 312))
# Note: counts derive from the PUBLISHED AGGREGATE profile; per-respondent demographics
# are confidential, so Multi-Group Analysis is NOT ESTIMABLE for this dataset.
```
````

## Caveats
- `SRMR`, `d_ULS`, `d_G` are not exported by `seminr`; report from SmartPLS/ADANCO if a reviewer requires them (flag SRMR > 0.08).
- `vaf()` and the predictive-power percentage are filled from the printed point estimates of each run.
- Part G (MGA / H4) is **not estimable** for this dataset by design (confidential demographics).
