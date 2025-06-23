# Music Analytics Data Warehouse

A unified, query-ready data warehouse built from **four complementary public music datasets**.
The warehouse is designed for **multidimensional analysis of music trends, audio characteristics, artist careers, and chart performance** from the late-1950s to today. The pipeline is **coded in Python (ETL)** and the resulting data is **explored in Tableau Public**.

---

## 📦 Source Datasets

| # | Dataset                     | What It Adds                                                                                                  | Link                                                                                                                                                                                     |
| - | --------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | **Song Features Dataset**   | Spotify audio features (danceability, energy, acousticness, …), artist & track IDs, Spotify popularity score. | [https://www.kaggle.com/datasets/ayushnitb/song-features-dataset-regressing-popularity](https://www.kaggle.com/datasets/ayushnitb/song-features-dataset-regressing-popularity)           |
| 2 | **Spotify 1.2 M+ Songs**    | Large-scale genre tags, extra popularity metrics, decades of historical coverage.                             | [https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs](https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs)                                                   |
| 3 | **Billboard Hot 100 Songs** | Weekly U.S. chart ranks since 1958, including sales / streams–based performance.                              | [https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs](https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs)                                       |
| 4 | **Worldwide Music Artists** | Canonical artist names, primary genres, countries, artist images.                                             | [https://www.kaggle.com/datasets/harshdprajapati/worldwide-music-artists-dataset-with-image](https://www.kaggle.com/datasets/harshdprajapati/worldwide-music-artists-dataset-with-image) |

---

## 🗄️ Fact: `ChartPosition`

| Measure                           | Description                           |
| --------------------------------- | ------------------------------------- |
| **Rank**                          | Position in weekly Billboard Hot 100  |
| **Peak Rank**                     | Best-ever rank                        |
| **Days to #1**                    | Time between first entry and first #1 |
| **Weeks On Board**                | Longevity on chart                    |

### Key Dimensions

* **Song** – IDs, title, release year/decade, genre set, “most danceable in decade” flag, etc.
* **Artist** – canonical name, country, primary & secondary genres.
* **Time** – role-playing dimension (`Observation Date`, `First Entry Date`, `First #1 Date`).

---

## 🔍 Example of queries in Tableau Public

* How danceability and acousticness have evolved in top-charting songs from the 1960 s → 2020 s
* How long songs remain on the charts
* Which artists have the most unique entries on Billboard Hot 100
* Which decades produced the most danceable or most acoustic tracks
