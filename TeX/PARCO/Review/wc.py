from wordcloud import WordCloud

FILE_NAME = "Q19-others.txt"

with open(FILE_NAME, "r", encoding="utf-8") as f:
    CONTENT = f.read()

wc = WordCloud(width=1500, height=200,
               normalize_plurals=True,
               collocations=True,
               min_word_length=4,
               collocation_threshold=5,
               repeat=False,
               max_words=30,
               background_color="black")
wc.generate(CONTENT)
wc.to_file("Figs/Q19-others.pdf")
