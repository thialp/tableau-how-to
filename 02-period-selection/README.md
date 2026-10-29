# How-To #2: a period picker for year, year to date, quarter and month

Build one picker that switches a whole Tableau page between comparisons: the span (year, year to date, quarter or month), the report month it ends on, and whether it's compared with last year or the prior period. Two shaded windows on a line show exactly which months each number covers. Every date is counted back from the latest month in the data, so no year is typed anywhere.

## ⬇️ Download

**[Download everything (period-selection-files.zip)](https://github.com/thialp/tableau-how-to/raw/main/02-period-selection/period-selection-files.zip)**, under 1 MB: the data (`arcadia_monthly_headcount.csv`, 61 month-ends) and the images (folder `Arcadia How-To`).

## Get started

1. Unzip the file.
2. Move the folder **Arcadia How-To** into `Documents/My Tableau Repository/Shapes/` (on Windows, `Documents\My Tableau Repository\Shapes\`), replacing How-To #1's folder if you have it, then restart Tableau.
3. Open a new Tableau workbook, connect to `arcadia_monthly_headcount.csv`, and follow the steps.

## The steps

- **In Tableau:** download the workbook from Tableau Public (the download icon under the viz) and open its tabs **Step 1** to **Step 14**. Each sheet's caption, on its left, has that step's instructions and every formula to paste.
- **On this page:** the same 14 steps, with the reasons behind them, are in the **[step-by-step guide](GUIDE.md)**.

## Use it on your own data

The data is a monthly balance: a count at every month-end, like headcount, open positions or inventory. Swap in your own count and date, change one number if your fiscal year doesn't start in July, and every window keeps working. For a flow (hires, sales), sum the months inside each window instead; the guide shows how.

---

Arcadia Systems is a fictional company; all data is synthetic. Images: the Arcadia design system ([Figma UI kit](https://www.figma.com/community/file/1690422855000144024)). Built by Thiago Alpoin · [LinkedIn](https://www.linkedin.com/in/thiagoalpoin) · MIT License.
