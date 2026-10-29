# How-To #2: a period picker for year, year to date, quarter and month

Build the period picker below from an empty Tableau workbook: one capsule that opens a panel, a span list (year, year to date, quarter, month), a grid of report months, two shaded windows on a line chart, number cards that compare the two windows, and a toggle that switches the comparison between last year and the prior period. Every date is counted back from the latest month in the data, so no year is typed anywhere. Every step is a calculation or a click in Tableau. There is no SQL and no extension.

**What you need:** Tableau Desktop or Tableau Public (the free app), version 2022.3 or later (for showing and hiding containers with a parameter). Plan on about two hours.

**How the lesson works.** There are 14 steps, and each one builds one worksheet. The downloadable workbook on Tableau Public has the same 14 sheets, named **Step 1 · Try It** to **Step 14 · Title**; each sheet's caption (on its left) holds that step's instructions and every formula to paste. So you can follow this page, the workbook, or both side by side.

**What you'll learn**

| Steps | Technique | Used for |
|---|---|---|
| 2–3 | An image as a button, a container shown by a parameter, the deselect trick | The rail capsule and the panel it opens |
| 4 | A list where exactly one option is ticked, drawn from a "menu field" | Year, year to date, quarter, month |
| 5 | An integer parameter that counts months back from the latest month | A report month that never names a year |
| 5 | A grid with a row per fiscal year | Picking any of 36 report months with one click |
| 6 | Every date as "the month-end k months before the latest one" | The current window and the window it's compared with |
| 6 | Reference bands driven by calculated fields | Two shaded windows that follow every click |
| 8–10 | Balances versus flows | Why the closing number ignores the span, and growth and averages don't |
| 11–12 | A segmented toggle made of two image buttons, on your own | Compare with last year, or with the prior period |
| 13 | Reset to default view | One click back to the start |

Arcadia Systems is a fictional company. All data is synthetic.

---

## Contents

