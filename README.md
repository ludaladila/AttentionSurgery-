---
title: Attention Surgery Backend
emoji: 🧠
colorFrom: purple
colorTo: pink
sdk: docker
app_port: 7860
pinned: false
---

# Attention Surgery: Interactive Mechanistic Interpretability

This is the backend API service for the **Attention Surgery** project.
It provides model inference (GPT-2 Small), attention pattern ablation, and real-time metrics computation.

## Features
- **Head Ablation**: Zero, Mean, Random, and Previous-Layer ablation methods.
- **Importance Scoring**: Gradient-based and Rollback-based head importance estimation.
- **Real-time Metrics**: KL Divergence, Top-1 Changed Ratio, Perplexity Delta.
- **Logit Lens**: Layer-wise prediction confidence analysis.

The frontend is hosted separately (e.g., on Vercel) and communicates with this service via REST API.
