# Graph-Based Modeling of osu! Beatmaps for Estimating Gameplay Difficulty

This implementation explores an alternative method for estimating the gameplay difficulty of osu! beatmaps using graph theory. By parsing .osu files, each beatmap is modeled as a directed graph, where nodes represent hit objects and weighted edges reflect the spatial and temporal difficulty of transitions. A custom difficulty formula is applied, and the resulting graph is visualized to better understand the beatmap's structure.

Features:
- Parses .osu beatmap files to extract hit object data
- Models beatmaps as directed graphs using networkx
- Calculates edge weights
- Visualizes the beatmap graph using Matplotlib
- Estimates gameplay difficulty
