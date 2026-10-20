# Загрузка P2588 на GitHub

Название репозитория: **P2588-2SAT-Threshold**.

Владелец: **Sergpreneur**.

Адрес, уже добавленный в препринт и журнальную версию:
https://github.com/Sergpreneur/P2588-2SAT-Threshold

Эта версия подготовлена для загрузки. Репозиторий из этой сессии не создавался,
публичная доступность адреса пока не подтверждена. В статье это отмечено явно.

## Через сайт GitHub

1. Распакуй `P2588-2SAT-Threshold_GitHub.zip`.
2. Открой https://github.com/new и создай публичный репозиторий
   `Sergpreneur/P2588-2SAT-Threshold`.
3. Загрузи **содержимое** распакованной папки `P2588-2SAT-Threshold/`, чтобы
   `README.md`, `src/`, `verify/`, `paper/` и `lean/` находились в корне репозитория.
   Сам ZIP-файл вместо исходников загружать не нужно.
4. Сохрани начальный коммит и проверь, что README отображается на главной странице.
5. После успешной публикации можно убрать фразу о pending public upload
   из `paper/main.tex` и пересобрать PDF. Текущий PDF уже содержит нужную ссылку.

Описание репозитория:

> Exact six-variable random 2-SAT median threshold: reproducible counts, integer certificates and partial Lean 4 verification.

## Через Git

После создания пустого репозитория выполни из распакованной папки:

```bash
git init -b main
git add .
git commit -m "Add exact 2-SAT threshold materials and partial Lean verification"
git remote add origin https://github.com/Sergpreneur/P2588-2SAT-Threshold.git
git push -u origin main
```

Архив содержит исходники, данные, сертификаты, препринт и Lean-проект с журналами.
Полная формализация соответствия коэффициентов числу выполнимых формул
по-прежнему не заявляется. Письмо в редакцию и документы для подачи в журнал
хранятся в отдельном комплекте и не включены в GitHub-архив.
