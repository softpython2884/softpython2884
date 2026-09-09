<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0B0E14,100:1B2A4A&height=210&section=header&text=NightFury&fontColor=ffffff&fontSize=66&fontAlignY=34&desc=Full-Stack%20%C2%B7%20SysAdmin%20%C2%B7%20OS%20Builder&descSize=18&descAlignY=58&animation=fadeIn" width="100%" alt="NightFury" />

<a href="https://forgenet.fr">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=900&color=22D3EE&center=true&vCenter=true&width=760&lines=Founder+%40+Forge+Network+%E2%80%94+forgenet.fr;Multi-tenant+SaaS+%C2%B7+one+database+schema+per+customer;~20+apps+in+production+%C2%B7+302+models+%C2%B7+fr%2Fen%2Fes%2Fde;TypeScript+%C2%B7+Flutter+%C2%B7+PostgreSQL+%C2%B7+Docker+%C2%B7+Debian" alt="What I do" />
</a>

<br/>

[![Forge Network](https://img.shields.io/badge/Forge_Network-forgenet.fr-7C3AED?style=flat-square&labelColor=0B0E14)](https://forgenet.fr)
[![Capibara](https://img.shields.io/badge/Capibara-capibara.fr-22D3EE?style=flat-square&labelColor=0B0E14&logo=icloud&logoColor=white)](https://capibara.fr)
[![Marcus](https://img.shields.io/badge/Marcus-marcusbot.fr-5865F2?style=flat-square&labelColor=0B0E14&logo=discord&logoColor=white)](https://marcusbot.fr)
[![Location](https://img.shields.io/badge/France-UTC%2B1-ffffff?style=flat-square&labelColor=0B0E14&logo=googlemaps&logoColor=22D3EE)](#)

</div>

---

### <img src="https://api.iconify.design/lucide/user-round.svg?color=%237C3AED&height=22" height="22" alt="" />&nbsp; About

I'm **NightFury**, a French developer, and I run **Forge Network** (`forgenet.fr`) — a non-profit
association that publishes the projects on this page.

I tend to take a product across its whole stack rather than one layer of it: the database and its
isolation model, the API, the interface, then the Debian machine it runs on — nginx, Docker, PM2,
certificates, backups. Most of what follows exists because something had to be decided at that
level.

```javascript
const nightFury = {
  role:    ["Full-Stack", "SysAdmin", "Data Eng", "OS Builder"],
  founder: "Forge Network · forgenet.fr",
  stack:   ["TypeScript", "Next.js", "React", "Node", "Dart", "PostgreSQL", "Docker", "Linux"],
  now:     ["Capibara (SaaS suite)", "a custom Linux distro", "a new Grand Projet"],
  learning:"Scala & high-performance JVM systems",
};
```

---

## <img src="https://api.iconify.design/lucide/shield.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; OpenCoperLock &nbsp;·&nbsp; <sub>the one you can read</sub>

> My main open-source project, and the only place where the claims on this page can be checked
> against the source. Everything after it is private, so start here.

<div align="center">

<table>
<tr><td width="850" align="center">

### <img src="https://api.iconify.design/lucide/hard-drive.svg?color=%237C3AED&height=24" height="24" alt="" /> A private cloud for one dedicated machine

*A self-hostable Drive — files, folders, quotas, sharing — with three things most "drop a file" tools don't have.*

![TypeScript](https://img.shields.io/badge/TypeScript-000?style=flat-square&labelColor=0B0E14&logo=typescript&logoColor=3178C6)
![Next.js](https://img.shields.io/badge/Next.js_15-000?style=flat-square&labelColor=0B0E14&logo=nextdotjs)
![Fastify](https://img.shields.io/badge/Fastify_5-000?style=flat-square&labelColor=0B0E14&logo=fastify)
![Prisma](https://img.shields.io/badge/Prisma_6-000?style=flat-square&labelColor=0B0E14&logo=prisma)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-000?style=flat-square&labelColor=0B0E14&logo=postgresql&logoColor=4169E1)
![Docker](https://img.shields.io/badge/Docker-000?style=flat-square&labelColor=0B0E14&logo=docker&logoColor=2496ED)

**Quick-Upload** opens a temporary drop zone on any device from a code — no login — with optional
password, expiry and usage limit. **Remote-Upload** makes the server fetch a link itself, so a phone
on a metered connection never relays the bytes. **Hybrid encryption** is a choice made per folder:
encrypted at rest so the antivirus can still scan the file, or a zero-knowledge vault encrypted in
the browser that the server cannot read at all.

Shared Spaces are encrypted server-side only, because a zero-knowledge vault cannot be shared —
that trade-off is written in the docs rather than left for you to discover. Same for the rest:
background work runs inside the API process to keep a deployment to a single moving part, with
Redis/BullMQ documented as the upgrade for horizontal scale instead of required up front.

<sub>Antivirus scanning on upload · WebDAV mounting · personal-token REST API · desktop right-click integration · one-click self-update from GitHub · architecture, security policy and a candid threat model in `docs/`</sub>

![arch](https://img.shields.io/badge/Architecture-pnpm_monorepo-7C3AED?style=flat-square&labelColor=0B0E14)
![files](https://img.shields.io/badge/TS_files-~148-22D3EE?style=flat-square&labelColor=0B0E14)
![enc](https://img.shields.io/badge/At_rest-AES--256--GCM-7C3AED?style=flat-square&labelColor=0B0E14)
![hash](https://img.shields.io/badge/Passwords-Argon2id-22D3EE?style=flat-square&labelColor=0B0E14)
![license](https://img.shields.io/badge/License-AGPL_v3-7C3AED?style=flat-square&labelColor=0B0E14)

<br/>

![cost](https://img.shields.io/badge/Est._rebuild_cost-~155k%E2%82%AC-F59E0B?style=flat-square&labelColor=0B0E14)
![effort](https://img.shields.io/badge/Est._effort-~12_person--months-F59E0B?style=flat-square&labelColor=0B0E14)

[![Repo](https://img.shields.io/badge/▶_Read_the_source-181717?style=for-the-badge&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/OpenCoperLock)
[![Live](https://img.shields.io/badge/copper.forgenet.fr-22D3EE?style=for-the-badge&labelColor=0B0E14)](https://copper.forgenet.fr)

</td></tr>
</table>

</div>

---

## <img src="https://api.iconify.design/lucide/rocket.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; Flagship Work

> Four systems in production. All four are private — client work and products that are sold — so the
> links go to the live product or the download, and the numbers come from the repositories.

<div align="center">

<!-- ============== CAPIBARA ============== -->
<table>
<tr><td width="850" align="center">

### <img src="https://api.iconify.design/lucide/bird.svg?color=%237C3AED&height=24" height="24" alt="" /> Capibara &nbsp;·&nbsp; <sub>private · in production</sub>

*The software a small company runs its day on: quotes, invoices, accounting, customers, stock, staff, shop — and the website that fronts it.*

![Next.js](https://img.shields.io/badge/Next.js_15-000?style=flat-square&labelColor=0B0E14&logo=nextdotjs)
![React](https://img.shields.io/badge/React_19-000?style=flat-square&labelColor=0B0E14&logo=react&logoColor=61DAFB)
![tRPC](https://img.shields.io/badge/tRPC_v11-000?style=flat-square&labelColor=0B0E14&logo=trpc&logoColor=2596BE)
![Prisma](https://img.shields.io/badge/Prisma-000?style=flat-square&labelColor=0B0E14&logo=prisma)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-000?style=flat-square&labelColor=0B0E14&logo=postgresql&logoColor=4169E1)
![Stripe](https://img.shields.io/badge/Stripe-000?style=flat-square&labelColor=0B0E14&logo=stripe&logoColor=635BFF)
![Docker](https://img.shields.io/badge/Docker-000?style=flat-square&labelColor=0B0E14&logo=docker&logoColor=2496ED)

Around twenty applications sharing one set of customers, one accounting ledger and one search index,
so an invoice, the stock movement behind it and the ticket about it are the same object seen from
three places. Each company also gets a public website it edits itself, built from blocks, served
from its own domain.

The isolation is structural rather than a filter: **every customer gets its own copy of the database
schema**, so one company's data can't turn up in another's query even if a `WHERE` clause is
forgotten. What it costs is honest to state — a schema change has to be replayed on every customer,
which is where the 182 tenant migrations come from, and why a deployment stops instead of running
new code against a database that hasn't caught up.

CRM · French invoicing (Factur-X) · Accounting with FEC export · Shop · Inventory · Purchasing · Planning · Support · Projects · HR · Training · Blog · Newsletter · Chat · Wiki & storage

<sub>Permissions are re-read from the database on every call rather than trusted from the session · Meilisearch, MinIO, a mail server with webmail, self-hosted video and a Stripe Connect marketplace each run as their own container · Not multi-region and not one database per client: a single Postgres holds them all, and scaling past one machine is a known open problem rather than a solved one.</sub>

![files](https://img.shields.io/badge/TS_files-~2%2C480-7C3AED?style=flat-square&labelColor=0B0E14)
![loc](https://img.shields.io/badge/LOC-~364k-22D3EE?style=flat-square&labelColor=0B0E14)
![models](https://img.shields.io/badge/Data_models-302-7C3AED?style=flat-square&labelColor=0B0E14)
![migrations](https://img.shields.io/badge/Tenant_migrations-182-22D3EE?style=flat-square&labelColor=0B0E14)
![tests](https://img.shields.io/badge/Tests-5%2C200%2B-7C3AED?style=flat-square&labelColor=0B0E14)
![langs](https://img.shields.io/badge/Locales-fr_en_es_de-22D3EE?style=flat-square&labelColor=0B0E14)
![svc](https://img.shields.io/badge/Docker_services-17-7C3AED?style=flat-square&labelColor=0B0E14)

<br/>

![cost](https://img.shields.io/badge/Est._rebuild_cost-~2.46M%E2%82%AC-F59E0B?style=flat-square&labelColor=0B0E14)
![effort](https://img.shields.io/badge/Est._effort-~189_person--months-F59E0B?style=flat-square&labelColor=0B0E14)

<sub><i>Payment, security and compliance code is 11 % of the lines and 29 % of that estimate.</i></sub>

[![Visit Capibara](https://img.shields.io/badge/▶_capibara.fr-7C3AED?style=for-the-badge&labelColor=0B0E14)](https://capibara.fr)
[![Forge Network](https://img.shields.io/badge/forgenet.fr-22D3EE?style=for-the-badge&labelColor=0B0E14)](https://forgenet.fr)

</td></tr>
</table>

<!-- ============== OPUS ============== -->
<table>
<tr><td width="850" align="center">

### <img src="https://api.iconify.design/lucide/layout-dashboard.svg?color=%237C3AED&height=24" height="24" alt="" /> OPUS &nbsp;·&nbsp; <sub>forgenet.fr</sub>

*The platform Forge Network runs on: client projects and invoicing, server hosting, software licensing and a store.*

![React](https://img.shields.io/badge/React_19-000?style=flat-square&labelColor=0B0E14&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite_6-000?style=flat-square&labelColor=0B0E14&logo=vite&logoColor=646CFF)
![Express](https://img.shields.io/badge/Express_4-000?style=flat-square&labelColor=0B0E14&logo=express)
![Prisma](https://img.shields.io/badge/Prisma_6-000?style=flat-square&labelColor=0B0E14&logo=prisma)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-000?style=flat-square&labelColor=0B0E14&logo=postgresql&logoColor=4169E1)
![Stripe](https://img.shields.io/badge/Stripe-000?style=flat-square&labelColor=0B0E14&logo=stripe&logoColor=635BFF)

**OPUS Cloud** rents out servers with a console, a web file manager and backups in the browser. A
Cloud Box behaves like a small VPS — SSH, a persistent home directory, your own packages — but it
isn't a virtual machine: the sandbox refuses the privileges a normal SSH daemon needs, so the box
ships its own lightweight root filesystem and SSH server instead. Docker doesn't run inside it and
only the home directory survives a rebuild. Both limits are on the page, not discovered after
signing up.

**Forge Licensing** issues the licence keys for the group's software. Every answer is signed, so an
application can verify a licence without calling home and a captured answer can't be replayed as a
valid one. Elipse RSAI runs on it.

<sub>Client workspace with quotes, invoices and instalment plans · certification program (27 tracks × 4 levels × 5 real-project briefs) · store with Stripe checkout and automatic licence delivery · news feed with RSS</sub>

![models](https://img.shields.io/badge/Data_models-94-7C3AED?style=flat-square&labelColor=0B0E14)
![loc](https://img.shields.io/badge/LOC-~92k-22D3EE?style=flat-square&labelColor=0B0E14)
![routes](https://img.shields.io/badge/API_route_files-52-7C3AED?style=flat-square&labelColor=0B0E14)
![cert](https://img.shields.io/badge/Assessments-540-22D3EE?style=flat-square&labelColor=0B0E14)
![sig](https://img.shields.io/badge/Licences-signed_%C2%B7_offline--verifiable-7C3AED?style=flat-square&labelColor=0B0E14)

<br/>

![cost](https://img.shields.io/badge/Est._rebuild_cost-~687k%E2%82%AC-F59E0B?style=flat-square&labelColor=0B0E14)
![effort](https://img.shields.io/badge/Est._effort-~53_person--months-F59E0B?style=flat-square&labelColor=0B0E14)

[![Live](https://img.shields.io/badge/▶_forgenet.fr-7C3AED?style=for-the-badge&labelColor=0B0E14)](https://forgenet.fr)
[![Console](https://img.shields.io/badge/console.forgenet.fr-22D3EE?style=for-the-badge&labelColor=0B0E14)](https://console.forgenet.fr)

</td></tr>
</table>

<!-- ============== MARCUS ============== -->
<table>
<tr><td width="850" align="center">

### <img src="https://api.iconify.design/lucide/bot.svg?color=%237C3AED&height=24" height="24" alt="" /> Marcus &nbsp;·&nbsp; <sub>marcusbot.fr</sub>

*A Discord bot that server owners extend themselves — by drawing what they want, not by writing code.*

![Discord.js](https://img.shields.io/badge/Discord.js_14-000?style=flat-square&labelColor=0B0E14&logo=discord&logoColor=5865F2)
![Next.js](https://img.shields.io/badge/Next.js_15-000?style=flat-square&labelColor=0B0E14&logo=nextdotjs)
![SQLite](https://img.shields.io/badge/better--sqlite3-000?style=flat-square&labelColor=0B0E14&logo=sqlite&logoColor=003B57)
![Gemini](https://img.shields.io/badge/Genkit_·_Gemini_2.5-000?style=flat-square&labelColor=0B0E14&logo=googlegemini&logoColor=8E75FF)

The usual bot features — 93 commands, levels, moderation with an AI pass, premium tiers — plus a
visual editor where a module is a diagram of blocks. Nothing is compiled: the editor saves a graph
and one interpreter walks it at runtime, so a server owner can build a ticket system or a role menu
without touching a line of TypeScript.

The hard part was never the editor. A button posted in a Discord channel outlives the process that
posted it, so every component is written to the database and restored when the bot boots — without
that, each restart leaves dead buttons in old messages. That, and the fact that Discord's limits
(five buttons a row, five rows a message) have to be enforced in the editor rather than discovered
by the user when the message fails to send.

![files](https://img.shields.io/badge/Files-~579-7C3AED?style=flat-square&labelColor=0B0E14)
![loc](https://img.shields.io/badge/LOC-~105k-22D3EE?style=flat-square&labelColor=0B0E14)
![cmd](https://img.shields.io/badge/Commands-93-7C3AED?style=flat-square&labelColor=0B0E14)
![events](https://img.shields.io/badge/Event_handlers-114-22D3EE?style=flat-square&labelColor=0B0E14)
![flows](https://img.shields.io/badge/AI_flows-30-7C3AED?style=flat-square&labelColor=0B0E14)
![rework](https://img.shields.io/badge/Written_%2F_kept-2.07x-22D3EE?style=flat-square&labelColor=0B0E14)

<br/>

![cost](https://img.shields.io/badge/Est._rebuild_cost-~867k%E2%82%AC-F59E0B?style=flat-square&labelColor=0B0E14)
![effort](https://img.shields.io/badge/Est._effort-~67_person--months-F59E0B?style=flat-square&labelColor=0B0E14)

<sub><i>Least flattering number on this page, and it stays: 2.07× more lines were written than survive. The visual editor was rebuilt more than once.</i></sub>

[![Live](https://img.shields.io/badge/▶_marcusbot.fr-7C3AED?style=for-the-badge&labelColor=0B0E14)](https://marcusbot.fr)

</td></tr>
</table>

<!-- ============== ELIPSE RSAI ============== -->
<table>
<tr><td width="850" align="center">

### <img src="https://api.iconify.design/lucide/heart-pulse.svg?color=%237C3AED&height=24" height="24" alt="" /> Elipse RSAI &nbsp;·&nbsp; <sub>private · shipped</sub>

*A field app for the health referents who follow French nurseries — on the phone, in the car, with no signal and no account.*

![Flutter](https://img.shields.io/badge/Flutter_3-000?style=flat-square&labelColor=0B0E14&logo=flutter&logoColor=02569B)
![Dart](https://img.shields.io/badge/Dart_3-000?style=flat-square&labelColor=0B0E14&logo=dart&logoColor=0175C2)
![SQLite](https://img.shields.io/badge/SQLite-000?style=flat-square&labelColor=0B0E14&logo=sqlite&logoColor=003B57)
![Android](https://img.shields.io/badge/Android_8%2B-000?style=flat-square&labelColor=0B0E14&logo=android&logoColor=3DDC84)
![Windows](https://img.shields.io/badge/Windows_10%2B-000?style=flat-square&labelColor=0B0E14&logo=windows&logoColor=0078D4)

A referent covers 5 to 30 nurseries and owes each one a number of hours set by decree, split by
quarter, and has to be able to prove it. Between two visits it gets written on a notepad, or not at
all, and reconstructed in December. The app logs a visit in three taps, keeps four counters per
nursery, and flags the quarter that is drifting — the quarterly minimum is the one people miss, you
can reach the annual total and still be short on three quarters. It then writes the paperwork —
visit reports, referral letters, care plans, annual review — as PDFs, offline.

Nothing leaves the device, and that is a consequence rather than a preference. Records naming a
child are health data; hosting them in France requires a certification well out of reach for a
project this size, so the hosted version was dropped and the server removed entirely. The bill lands
on synchronisation: with no server to reconcile against, two devices sync directly over the local
wifi, or through an encrypted file on a USB stick when the nursery network keeps them apart — which
it often does.

<sub>Local database with sensitive fields encrypted · devices paired by QR code and a six-digit code read out loud · PDF engine written in Dart, no network · the only outbound call checks the licence and carries no data about anyone · an expired licence drops the app to read-only and never holds the records hostage</sub>

![files](https://img.shields.io/badge/Dart_files-182-7C3AED?style=flat-square&labelColor=0B0E14)
![loc](https://img.shields.io/badge/LOC-~74k-22D3EE?style=flat-square&labelColor=0B0E14)
![screens](https://img.shields.io/badge/Screens-49-7C3AED?style=flat-square&labelColor=0B0E14)
![tests](https://img.shields.io/badge/Test_files-58-22D3EE?style=flat-square&labelColor=0B0E14)
![targets](https://img.shields.io/badge/Targets-Android_%26_Windows-7C3AED?style=flat-square&labelColor=0B0E14)
![version](https://img.shields.io/badge/Version-1.6.2-22D3EE?style=flat-square&labelColor=0B0E14)

<br/>

![cost](https://img.shields.io/badge/Est._rebuild_cost-~434k%E2%82%AC-F59E0B?style=flat-square&labelColor=0B0E14)
![effort](https://img.shields.io/badge/Est._effort-~33_person--months-F59E0B?style=flat-square&labelColor=0B0E14)

<sub><i>17k lines of tests against 56k lines of app. The rules that decide whether someone is compliant are kept apart from the interface so they can be tested on their own.</i></sub>

[![Download](https://img.shields.io/badge/▶_Download-7C3AED?style=for-the-badge&labelColor=0B0E14)](https://forgenet.fr/telechargements/elipse)

</td></tr>
</table>

<br/>

### <img src="https://api.iconify.design/lucide/calculator.svg?color=%237C3AED&height=24" height="24" alt="" />&nbsp; Where those estimates come from

| Project | Lines counted | Effort | Rebuild cost | Written / kept |
|:---|---:|---:|---:|---:|
| **Capibara** | 430 122 | 189 person-months | ~2.46 M€ | 1.14× |
| **Marcus** | 112 364 | 67 person-months | ~867 k€ | 2.07× |
| **OPUS** | 103 925 | 53 person-months | ~687 k€ | 1.39× |
| **Elipse RSAI** | 83 471 | 33 person-months | ~434 k€ | 1.05× |
| **OpenCoperLock** | 28 147 | 12 person-months | ~155 k€ | 1.12× |

<sub><b>Not money anyone spent.</b> <i>These estimate what it would cost to <b>rebuild</b> each project from scratch with a senior team at the 2026 French senior rate (~650 €/day) — and they are computed rather than guessed. The script is <a href="tools/estimate.py"><code>tools/estimate.py</code></a> and it runs on any of these repositories.</i></sub>

<sub><b>How.</b> <i>Every file is sorted into a zone — payment, security, compliance, integrations, business logic, interface, data model, infrastructure, tests, docs — and each zone carries its own lines-per-hour rate, because billing code with idempotency, webhooks and reconciliation does not cost what CRUD costs. Git history then adds what was written and later rewritten or thrown away, since abandoned work took the same time, and an overhead factor covers what leaves no file behind: architecture, deployment, operations.</i></sub>

<sub><b>A person-month</b> <i>is one person working full time for one month. It is a unit of effort, not a headcount — 189 person-months is roughly what a team of ~46 delivers in four months.</i></sub>

<sub><b>Two caveats.</b> <i>The productivity assumption sits at the optimistic end of the published 10–20 lines/hour range, so if these figures are wrong they are low rather than high. And on Capibara, payment, security and compliance code is 11 % of the lines but 29 % of the estimate — which is exactly why a flat average would have been worthless here.</i></sub>

</div>

---

## <img src="https://api.iconify.design/lucide/package-open.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; More public repositories

> Experiments, tools and weekend builds. Smaller, and that's the point.

<div align="center">

<table>
<tr>
<td width="425" valign="top">

#### <img src="https://api.iconify.design/lucide/brain.svg?color=%237C3AED&height=20" height="20" alt="" /> [Gemini-Assistant](https://github.com/softpython2884/Gemini-Assistant)

A clipboard assistant that stays in the background. A hotkey grabs the selection from whatever
application is in front, sends it to Gemini and pastes the answer at the cursor — falling back to
another model when a quota runs out.

![Python](https://img.shields.io/badge/Python-000?style=flat-square&labelColor=0B0E14&logo=python&logoColor=3776AB)
![Gemini](https://img.shields.io/badge/Google_Gemini-000?style=flat-square&labelColor=0B0E14&logo=googlegemini&logoColor=8E75FF)

[![Repo](https://img.shields.io/badge/Code-181717?style=flat-square&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/Gemini-Assistant)

</td>
<td width="425" valign="top">

#### <img src="https://api.iconify.design/lucide/link.svg?color=%237C3AED&height=20" height="20" alt="" /> [NightSlavery](https://github.com/softpython2884/NightSlavery)

A Minecraft Fabric mod (1.21, Java 21) inspired by *Kenshi*: capture built as a state machine —
free, knocked out, imprisoned, enslaved — with cages, a control scepter, escapes, rebellions, and
gamerule switches so it can't be used to grief a server.

![Java](https://img.shields.io/badge/Java_21-000?style=flat-square&labelColor=0B0E14&logo=openjdk&logoColor=white)
![Fabric](https://img.shields.io/badge/Fabric_·_MC_1.21-000?style=flat-square&labelColor=0B0E14)

[![Repo](https://img.shields.io/badge/Code-181717?style=flat-square&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/NightSlavery)

</td>
</tr>
<tr>
<td width="425" valign="top">

#### <img src="https://api.iconify.design/lucide/gamepad-2.svg?color=%237C3AED&height=20" height="20" alt="" /> [Macro](https://github.com/softpython2884/Macro)

An older one. A console-style layer for the TV, navigable entirely with an Xbox controller, that
launches local games and media — bridged to Windows through a Python hotkey listener.

![Next](https://img.shields.io/badge/Next.js-000?style=flat-square&labelColor=0B0E14&logo=nextdotjs)
![Python](https://img.shields.io/badge/Python-000?style=flat-square&labelColor=0B0E14&logo=python&logoColor=3776AB)

[![Repo](https://img.shields.io/badge/Code-181717?style=flat-square&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/Macro)

</td>
<td width="425" valign="top">

#### <img src="https://api.iconify.design/lucide/sliders-horizontal.svg?color=%237C3AED&height=20" height="20" alt="" /> StreamDeck utilities

Gaming and office setups need different mice and different speakers. Two PowerShell scripts on one
key: **MouseMode** swaps the Windows pointer profile, **AudioSwitcher** changes the default output
*and* moves every running application onto the new device.

![PowerShell](https://img.shields.io/badge/PowerShell-000?style=flat-square&labelColor=0B0E14&logo=powershell&logoColor=5391FE)

[![MouseMode](https://img.shields.io/badge/MouseMode-181717?style=flat-square&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/MouseMode)
[![AudioSwitcher](https://img.shields.io/badge/AudioSwitcher-181717?style=flat-square&labelColor=0B0E14&logo=github)](https://github.com/softpython2884/AudioSwitcher)

</td>
</tr>
</table>

<sub><b>Also in the lab</b></sub>

[![Betty](https://img.shields.io/badge/Betty-gamified_coding_edu-7C3AED?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/Betty)
[![SimuBourse](https://img.shields.io/badge/SimuBourse-financial_sim-22D3EE?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/SimuBourse)
[![StudyVerse](https://img.shields.io/badge/StudyVerse-AI_notes-7C3AED?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/StudyVerse)
[![CreepOS](https://img.shields.io/badge/CreepOS-horror_fake--OS_game-22D3EE?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/CreepOS)
[![OpenMark-Blog](https://img.shields.io/badge/OpenMark-AI_blogging-7C3AED?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/OpenMark-Blog)
[![Mana-Clash](https://img.shields.io/badge/Mana--Clash-tactical_card_game-22D3EE?style=flat-square&labelColor=0B0E14)](https://github.com/softpython2884/Mana-Clash)

</div>

---

## <img src="https://api.iconify.design/lucide/monitor.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; Custom Linux distribution &nbsp;·&nbsp; <sub>unfinished, nothing to download</sub>

The least finished thing on this page, and the only one with no artifact behind it: no installer, no
release, no repository yet. The target is a distribution built against the bare kernel — its own
window manager, session, package and file managers — rather than a theme over an existing desktop,
aiming for Arch-level configurability without Arch-level setup.

It's here because it's where a large share of my time goes, not because it's usable. Treat it as a
statement of intent until there's something to install.

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
![Redis](https://img.shields.io/badge/Redis-000?style=flat-square&labelColor=0B0E14&logo=redis&logoColor=DC382D)
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

## <img src="https://api.iconify.design/lucide/languages.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; What I actually write

<div align="center">

![TypeScript](https://img.shields.io/badge/TypeScript-82.8_%25-3178C6?style=flat-square&labelColor=0B0E14)
![Dart](https://img.shields.io/badge/Dart-10.3_%25-0175C2?style=flat-square&labelColor=0B0E14)
![SQL](https://img.shields.io/badge/SQL-1.4_%25-4169E1?style=flat-square&labelColor=0B0E14)
![Prisma](https://img.shields.io/badge/Prisma-1.3_%25-2D3748?style=flat-square&labelColor=0B0E14)
![Java](https://img.shields.io/badge/Java-1.3_%25-EA2D2E?style=flat-square&labelColor=0B0E14)
![HTML / CSS](https://img.shields.io/badge/HTML_%2F_CSS-1.2_%25-E34F26?style=flat-square&labelColor=0B0E14)
![Shell](https://img.shields.io/badge/Shell-0.8_%25-4EAA25?style=flat-square&labelColor=0B0E14)
![Python](https://img.shields.io/badge/Python-0.2_%25-3776AB?style=flat-square&labelColor=0B0E14)

<sub><i>Counted across the eight repositories behind this page — <b>717 526 lines</b>, private ones included. Re-derive it with <a href="tools/languages.py"><code>tools/languages.py</code></a>. A GitHub language graph would only see the public repos, which is the smaller half.</i></sub>

</div>

---

## <img src="https://api.iconify.design/lucide/badge-check.svg?color=%237C3AED&height=26" height="26" alt="" />&nbsp; Certified

<div align="center">

[![OPUS Certified](https://img.shields.io/badge/OPUS_Certified-Ma%C3%AEtrise_Full--Stack_%C2%B7_DevOps_%C2%B7_Syst%C3%A8mes-7C3AED?style=for-the-badge&labelColor=0B0E14)](https://forgenet.fr/verify/OPUS-2026-Z26F2D)

<br/>

![Frontend](https://img.shields.io/badge/Frontend_%C2%B7_React_%2F_Vue_%2F_Next.js_%2F_TypeScript-8%2F10-22D3EE?style=flat-square&labelColor=0B0E14)

![Backend](https://img.shields.io/badge/Backend_%C2%B7_Node.js_%2F_REST_APIs_%2F_Next.js-9%2F10-7C3AED?style=flat-square&labelColor=0B0E14)

![DevOps](https://img.shields.io/badge/DevOps_%C2%B7_Git_%2F_GitHub_%2F_CI--CD-10%2F10-22D3EE?style=flat-square&labelColor=0B0E14)

![Systems](https://img.shields.io/badge/Systems_%26_network_%C2%B7_Linux_%2F_Windows_%2F_GCP-10%2F10-7C3AED?style=flat-square&labelColor=0B0E14)

![Databases](https://img.shields.io/badge/Databases_%C2%B7_SQL_%2F_Prisma_%2F_PostgreSQL_%2F_MariaDB_%2F_Redis-9%2F10-22D3EE?style=flat-square&labelColor=0B0E14)

![SEO](https://img.shields.io/badge/Technical_SEO_%26_web_performance-10%2F10-7C3AED?style=flat-square&labelColor=0B0E14)

<br/>

<sub><b>How to read these scores?</b> <i>Each score (out of 10) measures a concrete ability — not theory learned by heart. It reflects the ability to write clean, maintainable code and to handle a production deployment autonomously. Assessments are carried out and approved by OPUS on the basis of real, delivered projects.</i></sub>

<br/>

<sub>Verifiable at <a href="https://forgenet.fr/verify/OPUS-2026-Z26F2D">forgenet.fr/verify/OPUS-2026-Z26F2D</a></sub>

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
