# How-To #2: a period picker for year, year to date, quarter and month

Build one picker that switches a whole Tableau page between comparisons: the span (year, year to date, quarter or month), the report date it ends on (today, or any closed month-end), and whether it's compared with last year or the prior period. Two shaded windows on a line show exactly which days each number covers. A month-end compares with month-ends and any other day with the same day, so "to date" is always fair, and every date is counted back from the latest day in the data, so no year is typed anywhere.

## ⬇️ Download

**[Download everything (period-selection-files.zip)](https://github.com/thialp/tableau-how-to/raw/main/02-period-selection/period-selection-files.zip)**, under 1 MB: the data (`arcadia_daily_headcount.csv`, every day from Jun 30, 2021 to Jul 5, 2026) and the images (folder `Arcadia How-To`).

## Get started

1. Unzip the file.
2. Move the folder **Arcadia How-To** into `Documents/My Tableau Repository/Shapes/` (on Windows, `Documents\My Tableau Repository\Shapes\`), replacing How-To #1's folder if you have it, then restart Tableau.
3. Open a new Tableau workbook, connect to `arcadia_daily_headcount.csv`, and follow the steps.

## The steps

- **In Tableau:** download the workbook from Tableau Public (the download icon under the viz) and open its tabs **Step 1** to **Step 15**. Each sheet's caption, on its left, has that step's instructions and every formula to paste.
- **On this page:** the same 15 steps, with the reasons behind them, are in the **[step-by-step guide](GUIDE.md)**.

## Use it on your own data

The data is a daily balance: a count on every day, like headcount, open positions or inventory. Swap in your own count and date, change one number if your fiscal year doesn't start in July, and every window keeps working. For a flow (hires, sales), sum the days inside each window instead; the guide shows how.

---

Arcadia Systems is a fictional company; all data is synthetic. The data is the daily headcount mart of the [Arcadia people analytics warehouse](https://github.com/thialp/people-analytics-warehouse). Images: the Arcadia design system ([Figma UI kit](https://www.figma.com/community/file/1690422855000144024)). Built by Thiago Alpoin · [LinkedIn](https://www.linkedin.com/in/thiagoalpoin) · MIT License.