- [0. Get ready](#0-get-ready)
   - [0.1 Download the files](#01-download-the-files)
   - [0.2 Install the shapes](#02-install-the-shapes)
   - [0.3 Connect the data](#03-connect-the-data)
   - [0.4 Three helper fields you'll use all the time](#04-three-helper-fields-youll-use-all-the-time)
- [Part 1: a line to watch, and a capsule that opens a panel](#part-1-a-line-to-watch-and-a-capsule-that-opens-a-panel)
   - [Step 1: the line you'll watch](#step-1-the-line-youll-watch)
   - [Step 2: the capsule, and the panel it opens](#step-2-the-capsule-and-the-panel-it-opens)
   - [Step 3: the ✕, and buttons that never stay highlighted](#step-3-the--and-buttons-that-never-stay-highlighted)
- [Part 2: pick a span and a report month](#part-2-pick-a-span-and-a-report-month)
   - [Step 4: the span list](#step-4-the-span-list)
   - [Step 5: the report month grid](#step-5-the-report-month-grid)
- [Part 3: from two picks to two windows](#part-3-from-two-picks-to-two-windows)
   - [Step 6: the two windows, shaded on the line](#step-6-the-two-windows-shaded-on-the-line)
   - [Step 7: make the capsule talk](#step-7-make-the-capsule-talk)
- [Part 4: the numbers](#part-4-the-numbers)
   - [Step 8: employees at the end](#step-8-employees-at-the-end)
   - [Step 9: growth in the period](#step-9-growth-in-the-period)
   - [Step 10: average employees](#step-10-average-employees)
- [Part 5: your turn, reset, and the finished page](#part-5-your-turn-reset-and-the-finished-page)
   - [Step 11: your turn, compare with the prior period](#step-11-your-turn-compare-with-the-prior-period)
   - [Step 12: the second half of the toggle](#step-12-the-second-half-of-the-toggle)
   - [Step 13: reset to default view](#step-13-reset-to-default-view)
   - [Step 14: the title, and the finished page](#step-14-the-title-and-the-finished-page)
- [Use it on your own data](#use-it-on-your-own-data)
- [Checks](#checks)
- [Why it works this way](#why-it-works-this-way)

---

## 0. Get ready

### 0.1 Download the files

Download **[period-selection-files.zip](https://github.com/thialp/tableau-how-to/raw/main/02-period-selection/period-selection-files.zip)** and unzip it. You get:

- `arcadia_monthly_headcount.csv`: employee counts at every month-end from Jun 30, 2021 to Jun 30, 2026, by department, office and level band (152,199 rows);
- a folder **Arcadia How-To** with the eleven images the page is drawn with.

Arcadia's fiscal year starts on July 1, so FY26 runs from July 2025 to June 2026.

Want to restyle the images? They're drawn in the [Arcadia Analytics · Tableau UI Kit](https://www.figma.com/community/file/1690422855000144024) on Figma: open it, change the colors, and export at 2×. You don't need Figma to follow this guide.

### 0.2 Install the shapes

Move the folder **Arcadia How-To** into:

- Windows: `Documents\My Tableau Repository\Shapes\`
- Mac: `Documents/My Tableau Repository/Shapes/`

If you did How-To #1, replace the old folder: this one holds the same seven images plus four new ones.

| File | Size (px) | What it draws |
|---|---|---|
| `capsule_dark.png` | 600 × 96 | The rail button |
| `tick_on.png` | 36 × 36 | A ticked box (teal, white tick) |
| `tick_off.png` | 36 × 36 | An empty box |
| `seg_left_on.png` | 200 × 64 | Left half of the toggle, chosen |
| `seg_left_off.png` | 200 × 64 | Left half of the toggle, not chosen |
| `seg_right_on.png` | 200 × 64 | Right half of the toggle, chosen |
| `seg_right_off.png` | 200 × 64 | Right half of the toggle, not chosen |
| `reset_button.png` | 600 × 96 | "Reset to default view" (Step 13) |
| `popover_line.png` | 1248 × 18 | The thin line under a panel's title |
| `rail_divider.png` | 400 × 48 | The line across the rail |
| `arcadia_logo_reverse.png` | 1200 × 326 | The logo for the rail |

The images are drawn at twice their on-screen size, so they stay sharp on high-resolution screens. If Tableau was open, restart it, or click **Reload Shapes** in the shape picker, so it sees the new folder.

### 0.3 Connect the data

1. Open Tableau. **Connect > To a File > Text file**, and pick `arcadia_monthly_headcount.csv`.
2. Check the types on the Data Source page: `as_of_date` is a date, `employees` is a whole number, and every other column is a string (Abc).
3. Go to Sheet 1. **File > Save As** `Period selection.twbx` (Tableau Public saves to your profile instead; that's fine).

**You should see** 9 fields in the Data pane. Each row is one month-end, department, office and level band; `as_of_date` is the month-end it counts, and `employees` is how many people it counts.

### 0.4 Three helper fields you'll use all the time

Create these now (**Analysis > Create Calculated Field**). Each formula box below starts with a `//` line naming the field; type that name in the name box and paste the rest.

```
// Headcount
SUM([employees])
```

```
// Latest
{ MAX([as_of_date]) }
```

```
// First Month
{ MIN([as_of_date]) }
```

Give `Headcount` the number format **Number, 0 decimals, thousands separator**.

`Latest` is the newest month-end in the data, and `First Month` the oldest. The curly braces with nothing before them are a FIXED level of detail over the whole data source, written short: one date, however the sheet is built. Every date on the page will be counted back from `Latest`, which is why no year is ever typed.

## Part 1: a line to watch, and a capsule that opens a panel

### Step 1: the line you'll watch

Every step changes what this one sheet shows, so you can see your work.

1. New sheet, name it **Try It**.
2. Drag `as_of_date` to Columns, right-click it and pick **Exact Date**, then right-click again and pick **Continuous**. Drag `Headcount` to Rows.
3. Marks **Line**, color navy `#13233A`.
4. Right-click the `Headcount` axis > **Edit Axis**: untick **Include zero**. A headcount that moves from 23,000 to 30,000 reads as a flat line if the axis starts at zero.

**You should see** one line climbing from 23,507 on Jun 30, 2021 to 30,005 on Jun 30, 2026: 61 month-ends.

**Tidy it for the finished page**: title hidden; the date axis title empty; the `Headcount` axis title empty, labels Tableau Book 8 `#5A6170`; grid lines None; tooltip `<as_of_date>` / `<Headcount> employees`, command buttons off.

> **If the sheet shows nothing at all**, look for a red pill on the Marks card. A field that is already on Rows or Columns doesn't also need to sit on Tooltip; Tableau can mark the second copy invalid, and an invalid field blanks the whole view. Insert it into the tooltip text instead, which works because every field in the view is available there.

---

The rail capsule on the [Arcadia dashboards](https://public.tableau.com/app/profile/thialp) isn't a Tableau filter. It's a sheet with exactly one mark. The mark is drawn with a custom shape (the capsule picture), its label is the text, and a click on it runs a parameter action. That's the whole idea of an image button.

### Step 2: the capsule, and the panel it opens

**Why.** A sheet with no dimension in the view draws one mark. Give that mark a picture and a click action, and you have a button you can style any way you like.

**Do.**

1. Create a parameter: right-click in the Data pane > **Create Parameter**.

   | Name | Data type | Current value |
   |---|---|---|
   | `p_PeriodOpen` | Boolean | False |

2. Create these calculated fields:

```
// Toggle Period Panel
NOT [p_PeriodOpen]
```

```
// Close Panel
FALSE
```

```
// zzTrue
TRUE
```

```
// zzFalse
FALSE
```

```
// Period Capsule Shape
"capsule_dark"
```

```
// Period Field Text
"FY26"
```

`Period Field Text` is a placeholder: Step 7 makes it follow the picks. `Period Capsule Shape` stays as it is; the capsule is the same navy picture whatever you pick, and the text on it does the talking.

3. New sheet, name it **Period Field**.
   - Marks type **Shape**. Drag `Period Capsule Shape` to Shape. Click **Shape**, pick the palette **Arcadia How-To**, and assign `capsule_dark.png` to the value `capsule_dark`.
   - Drag `Period Field Text` to Label. Click **Label**: font Tableau Medium 9, color `#E4E9F0`; Alignment horizontal **left**, vertical **middle**.
   - Drag `Toggle Period Panel`, `Close Panel`, `zzTrue` and `zzFalse` to Detail. They don't draw anything; actions can only read fields that are in the view.
   - Size: drag the size slider until the capsule fills the cell. If the label sits on top of the image's edge, add three or four leading spaces inside the label text, before `<Period Field Text>`.
   - **Format > Shading**: worksheet None. **Format > Borders** and **Lines**: None everywhere. Tooltip: open it and type `Choose the period`, untick **Include command buttons**.

**You should see** one dark capsule reading "FY26", and nothing else on the sheet.

**Try it.** Click the capsule. It highlights and stays highlighted. Step 3 fixes that.

#### The panel that opens

**Why.** A dashboard container can be shown or hidden by a Boolean parameter. The capsule click flips the parameter, so the container appears and disappears.

**Do.**

1. Create a new dashboard, **Period selection**, size **Fixed 1400 × 850**. Shading `#F3F3EF`.
2. Drag a **Vertical** container onto the dashboard, **floating**: x 0, y 0, w 216, h 850. Background navy `#13233A`. This is the rail.
3. Drag **Period Field** into the rail. Hide its title. Fixed height 32.
4. Drag another **Vertical** container, floating, to x 216, y 96, w 640, h 280. Its top lines up with the PERIOD heading in the rail. Background `#13233A`, no border. Name it **Period Popover** (Layout pane > Item hierarchy, double-click the name).
5. Into **Period Popover** drag a **Text** object: `Period`, Tableau Bold 12, white. Fixed height 44. This is the panel's title; Step 3 adds the ✕ beside it.
6. Select **Period Popover**. In the Layout pane tick **Control visibility using value**, and pick **Parameters > p_PeriodOpen**.
7. **Dashboard > Actions > Add Action > Change Parameter**:

   | Name | Source sheet | Run on | Target parameter | Source field | Aggregation | Clearing the selection |
   |---|---|---|---|---|---|---|
   | Open period popover | Period Field | Select | p_PeriodOpen | Toggle Period Panel | None | Keep current value |

**You should see** a navy rail with the capsule and no panel. Click the capsule: the panel appears. Click it again: the panel... doesn't close. Why? The first click left the capsule selected, so the second click only clears the selection, and clearing keeps the parameter as it was. That's Step 3.

---

### Step 3: the ✕, and buttons that never stay highlighted

**Why.** A selected mark stays selected until you click it again, and that second click is spent on unselecting instead of running your action. The fix is the **deselect trick**: a Filter action on the same sheet that maps `zzTrue` to `zzFalse`. On every click it asks Tableau to keep only rows where TRUE equals FALSE. No row qualifies, so Tableau drops the selection at once, and because the action clears to **Show all values**, nothing disappears. Every click is now a fresh click.

**Do.**

1. **Dashboard > Actions > Add Action > Filter**:

   | Name | Source | Run on | Target | Clearing the selection | Filter |
   |---|---|---|---|---|---|
   | Deselect Period Field | Period Field (this dashboard) | Select | Period Field | Show all values | Selected fields: `zzTrue` → `zzFalse` |

   Under **Target Filters**, choose **Selected Fields**, Source field `zzTrue`, Target field `zzFalse`.

2. Create

   ```
   // Close X
   "✕"
   ```

   New sheet **Period Close**: Marks **Text**; drag `Close X` to Text (Tableau Book 12, `#B8C0CC`), centered. Why a field and not typed text: a Text sheet with no field on it draws Tableau's "Abc" placeholder instead of your text. Detail `Close Panel`, `zzTrue`, `zzFalse`. Tooltip `Close`, command buttons off. Shading None.
3. On the dashboard, put a **Horizontal** container at the top of **Period Popover** in place of the title text: the title text on the left (width 600), **Period Close** on the right (width 40), height 44.
4. Two actions:

   | Name | Type | Source | Target | Field |
   |---|---|---|---|---|
   | Period popover on ✕ | Change Parameter | Period Close | p_PeriodOpen | Close Panel |
   | Deselect Period Close | Filter | Period Close | Period Close | `zzTrue` → `zzFalse` |

**You should see** the capsule open and close the panel on every click, the ✕ close it, and nothing ever stay highlighted.

**Rule for the rest of this guide:** every sheet you click gets its own deselect action (`zzTrue` → `zzFalse`, Show all values), and `zzTrue` and `zzFalse` on its Detail. Every tooltip has **Include command buttons** unticked.

---

## Part 2: pick a span and a report month

A period is two picks: **how long** (the span) and **ending when** (the report month). Every number on the page will come from those two, plus how far back the comparison sits. This part builds the two picks; Part 3 turns them into dates.

### Step 4: the span list

**Why.** The span list is a list where exactly one option is ticked: a click writes that option's name into a string parameter, and the tick follows the parameter. There's no "untick", so one option is always picked and no click can lead to an empty page.

There's one puzzle first. Tableau draws one mark per value of a dimension, and no column in the data holds the words "Year", "Year to date", "Quarter" and "Month". So we borrow a column that has exactly four values: the fiscal quarter of each month-end. Every month-end falls in one of four quarters, so relabeling quarters 1 to 4 as the four options gives the list its four rows. This **menu field** doesn't filter or count anything; it only gives the list something to draw.

**Do.**

1. Create a parameter:

   | Name | Data type | Current value |
   |---|---|---|
   | `p_Span` | String | Year |

2. Create:

```
// Span No
INT(((MONTH([as_of_date]) + 5) % 12) / 3) + 1
```

```
// Span Option
CASE [Span No]
WHEN 1 THEN "Year"
WHEN 2 THEN "Year to date"
WHEN 3 THEN "Quarter"
ELSE "Month" END
```

```
// Span Pick
MIN([Span Option])
```

```
// Span Shape
IF MIN([Span Option]) = [p_Span] THEN "tick_on" ELSE "tick_off" END
```

```
// Tick X
MIN(0.6)
```

How `Span No` reads: `(MONTH + 5) % 12` turns July into 0 and June into 11, the month's place in a fiscal year that starts in July. Dividing by 3 and keeping the whole part gives 0 to 3; adding 1 gives the fiscal quarter, 1 to 4. `Tick X` puts every box at the same spot near the left of a 0-to-10 axis, a little in from the edge so the box isn't cut in half.

3. Right-click `Span No` in the Data pane > **Convert to Dimension**, then **Convert to Discrete**.
4. New sheet **Span List**:
   - Rows `Span No` (header hidden: right-click > untick **Show Header**). Columns `Tick X`; right-click the axis > Edit Axis: Fixed **0 to 10**; then untick **Show Header**.
   - Marks **Shape**, Shape `Span Shape`: assign `tick_on.png` to `tick_on` and `tick_off.png` to `tick_off` (palette Arcadia How-To). Size: one step left of the middle of the slider.
   - Label: type two spaces, then insert `Span Option`: `  <Span Option>`. Tableau Book 10, `#E4E9F0`; alignment left, middle. Under Label, tick **Allow labels to overlap other marks**.
   - Detail `Span Pick`, `zzTrue`, `zzFalse`.
   - Format: shading None, row and column dividers None, grid lines None, zero lines None. Fit **Entire View**. Tooltip off (Tooltip > untick **Show tooltips**).
5. On your dashboard, put **Span List** inside **Period Popover**, under the title, width 200.
6. Actions:

   | Name | Type | Source | Target | Field |
   |---|---|---|---|---|
   | Pick span | Change Parameter | Span List | p_Span | Span Pick (aggregation None) |
   | Deselect Span List | Filter | Span List | Span List | `zzTrue` → `zzFalse` |

**You should see** four rows, Year to Month, with Year ticked. Click Quarter: the tick moves. Click Quarter again: it stays. Nothing else on the page uses `p_Span` yet; Step 6 changes that.

---

### Step 5: the report month grid

**Why.** The report month is where every period ends. Storing it as a date would mean typing a year into the parameter, and a year typed today is wrong next year. So the parameter stores **how many months back from the latest month-end**: 0 is the latest, 3 is three months earlier. When a new month arrives in the data, 0 moves with it, and so does everything built on it.

The grid offers the report months that have two full years of data behind them: one year for their own window, one for the year they're compared with. The data starts on Jun 30, 2021, so the grid starts on Jul 31, 2023: 36 month-ends, three whole fiscal years. As new months arrive, the grid grows by itself.

**Do.**

1. Create a parameter:

   | Name | Data type | Current value |
   |---|---|---|
   | `p_Back` | Integer | 0 |

2. Create:

```
// Report Date
DATE(DATEADD('day', -1, DATEADD('month', 1 - [p_Back], DATETRUNC('month', [Latest]))))
```

```
// Month Offered
[as_of_date] > DATEADD('month', 24, [First Month])
```

```
// Months Back
DATEDIFF('month', [as_of_date], [Latest])
```

```
// Month Pick
MIN([Months Back])
```

```
// FY Label
"FY" + RIGHT(STR(YEAR([as_of_date]) + (IF MONTH([as_of_date]) >= 7 THEN 1 ELSE 0 END)), 2)
```

```
// Fiscal Month No
((MONTH([as_of_date]) + 5) % 12) + 1
```

```
// Month Abbr
LEFT(DATENAME('month', [as_of_date]), 3)
```

```
// Month State
IF MIN([as_of_date]) = MIN([Report Date]) THEN "picked" ELSE "open" END
```

How `Report Date` reads, inside out: `DATETRUNC('month', [Latest])` is the first day of the latest month (Jun 1, 2026); move it `1 - [p_Back]` months (with `p_Back` = 0, one month on, to Jul 1); step back one day (Jun 30). That lands on a month-end every time, even for February. `DATEADD('month', -1, ...)` on a month-end wouldn't: one month before Jun 30 is May 30, not May 31.

`Months Back` is the reverse trip: how many months a month-end sits before `Latest`. A click on Mar 2026 writes 3 into `p_Back`, and `Report Date` turns 3 back into Mar 31, 2026.

3. Right-click `Fiscal Month No` in the Data pane > **Convert to Dimension**, then **Convert to Discrete**.
4. New sheet **Month Grid**:
   - Drag `Month Offered` to Filters and keep **True**.
   - Rows `FY Label`. Columns `Fiscal Month No`, header hidden. The row header stays: it labels each row FY24, FY25, FY26. Format the row header Tableau Semibold 9 `#8FA0B8`.
   - Marks **Text**. Drag `Month Abbr` to Text and `Month State` to Color. Click **Color** > Edit Colors: `picked` teal `#51C69E`, `open` `#B8C4D6`. Text Tableau Book 9, centered. The label takes the mark's color, so the picked month turns teal.
   - Detail `Month Pick`, `zzTrue`, `zzFalse`.
   - Format: shading None, dividers None, grid lines None. Rows about 30 px high. Fit **Entire View**. Tooltip off.
5. Put **Month Grid** in **Period Popover** to the right of Span List (width 420).
6. Actions:

   | Name | Type | Source | Target | Field |
   |---|---|---|---|---|
   | Pick month | Change Parameter | Month Grid | p_Back | Month Pick (aggregation None) |
   | Deselect Month Grid | Filter | Month Grid | Month Grid | `zzTrue` → `zzFalse` |

**You should see** three rows, FY24 to FY26, Jul to Jun across, with Jun in FY26 teal. Click Mar in FY26: it turns teal and `p_Back` is 3. Click Jul in FY24: `p_Back` is 35, the oldest month offered. Click Jun in FY26 again to go back.

---

## Part 3: from two picks to two windows

### Step 6: the two windows, shaded on the line

**Why.** A period is a **window**: an opening month-end and a closing month-end. The window covers the months after the opening, up to and including the closing. FY26 opens on Jun 30, 2025 and closes on Jun 30, 2026, so it covers July 2025 to June 2026, and its growth is the closing headcount minus the opening one.

Here's the trick that keeps every formula short. Every date on this page is **the month-end k months before the latest one**, the same expression as `Report Date` with a different k:

| Date | k |
|---|---|
| Current close | `p_Back` |
| Current open | `p_Back` + months in the span |
| Comparison close | `p_Back` + shift |
| Comparison open | `p_Back` + shift + months in the span |

The **span** decides how many months a window holds. A year holds 12. Year to date holds the months since the fiscal year began: 9 at the end of March, 12 at the end of June. A quarter holds the months since the last quarter-end: 3 at a quarter-end, 2 at the end of May. A month holds 1.

The **shift** decides where the comparison sits. For now it's 12: every window is compared with the same window a year earlier. Step 11 adds the other choice.

**Do.**

1. Create:

```
// Months In
CASE [p_Span]
WHEN "Year" THEN 12
WHEN "Year to date" THEN ((MONTH([Report Date]) + 5) % 12) + 1
WHEN "Quarter" THEN ((MONTH([Report Date]) - 1) % 3) + 1
ELSE 1 END
```

```
// Shift
12
```

```
// Current Close
[Report Date]
```

```
// Current Open
DATE(DATEADD('day', -1, DATEADD('month', 1 - [p_Back] - [Months In], DATETRUNC('month', [Latest]))))
```

```
// Comparison Close
DATE(DATEADD('day', -1, DATEADD('month', 1 - [p_Back] - [Shift], DATETRUNC('month', [Latest]))))
```

```
// Comparison Open
DATE(DATEADD('day', -1, DATEADD('month', 1 - [p_Back] - [Shift] - [Months In], DATETRUNC('month', [Latest]))))
```

```
// In Current
[as_of_date] > [Current Open] AND [as_of_date] <= [Current Close]
```

```
// In Comparison
[as_of_date] > [Comparison Open] AND [as_of_date] <= [Comparison Close]
```

The quarter rule works because Arcadia's fiscal quarters end in September, December, March and June, the same months as calendar quarters. `(MONTH - 1) % 3` is 0 in the first month of a quarter and 2 in the last, so adding 1 counts the months so far.

2. Name each window the way people say it. Create:

```
// Now FY
"FY" + RIGHT(STR(YEAR([Current Close]) + (IF MONTH([Current Close]) >= 7 THEN 1 ELSE 0 END)), 2)
```

```
// Now Month
LEFT(DATENAME('month', [Current Close]), 3) + " " + STR(YEAR([Current Close]))
```

```
// Now Name
CASE [p_Span]
WHEN "Year" THEN (IF MONTH([Current Close]) = 6 THEN [Now FY] ELSE "12 months to " + [Now Month] END)
WHEN "Year to date" THEN [Now FY] + " to " + LEFT(DATENAME('month', [Current Close]), 3)
WHEN "Quarter" THEN [Now FY] + " Q" + STR(INT(((MONTH([Current Close]) + 5) % 12) / 3) + 1)
    + (IF [Months In] < 3 THEN " to " + LEFT(DATENAME('month', [Current Close]), 3) ELSE "" END)
ELSE [Now Month] END
```

```
// Now From
LEFT(DATENAME('month', DATEADD('month', 1, [Current Open])), 3) + " " + STR(YEAR(DATEADD('month', 1, [Current Open])))
```

```
// Now Range
IF [Months In] = 1 THEN [Now Month] ELSE [Now From] + " – " + [Now Month] END
```

And the same five for the comparison:

```
// Before FY
"FY" + RIGHT(STR(YEAR([Comparison Close]) + (IF MONTH([Comparison Close]) >= 7 THEN 1 ELSE 0 END)), 2)
```

```
// Before Month
LEFT(DATENAME('month', [Comparison Close]), 3) + " " + STR(YEAR([Comparison Close]))
```

```
// Before Name
CASE [p_Span]
WHEN "Year" THEN (IF MONTH([Comparison Close]) = 6 THEN [Before FY] ELSE "12 months to " + [Before Month] END)
WHEN "Year to date" THEN [Before FY] + " to " + LEFT(DATENAME('month', [Comparison Close]), 3)
WHEN "Quarter" THEN [Before FY] + " Q" + STR(INT(((MONTH([Comparison Close]) + 5) % 12) / 3) + 1)
    + (IF [Months In] < 3 THEN " to " + LEFT(DATENAME('month', [Comparison Close]), 3) ELSE "" END)
ELSE [Before Month] END
```

```
// Before From
LEFT(DATENAME('month', DATEADD('month', 1, [Comparison Open])), 3) + " " + STR(YEAR(DATEADD('month', 1, [Comparison Open])))
```

```
// Before Range
IF [Months In] = 1 THEN [Before Month] ELSE [Before From] + " – " + [Before Month] END
```

A year that closes in June is a fiscal year, so it's called FY26; a year that closes in December is "12 months to Dec 2025". A quarter still in progress says how far it got: "FY26 Q4 to May".

3. **The legend.** New sheet **Windows**: no field on Rows or Columns, so it draws one mark. Marks **Text**, left, top, two lines:
   - `■ ` in `#A8D3C2`, then `<Now Name>` Tableau Semibold 10 navy, then `  <Now Range>` Tableau Book 9 `#5A6170`;
   - `■ ` in `#D3CBBB`, then `<Before Name>` Tableau Semibold 10 navy, then `  <Before Range>` Tableau Book 9 `#5A6170`.

   Detail `zzTrue`, `zzFalse`; tooltip off; a deselect action.

4. **The shading.** Back on **Try It**:
   - Drag `Current Open`, `Current Close`, `Comparison Open` and `Comparison Close` to Detail. Each comes in as `MIN(...)`; keep it. A reference band can only read fields that are in the view.
   - **Analytics** pane > drag **Reference Band** onto the view, Scope **Entire Table**, onto the date axis. Band From: Value `MIN(Current Open)`, Label None. Band To: Value `MIN(Current Close)`, Label None. Fill `#DCEDE6`, no line.
   - A second band the same way: `MIN(Comparison Open)` to `MIN(Comparison Close)`, fill `#ECE8DF`.
   - Label the two closing points. Create

     ```
     // Point Label
     IF MIN([as_of_date]) = MIN([Current Close]) OR MIN([as_of_date]) = MIN([Comparison Close]) THEN [Headcount] END
     ```

     with the format **Number, 0 decimals, thousands separator**. Drag it to Label: Tableau Semibold 9 navy, **Allow labels to overlap other marks**. Every other month has no value, so only the two closing points show a number.

**You should see**, with Year and Jun 2026 picked: a green band over July 2025 to June 2026, a sand band over the year before it, and the points labeled 30,005 and 28,438. The legend reads "FY26 · Jul 2025 – Jun 2026" and "FY25 · Jul 2024 – Jun 2025".

| Span, report month | Legend, current | Legend, comparison |
|---|---|---|
| Year, Jun 2026 | FY26 · Jul 2025 – Jun 2026 | FY25 · Jul 2024 – Jun 2025 |
| Year to date, Mar 2026 | FY26 to Mar · Jul 2025 – Mar 2026 | FY25 to Mar · Jul 2024 – Mar 2025 |
| Quarter, May 2026 | FY26 Q4 to May · Apr 2026 – May 2026 | FY25 Q4 to May · Apr 2025 – May 2025 |
| Month, Jun 2026 | Jun 2026 | Jun 2025 |
| Year, Dec 2025 | 12 months to Dec 2025 · Jan 2025 – Dec 2025 | 12 months to Dec 2024 · Jan 2024 – Dec 2024 |

---

### Step 7: make the capsule talk

**Why.** The capsule should say which period is on the page, and the line under it what it's compared with.

**Do.**

1. Edit the placeholder from Step 2, and add the sub-line:

```
// Period Field Text
[Now Name]
```

```
// Period Sub Text
"vs " + [Before Name]
```

2. On **Period Field**, the label `<Period Field Text>` now follows the picks by itself.
3. New sheet **Period Sub**: Marks Text, `<Period Sub Text>` Tableau Book 9 `#8A97A8`, left. Detail `zzTrue`, `zzFalse`; tooltip off; a deselect action. Put it in the rail under Period Field, height 20.
4. Put a text object `PERIOD` (Tableau Semibold 8, `#B8C4D6`) above the capsule.

**You should see**

| You pick | Capsule | Under it |
|---|---|---|
| Year, Jun 2026 | "FY26" | vs FY25 |
| Year to date, Mar 2026 | "FY26 to Mar" | vs FY25 to Mar |
| Quarter, Jun 2026 | "FY26 Q4" | vs FY25 Q4 |
| Month, Jun 2026 | "Jun 2026" | vs Jun 2025 |
| Year, Dec 2025 | "12 months to Dec 2025" | vs 12 months to Dec 2024 |

---

## Part 4: the numbers

Three cards compare the two windows. They also show the one idea worth taking from this lesson: **headcount is a balance**. A balance is counted at a moment (a month-end), not added up over time. That changes which numbers move when you switch the span.

### Step 8: employees at the end

**Why.** The closing headcount of a window is simply the headcount on its closing month-end.

**Do.**

1. Create:

```
// End Now
SUM(IF [as_of_date] = [Current Close] THEN [employees] END)
```

```
// End Before
SUM(IF [as_of_date] = [Comparison Close] THEN [employees] END)
```

```
// End Change %
[End Now] / [End Before] - 1
```

Formats: `End Now` and `End Before` **Number, 0 decimals, thousands separator**; `End Change %` **Custom** `+0.0%;−0.0%`, so a rise reads "+5.5%".

2. Sheet **KPI End**: no field on Rows or Columns. Marks **Text**, left aligned, top, three lines: `EMPLOYEES AT THE END` Tableau Semibold 8 `#5A6170`; `<End Now>` Tableau Bold 24 navy `#13233A`; `vs <End Before> · <End Change %>` Tableau Book 9 `#5A6170`. Detail `zzTrue`, `zzFalse`; tooltip off; a deselect action.

**You should see** 30,005, "vs 28,438 · +5.5%".

**Try it.** Switch Year to Quarter, then to Month. The card doesn't move. That's right: all three end on Jun 30, 2026 and compare with Jun 30, 2025, so they end on the same two numbers. Pick Mar 2026 instead and it changes to 29,618, "vs 28,137 · +5.3%". This is the question a period picker gets most often, and the next two cards are the answer to it.

---

### Step 9: growth in the period

**Why.** The span shows up in what happened **inside** the window: the closing headcount minus the opening one.

**Do.**

1. Create:

```
// Start Now
SUM(IF [as_of_date] = [Current Open] THEN [employees] END)
```

```
// Start Before
SUM(IF [as_of_date] = [Comparison Open] THEN [employees] END)
```

```
// Growth Now
[End Now] - [Start Now]
```

```
// Growth Before
[End Before] - [Start Before]
```

Format both growth fields **Custom** `+#,##0;−#,##0;0`.

2. Sheet **KPI Growth**, built like KPI End: `GROWTH IN THE PERIOD`; `<Growth Now>` Tableau Bold 24 navy; `vs <Growth Before>` Tableau Book 9 `#5A6170`.

**You should see**

| You pick | Growth | vs |
|---|---|---|
| Year, Jun 2026 | +1,567 | +1,230 |
| Quarter, Jun 2026 | +387 | +301 |
| Month, Jun 2026 | +131 | +104 |
| Year to date, Mar 2026 | +1,180 | +929 |

---

### Step 10: average employees

**Why.** An average over the window counts each month-end inside it once: the sum of the month-end headcounts divided by the months in the span. It's the number to divide by for anything "per employee", such as cost per head or turnover rate.

**Do.**

1. Create:

```
// Average Now
SUM(IF [In Current] THEN [employees] END) / MIN([Months In])
```

```
// Average Before
SUM(IF [In Comparison] THEN [employees] END) / MIN([Months In])
```

```
// Average Change %
[Average Now] / [Average Before] - 1
```

`MIN([Months In])` because `Months In` is the same on every row, and Tableau needs it aggregated to divide an aggregate by it. Formats: the averages **Number, 0 decimals, thousands separator**; `Average Change %` **Custom** `+0.0%;−0.0%`.

2. Sheet **KPI Average**, built like KPI End: `AVERAGE EMPLOYEES`; `<Average Now>` Tableau Bold 24 navy; `vs <Average Before> · <Average Change %>` Tableau Book 9 `#5A6170`.

**You should see** 29,290, "vs 27,877 · +5.1%" for FY26. Quarter: 29,878, "vs 28,341 · +5.4%". Month: 30,005, the same as the closing number, because a one-month window holds one month-end.

---

## Part 5: your turn, reset, and the finished page

### Step 11: your turn, compare with the prior period

"Last year" isn't the only comparison people ask for. For a quarter, the question is often "how did we do against **last** quarter?" Build a toggle under the capsule with two halves, **Last year** and **Prior period**, and make the shift follow it. Use the hints first; the full answer is below them, and the finished sheets are in the downloadable workbook (Basis Year and Basis Prior), so you can open them and compare.

**Hints**

- One more string parameter, `p_Basis`, current value `Last year`.
- `Shift` becomes 3 for a quarter and 1 for a month when `p_Basis` is "Prior period", and stays 12 otherwise. For a year and year to date, the prior period **is** last year, so both halves read the same there.
- Each half of the toggle is an image button like the capsule in Step 2: a one-mark sheet whose shape depends on `p_Basis`, with a click that writes its own value into `p_Basis`.
- Text on a chosen half is navy on a pale background; on the other half, pale on navy. Two label runs, one of them always empty, give each half the right color (the same trick as a two-color label anywhere).

<details>
<summary><b>The answer: every toggle field</b></summary>

Parameter: `p_Basis`, String, current value `Last year`.

```
// Shift
IF [p_Basis] = "Prior period" AND [p_Span] = "Quarter" THEN 3
ELSEIF [p_Basis] = "Prior period" AND [p_Span] = "Month" THEN 1
ELSE 12 END

// Basis Year Value
"Last year"

// Basis Year Shape
IF [p_Basis] = "Last year" THEN "seg_left_on" ELSE "seg_left_off" END

// Basis Year On
IF [p_Basis] = "Last year" THEN "Last year" END

// Basis Year Off
IF [p_Basis] <> "Last year" THEN "Last year" END
```

Sheet **Basis Year**: Marks **Shape**, Shape `Basis Year Shape` (assign `seg_left_on.png` to `seg_left_on` and `seg_left_off.png` to `seg_left_off`). Label `<Basis Year On><Basis Year Off>`, the first run Tableau Semibold 9 navy `#13233A`, the second Tableau Book 9 `#E4E9F0`, centered. Detail `Basis Year Value`, `zzTrue`, `zzFalse`. Tooltip `Compare with the same period last year`, command buttons off.

Action: **Basis to last year** (Change Parameter, Basis Year, `p_Basis` ← `Basis Year Value`), plus its deselect.

In the rail: a text object `COMPARED WITH` (Tableau Semibold 8, `#B8C4D6`) under Period Sub, then a **Horizontal** container, height 32, with Basis Year (width 100) on the left. Step 12 fills the right half.

</details>

**You should see** the left half pale with "Last year" in navy. Nothing changes yet when you click it, because `p_Basis` already says "Last year".

---

### Step 12: the second half of the toggle

Sheet **Basis Prior**, the mirror of Basis Year:

```
// Basis Prior Value
"Prior period"
```

```
// Basis Prior Shape
IF [p_Basis] = "Prior period" THEN "seg_right_on" ELSE "seg_right_off" END
```

```
// Basis Prior On
IF [p_Basis] = "Prior period" THEN "Prior period" END
```

```
// Basis Prior Off
IF [p_Basis] <> "Prior period" THEN "Prior period" END
```

Shape `Basis Prior Shape` (`seg_right_on.png`, `seg_right_off.png`); label `<Basis Prior On><Basis Prior Off>` with the same two colors; Detail `Basis Prior Value`, `zzTrue`, `zzFalse`; tooltip `Compare with the period just before`, command buttons off. Put it in the toggle's container on the right, width 100.

Action: **Basis to prior period** (Change Parameter, Basis Prior, `p_Basis` ← `Basis Prior Value`), plus its deselect.

**You should see**

| You pick | Capsule | Under it | End | Growth |
|---|---|---|---|---|
| Quarter, Jun 2026, Prior period | "FY26 Q4" | vs FY26 Q3 | 30,005 vs 29,618 · +1.3% | +387 vs +397 |
| Month, Jun 2026, Prior period | "Jun 2026" | vs May 2026 | 30,005 vs 29,874 · +0.4% | +131 vs +118 |
| Quarter, Mar 2026, Prior period | "FY26 Q3" | vs FY26 Q2 | 29,618 vs 29,221 · +1.4% | +397 vs +393 |
| Year, Jun 2026, Prior period | "FY26" | vs FY25 | the same as Last year | |

With Prior period, the two bands on Try It sit side by side instead of a year apart.

---

### Step 13: reset to default view

One button that puts every pick back and closes the panel.

1. Create:

```
// Reset Span
"Year"
```

```
// Reset Back
0
```

```
// Reset Basis
"Last year"
```

```
// Reset Shape
"reset_button"
```

2. New sheet **Reset**: Marks Shape, Shape `Reset Shape` (assign `reset_button.png` to `reset_button`). Detail `Reset Span`, `Reset Back`, `Reset Basis`, `Close Panel`, `zzTrue`, `zzFalse`. Tooltip `Reset to default view`, command buttons off. Put it in the rail under the toggle, height 32.
3. Actions, all from **Reset**, run on Select:

   | Target | Field |
   |---|---|
   | p_Span | Reset Span |
   | p_Back | Reset Back |
   | p_Basis | Reset Basis |
   | p_PeriodOpen | Close Panel |

   Plus the deselect action.

**You should see** Year ticked, Jun in FY26 teal, Last year chosen, the panel closed, and the cards back at 30,005 · +1,567 · 29,290.

---

### Step 14: the title, and the finished page

The title says what the page shows, in words that follow the picks.

```
// Page Subtitle
"Employees, " + [Now Name] + " compared with " + [Before Name] + " · report month " + [Now Month]
```

Sheet **Title**: Marks **Text**, three lines, left, top: `HOW-TO · STEP-BY-STEP LESSON` Tableau Semibold 9 teal `#0F6E56`; `How to build a period picker for year, year to date, quarter and month` Tableau Bold 18 navy; `<Page Subtitle>` Tableau Book 11 `#5A6170`. The first two lines say what the page is before anyone reads a number: a lesson, not an analysis. Detail `zzTrue`, `zzFalse`; tooltip off; a deselect action.

**You should see** "Employees, FY26 compared with FY25 · report month Jun 2026". No year is typed anywhere: when a newer file arrives, the title, the grid and every card move on their own.

#### The finished page

Dashboard **Period selection**, Fixed 1400 × 850, shading `#F3F3EF`, every item floating:

| Item | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Rail (vertical container) | 0 | 0 | 216 | 850 | Navy `#13233A`, padding 8 left and right |
| Title (sheet) | 240 | 8 | 1136 | 78 | Three lines need the full 78 px, or the subtitle is cut |
| Lesson card (text and images in a white container) | 240 | 88 | 600 | 724 | What the page is, the images, how to try it, how to build it, how to use your own data |
| KPI End / Growth / Average (each in a white container) | 872 / 1044 / 1216 | 88 | 160 | 116 | Radius 14, border 1 px `#E4E3DD`, padding 14. Three lines need 88 px inside, or Tableau shows ##### |
| Chart card (white container) | 872 | 216 | 504 | 596 | Text "Employees at each month-end" Semibold 11 navy, then Try It, then Windows |
| Footnote (text) | 240 | 822 | 1136 | 18 | "Arcadia Systems is fictional; all data is synthetic. Executive officers excluded. Fiscal year starts July 1." Book 9 `#5A6170` |
| Period Popover | 216 | 96 | 640 | 280 | Visibility `p_PeriodOpen` |

Inside the rail, top to bottom: blank 24 · `arcadia_logo_reverse.png` 160 × 40 · blank 32 · PERIOD 18 · Period Field 32 · Period Sub 20 · blank 10 · COMPARED WITH 18 · the toggle 32 (Basis Year, Basis Prior) · `rail_divider.png` 24 · Reset 32 · flexible blank · a credit line at the foot, Tableau Book 9: your name in `#E4E9F0`, then "Files and guide on GitHub" in `#B9C3D1`.

Inside the popover, top to bottom: the title row 44 (title and ✕) · `popover_line.png` · two columns, each with a small heading (Tableau Semibold 8, `#8FA0B8`): `SPAN` over Span List (200 wide) and `REPORT MONTH` over Month Grid (420 wide) · a footer text 30, Book 9 `#8FA0B8`: "Every period ends on the report month; the cards and the line follow every click." Keep the footer to one line: a longer one is cut off.

The popover sits in front of everything; the rail in front of the page. The cards and the chart sit right of x 856, so they stay in view while the panel is open.

---

## Use it on your own data

Arcadia's file is a **monthly balance**: one row per month-end and group, with a count. Any month-end balance works the same way: headcount, open positions, active customers, inventory on hand, account balances.

- **Your own balance.** Swap `employees` for your count and `as_of_date` for your month-end date. Every window field keeps working, because none of them names a column other than the date.
- **Your fiscal year.** Arcadia's starts in July, which is where the `+ 5` comes from in `Span No`, `Fiscal Month No`, `Months In` and the names: `(MONTH + 5) % 12` is 0 in July. For a year starting in October use `+ 2`; for a calendar year, `+ 11` (or simply `MONTH - 1`). The FY rule `MONTH >= 7` becomes `MONTH >= 10` for October. Quarters follow by themselves when your fiscal quarters end in March, June, September and December.
- **A flow instead of a balance.** For hires, sales or tickets, the window total is the sum of the months inside it: `SUM(IF [In Current] THEN [your measure] END)`. Year, year to date, quarter and month then each give a different number, as you'd expect.
- **More history, or less.** The grid offers every month with two years behind it. With three years of data you get one fiscal year of choices; with ten, eight.

---

## Checks

Run these in Presentation mode, then again after publishing.

| # | Do | Expect |
|---:|---|---|
| 1 | Nothing | Capsule "FY26", "vs FY25"; Last year chosen; cards 30,005 · vs 28,438 · +5.5% / +1,567 vs +1,230 / 29,290 · vs 27,877 · +5.1% |
| 2 | Click the capsule, every list row, grid month, toggle half, ✕ and Reset | Nothing stays highlighted |
| 3 | Quarter | "FY26 Q4", "vs FY25 Q4"; growth +387 vs +301; average 29,878 · vs 28,341 · +5.4%; the end card doesn't move |
| 4 | Month | "Jun 2026", "vs Jun 2025"; growth +131 vs +104; average 30,005 |
| 5 | Year to date, then Mar in FY26 | "FY26 to Mar", "vs FY25 to Mar"; cards 29,618 · vs 28,137 · +5.3% / +1,180 vs +929 / 29,094 · vs 27,722 · +4.9% |
| 6 | Year, then Dec in FY26 | "12 months to Dec 2025"; cards 29,221 · vs 27,825 · +5.0% / +1,396 vs +754 |
| 7 | Quarter, then May in FY26 | "FY26 Q4 to May", "vs FY25 Q4 to May"; growth +256 vs +197 |
| 8 | Reset, Quarter, Prior period | "vs FY26 Q3"; 30,005 · vs 29,618 · +1.3%; growth +387 vs +397; the bands sit side by side |
| 9 | Month, Prior period | "vs May 2026"; 30,005 · vs 29,874 · +0.4% |
| 10 | Year, Prior period | The same as check 1 |
| 11 | Jul in FY24, Year, Last year | "12 months to Jul 2023", "vs 12 months to Jul 2022"; 26,961 · vs 25,233 · +6.8% |
| 12 | Reset | Everything as in check 1, panel closed |

---

## Why it works this way

- **Why count months back instead of storing a date?** A date parameter holds a year, and a year typed today is out of date the day new data arrives. `p_Back` = 0 always means "the latest month", so a refresh moves the whole page forward by itself.
- **Why one expression for every date?** "The month-end k months before the latest" lands on a real month-end every time, so equality tests like `[as_of_date] = [Current Close]` always find their row. `DATEADD('month', -1, ...)` on a month-end can land on the 30th of a 31-day month and match nothing.
- **Why a menu field for the span list?** A list needs one mark per option, and the options aren't in the data. Any column with exactly as many values as you have options will do; the fiscal quarter has four, one for each span.
- **Why does the end card ignore the span?** Headcount is a balance, counted at a moment. A year, a quarter and a month that end on the same month-end end on the same headcount. Growth and averages depend on the months inside the window, so they follow the span.
- **Why reference bands?** A band reads its edges from fields in the view, so the shading moves with every click without a second chart or a dual axis.
- **Why the deselect trick?** A click on an already-selected mark only unselects it. Clearing the selection right away means every click runs its action.

---

## Files in this folder

| Path | What it is |
|---|---|
| `period-selection-files.zip` | Everything you need: the CSV and the Arcadia How-To shapes folder |
| `shapes/*.png` | The images on their own, to preview on GitHub |
| `GUIDE.md` | This guide |

The CSV is only in the zip: at 15 MB it's too large for GitHub to preview. How it was made from the Arcadia warehouse is in [`tools/`](../tools/) at the top of the repository; you don't need it for the lesson.

### The data, column by column

| Column | Example | Notes |
|---|---|---|
| `as_of_date` | 2026-06-30 | The month-end each row counts; 61 month-ends, Jun 30, 2021 to Jun 30, 2026 |
| `function_name` | Commercial | 8 functions |
| `sub_function` | Client Services | 10 sub-functions |
| `department_name` | Client Success | 31 departments |
| `region` | Asia Pacific | 5 regions |
| `country_name` | Australia | 22 countries |
| `office_name` | Melbourne | 35 offices |
| `level_band` | L5–L6 Manager | 4 bands |
| `employees` | 13 | Employees in that department, office and level band on that month-end |

The column names match How-To #1's file, so its calculations paste straight in. Executive officers are excluded, as on every Arcadia dashboard: 30,005 employees on Jun 30, 2026. Someone whose last day is a month-end still counts on that day.
