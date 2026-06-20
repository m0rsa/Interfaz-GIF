# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Single-file personal finance dashboard (`finanzas.html`) — vanilla HTML/CSS/JavaScript, no build step, no dependencies beyond CDN-loaded Chart.js 4.4.1 and Google Fonts. Open directly in any browser.

## Architecture

All state lives in a single `data` object in the `<script>` block (line 545):

```js
data = {
  ingresos: [...],   // income records
  egresos: [...],    // cash expense records
  ahorros: [...],    // savings/investment movements
  deudaTC: number,   // current credit card balance (USD)
  movTC: [...],      // credit card transaction log
  sueldo: number,    // next expected salary (USD, editable inline)
}
```

**Currency model:** everything is stored in USD internally. The constants `USD_C`, `USD_V`, `USD_ARS` (line 540) are the buy/sell/average ARS exchange rate hardcoded at the top — update them manually when the rate changes. All display conversions multiply `usd × USD_ARS`.

**Account/instrument system:** `INSTRUMENTOS` (line 541) is the fixed list of savings vehicles. `getSaldos()` (line 601) computes live balances by summing across `ahorros`, `ingresos`, `egresos`, and credit card payments — there is no separate account balance field.

**Sections:** five sections (`resumen`, `ingresos`, `egresos`, `ahorro`, `patrimonio`) toggled via `showSection()`. Each renders independently; `renderAll()` refreshes everything. Charts are Chart.js instances stored in `chartFlujo`, `chartPatrim`, `chartEvo` — always destroy before re-creating to avoid memory leaks.

**MQV (Mejor que Voy):** projected next-month wealth = current net balance + `data.sueldo`. Editable inline in the Resumen section.

## Key functions

| Function | Purpose |
|---|---|
| `getSaldos()` | Computes live per-instrument balances from all transaction arrays |
| `eliminarTC(id)` | Deletes a TC record and reverses its effect on `deudaTC` (gastos subtract, pagos add back) |

## Updating the exchange rate

Change `USD_C`, `USD_V` on line 540 — `USD_ARS` is derived as their average. The sidebar footer (line 353) has a hardcoded display string that must also be updated manually.

## Adding a new instrument/account

Four places must stay in sync:

1. `INSTRUMENTOS` array (line 541) — drives account selectors and `getSaldos()`
2. `COLORS` object (line 542) — color used in charts and account pills
3. `ICONS` object (line 543) — emoji shown in the Patrimonio grid
4. `<select id="ah-tipo">` in the HTML (line 504) — the savings form dropdown

## Data persistence

**There is none.** All data resets on page refresh. To persist: add `localStorage` calls in `renderAll()` and on each mutation, and load from `localStorage` in the init block at the bottom (line 819).

## Gotcha: initial record IDs

Seed records in `data` use hardcoded numeric IDs (e.g. 101–115 for ingresos, 1–6 for ahorros). New records use `Date.now()`. If a seed ID ever collides with a `Date.now()` value, `eliminar()` will delete the wrong record. Keep seed IDs small (< 1 000) to avoid this.
