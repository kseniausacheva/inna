# ПДФ для клиента

- `katalog-programm.pdf` — каталог всех десяти программ, 13 страниц
- `kair-opisanie.pdf` — подробное описание Каира, 4 страницы
- `programmy/*.pdf` — по одной странице на каждую программу, чтобы отправлять по отдельности

Как пересобрать после правок:

```bash
cd la-royal-event/client-package/pdf
python3 build_catalog.py            # тексты лежат в этом же файле, вверху
NODE_PATH=$(npm root -g) node render.js
```

Шрифты лежат в `fonts/`, чтобы сборка не зависела от интернета.
