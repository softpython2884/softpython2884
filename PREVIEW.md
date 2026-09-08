> **Ceci est une proposition, pas le profil.** Le README en ligne reste `README.md`.
> Cette version réécrit le texte pour enlever ce qui sonne « promesse » et le remplacer par
> des mécanismes vérifiables. Mise en page, badges et structure sont inchangés — seule la
> formulation bouge. Le détail de ce qui a été retiré et pourquoi est **[en bas de page](#ce-qui-a-changé-et-pourquoi)**.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0B0E14,100:1B2A4A&height=210&section=header&text=NightFury&fontColor=ffffff&fontSize=66&fontAlignY=34&desc=Full-Stack%20%C2%B7%20SysAdmin%20%C2%B7%20OS%20Builder&descSize=18&descAlignY=58&animation=fadeIn" width="100%" alt="NightFury" />

<a href="https://forgenet.fr">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=900&color=22D3EE&center=true&vCenter=true&width=760&lines=Founder+%40+Forge+Network+%E2%80%94+forgenet.fr;Multi-tenant+SaaS+%C2%B7+one+PostgreSQL+schema+per+tenant;~20+apps+in+production+%C2%B7+302+models+%C2%B7+fr%2Fen%2Fes%2Fde;TypeScript+%C2%B7+Flutter+%C2%B7+PostgreSQL+%C2%B7+Docker+%C2%B7+Debian" alt="What I do" />
</a>

<br/>

[![Forge Network](https://img.shields.io/badge/Forge_Network-forgenet.fr-7C3AED?style=flat-square&labelColor=0B0E14)](https://forgenet.fr)
[![Capibara](https://img.shields.io/badge/Capibara-capibara.fr-22D3EE?style=flat-square&labelColor=0B0E14&logo=icloud&logoColor=white)](https://capibara.fr)
[![Marcus](https://img.shields.io/badge/Marcus-marcusbot.fr-5865F2?style=flat-square&labelColor=0B0E14&logo=discord&logoColor=white)](https://marcusbot.fr)
[![Location](https://img.shields.io/badge/France-UTC%2B1-ffffff?style=flat-square&labelColor=0B0E14&logo=googlemaps&logoColor=22D3EE)](#)

</div>

---

### <img src="https://api.iconify.design/lucide/user-round.svg?color=%237C3AED&height=22" height="22" alt="" />&nbsp; About

I'm **NightFury**, a French developer. I run **Forge Network** (`forgenet.fr`), a non-profit
association that publishes the projects on this page, and I work with the **NationQuest** team.

I tend to take a product across its whole stack rather than one layer of it: the PostgreSQL
schema and its isolation model, the API, the front end, then the Debian machine it runs on —
nginx, Docker, PM2, certificates, backups. Most of what follows exists because something had
to be decided at that level.

```javascript
const nightFury = {
  role:    ["Full-Stack", "SysAdmin", "Data Eng", "OS Builder"],
  founder: "Forge Network · forgenet.fr",
  stack:   ["TypeScript", "Next.js", "React", "Node", "Dart", "PostgreSQL", "Docker", "Linux"],
  now:     ["Colibri / Capibara (SaaS suite)", "a custom Linux distro", "a new Grand Projet"],
  learning:"Scala & high-performance JVM systems",
};
```

---

## <img src="https://api.iconify.design/lucide/rocket.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; Flagship Work

> Four systems in production. Three are private, so the links go to the live product or the
> download. Every count below comes from the repository and can be re-derived.

<div align="center">

<!-- ============== COLIBRI / CAPIBARA ============== -->
<table>
<tr><td width="850" align="center">

### <img src="https://api.iconify.design/lucide/bird.svg?color=%237C3AED&height=24" height="24" alt="" /> Colibri — `Capibara` &nbsp;·&nbsp; <sub>private · in production</sub>

*Multi-tenant business suite. Each tenant gets its own PostgreSQL schema, not a `tenant_id` column.*

![Next.js](https://img.shields.io/badge/Next.js_15-000?style=flat-square&labelColor=0B0E14&logo=nextdotjs)
![React](https://img.shields.io/badge/React_19-000?style=flat-square&labelColor=0B0E14&logo=react&logoColor=61DAFB)
![tRPC](https://img.shields.io/badge/tRPC_v11-000?style=flat-square&labelColor=0B0E14&logo=trpc&logoColor=2596BE)
![Prisma](https://img.shields.io/badge/Prisma-000?style=flat-square&labelColor=0B0E14&logo=prisma)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-000?style=flat-square&labelColor=0B0E14&logo=postgresql&logoColor=4169E1)
![Stripe](https://img.shields.io/badge/Stripe-000?style=flat-square&labelColor=0B0E14&logo=stripe&logoColor=635BFF)
![Docker](https://img.shields.io/badge/Docker-000?style=flat-square&labelColor=0B0E14&logo=docker&logoColor=2496ED)

Provisioning a tenant runs `CREATE SCHEMA t_<key>` and applies `tenant.sql`. A query cannot leak
across tenants because it never shares a table with them. The bill arrives at migration time:
every schema change has to be replayed against every schema, which is what the 182 tenant
migrations are. The runner applies one file per transaction per schema, validates the schema name
before any raw SQL, and stops the deployment on failure — shipping a new web container onto an
unmigrated database is worse than a rollback.

CRM · Billing FR (Factur-X) · Accounting (FEC export) · Shop · Inventory · Purchasing · Planning · Ticketing · Support · Projects · HR · Formation · Blog · Newsletter · Chat · Wiki & Storage — plus a block-based site builder that renders the tenant's public site.

<sub>Permissions are re-read from the database on each call rather than trusted from the session · Meilisearch, MinIO, Stalwart mail + webmail, self-hosted Jitsi and a Stripe Connect marketplace run as separate containers · Not multi-region, and not one database per client: a single Postgres, schemas inside it. Scaling past one machine is a known open problem, not a solved one.</sub>

![files](https://img.shields.io/badge/TS_files-~2%2C480-7C3AED?style=flat-square&labelColor=0B0E14)
![loc](https://img.shields.io/badge/LOC-~364k-22D3EE?style=flat-square&labelColor=0B0E14)
![models](https://img.shields.io/badge/Prisma_models-302-7C3AED?style=flat-square&labelColor=0B0E14)
![migrations](https://img.shields.io/badge/Tenant_migrations-182-22D3EE?style=flat-square&labelColor=0B0E14)
![tests](https://img.shields.io/badge/Tests-5%2C200%2B-7C3AED?style=flat-square&labelColor=0B0E14)
![langs](https://img.shields.io/badge/Locales-fr_en_es_de-22D3EE?style=flat-square&labelColor=0B0E14)
![svc](https://img.shields.io/badge/Docker_services-17-7C3AED?style=flat-square&labelColor=0B0E14)

[![Visit Capibara](https://img.shields.io/badge/▶_capibara.fr-7C3AED?style=for-the-badge&labelColor=0B0E14)](https://capibara.fr)
[![Forge Network](https://img.shields.io/badge/forgenet.fr-22D3EE?style=for-the-badge&labelColor=0B0E14)](https://forgenet.fr)

</td></tr>
</table>

<!-- ============== OPUS ============== -->
<table>
<tr><td width="850" align="center">

### <img src="https://api.iconify.design/lucide/layout-dashboard.svg?color=%237C3AED&height=24" height="24" alt="" /> OPUS &nbsp;·&nbsp; <sub>forgenet.fr</sub>

*Developer platform: project workspace, container hosting, a licensing server and a store.*

![React](https://img.shields.io/badge/React_19-000?style=flat-square&labelColor=0B0E14&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite_6-000?style=flat-square&labelColor=0B0E14&logo=vite&logoColor=646CFF)
![Express](https://img.shields.io/badge/Express_4-000?style=flat-square&labelColor=0B0E14&logo=express)
![Prisma](https://img.shields.io/badge/Prisma_6-000?style=flat-square&labelColor=0B0E14&logo=prisma)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-000?style=flat-square&labelColor=0B0E14&logo=postgresql&logoColor=4169E1)
![Stripe](https://img.shields.io/badge/Stripe-000?style=flat-square&labelColor=0B0E14&logo=stripe&logoColor=635BFF)

**OPUS Cloud** hands out containers through a Pterodactyl panel. A real `sshd` cannot run inside a
Wings container — unprivileged uid, read-only rootfs, `no-new-privileges`, `CAP_SYS_CHROOT`
dropped — so a Cloud Box ships a proot root filesystem with an SSH server built on asyncssh
instead. That buys a persistent fake-root under `/home/container`; it does not buy
Docker-in-Docker, and only `/home/container` survives a rebuild. Both limits are written on the
page rather than discovered later.

**Forge Licensing** signs every response with Ed25519 (JWS), so a client verifies a licence
offline and a captured response cannot be replayed as a valid one. Elipse RSAI runs on it.

<sub>Workspace with projects, quotes, invoices and instalment plans · certification program (27 tracks × 4 levels × 5 real-project briefs) · store with Stripe checkout and licence delivery · news feed with RSS</sub>

![models](https://img.shields.io/badge/Prisma_models-94-7C3AED?style=flat-square&labelColor=0B0E14)
![loc](https://img.shields.io/badge/LOC-~92k-22D3EE?style=flat-square&labelColor=0B0E14)
![routes](https://img.shields.io/badge/API_route_files-52-7C3AED?style=flat-square&labelColor=0B0E14)
![cert](https://img.shields.io/badge/Assessments-540-22D3EE?style=flat-square&labelColor=0B0E14)
![sig](https://img.shields.io/badge/Licence_signing-Ed25519_JWS-7C3AED?style=flat-square&labelColor=0B0E14)

[![Live](https://img.shields.io/badge/▶_forgenet.fr-7C3AED?style=for-the-badge&labelColor=0B0E14)](https://forgenet.fr)
[![Console](https://img.shields.io/badge/console.forgenet.fr-22D3EE?style=for-the-badge&labelColor=0B0E14)](https://console.forgenet.fr)

</td></tr>
</table>

<!-- ============== MARCUS ============== -->
<table>
<tr><td width="850" align="center">

### <img src="https://api.iconify.design/lucide/bot.svg?color=%237C3AED&height=24" height="24" alt="" /> Marcus &nbsp;·&nbsp; <sub>Discord platform</sub>

*Discord bot whose modules are drawn in an editor and interpreted at runtime, not compiled.*

![Discord.js](https://img.shields.io/badge/Discord.js_14-000?style=flat-square&labelColor=0B0E14&logo=discord&logoColor=5865F2)
![Next.js](https://img.shields.io/badge/Next.js_15-000?style=flat-square&labelColor=0B0E14&logo=nextdotjs)
![SQLite](https://img.shields.io/badge/better--sqlite3-000?style=flat-square&labelColor=0B0E14&logo=sqlite&logoColor=003B57)
![Gemini](https://img.shields.io/badge/Genkit_·_Gemini_2.5-000?style=flat-square&labelColor=0B0E14&logo=googlegemini&logoColor=8E75FF)

A module is a graph, not source code. The React Flow editor writes a workflow of typed blocks;
a single interpreter walks it at runtime and resolves the variables. The work went into what the
demo never shows: a button or a select menu posted in a channel outlives the process, so the
component registries are persisted to SQLite and rehydrated at boot — without that, every restart
leaves dead controls in old messages. The bot runs sharded under PM2.

Its git history is the least flattering number on this page and stays here for that reason: **2.07×
more lines were written than survive**. The visual editor was rebuilt more than once.

![files](https://img.shields.io/badge/Files-~579-7C3AED?style=flat-square&labelColor=0B0E14)
![loc](https://img.shields.io/badge/LOC-~105k-22D3EE?style=flat-square&labelColor=0B0E14)
![cmd](https://img.shields.io/badge/Commands-93-7C3AED?style=flat-square&labelColor=0B0E14)
![events](https://img.shields.io/badge/Event_handlers-114-22D3EE?style=flat-square&labelColor=0B0E14)
![flows](https://img.shields.io/badge/AI_flows-30-7C3AED?style=flat-square&labelColor=0B0E14)
![rework](https://img.shields.io/badge/Rework_ratio-2.07x-22D3EE?style=flat-square&labelColor=0B0E14)

[![Live](https://img.shields.io/badge/▶_marcusbot.fr-7C3AED?style=for-the-badge&labelColor=0B0E14)](https://marcusbot.fr)

</td></tr>
</table>

<!-- ============== ELIPSE RSAI ============== -->
<table>
<tr><td width="850" align="center">

### <img src="https://api.iconify.design/lucide/heart-pulse.svg?color=%237C3AED&height=24" height="24" alt="" /> Elipse RSAI &nbsp;·&nbsp; <sub>private · shipped</sub>

*Field app for French childcare health referents. No server, no account, no network call carrying data.*

![Flutter](https://img.shields.io/badge/Flutter_3-000?style=flat-square&labelColor=0B0E14&logo=flutter&logoColor=02569B)
![Dart](https://img.shields.io/badge/Dart_3-000?style=flat-square&labelColor=0B0E14&logo=dart&logoColor=0175C2)
![SQLite](https://img.shields.io/badge/SQLite-000?style=flat-square&labelColor=0B0E14&logo=sqlite&logoColor=003B57)
![Android](https://img.shields.io/badge/Android_8%2B-000?style=flat-square&labelColor=0B0E14&logo=android&logoColor=3DDC84)
![Windows](https://img.shields.io/badge/Windows_10%2B-000?style=flat-square&labelColor=0B0E14&logo=windows&logoColor=0078D4)

A referent covers 5 to 30 nurseries and owes each one a quota of hours set by decree, split by
quarter, and has to be able to prove it. The quarterly minimum is the part people miss: you can
reach the annual total and still be short on three quarters. So the app logs an intervention in
three taps and tracks four counters per site, flagging the drift as it happens rather than at year
end. It writes the paperwork — visit reports, referral letters, individual care plans, annual
review — as PDFs, offline.

The architecture is a consequence, not a preference. Records naming a child are health data under
GDPR art. 9; hosting them would require HDS certification, which is out of reach for a project this
size — so the hosted version was abandoned and the host removed entirely. What that costs is
synchronisation: there is no server to reconcile against, so two devices sync peer-to-peer over the
local wifi with an operation log and a hybrid logical clock, or through an encrypted file on a USB
key when the nursery network isolates them, which it often does.

<sub>Local SQLite, SQL written by hand, sensitive fields encrypted with ChaCha20-Poly1305 · pairing by QR code, X25519 Diffie–Hellman and a six-digit code read out loud · PDF engine in pure Dart · the only outbound call validates the licence key and carries no business data · an expired licence drops the app to read-only and never holds the records hostage</sub>

![files](https://img.shields.io/badge/Dart_files-182-7C3AED?style=flat-square&labelColor=0B0E14)
![loc](https://img.shields.io/badge/LOC-~74k-22D3EE?style=flat-square&labelColor=0B0E14)
![screens](https://img.shields.io/badge/Screens-49-7C3AED?style=flat-square&labelColor=0B0E14)
![tests](https://img.shields.io/badge/Test_files-58-22D3EE?style=flat-square&labelColor=0B0E14)
![targets](https://img.shields.io/badge/Targets-Android_%26_Windows-7C3AED?style=flat-square&labelColor=0B0E14)
![version](https://img.shields.io/badge/Version-1.6.2-22D3EE?style=flat-square&labelColor=0B0E14)

<sub><i>17k lines of tests against 56k lines of app. The domain layer imports no Flutter and does no I/O, so the regulatory rules can be tested on their own — they are the part that decides whether someone is compliant.</i></sub>

[![Download](https://img.shields.io/badge/▶_Download-7C3AED?style=for-the-badge&labelColor=0B0E14)](https://forgenet.fr/telechargements/elipse)

</td></tr>
</table>

</div>

### <img src="https://api.iconify.design/lucide/calculator.svg?color=%237C3AED&height=22" height="22" alt="" />&nbsp; Rebuild cost — what the estimator computes

These are not amounts anyone spent. They estimate what it would cost to **rebuild** each project
from scratch with a senior team at the 2026 French senior rate (~650 €/day), and they are computed
rather than guessed: the script is [`tools/estimate.py`](tools/estimate.py) and it runs on any of
these repositories.

Every file is sorted into a zone — payment, security, compliance, integrations, business logic, UI,
data model, infra, tests, docs — and each zone carries its own lines-per-hour rate, because billing
code with idempotency, webhooks and reconciliation does not cost what CRUD costs. Git history then
adds what was written and later rewritten or thrown away, since abandoned work took the same time,
and an overhead factor covers what leaves no file behind: architecture, deployment, ops.

A **person-month** is one person working full time for one month. It is a unit of effort, not a
headcount — 189 person-months is roughly what a team of ~46 delivers in four months.

| Project | Lines counted | Effort | Rebuild cost | Written / kept |
|---|---:|---:|---:|---:|
| Capibara | 430 122 | 189 pm | ~2.46 M€ | 1.14× |
| Marcus | 112 364 | 67 pm | ~867 k€ | 2.07× |
| OPUS | 103 925 | 53 pm | ~687 k€ | 1.39× |
| Elipse RSAI | 83 471 | 33 pm | ~434 k€ | 1.05× |
| OpenCoperLock | 28 147 | 12 pm | ~155 k€ | 1.12× |

Two caveats worth stating. The productivity assumption sits at the optimistic end of the published
10–20 lines/hour range, so if these figures are wrong they are low rather than high. And on
Capibara, payment, security and compliance code is 11 % of the lines but 29 % of the estimated cost
— which is the whole reason a flat lines-per-hour average would have been useless here.

---

## <img src="https://api.iconify.design/lucide/package-open.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; Open Source

> Most public repositories here are experiments. One is maintained, documented and deployed.

<div align="center">

<!-- ============== OPENCOPERLOCK ============== -->
<table>
<tr><td width="850" align="center">

### <img src="https://api.iconify.design/lucide/shield.svg?color=%237C3AED&height=24" height="24" alt="" /> OpenCoperLock &nbsp;·&nbsp; <sub>AGPL v3 · self-hostable</sub>

*A private cloud for one dedicated machine: an ordinary Drive, plus three things most "drop a file" tools don't have.*

![TypeScript](https://img.shields.io/badge/TypeScript-000?style=flat-square&labelColor=0B0E14&logo=typescript&logoColor=3178C6)
![Next.js](https://img.shields.io/badge/Next.js_15-000?style=flat-square&labelColor=0B0E14&logo=nextdotjs)
![Fastify](https://img.shields.io/badge/Fastify_5-000?style=flat-square&labelColor=0B0E14&logo=fastify)
![Prisma](https://img.shields.io/badge/Prisma_6-000?style=flat-square&labelColor=0B0E14&logo=prisma)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-000?style=flat-square&labelColor=0B0E14&logo=postgresql&logoColor=4169E1)
![Docker](https://img.shields.io/badge/Docker-000?style=flat-square&labelColor=0B0E14&logo=docker&logoColor=2496ED)

**Quick-Upload** opens a temporary drop zone on any device from a code, with optional password,
expiry and usage limit. **Remote-Upload** makes the server fetch a link itself, so a phone on a
metered connection never relays the bytes — SSRF-guarded. **Hybrid encryption** is a per-folder
choice: AES-256-GCM at rest, which lets ClamAV scan the file, or a zero-knowledge vault encrypted
in the browser, which the server cannot read. Shared Spaces are server-side encrypted only, because
zero-knowledge cannot be shared — that trade-off is stated in the docs rather than hidden.

Background work runs on a database-backed loop inside the API process, which keeps a deployment to
a single moving part; Redis/BullMQ is documented as the upgrade for horizontal scale rather than
required up front. Storage sits behind a driver interface — the local filesystem one ships, S3 can
be added without touching the routes.

<sub>pnpm monorepo · WebDAV mounting · personal-token REST API · one-click self-update from GitHub · architecture, security policy and a candid threat model in `docs/`</sub>

![arch](https://img.shields.io/badge/Architecture-pnpm_monorepo-7C3AED?style=flat-square&labelColor=0B0E14)
![files](https://img.shields.io/badge/TS_files-~148-22D3EE?style=flat-square&labelColor=0B0E14)
![enc](https://img.shields.io/badge/At_rest-AES--256--GCM-7C3AED?style=flat-square&labelColor=0B0E14)
![hash](https://img.shields.io/badge/Passwords-Argon2-22D3EE?style=flat-square&labelColor=0B0E14)
![license](https://img.shields.io/badge/License-AGPL_v3-7C3AED?style=flat-square&labelColor=0B0E14)

[![Repo](https://img.shields.io/badge/▶_GitHub-181717?style=for-the-badge&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/OpenCoperLock)
[![Live](https://img.shields.io/badge/copper.forgenet.fr-22D3EE?style=for-the-badge&labelColor=0B0E14)](https://copper.forgenet.fr)

</td></tr>
</table>

<sub><b>Other public repositories</b></sub>

<table>
<tr>
<td width="425" valign="top">

#### <img src="https://api.iconify.design/lucide/brain.svg?color=%237C3AED&height=20" height="20" alt="" /> [Gemini-Assistant](https://github.com/softpython2884/Gemini-Assistant)

A clipboard-driven assistant that stays in the background. Hotkeys capture the selection from any
application, send it to Gemini and paste the answer at the cursor, falling back to another model
when a quota is hit.

![Python](https://img.shields.io/badge/Python-000?style=flat-square&labelColor=0B0E14&logo=python&logoColor=3776AB)
![Gemini](https://img.shields.io/badge/Google_Gemini-000?style=flat-square&labelColor=0B0E14&logo=googlegemini&logoColor=8E75FF)

[![Repo](https://img.shields.io/badge/Code-181717?style=flat-square&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/Gemini-Assistant)

</td>
<td width="425" valign="top">

#### <img src="https://api.iconify.design/lucide/link.svg?color=%237C3AED&height=20" height="20" alt="" /> [NightSlavery](https://github.com/softpython2884/NightSlavery)

A Minecraft Fabric mod (1.21, Java 21) inspired by *Kenshi*: a capture system built as a
`FREE → K.O. → imprisoned → enslaved` state machine, with cages, a control scepter, escape and
rebellion mechanics, and gamerule-based anti-grief limits.

![Java](https://img.shields.io/badge/Java_21-000?style=flat-square&labelColor=0B0E14&logo=openjdk&logoColor=white)
![Fabric](https://img.shields.io/badge/Fabric_·_MC_1.21-000?style=flat-square&labelColor=0B0E14)

[![Repo](https://img.shields.io/badge/Code-181717?style=flat-square&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/NightSlavery)

</td>
</tr>
<tr>
<td width="425" valign="top">

#### <img src="https://api.iconify.design/lucide/gamepad-2.svg?color=%237C3AED&height=20" height="20" alt="" /> [Macro](https://github.com/softpython2884/Macro)

An older one: a web console layer navigable with an Xbox controller, launching local games and
media, bridged to the OS through a Python hotkey listener.

![Next](https://img.shields.io/badge/Next.js-000?style=flat-square&labelColor=0B0E14&logo=nextdotjs)
![Python](https://img.shields.io/badge/Python-000?style=flat-square&labelColor=0B0E14&logo=python&logoColor=3776AB)

[![Repo](https://img.shields.io/badge/Code-181717?style=flat-square&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/Macro)

</td>
<td width="425" valign="top">

#### <img src="https://api.iconify.design/lucide/sliders-horizontal.svg?color=%237C3AED&height=20" height="20" alt="" /> StreamDeck utilities

Two PowerShell scripts on one key: **MouseMode** swaps Windows mouse profiles, **AudioSwitcher**
changes the default output and moves every running application onto the new device.

![PowerShell](https://img.shields.io/badge/PowerShell-000?style=flat-square&labelColor=0B0E14&logo=powershell&logoColor=5391FE)

[![MouseMode](https://img.shields.io/badge/MouseMode-181717?style=flat-square&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/MouseMode)
[![AudioSwitcher](https://img.shields.io/badge/AudioSwitcher-181717?style=flat-square&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/AudioSwitcher)

</td>
</tr>
</table>
</div>

---

<div align="center">

> ### <img src="https://api.iconify.design/lucide/lock.svg?color=%237C3AED&height=22" height="22" alt="" /> Why the good stuff isn't here
> **Colibri / Capibara**, **OPUS**, **Marcus** and **Elipse RSAI** are private — client work and
> products that are sold, not portfolio pieces. That is why this page leans on numbers taken from
> the repositories and on the live deployments rather than on code you can read. **OpenCoperLock**
> is the one where you can check the claims against the source.

</div>

---

## <img src="https://api.iconify.design/lucide/flask-conical.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; Also in the lab

<div align="center">

[![Betty](https://img.shields.io/badge/Betty-gamified_coding_edu-7C3AED?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/Betty)
[![SimuBourse](https://img.shields.io/badge/SimuBourse-financial_sim-22D3EE?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/SimuBourse)
[![StudyVerse](https://img.shields.io/badge/StudyVerse-AI_notes-7C3AED?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/StudyVerse)
[![CreepOS](https://img.shields.io/badge/CreepOS-horror_fake--OS_game-22D3EE?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/CreepOS)
[![OpenMark-Blog](https://img.shields.io/badge/OpenMark-AI_blogging-7C3AED?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/OpenMark-Blog)
[![Mana-Clash](https://img.shields.io/badge/Mana--Clash-tactical_card_game-22D3EE?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/Mana-Clash)

</div>

---

## <img src="https://api.iconify.design/lucide/monitor.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; Custom Linux distribution &nbsp;·&nbsp; <sub>unfinished, nothing to download</sub>

The least finished thing on this page, and the only one with no artifact behind it: no installer,
no release, no repository yet. The target is a distribution built against the bare kernel — its own
window manager, session, package and file managers — rather than a theme over an existing desktop,
aiming for Arch-level configurability without Arch-level setup.

It is listed because it is where a large share of my time goes, not because it is usable. Take it
as a statement of intent until there is something to install.

---

## <img src="https://api.iconify.design/lucide/wrench.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; Tech Stack

<div align="center">

**Languages**

![TypeScript](https://img.shields.io/badge/TypeScript-000?style=flat-square&labelColor=0B0E14&logo=typescript&logoColor=3178C6)
![JavaScript](https://img.shields.io/badge/JavaScript-000?style=flat-square&labelColor=0B0E14&logo=javascript&logoColor=F7DF1E)
![Python](https://img.shields.io/badge/Python-000?style=flat-square&labelColor=0B0E14&logo=python&logoColor=3776AB)
![Dart](https://img.shields.io/badge/Dart-000?style=flat-square&labelColor=0B0E14&logo=dart&logoColor=0175C2)
![Java](https://img.shields.io/badge/Java-000?style=flat-square&labelColor=0B0E14&logo=openjdk&logoColor=white)
![Scala](https://img.shields.io/badge/Scala-000?style=flat-square&labelColor=0B0E14&logo=scala&logoColor=DC322F)
![C++](https://img.shields.io/badge/C++-000?style=flat-square&labelColor=0B0E14&logo=cplusplus&logoColor=00599C)
![Bash](https://img.shields.io/badge/Bash-000?style=flat-square&labelColor=0B0E14&logo=gnubash&logoColor=4EAA25)

**Frontend**

![Next.js](https://img.shields.io/badge/Next.js-000?style=flat-square&labelColor=0B0E14&logo=nextdotjs)
![React](https://img.shields.io/badge/React-000?style=flat-square&labelColor=0B0E14&logo=react&logoColor=61DAFB)
![Tailwind](https://img.shields.io/badge/Tailwind-000?style=flat-square&labelColor=0B0E14&logo=tailwindcss&logoColor=38BDF8)
![Vite](https://img.shields.io/badge/Vite-000?style=flat-square&labelColor=0B0E14&logo=vite&logoColor=646CFF)
![Flutter](https://img.shields.io/badge/Flutter-000?style=flat-square&labelColor=0B0E14&logo=flutter&logoColor=02569B)

**Backend & Data**

![Node.js](https://img.shields.io/badge/Node.js-000?style=flat-square&labelColor=0B0E14&logo=nodedotjs&logoColor=339933)
![tRPC](https://img.shields.io/badge/tRPC-000?style=flat-square&labelColor=0B0E14&logo=trpc&logoColor=2596BE)
![Express](https://img.shields.io/badge/Express-000?style=flat-square&labelColor=0B0E14&logo=express)
![Prisma](https://img.shields.io/badge/Prisma-000?style=flat-square&labelColor=0B0E14&logo=prisma)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-000?style=flat-square&labelColor=0B0E14&logo=postgresql&logoColor=4169E1)
![MongoDB](https://img.shields.io/badge/MongoDB-000?style=flat-square&labelColor=0B0E14&logo=mongodb&logoColor=47A248)

**Systems & DevOps**

![Linux](https://img.shields.io/badge/Linux-000?style=flat-square&labelColor=0B0E14&logo=linux&logoColor=FCC624)
![Docker](https://img.shields.io/badge/Docker-000?style=flat-square&labelColor=0B0E14&logo=docker&logoColor=2496ED)
![Nginx](https://img.shields.io/badge/Nginx-000?style=flat-square&labelColor=0B0E14&logo=nginx&logoColor=009639)
![Caddy](https://img.shields.io/badge/Caddy-000?style=flat-square&labelColor=0B0E14&logo=caddy&logoColor=1F88C0)
![GitHub Actions](https://img.shields.io/badge/CI/CD-000?style=flat-square&labelColor=0B0E14&logo=githubactions&logoColor=2088FF)
![Stripe](https://img.shields.io/badge/Stripe-000?style=flat-square&labelColor=0B0E14&logo=stripe&logoColor=635BFF)

</div>

---

## <img src="https://api.iconify.design/lucide/badge-check.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; Certified

<div align="center">

[![OPUS Certified](https://img.shields.io/badge/OPUS_Certified-Ma%C3%AEtrise_Full--Stack_%C2%B7_DevOps_%C2%B7_Syst%C3%A8mes-7C3AED?style=for-the-badge&labelColor=0B0E14)](https://forgenet.fr/verify/OPUS-2026-Z26F2D)

<br/>

![Frontend](https://img.shields.io/badge/Frontend-9%2F10-22D3EE?style=flat-square&labelColor=0B0E14)
![Backend](https://img.shields.io/badge/Backend-8%2F10-7C3AED?style=flat-square&labelColor=0B0E14)
![DevOps](https://img.shields.io/badge/DevOps-10%2F10-22D3EE?style=flat-square&labelColor=0B0E14)
![Sysadmin & Network](https://img.shields.io/badge/Sysadmin_%26_Network-10%2F10-7C3AED?style=flat-square&labelColor=0B0E14)
![Databases](https://img.shields.io/badge/Databases-8%2F10-22D3EE?style=flat-square&labelColor=0B0E14)
![SEO & Web Perf](https://img.shields.io/badge/SEO_%26_Web_Perf-9%2F10-7C3AED?style=flat-square&labelColor=0B0E14)

<br/>

<sub><b>How to read these scores?</b> <i>Each score (out of 10) measures a concrete ability — not theory learned by heart. It reflects the ability to write clean, maintainable code and to handle a production deployment autonomously. Assessments are carried out and approved by OPUS on the basis of real, delivered projects.</i></sub>

<br/>

<sub>Verifiable at forgenet.fr/verify/OPUS-2026-Z26F2D</sub>

</div>

---

## <img src="https://api.iconify.design/lucide/languages.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; Most-used languages

<div align="center">

<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=softpython2884&layout=compact&theme=tokyonight&hide_border=true&bg_color=0B0E14&title_color=7C3AED&langs_count=10" alt="top languages" />

<sub>Public repositories only — the projects above are private and do not appear here.</sub>

</div>

---

## <img src="https://api.iconify.design/lucide/mail.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; Contact

<div align="center">

[![Forge](https://img.shields.io/badge/Platform-forgenet.fr-7C3AED?style=for-the-badge&labelColor=0B0E14&logo=googlechrome&logoColor=22D3EE)](https://forgenet.fr)
[![Email Pro](https://img.shields.io/badge/Pro-contact@forgenet.fr-22D3EE?style=for-the-badge&labelColor=0B0E14&logo=gmail&logoColor=white)](mailto:contact@forgenet.fr)
[![Email Perso](https://img.shields.io/badge/Personal-nightfury@nationquest.fr-7C3AED?style=for-the-badge&labelColor=0B0E14&logo=gmail&logoColor=white)](mailto:nightfury@nationquest.fr)

[![Discord](https://img.shields.io/badge/Discord-nightfury__httyd-5865F2?style=for-the-badge&labelColor=0B0E14&logo=discord&logoColor=white)](https://discord.com/users/nightfury_httyd)
[![Ko-fi](https://img.shields.io/badge/Support-Ko--fi-FF5E5B?style=for-the-badge&labelColor=0B0E14&logo=kofi&logoColor=white)](https://ko-fi.com/nationquestproject)

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1B2A4A,100:0B0E14&height=120&section=footer&text=Thanks%20for%20visiting&fontColor=ffffff&fontSize=20&fontAlignY=70" width="100%" alt="footer" />

---
---

## Ce qui a changé, et pourquoi

Le principe appliqué partout : **un adjectif ne prouve rien, un mécanisme oui.** Chaque fois qu'une
phrase disait qu'un truc était bien, elle a été remplacée par ce qui le fait fonctionner — et
souvent par ce que ça coûte.

### 1. Les superlatifs sont partis

| Avant | Après |
|---|---|
| `PRIVATE FLAGSHIP` / `BIGGEST OPEN-SOURCE PROJECT` (majuscules) | `private · in production` / `AGPL v3 · self-hostable` |
| « The heavy lifting. These are the **serious** systems » | « Four systems in production. Three are private, so… » |
| « **All-in-one** developer & agency platform… in one dashboard » | « Developer platform: workspace, container hosting, licensing server, store » |
| « a native, **Canva-like** no-code site builder » | « a block-based site builder that renders the tenant's public site » |
| « Most of my public repos are experiments — but one is **the real deal** » | « One is maintained, documented and deployed » |

### 2. Chaque projet gagne un mécanisme et une limite

C'est le vrai changement. Exemples :

- **Capibara** — au lieu de lister 16 modules, la carte explique `CREATE SCHEMA t_<key>`, pourquoi
  une requête ne peut pas fuiter d'un tenant à l'autre, et **ce que ça coûte** : les 182 migrations
  ne sont plus un trophée, elles sont la facture de l'isolation. Ajout d'une limite assumée :
  *pas de multi-région, pas une base par client, et le scaling au-delà d'une machine est un problème
  ouvert*.
- **OPUS** — le détail Cloud Box remplace « Pterodactyl-backed VPS » : pourquoi un vrai `sshd` est
  impossible sous Wings (uid non-root, rootfs RO, `no-new-privileges`, `CAP_SYS_CHROOT` retiré),
  donc proot + serveur SSH maison, **et ce qu'on n'a pas** : pas de Docker-in-Docker, seul
  `/home/container` survit.
- **Marcus** — « no-code visual editor » devient l'interpréteur de graphe + la persistance des
  boutons/menus en SQLite réhydratée au boot, avec la raison (sinon chaque redémarrage laisse des
  contrôles morts dans les vieux messages).
- **Elipse** — l'archi hors ligne est présentée comme une **conséquence** du mur HDS, pas comme un
  choix de design malin, et le prix est nommé : pas de serveur ⇒ sync pair-à-pair à écrire.

### 3. Le ratio de réécriture de Marcus est publié

**2,07× plus de lignes écrites que de lignes gardées.** C'est le chiffre le moins flatteur de la
page et il est mis en badge. Rien ne crédibilise plus vite le reste des chiffres qu'un chiffre qui
ne t'arrange pas.

### 4. Les euros sortent des cartes

Avant : `~2.46M€` en badge orange sur chaque projet, méthode en tout petit après. Un lecteur
sceptique voit le montant d'abord et décroche.

Après : **aucun € sur les cartes**, une seule section « Rebuild cost » avec la méthode **avant** le
tableau, le mot « rebuild » assumé, et deux garde-fous ajoutés :
- l'hypothèse de productivité est au **haut** de la fourchette publiée 10–20 lignes/heure, donc une
  erreur va vers le bas, pas vers le haut ;
- les 11 % de lignes / 29 % du coût de Capibara servent à justifier pourquoi une moyenne plate
  n'aurait rien valu.

Les chiffres sont identiques, c'est la mise en scène qui change.

### 5. Ce qui a été supprimé

- **« Un nouveau Grand Projet arrive. »** — teaser pur, zéro contenu vérifiable. C'était l'élément
  le plus « pub » du fichier. *(Facile à remettre si tu y tiens.)*
- **« The real heavy lifting happens off GitHub »** — remplacé par une explication factuelle de
  *pourquoi* c'est privé (travail client, produits vendus) et de ce qu'on peut vérifier à la place.
- **« Public repos are my playground. The real work is private. »** (bandeau animé) — remplacé par
  la liste des technos.
- **`### *From the kernel up.*`** en signature — slogan.
- **Les badges « Team — ~46 people »** — un effectif ne se vérifie pas depuis l'extérieur, et à
  côté d'un montant en euros ça ressemble à un argumentaire commercial. L'info reste dans la
  section coût, à sa place.

### 6. La distro Linux dit enfin la vérité

C'était le point le plus attaquable : trois paragraphes ambitieux, aucun lien, aucun artefact. La
nouvelle version l'annonce en sous-titre — *unfinished, nothing to download* — et se termine par
« prends ça comme une déclaration d'intention tant qu'il n'y a rien à installer ».

Un lecteur technique le pardonne toujours quand c'est annoncé. Jamais quand il le découvre.

### 7. Petits ajouts factuels

- `Locales — fr en es de` au lieu de `Languages — 4` (on lit lesquelles).
- `Event handlers — 114` sur Marcus (compté dans le repo).
- `Licence signing — Ed25519 JWS` sur OPUS : vérifiable hors ligne, non rejouable.
- Une ligne sous le graphe des langages : *dépôts publics uniquement, les projets ci-dessus sont
  privés et n'y apparaissent pas* — sinon le graphe contredit silencieusement le reste de la page.

---

**Pour l'appliquer :** `cp PREVIEW.md README.md` puis on enlève le bandeau du haut et cette section.
Dis-moi ce que tu gardes et ce que tu jettes — notamment le teaser, les badges d'équipe et la
signature, qui sont des choix, pas des erreurs.
