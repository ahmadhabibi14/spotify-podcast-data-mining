import pandas as pd
import time

start_time = time.time()

# Kolom untuk di skip
unwanted_columns = [
  "chartRankMove", "episodeUri", "showUri", "show.name", "show.description", 
  "duration_ms", "explicit", "is_externally_hosted", "region",
  "is_playable", "language", "release_date_precision",
  "show.copyrights", "show.explicit", "show.href", "show.html_description", "show.is_externally_hosted",
  "show.languages", "show.media_type", "show.total_episodes", "show.type", "show.uri"
]

# Nilai dari kolom "episodeName" untuk di skip
unwanted_values = [
  "", "The", "Ep", "A", "Ep", "I", "O", "LA", "EL"
]

idx_col_date      = 0
idx_col_rank      = 1
idx_col_epsname   = 2
idx_col_desc      = 3
idx_col_publisher = 4
idx_col_langs     = 5
idx_col_release   = 6

# Baca dataset dari file CSV
df = pd.read_csv(
  filepath_or_buffer="top_podcasts_raw.csv",
  low_memory=False,
  encoding="utf-8",
)

# Hapus podcast yang tidak berasal dari Indonesia
df = df.drop(
  index=df[df["region"] != "id"].index
)

# Ambil data hanya 300 baris
df = df.iloc[:300]

# Hapus kolom - kolom yang tidak diperlukan
df = df.drop(
  columns=unwanted_columns,
  axis=1
)

# Filter data:
# - skip jika kolom episodeName kosong atau ada value yang diabaikan
# - skip jika kolom description kosong
df_filtered = df.dropna(
  subset=["description"],
)
df_filtered = df_filtered[
  df_filtered["episodeName"].map(lambda x: x not in unwanted_values)
]

# Ganti nama kolom ke dalam Bahasa Indonesia
df_filtered = df_filtered.rename(
  columns={
    df_filtered.columns[idx_col_date]: "Tanggal",
    df_filtered.columns[idx_col_rank]: "Ranking",
    df_filtered.columns[idx_col_epsname]: "Episode",
    df_filtered.columns[idx_col_desc]: "Deskripsi",
    df_filtered.columns[idx_col_publisher]: "Penerbit",
    df_filtered.columns[idx_col_langs]: "Bahasa",
    df_filtered.columns[idx_col_release]: "Rilis"
  }
)

# Buat file dataset baru dengan format CSV
df_filtered.to_csv(
  path_or_buf="top_podcast_cleaned.csv",
  index=False,
  sep="\t"
)

end_time = time.time()
duration = end_time - start_time

print("Selesai !!")
print(f"Waktu eksekusi: {duration:.2f} detik")
