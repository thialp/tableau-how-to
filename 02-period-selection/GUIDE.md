# How-To #2: a period picker for year, year to date, quarter and month

Build the period picker below from an empty Tableau workbook: one capsule that opens a panel, a span list (year, year to date, quarter, month), a grid of report dates that ends on **today**, two shaded windows on a line chart, number cards that compare the two windows, and a toggle that switches the comparison between last year and the prior period. The page works on a closed month-end and on a day in the middle of a month ("to date"), and every date is counted back from the latest day in the data, so no year is typed anywhere. Every step is a calculation or a click in Tableau. There is no SQL and no extension.

**What you need:** Tableau Desktop or Tableau Public (the free app), version 2022.3 or later (for showing and hiding containers with a parameter). Plan on about two hours.

**How the lesson works.** There are 14 steps, and each one builds one worksheet. The downloadable workbook on Tableau Public has the same 14 sheets, named **Step 1 · Try It** to **Step 14 · Title**; each sheet's caption (on its left) holds that step's instructions and every formula to paste. So you can follow this page, the workbook, or both side by side.

**What you'll learn**

| Steps | Technique | Used for |
|---|---|---|
| 2–3 | An image as a button, a container shown by a parameter, the deselect trick | The rail capsule and the panel it opens |
| 4 | A list where exactly one option is ticked, drawn from a "menu field" | Year, year to date, quarter, month |
| 5 | An integer parameter that counts months back from the latest day | A report date that never names a year, and today as one of the choices |
| 5 | A grid with a row per fiscal year | Picking any of 37 report dates with one click |
| 6 | The to-date rule: a month-end looks back to month-ends, any other day to the same day | The current window and the window it's compared with |
| 6 | Reference bands driven by calculated fields, and a chart that zooms to them | Two shaded windows that follow every click |
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
- [Part 2: pick a span and a report date](#part-2-pick-a-span-and-a-report-date)
   - [Step 4: the span list](#step-4-the-span-list)
   - [Step 5: the report date grid](#step-5-the-report-date-grid)
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

- `arcadia_daily_headcount.csv`: employees on every day from Jun 30, 2021 to Jul 5, 2026, by department (55,572 rows);
- a folder **Arcadia How-To** with the eleven images the page is drawn with.

Arcadia's fiscal year starts on July 1, so FY26 runs from July 2025 to June 2026, and Jul 5, 2026 is the fifth day of FY27. Think of Jul 5 as **today**: June is closed, and July is still going.

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

1. Open Tableau. **Connect > To a File > Text file**, and pick `arcadia_daily_headcount.csv`.
2. Check the types on the Data Source page: `as_of_date` is a date, `employees` is a whole number, `is_closed` is true/false, and the other three columns are strings (Abc).
3. Go to Sheet 1. **File > Save As** `Period selection.twbx` (Tableau Public saves to your profile instead; that's fine).

**You should see** 6 fields in the Data pane. Each row is one day and department; `as_of_date` is the day it counts, `employees` is how many people it counts, and `is_closed` is true up to Jun 30, 2026, the last closed month-end.

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

`Latest` is the newest day in the data, today, and `First Month` the oldest. The curly braces with nothing before them are a FIXED level of detail over the whole data source, written short: one date, however the sheet is built. Every date on the page will be counted back from `Latest`, which is why no year is ever typed.

## Part 1: a line to watch, and a capsule that opens a panel

### Step 1: the line you'll watch

Every step changes what this one sheet shows, so you can see your work.

1. New sheet, name it **Try It**.
2. Drag `as_of_date` to Columns, right-click it and pick **Exact Date**, then right-click again and pick **Continuous**. Drag `Headcount` to Rows.
3. Marks **Line**, color navy `#13233A`.
4. Right-click the `Headcount` axis > **Edit Axis**: untick **Include zero**. A headcount that moves from 23,000 to 30,000 reads as a flat line if the axis starts at zero.

**You should see** one line climbing from 23,507 on Jun 30, 2021 to 30,041 on Jul 5, 2026: 1,832 days.

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
"FY27 to Jul 5"
```

`Period Field Text` is a placeholder: Step 7 makes it follow the picks. `Period Capsule Shape` stays as it is; the capsule is the same navy picture whatever you pick, and the text on it does the talking.

3. New sheet, name it **Period Field**.
   - Marks type **Shape**. Drag `Period Capsule Shape` to Shape. Click **Shape**, pick the palette **Arcadia How-To**, and assign `capsule_dark.png` to the value `capsule_dark`.
   - Drag `Period Field Text` to Label. Click **Label**: font Tableau Medium 9, color `#E4E9F0`; Alignment horizontal **left**, vertical **middle**.
   - Drag `Toggle Period Panel`, `Close Panel`, `zzTrue` and `zzFalse` to Detail. They don't draw anything; actions can only read fields that are in the view.
   - Size: drag the size slider until the capsule fills the cell. If the label sits on top of the image's edge, add three or four leading spaces inside the label text, before `<Period Field Text>`.
   - **Format > Shading**: worksheet None. **Format > Borders** and **Lines**: None everywhere. Tooltip: open it and type `Choose the period`, untick **Include command buttons**.

**You should see** one dark capsule reading "FY27 to Jul 5", and nothing else on the sheet.

**Try it.** Click the capsule. It highlights and stays highlighted. Step 3 fixes that.

#### The panel that opens

**Why.** A dashboard container can be shown or hidden by a Boolean parameter. The capsule click flips the parameter, so the container appears and disappears.

**Do.**

1. Create a new dashboard, **Period selection**, size **Fixed 1400 × 850**. Shading `#F3F3EF`.
2. Drag a **Vertical** container onto the dashboard, **floating**: x 0, y 0, w 216, h 850. Background navy `#13233A`. This is the rail.
3. Drag **Period Field** into the rail. Hide its title. Fixed height 32.
4. Drag another **Vertical** container, floating, to x 216, y 96, w 640, h 300. Its top lines up with the PERIOD heading in the rail. Background `#13233A`, no border. Name it **Period Popover** (Layout pane > Item hierarchy, double-click the name).
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

## Part 2: pick a span and a report date

A period is two picks: **how long** (the span) and **ending when** (the report date). Every number on the page will come from those two, plus how far back the comparison sits. This part builds the two picks; Part 3 turns them into dates.

### Step 4: the span list

**Why.** The span list is a list where exactly one option is ticked: a click writes that option's name into a string parameter, and the tick follows the parameter. There's no "untick", so one option is always picked and no click can lead to an empty page.

There's one puzzle first. Tableau draws one mark per value of a dimension, and no column in the data holds the words "Year", "Year to date", "Quarter" and "Month". So we borrow a column that has exactly four values: the fiscal quarter of each day. Every day falls in one of four quarters, so relabeling quarters 1 to 4 as the four options gives the list its four rows. This **menu field** doesn't filter or count anything; it only gives the list something to draw.

**Do.**

1. Create a parameter:

   | Name | Data type | Current value |
   |---|---|---|
   | `p_Span` | String | Year to date |

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

**You should see** four rows, Year to Month, with Year to date ticked. Click Quarter: the tick moves. Click Quarter again: it stays. Nothing else on the page uses `p_Span` yet; Step 6 changes that.

---

### Step 5: the report date grid

**Why.** The report date is where every period ends. Most of the time people want **today**, with the period so far ("year to date"); sometimes they want a closed month-end, to see a finished month, quarter or year. So the grid offers every closed month-end, plus today in the current month.

Storing the report date as a date would mean typing a year into the parameter, and a year typed today is wrong next year. So the parameter stores **how many months back from the latest month**: 0 is the latest month, which ends today (Jul 5, 2026); 1 is the month-end before it (Jun 30, 2026); 3 is Apr 30. When a new day arrives in the data, 0 moves with it, and so does everything built on it.

The grid offers the report dates that have two full years of data behind them: one year for their own window, one for the year they're compared with. The data starts on Jun 30, 2021, so the grid starts on Jul 31, 2023: three whole fiscal years, plus today. As new days arrive, the grid grows by itself.

**Do.**

1. Create a parameter:

   | Name | Data type | Current value |
   |---|---|---|
   | `p_Back` | Integer | 0 |

2. Create:

```
// Report Date
MIN([Latest], DATE(DATEADD('day', -1, DATEADD('month', 1 - [p_Back], DATETRUNC('month', [Latest])))))
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
// Month Label
IF MIN([Months Back]) = 0 AND DAY(DATEADD('day', 1, MAX([as_of_date]))) <> 1
THEN MIN([Month Abbr]) + " " + STR(DAY(MAX([as_of_date])))
ELSE MIN([Month Abbr]) END
```

```
// Month State
IF MIN([Months Back]) = [p_Back] THEN "picked" ELSE "open" END
```

How `Report Date` reads, inside out: `DATETRUNC('month', [Latest])` is the first day of the latest month (Jul 1, 2026); move it `1 - [p_Back]` months (with `p_Back` = 1, no months, still Jul 1); step back one day (Jun 30). That lands on a month-end every time, even for February. With `p_Back` = 0 it lands on Jul 31, a day the data hasn't reached yet, so `MIN([Latest], ...)` caps it at today. Tableau's `MIN` with two arguments simply returns the smaller one.

`Months Back` is the reverse trip: how many months a day sits before `Latest`. Every day in March 2026 is 4 months back, so a click anywhere in the March cell writes 4 into `p_Back`, and `Report Date` turns 4 back into Mar 31, 2026.

`Month Label` writes the day next to the month only in the cell for the latest month, when that month isn't finished: "Jul 5". The test `DAY(DATEADD('day', 1, d)) = 1` asks "is tomorrow the 1st?", which is true only on a month-end.

3. Right-click `Fiscal Month No` in the Data pane > **Convert to Dimension**, then **Convert to Discrete**.
4. New sheet **Month Grid**:
   - Drag `Month Offered` to Filters and keep **True**.
   - Rows `FY Label`. Columns `Fiscal Month No`, header hidden. The row header stays: it labels each row FY24 to FY27. Format the row header Tableau Semibold 9 `#8FA0B8`.
   - Marks **Text**. Drag `Month Label` to Text and `Month State` to Color. Click **Color** > Edit Colors: `picked` teal `#51C69E`, `open` `#B8C4D6`. Text Tableau Book 9, centered. The label takes the mark's color, so the picked cell turns teal.
   - Detail `Month Pick`, `zzTrue`, `zzFalse`.
   - Format: shading None, dividers None, grid lines None. Rows about 26 px high. Fit **Entire View**. Tooltip off.
5. Put **Month Grid** in **Period Popover** to the right of Span List (width 420).
6. Actions:

   | Name | Type | Source | Target | Field |
   |---|---|---|---|---|
   | Pick month | Change Parameter | Month Grid | p_Back | Month Pick (aggregation None) |
   | Deselect Month Grid | Filter | Month Grid | Month Grid | `zzTrue` → `zzFalse` |

**You should see** four rows, FY24 to FY27, Jul to Jun across. FY27 has one cell, "Jul 5", in teal. Click Jun in FY26: it turns teal and `p_Back` is 1. Click Mar in FY26: `p_Back` is 4. Click Jul in FY24: 36, the oldest date offered. Click "Jul 5" to go back to today.

---

## Part 3: from two picks to two windows

### Step 6: the two windows, shaded on the line

**Why.** A period is a **window**: an opening date and a closing date. The window covers the days after the opening, up to and including the closing. FY26 opens on Jun 30, 2025 and closes on Jun 30, 2026, so it covers July 2025 to June 2026, and its growth is the closing headcount minus the opening one. FY27 to date opens on Jun 30, 2026 and closes today, Jul 5.

The **span** decides where the current window opens. Year to date, quarter to date and month to date open at the last month-end before the period began: FY27 to date opens on Jun 30. Year opens a year before the report date: 12 months to Jul 5, 2026 opens on Jul 5, 2025.

The **shift** decides where the comparison sits: 12 months back for now. Step 11 adds the other choice.

Here is the one rule that makes "to date" work. Count back from a **month-end**, and you land on month-ends: Apr 30 minus one month is Mar 31, not Mar 30. Count back from **any other day**, and you land on the same day: Jul 5 minus a year is Jul 5, 2025. Compare 30 days of April with 30 days of March, and you'd silently drop a day; compare Jul 1–5 with all of July last year, and the comparison would be meaningless.

| Date | Report date is a month-end | Report date is any other day |
|---|---|---|
| Current close | the report date | the report date |
| Current open | the month-end before the period began (Year: 12 months back) | the month-end before the period began (Year: the same day a year back) |
| Comparison close | the month-end `Shift` months back | the same day `Shift` months back |
| Comparison open | the month-end `Shift` months before the current open | the same, or the same day a year before the comparison close for Year |

**Do.**

1. Create:

```
// Is Month End
DAY(DATEADD('day', 1, [Report Date])) = 1
```

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
IF [p_Span] = "Year" AND NOT [Is Month End] THEN DATE(DATEADD('month', -12, [Report Date]))
ELSE DATE(DATEADD('day', -1, DATEADD('month', 1 - [Months In], DATETRUNC('month', [Report Date])))) END
```

```
// Comparison Close
IF [Is Month End] THEN DATE(DATEADD('day', -1, DATEADD('month', 1 - [Shift], DATETRUNC('month', [Report Date]))))
ELSE DATE(DATEADD('month', -[Shift], [Report Date])) END
```

```
// Comparison Open
IF [p_Span] = "Year" AND NOT [Is Month End] THEN DATE(DATEADD('month', -[Shift] - 12, [Report Date]))
ELSE DATE(DATEADD('day', -1, DATEADD('month', 1 - [Shift] - [Months In], DATETRUNC('month', [Report Date])))) END
```

```
// In Current
[as_of_date] > [Current Open] AND [as_of_date] <= [Current Close]
```

```
// In Comparison
[as_of_date] > [Comparison Open] AND [as_of_date] <= [Comparison Close]
```

How `Months In` reads: the months of the period the report date falls in, counting its own month. Year to date in March is 9 (July to March); in July it's 1. A quarter at the end of May is 2 (April and May). Arcadia's fiscal quarters end in September, December, March and June, the same months as calendar quarters, so `(MONTH - 1) % 3` counts the months so far.

Both branches of `Current Open` and `Comparison Open` use the same month-end expression as `Report Date`, counted from the report date's own month: "the month-end k months before this month". The only other branch is Year on a day that isn't a month-end, which counts back to the same day.

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
// Now Day
LEFT(DATENAME('month', [Current Close]), 3) + " " + STR(DAY([Current Close])) + ", " + STR(YEAR([Current Close]))
```

```
// Now Short
LEFT(DATENAME('month', [Current Close]), 3) + (IF [Is Month End] THEN "" ELSE " " + STR(DAY([Current Close])) END)
```

```
// Now Name
CASE [p_Span]
WHEN "Year" THEN (IF [Is Month End] AND MONTH([Current Close]) = 6 THEN [Now FY]
                  ELSEIF [Is Month End] THEN "12 months to " + [Now Month]
                  ELSE "12 months to " + [Now Day] END)
WHEN "Year to date" THEN [Now FY] + " to " + [Now Short]
WHEN "Quarter" THEN [Now FY] + " Q" + STR(INT(((MONTH([Current Close]) + 5) % 12) / 3) + 1)
    + (IF [Months In] = 3 AND [Is Month End] THEN "" ELSE " to " + [Now Short] END)
ELSE (IF [Is Month End] THEN [Now Month]
      ELSE LEFT(DATENAME('month', [Current Close]), 3) + " 1–" + STR(DAY([Current Close])) + ", " + STR(YEAR([Current Close])) END) END
```

```
// Now From
DATEADD('day', 1, [Current Open])
```

```
// Now Range
IF NOT [Is Month End]
THEN LEFT(DATENAME('month', [Now From]), 3) + " " + STR(DAY([Now From])) + ", " + STR(YEAR([Now From])) + " – " + [Now Day]
ELSEIF DATEDIFF('month', [Current Open], [Current Close]) = 1 THEN [Now Month]
ELSE LEFT(DATENAME('month', [Now From]), 3) + " " + STR(YEAR([Now From])) + " – " + [Now Month] END
```

And the same seven for the comparison:

```
// Before FY
"FY" + RIGHT(STR(YEAR([Comparison Close]) + (IF MONTH([Comparison Close]) >= 7 THEN 1 ELSE 0 END)), 2)
```

```
// Before Month
LEFT(DATENAME('month', [Comparison Close]), 3) + " " + STR(YEAR([Comparison Close]))
```

```
// Before Day
LEFT(DATENAME('month', [Comparison Close]), 3) + " " + STR(DAY([Comparison Close])) + ", " + STR(YEAR([Comparison Close]))
```

```
// Before Short
LEFT(DATENAME('month', [Comparison Close]), 3) + (IF [Is Month End] THEN "" ELSE " " + STR(DAY([Comparison Close])) END)
```

```
// Before Name
CASE [p_Span]
WHEN "Year" THEN (IF [Is Month End] AND MONTH([Comparison Close]) = 6 THEN [Before FY]
                  ELSEIF [Is Month End] THEN "12 months to " + [Before Month]
                  ELSE "12 months to " + [Before Day] END)
WHEN "Year to date" THEN [Before FY] + " to " + [Before Short]
WHEN "Quarter" THEN [Before FY] + " Q" + STR(INT(((MONTH([Comparison Close]) + 5) % 12) / 3) + 1)
    + (IF [Months In] = 3 AND [Is Month End] THEN "" ELSE " to " + [Before Short] END)
ELSE (IF [Is Month End] THEN [Before Month]
      ELSE LEFT(DATENAME('month', [Comparison Close]), 3) + " 1–" + STR(DAY([Comparison Close])) + ", " + STR(YEAR([Comparison Close])) END) END
```

```
// Before From
DATEADD('day', 1, [Comparison Open])
```

```
// Before Range
IF NOT [Is Month End]
THEN LEFT(DATENAME('month', [Before From]), 3) + " " + STR(DAY([Before From])) + ", " + STR(YEAR([Before From])) + " – " + [Before Day]
ELSEIF DATEDIFF('month', [Comparison Open], [Comparison Close]) = 1 THEN [Before Month]
ELSE LEFT(DATENAME('month', [Before From]), 3) + " " + STR(YEAR([Before From])) + " – " + [Before Month] END
```

A year that closes on Jun 30 is a fiscal year, so it's called FY26; one that closes on Dec 31 is "12 months to Dec 2025", and one that closes today is "12 months to Jul 5, 2026". A period still in progress says how far it got: "FY27 to Jul 5", "FY26 Q4 to May", "Jul 1–5, 2026".

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

     with the format **Number, 0 decimals, thousands separator**. Drag it to Label: Tableau Semibold 9 navy, **Allow labels to overlap other marks**. Every other day has no value, so only the two closing points show a number.

5. **The zoom.** Five years of days make a five-day window a sliver. Create

   ```
   // In View
   [as_of_date] >= DATEADD('month', -1, [Comparison Open])
   ```

   and drag it to Filters on **Try It**, keeping **True**. The date axis then starts a month before the comparison window and ends today, so it zooms in or out with every pick.

**You should see**, with Year to date and today picked: the line from late May 2025 to Jul 5, 2026, a thin green band over Jul 1–5, 2026 and a sand band over Jul 1–5, 2025, and the points labeled 30,041 and 28,465. The legend reads "FY27 to Jul 5 · Jul 1, 2026 – Jul 5, 2026" and "FY26 to Jul 5 · Jul 1, 2025 – Jul 5, 2025".

| Span, report date | Legend, current | Legend, comparison |
|---|---|---|
| Year to date, today | FY27 to Jul 5 · Jul 1, 2026 – Jul 5, 2026 | FY26 to Jul 5 · Jul 1, 2025 – Jul 5, 2025 |
| Year, today | 12 months to Jul 5, 2026 · Jul 6, 2025 – Jul 5, 2026 | 12 months to Jul 5, 2025 · Jul 6, 2024 – Jul 5, 2025 |
| Year to date, Jun 2026 | FY26 to Jun · Jul 2025 – Jun 2026 | FY25 to Jun · Jul 2024 – Jun 2025 |
| Year, Jun 2026 | FY26 · Jul 2025 – Jun 2026 | FY25 · Jul 2024 – Jun 2025 |
| Quarter, May 2026 | FY26 Q4 to May · Apr 2026 – May 2026 | FY25 Q4 to May · Apr 2025 – May 2025 |
| Month, Jun 2026 | Jun 2026 | Jun 2025 |

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
| Year to date, today | "FY27 to Jul 5" | vs FY26 to Jul 5 |
| Year, today | "12 months to Jul 5, 2026" | vs 12 months to Jul 5, 2025 |
| Month, today | "Jul 1–5, 2026" | vs Jul 1–5, 2025 |
| Year, Jun 2026 | "FY26" | vs FY25 |
| Year to date, Mar 2026 | "FY26 to Mar" | vs FY25 to Mar |
| Year, Dec 2025 | "12 months to Dec 2025" | vs 12 months to Dec 2024 |

---

## Part 4: the numbers

Three cards compare the two windows. They also show the one idea worth taking from this lesson: **headcount is a balance**. A balance is counted at a moment (a day), not added up over time. That changes which numbers move when you switch the span.

### Step 8: employees at the end

**Why.** The closing headcount of a window is simply the headcount on its closing day.

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

2. Sheet **KPI End**: no field on Rows or Columns. Marks **Text**, left aligned, top, three lines: `EMPLOYEES AT END` Tableau Semibold 8 `#5A6170`; `<End Now>` Tableau Bold 24 navy `#13233A`; `vs <End Before> · <End Change %>` Tableau Book 9 `#5A6170`. Detail `zzTrue`, `zzFalse`; tooltip off; a deselect action.

   Keep the first line short: a card is 160 px wide, and Tableau shows `#####` instead of a text mark whose line doesn't fit.

**You should see** 30,041, "vs 28,465 · +5.5%".

**Try it.** Switch Year to date to Year, Quarter and Month. The card doesn't move. That's right: all four end today and compare with the same day last year, so they end on the same two numbers. Pick Jun in FY26 and it changes to 30,005, "vs 28,438 · +5.5%". This is the question a period picker gets most often, and the next two cards are the answer to it.

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

2. Sheet **KPI Growth**, built like KPI End: `GROWTH IN PERIOD`; `<Growth Now>` Tableau Bold 24 navy; `vs <Growth Before>` Tableau Book 9 `#5A6170`.

**You should see**

| You pick | Growth | vs |
|---|---|---|
| Year to date, today | +36 | +27 |
| Year, today | +1,576 | +1,233 |
| Year, Jun 2026 | +1,567 | +1,230 |
| Quarter, Jun 2026 | +387 | +301 |
| Month, Jun 2026 | +131 | +104 |
| Year to date, Mar 2026 | +1,180 | +929 |

Today, year to date, quarter to date and month to date all show +36: July is the first month of FY27 and of its first quarter, so all three windows are the same five days. Pick Jun in FY26 and they come apart.

---

### Step 10: average employees

**Why.** An average over the window counts each day inside it once: the sum of the daily headcounts divided by the days in the window. It's the number to divide by for anything "per employee", such as cost per head or turnover rate. The two windows can hold different numbers of days (a leap year, March against February), so each is divided by its own.

**Do.**

1. Create:

```
// Days Now
DATEDIFF('day', [Current Open], [Current Close])
```

```
// Days Before
DATEDIFF('day', [Comparison Open], [Comparison Close])
```

```
// Average Now
SUM(IF [In Current] THEN [employees] END) / MIN([Days Now])
```

```
// Average Before
SUM(IF [In Comparison] THEN [employees] END) / MIN([Days Before])
```

```
// Average Change %
[Average Now] / [Average Before] - 1
```

`MIN([Days Now])` because `Days Now` is the same on every row, and Tableau needs it aggregated to divide an aggregate by it. Formats: the averages **Number, 0 decimals, thousands separator**; `Average Change %` **Custom** `+0.0%;−0.0%`.

2. Sheet **KPI Average**, built like KPI End: `AVERAGE EMPLOYEES`; `<Average Now>` Tableau Bold 24 navy; `vs <Average Before> · <Average Change %>` Tableau Book 9 `#5A6170`.

**You should see** 30,025, "vs 28,461 · +5.5%" for FY27 to Jul 5. Year, today: 29,245, "vs 27,841 · +5.0%". FY26 (Year, Jun 2026): 29,224, "vs 27,824 · +5.0%".

---

## Part 5: your turn, reset, and the finished page

### Step 11: your turn, compare with the prior period

"Last year" isn't the only comparison people ask for. For a quarter, the question is often "how are we doing against **last** quarter, at the same point?" Build a toggle under the capsule with two halves, **Last year** and **Prior period**, and make the shift follow it. Use the hints first; the full answer is below them, and the finished sheets are in the downloadable workbook (Basis Year and Basis Prior), so you can open them and compare.

**Hints**

- One more string parameter, `p_Basis`, current value `Last year`.
- `Shift` becomes 3 for a quarter and 1 for a month when `p_Basis` is "Prior period", and stays 12 otherwise. For a year and year to date, the prior period **is** last year, so both halves read the same there.
- The to-date rule from Step 6 still applies: Jul 5 against the prior quarter is Apr 5, the same day three months back.
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
| Quarter, today, Prior period | "FY27 Q1 to Jul 5" | vs FY26 Q4 to Apr 5 | 30,041 vs 29,653 · +1.3% | +36 vs +35 |
| Month, today, Prior period | "Jul 1–5, 2026" | vs Jun 1–5, 2026 | 30,041 vs 29,889 · +0.5% | +36 vs +15 |
| Quarter, Jun 2026, Prior period | "FY26 Q4" | vs FY26 Q3 | 30,005 vs 29,618 · +1.3% | +387 vs +397 |
| Month, Jun 2026, Prior period | "Jun 2026" | vs May 2026 | 30,005 vs 29,874 · +0.4% | +131 vs +118 |
| Year to date, today, Prior period | "FY27 to Jul 5" | vs FY26 to Jul 5 | the same as Last year | |

With Prior period, the two bands on Try It sit close together instead of a year apart.

---

### Step 13: reset to default view

One button that puts every pick back and closes the panel.

1. Create:

```
// Reset Span
"Year to date"
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

**You should see** Year to date ticked, "Jul 5" teal, Last year chosen, the panel closed, and the cards back at 30,041 · +36 · 30,025.

---

### Step 14: the title, and the finished page

The title says what the page shows, in words that follow the picks.

```
// Page Subtitle
"Employees, " + [Now Name] + " compared with " + [Before Name] + " · report date " + [Now Day]
```

Sheet **Title**: Marks **Text**, three lines, left, top: `HOW-TO · STEP-BY-STEP LESSON` Tableau Semibold 9 teal `#0F6E56`; `How to build a period picker for year, year to date, quarter and month` Tableau Bold 18 navy; `<Page Subtitle>` Tableau Book 11 `#5A6170`. The first two lines say what the page is before anyone reads a number: a lesson, not an analysis. Detail `zzTrue`, `zzFalse`; tooltip off; a deselect action.

**You should see** "Employees, FY27 to Jul 5 compared with FY26 to Jul 5 · report date Jul 5, 2026". No year is typed anywhere: when a newer file arrives, the title, the grid and every card move on their own.

#### The finished page

Dashboard **Period selection**, Fixed 1400 × 850, shading `#F3F3EF`, every item floating:

| Item | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Rail (vertical container) | 0 | 0 | 216 | 850 | Navy `#13233A`, padding 8 left and right |
| Title (sheet) | 240 | 8 | 1136 | 78 | Three lines need the full 78 px, or the subtitle is cut |
| Lesson card (text and images in a white container) | 240 | 88 | 600 | 724 | What the page is, the images, how to try it, how to build it, how to use your own data |
| KPI End / Growth / Average (each in a white container) | 872 / 1044 / 1216 | 88 | 160 | 116 | Radius 14, border 1 px `#E4E3DD`, padding 14. Three lines need 88 px inside |
| Chart card (white container) | 872 | 216 | 504 | 596 | Text "Employees each day" Semibold 11 navy, then Try It, then Windows |
| Footnote (text) | 240 | 822 | 1136 | 18 | "Arcadia Systems is fictional; all data is synthetic. Executive officers excluded. Fiscal year starts July 1." Book 9 `#5A6170` |
| Period Popover | 216 | 96 | 640 | 300 | Visibility `p_PeriodOpen` |

Inside the rail, top to bottom: blank 24 · `arcadia_logo_reverse.png` 160 × 40 · blank 32 · PERIOD 18 · Period Field 32 · Period Sub 20 · blank 10 · COMPARED WITH 18 · the toggle 32 (Basis Year, Basis Prior) · `rail_divider.png` 24 · Reset 32 · flexible blank · a credit line at the foot, Tableau Book 9: your name in `#E4E9F0`, then "Files and guide on GitHub" in `#B9C3D1`.

Inside the popover, top to bottom: the title row 44 (title and ✕) · `popover_line.png` · two columns, each with a small heading (Tableau Semibold 8, `#8FA0B8`): `SPAN` over Span List (200 wide) and `REPORT DATE` over Month Grid (420 wide) · a footer text 30, Book 9 `#8FA0B8`: "Every period ends on the report date: today, or a closed month-end." Keep the footer to one line: a longer one is cut off.

The popover sits in front of everything; the rail in front of the page. The cards and the chart sit right of x 856, so they stay in view while the panel is open.

---

## Use it on your own data

Arcadia's file is a **daily balance**: one row per day and group, with a count. Any daily balance works the same way: headcount, open positions, active customers, inventory on hand, account balances. A monthly balance works too: the page then only ever lands on month-ends.

- **Your own balance.** Swap `employees` for your count and `as_of_date` for your date. Every window field keeps working, because none of them names a column other than the date.
- **Your fiscal year.** Arcadia's starts in July, which is where the `+ 5` comes from in `Span No`, `Fiscal Month No`, `Months In` and the names: `(MONTH + 5) % 12` is 0 in July. For a year starting in October use `+ 2`; for a calendar year, `+ 11` (or simply `MONTH - 1`). The FY rule `MONTH >= 7` becomes `MONTH >= 10` for October. Quarters follow by themselves when your fiscal quarters end in March, June, September and December.
- **A flow instead of a balance.** For hires, sales or tickets, the window total is the sum of the days inside it: `SUM(IF [In Current] THEN [your measure] END)`. Year, year to date, quarter and month then each give a different number, as you'd expect, and the to-date rule keeps the comparison fair: the same five days last year, not the whole month.
- **More history, or less.** The grid offers every month-end with two years behind it, plus today. With three years of data you get about one fiscal year of choices; with ten, eight.

---

## Checks

Run these in Presentation mode, then again after publishing.

| # | Do | Expect |
|---:|---|---|
| 1 | Nothing | Capsule "FY27 to Jul 5", "vs FY26 to Jul 5"; Year to date ticked; "Jul 5" teal; Last year chosen; cards 30,041 · vs 28,465 · +5.5% / +36 vs +27 / 30,025 · vs 28,461 · +5.5% |
| 2 | Click the capsule, every list row, grid cell, toggle half, ✕ and Reset | Nothing stays highlighted |
| 3 | Year | "12 months to Jul 5, 2026"; growth +1,576 vs +1,233; average 29,245 · vs 27,841 · +5.0%; the end card doesn't move |
| 4 | Quarter, then Month | The same cards as check 1: all three windows are Jul 1–5 |
| 5 | Quarter, Prior period | "vs FY26 Q4 to Apr 5"; 30,041 · vs 29,653 · +1.3%; growth +36 vs +35 |
| 6 | Month, Prior period | "vs Jun 1–5, 2026"; 30,041 · vs 29,889 · +0.5%; growth +36 vs +15 |
| 7 | Reset, then Jun in FY26 | "FY26 to Jun", "vs FY25 to Jun"; cards 30,005 · vs 28,438 · +5.5% / +1,567 vs +1,230 / 29,224 · vs 27,824 · +5.0% |
| 8 | Quarter | "FY26 Q4", "vs FY25 Q4"; growth +387 vs +301; average 29,813 · vs 28,290 · +5.4% |
| 9 | Year to date, then Mar in FY26 | "FY26 to Mar"; cards 29,618 · vs 28,137 · +5.3% / +1,180 vs +929 / 29,028 · vs 27,670 · +4.9% |
| 10 | Year, then Dec in FY26 | "12 months to Dec 2025"; 29,221 · vs 27,825 · +5.0%; growth +1,396 vs +754 |
| 11 | Quarter, then May in FY26 | "FY26 Q4 to May", "vs FY25 Q4 to May"; growth +256 vs +197 |
| 12 | Year, then Jul in FY24 | "12 months to Jul 2023", "vs 12 months to Jul 2022"; 26,961 · vs 25,233 · +6.8% |
| 13 | Reset | Everything as in check 1, panel closed |

---

## Why it works this way

- **Why count months back instead of storing a date?** A date parameter holds a year, and a year typed today is out of date the day new data arrives. `p_Back` = 0 always means "the latest month", so a refresh moves the whole page forward by itself.
- **Why one rule for "to date"?** A month-end report date compares with month-ends, so a closed month is always a whole month, February included. Any other day compares with the same day, so five days are compared with five days. Mixing the two is how "month to date" ends up compared with a whole month.
- **Why a menu field for the span list?** A list needs one mark per option, and the options aren't in the data. Any column with exactly as many values as you have options will do; the fiscal quarter has four, one for each span.
- **Why does the end card ignore the span?** Headcount is a balance, counted at a moment. A year, a quarter and a month that end on the same day end on the same headcount. Growth and averages depend on the days inside the window, so they follow the span.
- **Why reference bands, and a filter for the zoom?** A band reads its edges from fields in the view, so the shading moves with every click without a second chart or a dual axis. A continuous date axis fits whatever the filter keeps, so filtering to the windows is a zoom.
- **Why the deselect trick?** A click on an already-selected mark only unselects it. Clearing the selection right away means every click runs its action.

---

## Files in this folder

| Path | What it is |
|---|---|
| `period-selection-files.zip` | Everything you need: the CSV and the Arcadia How-To shapes folder |
| `data/arcadia_daily_headcount.csv` | The data on its own, to preview on GitHub |
| `shapes/*.png` | The images on their own, to preview on GitHub |
| `GUIDE.md` | This guide |

The CSV is the Arcadia warehouse's `mart_daily_headcount`: the [people analytics warehouse](https://github.com/thialp/people-analytics-warehouse) closes each month at the report date (Jun 30, 2026) and keeps reading its HR system every night, so the daily headcount runs on to the latest extract (Jul 5, 2026). You don't need the warehouse for the lesson.

### The data, column by column

| Column | Example | Notes |
|---|---|---|
| `as_of_date` | 2026-07-05 | The day each row counts; every day from Jun 30, 2021 to Jul 5, 2026 |
| `is_closed` | false | True up to Jun 30, 2026, the last closed month-end; false for the days of July so far |
| `function_name` | Commercial | 8 functions |
| `sub_function` | Client Services | 10 sub-functions |
| `department_name` | Client Success | 31 departments |
| `employees` | 1,665 | Employees in that department on that day (Client Success, Jul 5, 2026) |

The column names match How-To #1's file, so its calculations paste straight in. Executive officers are excluded, as on every Arcadia dashboard: 30,005 employees on Jun 30, 2026 and 30,041 on Jul 5, 2026. Someone whose last day is a given day still counts on that day.
