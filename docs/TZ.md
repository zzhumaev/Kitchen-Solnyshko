# ТЗ «Kitchen Stock» (бэкенд + бот + веб-админка + отчёты XLSX)

## Цель
Учёт товаров (приход/расход/корректировка), ежедневные показатели (дети/сотрудники), отчёты в XLSX строго по макетам: **Накладная (день)**, **Приход (месяц-матрица)**, **Остаток (на месяц)**, **Основной отчёт (матрица)**.

## Роли
- **ADMIN** — всё (пользователи/роли, товары/цены, документы, корректировки, рассылки).
- **STOREKEEPER** (завхоз) — приход, изменение товаров/цен, ввод daily metrics, списание (нужно подтверждение ADMIN).
- **COOK** (повар) — создаёт расход (заявка) → подтверждает STOREKEEPER; если нет ответа 4 часа — автоэскалация ADMIN.
- **STAFF** (сотрудник) — получает рассылки, (опц.) вводит daily metrics.

## БД (основное)
- `units(id, code, name, to_base_factor)`
- `products(id, code, name, unit_id, base_unit_id, to_base_factor, note)`
- `product_prices(id, product_id, price, start_at, end_at NULL)` — история цен
- `locations(id, code, name)`
- `documents(id, doc_type['IN','OUT','ADJUST'], doc_no, doc_date, location_id, note,
  status['DRAFT','SUBMITTED','APPROVED','REJECTED'], requested_by, approver_id, approved_at,
  approver_role_target, escalate_after, created_at)`
- `doc_items(id, doc_id, product_id, qty_base, price)` — сумма = `qty_base * price`
- `daily_metrics(id, date, location_id, children_count, staff_count, created_by, UNIQUE(date,location_id))`
- `users(id, tg_user_id, phone, name, is_active)` / `roles(id, code, name)` / `user_roles(user_id, role_id)`

## Бизнес-правила
- Храним количества в **базовых единицах** (`qty_base`), отображаем через `to_base_factor`.
- `OUT` запрещён при недостатке остатка.
- Корректировки — документ `ADJUST` (ADMIN).
- Цена фиксируется в строке документа.

## API (v1)
База `/api`.

**Справочники:** `GET/POST/PUT/DELETE /units`, `/products`, `/locations`; цены: `GET/POST /products/{id}/prices`.  
**Документы:** `POST /docs/in`, `POST /docs/out`, `POST /docs/{id}/submit|approve|reject`, `POST /docs/adjust`, `GET /docs/{id}`.  
**Остатки/показатели:** `GET /stock?date=&location_id=`, `GET/POST /daily-metrics?date=&location_id=`.

## Отчёты (XLSX/JSON, строго по макетам)
1. **Накладная (день)** — `GET /reports/incoming/day.xlsx?date=YYYY-MM-DD&location_id=`  
   Шапка как в макете («ДОО "СОЛНЫШКО"…», «Через кого: Маратова М.М», «НАКЛАДНАЯ №», дата).  
   Таблица: **№ | Наименование | Ед.изм | Отпущено | Цена за ед. | Стоимость без НДС | Примечание**.  
   «Итого» + подписи.

2. **Приход (месяц, матрица по дням)** — `GET /reports/incoming/month.xlsx?month=YYYY-MM&location_id=`  
   Слева: **№ | Наименование | Ед.изм | Цена за ед.**, далее столбцы-дни **1…31**, справа **Итого (кол-во)** и **Сумма**.

3. **Остаток (на месяц)** — `GET /reports/opening.xlsx?month=YYYY-MM&location_id=`  
   **№ | Наименование | Остаток на <Месяц Год> | Цена за ед. | Стоимость без НДС | Примечание**. Шапка и подписи как в макете.

4. **Основной отчёт (матрица)** — `GET /reports/main.xlsx?month=YYYY-MM&location_id=`  
   **№ | Наименование | Цена за ед.товара | Остаток на начало <Месяц Год> | Оприходовано за <Месяц> | Всего | 01..31 (расход) | Всего расход | Остаток на <следующий месяц>**.

## Телеграм-бот
Reply-клавиатура: **Остатки**, **Приход**, **Расход**, **Дети/Сотрудники**, **Отчёты**, **Помощь**.  
Inline-кнопки для подтверждений (approve/reject) + эскалация через 4 часа.

## Веб-админка
Разделы: Единицы, Товары (с историей цен), Склады, Документы (IN/OUT/ADJUST), Остатки, Отчёты (скачивание XLSX), Пользователи/Роли, Дети/Сотрудники. Адаптивная (desktop+mobile).

## Безопасность
`X-API-Key` (старт) / далее JWT, CORS только для админки, опц. BasicAuth на `/api/docs`, Nginx rate-limit 5 r/s.

## DevOps
prod/dev compose, Alembic миграции, бэкап cron, CI/CD через GitHub Actions (push в `main` → деплой на VPS).

## Приёмка (кратко)
Роли/права и workflow подтверждений, корректность остатков, **все 4 отчёта** совпадают с макетами, бот и админка работают.
