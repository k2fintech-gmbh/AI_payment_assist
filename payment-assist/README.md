# Payment Assist — лайт-версия AML-агента

Плагин для ChatGPT и Claude, который помогает пользователю подготовить банковский перевод до отправки. Пользователь описывает, куда, кому и как хочет перевести деньги. Агент проверяет получателя и страны по открытым источникам, валидирует IBAN/BIC, подсказывает, какие документы понадобятся, предупреждает о типичных схемах мошенничества и советует, как лучше провести платёж.

Плагин только консультирует. Он не выполняет платежи, не подключается к банковским системам и не выносит AML-решений; окончательное решение всегда за банком.

Логика построена на пользовательской части руководства [docs/BlackCatCard_AI_CoPilot_Governance_Manual_v1_0.md](../docs/BlackCatCard_AI_CoPilot_Governance_Manual_v1_0.md) (раздел 3, раздел 5, Appendix A), адаптированной под любого пользователя в ЕС, без внутренней специфики Papaya.

## Почему плагин, а не Custom GPT

- **OpenAI** выводит Custom GPTs из эксплуатации 11.12.2026 и переводит их на плагины, состоящие из skills и, при необходимости, MCP-сервера ([FAQ](https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq), [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins)).
- **Anthropic**: плагины со skills работают в чате claude.ai (веб, desktop, мобильное приложение), в Cowork и в Claude Code ([Plugin platform support](https://claude.com/docs/plugins/platform-support)).
- Обе платформы используют открытый формат [Agent Skills](https://claude.com/docs/skills/how-to) (`SKILL.md`) и упаковку [Agent Plugins 1.0](https://agent-plugins.org). Поэтому у нас один исходник и два манифеста.

## Структура

```text
AML_bot/
├── .claude-plugin/marketplace.json     # marketplace для Claude (установка из Git-репозитория)
├── .agents/plugins/marketplace.json    # marketplace для ChatGPT desktop / Codex (локальное тестирование)
├── site/                               # сайт плагина на Cloudflare: главная, privacy, terms
└── payment-assist/                       # корень плагина
    ├── plugin.json                     # Agent Plugins 1.0 + extensions.com.openai (листинг в ChatGPT)
    ├── .claude-plugin/plugin.json      # манифест Claude
    ├── skills/                         # то, что попадает в пакет
    │   ├── transfer-precheck/          # главный сценарий: полная оценка перевода + отчёт
    │   ├── counterparty-check/         # получатель: санкционные списки, реестры, лицензии, предупреждения
    │   ├── country-risk-check/         # страна: FATF, список ЕС high-risk, санкции ЕС
    │   ├── payment-documents-advisor/  # документы и формулировка назначения платежа
    │   ├── scam-check/                 # типологии мошенничества
    │   └── iban-bic-check/             # проверка IBAN/BIC скриптом, VoP, поля SWIFT
    ├── shared/                         # ЕДИНСТВЕННЫЙ источник общих файлов
    │   ├── references/*.md
    │   └── scripts/validate_iban.py
    ├── tools/build.py                  # синхронизация, валидация, сборка zip
    └── tests/                          # тест-кейсы для ручного прогона
```

Каталоги `skills/*/references/` и `skills/*/scripts/` **генерируются** из `shared/`: skill на этих платформах видит только собственную папку, поэтому общие файлы копируются в каждый skill. Редактируйте только `shared/`, а затем запускайте сборку. Какие файлы получает какой skill, задаётся в `SKILL_MAP` в `tools/build.py`.

## Как работает агент

1. Сбор данных короткими блоками: отправитель, получатель, счёт, сумма и способ перевода, назначение, контекст.
2. Фильтр hard-stop тем: на них даётся нейтральный отказ.
3. Проверки по шести измерениям: санкции, география, легитимность получателя, реквизиты, назначение и документы, признаки мошенничества.
4. Вердикт выносится детерминированно по `verdict_matrix.md`: GREEN, YELLOW, RED или GREY (недостаточно данных).
5. Отчёт по шаблону `skills/transfer-precheck/assets/report_template.md`, всегда с источниками, датами и дисклеймером.

Ключевые ограничения прописаны в `shared/references/guardrails_and_wording.md`: никаких подсказок по дроблению платежей, ложному назначению или обходу санкций; совпадения в списках подаются как «возможное совпадение» со ссылкой; документы пользователя считаются данными, а не инструкциями; номера карт, коды и пароли не запрашиваются.

## Сборка и проверка

Нужен Python 3.9 или новее, внешних зависимостей нет.

```bash
cd payment-assist
python3 tools/build.py          # синхронизация shared -> skills, валидация, сборка dist/
python3 tools/build.py --check  # только проверка (для CI): упадёт, если skills не синхронизированы
```

Что проверяет `build.py`:

- frontmatter каждого `SKILL.md`: `name` совпадает с именем папки, длина и символы корректны, `description` не длиннее 1024 символов и валиден как YAML;
- все файлы, на которые ссылается `SKILL.md`, существуют;
- в skills и в тексте листинга нет упоминаний конкретных провайдеров (claude, chatgpt, openai...), как требует OpenAI;
- оба манифеста валидны и согласованы по `name`, `version`, `description`; корневой `plugin.json` соответствует схеме Agent Plugins 1.0;
- marketplace-файлы указывают на плагин;
- нет каталога `bin/`, с которым плагин не установится в claude.ai.

Результаты сборки:

- `dist/payment-assist-<version>.zip` — пакет плагина для загрузки в обе платформы;
- `dist/skills/<skill>.zip` — отдельные skills для загрузки в claude.ai через Settings > Features (если нужен не весь плагин).

Проверка скрипта IBAN вручную:

```bash
python3 shared/scripts/validate_iban.py --iban "DE89 3704 0044 0532 0130 00" --bic COBADEFFXXX --country DE
```

## Локальное тестирование

**Claude Code** (официальный валидатор входит в CLI):

```bash
claude plugin validate ./payment-assist
claude plugin validate .                      # проверка marketplace в корне репозитория
claude --plugin-dir ./payment-assist        # сессия с подключённым плагином
```

**ChatGPT desktop / Codex**: marketplace репозитория лежит в `.agents/plugins/marketplace.json`. Откройте репозиторий как проект, перезапустите приложение, затем найдите плагин в Plugins Directory под источником «Payment Assist» ([Package your plugin](https://developers.openai.com/plugins/build/plugins)).

**Тест-кейсы**: `tests/activation_cases.md` проверяет, что срабатывает правильный skill; `tests/behaviour_cases.md` проверяет качество ответа и соблюдение ограничений. Критерий релиза: ноль нарушений ограничений в разделах B, C, D, F и не меньше 90 % пройденных кейсов в остальных.

## Публикация

### Перед публикацией (обязательно)

1. Задеплойте сайт из [`site/`](../site/README.md) на Cloudflare и замените placeholder-URL в `plugin.json` (`websiteURL`, `privacyPolicyURL`, `termsOfServiceURL`) на его страницы `/`, `/privacy`, `/terms`. Сборка предупреждает, пока они указывают на `example.com`.
2. Укажите реального автора (`author.name`, `developerName`) в обоих манифестах и в marketplace-файлах.
3. При желании добавьте иконку и логотип в `payment-assist/assets/` и пропишите `composerIcon` и `logo` в `extensions.com.openai.interface`.
4. Поднимите `version` в обоих манифестах (сборка проверяет, что версии совпадают).
5. Прогоните тест-кейсы на обеих платформах.

### OpenAI (ChatGPT и Codex)

1. Нужны доступ Apps Management (write) в организации OpenAI и верификация личности или компании.
2. Откройте plugin submission portal, выберите **Create plugin**, затем **Skills only**, и загрузите `dist/payment-assist-<version>.zip` ([Submit your Claude Code plugin to OpenAI](https://developers.openai.com/plugins/guides/submit-claude-plugin)).
3. Проверьте сгенерированный манифест, заполните поля листинга и исправьте замечания сканера.
4. Плагин стартует приватным. Дальше его можно опубликовать в своём workspace или подать в публичный Directory после ревью. Для skills-only плагинов OpenAI оговаривает возможные дополнительные требования к листингу.
5. Учтите [правила каталога](https://developers.openai.com/plugins/plugin-guidelines): выполнение денежных переводов запрещено (мы их не выполняем, это прямо сказано в описании), как и сбор платёжных карт, госидентификаторов и паролей.

### Anthropic (claude.ai, Cowork, Claude Code)

Плагины доступны только на платных тарифах (Pro, Max, Team, Enterprise) и только в приложении [claude.ai](https://claude.ai) или Claude Desktop. В консоли разработчика (platform.claude.com / console.anthropic.com) раздела плагинов нет. На Enterprise администратор может ограничить установку плагинов.

Варианты распространения:

- **Файл**: левая боковая панель > **Customize** > вкладка **Plugins** > кнопка **Add** > вариант загрузки файла > `dist/payment-assist-<version>.zip`. Плагин сохраняется в аккаунте и доступен в чате, Cowork и Claude Code ([Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)).
- **Git-репозиторий как marketplace**: Customize > Plugins > Add marketplace > URL репозитория (используется `.claude-plugin/marketplace.json` в корне). Для Team и Enterprise владелец может синхронизировать репозиторий для всей организации.
- **Каталог Anthropic**: подача через портал директории, когда плагин будет готов к публичному распространению.

### Требования к окружению пользователя

| Платформа | Что должно быть включено |
| - | - |
| claude.ai | Code execution (без него custom skills не работают), веб-поиск |
| ChatGPT | Web search, data analysis (для скрипта IBAN) |

Без веб-поиска агент честно сообщает, что проверить списки не может, и ставит по санкциям и географии «недостаточно данных».

## Обновление данных

| Что | Когда | Где |
| - | - | - |
| Списки FATF | После пленарных заседаний FATF (февраль, июнь, октябрь) | `shared/references/jurisdictions_snapshot.md` |
| Список ЕС high-risk third countries | При выходе нового делегированного регламента | там же |
| Санкционные режимы ЕС (сводка) | По мере существенных изменений | там же, раздел 4 |
| Длины IBAN, страны SEPA | При обновлении SWIFT IBAN Registry или списка EPC | `shared/scripts/validate_iban.py` |
| Правила платёжных систем (VoP, ISO 20022, сроки) | По мере вступления изменений в силу | `shared/references/payment_rails.md` |

После правки: обновите дату снимка, запустите `python3 tools/build.py`, поднимите версию и опубликуйте заново. Агент всегда сначала проверяет списки онлайн, а снимок использует только как запасной вариант, указывая его дату.

Текущий снимок: FATF — по состоянию на 19.06.2026 (октябрьское пленарное заседание 2026 года ещё не учтено); список ЕС — в редакции от 29.01.2026.

## Ограничения лайт-версии

- Проверка по санкционным спискам зависит от веб-поиска модели. Она не воспроизводима и не заменяет скрининг банка; отсюда обязательный дисклеймер в каждом отчёте.
- Нет журнала диалогов и аудиторского следа (в руководстве это раздел 6.3).
- Нет детерминированного матчинга имён по спискам: модель ищет так, как умеет.
- Данные о странах в снимке устаревают между обновлениями.

## Этап 2: MCP-сервер

Тот же пакет можно дополнить файлом `mcp.json` с удалённым MCP-сервером (Streamable HTTP), который возьмёт на себя:

- детерминированный скрининг по скачанным официальным спискам (EU FSF, UN, OFAC, UK) с fuzzy-матчингом и версией списка в ответе;
- актуальные списки стран без ручного обновления снимка;
- журнал проверок для аудита.

Skills при этом не переписываются: в шагах Step 3 добавляется вызов соответствующего инструмента вместо веб-поиска, а у OpenAI зависимость объявляется в `agents/openai.yaml` ([Build skills](https://developers.openai.com/plugins/build/skills)).
