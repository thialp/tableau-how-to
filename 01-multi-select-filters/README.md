# How-To #1: multi-select filters with clicks and images

Build the filter panel below from an empty Tableau workbook: a button that opens a panel, a list you tick and untick, departments that follow their function, a last option that can't be unticked, and options that gray out when nobody is behind them. Every step is a calculation or a click in Tableau. There is no SQL and no extension.

<!-- Screenshot goes here after the build: ![The finished filter panel](images/finished.png) -->

**What you need:** Tableau Desktop or Tableau Public (the free app), version 2022.3 or later (for showing and hiding containers with a parameter). Plan on about two hours, or an hour for Part 1 and Part 2 alone.

**What you'll learn**

| Part | Technique | Used for |
|---|---|---|
| 1 | An image as a button: a one-mark sheet, a custom shape, a parameter action | The rail capsule that opens a panel |
| 1 | Show and hide a container with a parameter | The panel itself, and its ✕ |
| 1 | The deselect trick | Buttons that never stay highlighted |
| 2 | A string parameter as a list | Picking several options with a click each |
| 2 | Storing what's left out instead of what's in | Departments that start ticked when you pick their function |
| 2 | Cleaning up with `REGEXP_REPLACE` | A function click that also resets its departments |
| 2 | A guard on the last option | No click can lead to an empty page |
| 3 | Graying out options with nobody behind them | Two filters that respect each other |
| Bonus | Reset to default view | One click back to the start |

Arcadia Systems is a fictional company. All data is synthetic.

---

## Contents

0. [Get ready](#0-get-ready)
1. [Part 1: a button made of an image](#part-1-a-button-made-of-an-image)
   - [Step 1: the capsule](#step-1-the-capsule)
   - [Step 2: the panel that opens](#step-2-the-panel-that-opens)
   - [Step 3: the ✕, and buttons that never stay highlighted](#step-3-the--and-buttons-that-never-stay-highlighted)
2. [Part 2: a list you can tick](#part-2-a-list-you-can-tick)
   - [Step 4: a parameter that holds a list](#step-4-a-parameter-that-holds-a-list)
   - [Step 5: the function list](#step-5-the-function-list)
   - [Step 6: departments that follow their function](#step-6-departments-that-follow-their-function)
   - [Step 7: the last one ticked stays](#step-7-the-last-one-ticked-stays)
   - [Step 8: make the capsule talk](#step-8-make-the-capsule-talk)
3. [Part 3: two filters that respect each other](#part-3-two-filters-that-respect-each-other)
   - [Step 9: your turn, Location](#step-9-your-turn-location)
   - [Step 10: gray out what's empty](#step-10-gray-out-whats-empty)
4. [Bonus: reset to default view](#bonus-reset-to-default-view)
5. [Put the page together](#5-put-the-page-together)
6. [Checks](#6-checks)
7. [Why it works this way](#7-why-it-works-this-way)

---

## 0. Get ready

### 0.1 Download the files

From this folder on GitHub:

| File | What it is | How to download |
|---|---|---|
| [`data/arcadia_employees.csv`](data/arcadia_employees.csv) | 30,005 employees, one row each, on Jun 30, 2026 | Open it, then **Download raw file** (the arrow at the top right) |
| [`shapes/arcadia_how_to_shapes.zip`](shapes/arcadia_how_to_shapes.zip) | The button and tick images | Open it, then **Download raw file** |

Want to restyle the images? They're drawn in the [Arcadia Analytics · Tableau UI Kit](https://www.figma.com/community/file/1690422855000144024) on Figma: open it, change the colors, and export at 2×. You don't need Figma to follow this guide.

### 0.2 Install the shapes

Unzip `arcadia_how_to_shapes.zip`. You'll get a folder **Arcadia How-To** holding eight PNG files. Move that folder into:

- Windows: `Documents\My Tableau Repository\Shapes\`
- Mac: `Documents/My Tableau Repository/Shapes/`

| File | Size (px) | What it draws |
|---|---|---|
| `capsule_dark.png` | 600 × 96 | The rail button when nothing is chosen ("All functions") |
| `capsule_light.png` | 600 × 96 | The rail button when a choice is on |
| `tick_on.png` | 36 × 36 | A ticked box (teal, white tick) |
| `tick_off.png` | 36 × 36 | An empty box |
| `reset_button.png` | 600 × 96 | "Reset to default view" (Bonus) |
| `popover_line.png` | 1248 × 18 | The thin line under a panel's title |
| `rail_divider.png` | 400 × 48 | The line across the rail |
| `arcadia_logo_reverse.png` | 1200 × 326 | The logo for the rail |

The images are drawn at twice their on-screen size, so they stay sharp on high-resolution screens. If Tableau was open, restart it, or click **Reload Shapes** in the shape picker, so it sees the new folder.

### 0.3 Connect the data

1. Open Tableau. **Connect > To a File > Text file**, and pick `arcadia_employees.csv`.
2. Check the types on the Data Source page: `as_of_date` and `hire_date` are dates; every other column is a string (Abc).
3. Go to Sheet 1. **File > Save As** `Multi-select filters.twbx` (Tableau Public saves to your profile instead; that's fine).

**You should see** 13 fields in the Data pane, plus `arcadia_employees.csv (Count)`. Drag `arcadia_employees.csv (Count)` to Text: **30,005**.

### 0.4 Two helper fields you'll use all the time

Create these now (**Analysis > Create Calculated Field**). Each formula box below starts with a `//` line naming the field; type that name in the name box and paste the rest.

```
// Employees
COUNT([employee_id])
```

```
// One
1
```

`Employees` is the number you show. `One` is a 1 on every row, so `SUM(IF ... THEN [One] END)` counts the rows that pass a test, which is how the lists will ask "is anybody behind this option?"

### 0.5 The "try it" sheet

Every step changes what this one sheet shows, so you can see your work.

1. New sheet, name it **Try It**.
2. `department_name` on Rows, `Employees` on Columns, sort descending. Drag `Employees` to Label.
3. Color one navy, `#13233A`.

**You should see** 31 bars, starting with Core Platform Engineering. Leave it like this; in Step 4 you'll add one filter to it.

---

## Part 1: a button made of an image

The rail capsules on the [Arcadia dashboards](https://public.tableau.com/app/profile/thialp) aren't Tableau filters. Each is a sheet with exactly one mark. The mark is drawn with a custom shape (the capsule picture), its label is the text, and a click on it runs a parameter action. That's the whole idea of an image button.

### Step 1: the capsule

**Why.** A sheet with no dimension in the view draws one mark. Give that mark a picture and a click action, and you have a button you can style any way you like.

**Do.**

1. Create a parameter: right-click in the Data pane > **Create Parameter**.

   | Name | Data type | Current value |
   |---|---|---|
   | `p_OrgOpen` | Boolean | False |

   Boolean parameters show True and False; that's all we need. Repeat for **`p_LocOpen`** (Boolean, False), which you'll use in Step 9.

2. Create these calculated fields:

```
// Toggle Org Panel
NOT [p_OrgOpen]
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
// Org Capsule Shape
"capsule_dark"
```

```
// Org Field Text
"All functions"
```

`Org Capsule Shape` and `Org Field Text` are placeholders: Step 8 makes them follow the selection.

3. New sheet, name it **Org Field**.
   - Marks type **Shape**. Drag `Org Capsule Shape` to Shape. Click **Shape**, pick the palette **Arcadia How-To**, and assign `capsule_dark.png` to the value `capsule_dark`.
   - Drag `Org Field Text` to Label. Click **Label**: font Tableau Semibold 9, color `#E4E9F0`; Alignment horizontal **left**, vertical **middle**.
   - Drag `Toggle Org Panel`, `Close Panel`, `zzTrue` and `zzFalse` to Detail. They don't draw anything; actions can only read fields that are in the view.
   - Size: drag the size slider until the capsule fills the cell. If the label sits on top of the image, add two or three leading spaces inside the label text, before `<Org Field Text>`.
   - **Format > Shading**: worksheet None. **Format > Borders** and **Lines**: None everywhere. Tooltip: open it and type `Choose functions and departments`, untick **Include command buttons**.

**You should see** one dark capsule reading "All functions", and nothing else on the sheet.

**Try it.** Click the capsule. It highlights and stays highlighted. Step 3 fixes that.

### Step 2: the panel that opens

**Why.** A dashboard container can be shown or hidden by a Boolean parameter. The capsule click flips the parameter, so the container appears and disappears.

**Do.**

1. Create a new dashboard, **Step 2**, size **Fixed 1400 × 850**. Shading `#F3F3EF`.
2. Drag a **Vertical** container onto the dashboard, **floating**: x 0, y 0, w 216, h 850. Background navy `#13233A`. This is the rail.
3. Drag **Org Field** into the rail. Hide its title. Fixed height 32.
4. Drag another **Vertical** container, floating, to x 216, y 140, w 640, h 700. Background `#13233A`, no border. Name it **Org Popover** (Layout pane > Item hierarchy, double-click the name).
5. Into **Org Popover** drag a **Text** object: `Organization`, Tableau Bold 12, white. Fixed height 44. This is the panel's title; Step 3 adds the ✕ beside it.
6. Select **Org Popover**. In the Layout pane tick **Control visibility using value**, and pick **Parameters > p_OrgOpen**.
7. **Dashboard > Actions > Add Action > Change Parameter**:

   | Name | Source sheet | Run on | Target parameter | Source field | Aggregation | Clearing the selection |
   |---|---|---|---|---|---|---|
   | Open org popover | Org Field | Select | p_OrgOpen | Toggle Org Panel | None | Keep current value |

**You should see** a navy rail with the capsule and no panel. Click the capsule: the panel appears. Click it again: the panel... doesn't close. Why? The first click left the capsule selected, so the second click only clears the selection, and clearing keeps the parameter as it was. That's Step 3.

### Step 3: the ✕, and buttons that never stay highlighted

**Why.** A selected mark stays selected until you click it again, and that second click is spent on unselecting instead of running your action. The fix is the **deselect trick**: a Filter action on the same sheet that maps `zzTrue` to `zzFalse`. On every click it asks Tableau to keep only rows where TRUE equals FALSE. No row qualifies, so Tableau drops the selection at once, and because the action clears to **Show all values**, nothing disappears. Every click is now a fresh click.

**Do.**

1. **Dashboard > Actions > Add Action > Filter**:

   | Name | Source | Run on | Target | Clearing the selection | Filter |
   |---|---|---|---|---|---|
   | Deselect Org Field | Org Field (this dashboard) | Select | Org Field | Show all values | Selected fields: `zzTrue` → `zzFalse` |

   Under **Target Filters**, choose **Selected Fields**, Source field `zzTrue`, Target field `zzFalse`.

2. New sheet **Org Close**: Marks **Text**; Text `✕` typed into the label (Tableau Book 12, `#B8C0CC`), centered. Detail `Close Panel`, `zzTrue`, `zzFalse`. Tooltip `Close`, command buttons off. Shading None.
3. On the dashboard, put a **Horizontal** container at the top of **Org Popover** in place of the title text: the title text on the left (width 596), **Org Close** on the right (width 44), height 44.
4. Two actions:

   | Name | Type | Source | Target | Field |
   |---|---|---|---|---|
   | Org popover on ✕ | Change Parameter | Org Close | p_OrgOpen | Close Panel |
   | Deselect Org Close | Filter | Org Close | Org Close | `zzTrue` → `zzFalse` |

5. One panel at a time. Add:

   | Name | Type | Source | Target | Field |
   |---|---|---|---|---|
   | Org closes Loc | Change Parameter | Org Field | p_LocOpen | Close Panel |

   The Location capsule (Step 9) gets the mirror action, so opening one closes the other.

**You should see** the capsule open and close the panel on every click, the ✕ close it, and nothing ever stay highlighted.

**Rule for the rest of this guide:** every sheet you click gets its own deselect action (`zzTrue` → `zzFalse`, Show all values), and `zzTrue` and `zzFalse` on its Detail. Every tooltip has **Include command buttons** unticked.

---

## Part 2: a list you can tick

Tableau has no parameter that holds several values. So we keep them in a string: `|People|Finance|`. Each name sits between two bars, so `CONTAINS([p_Functions], "|People|")` tests for one name without matching a longer one by accident. An empty string means "everything".

### Step 4: a parameter that holds a list

**Do.**

1. Create two parameters:

   | Name | Data type | Current value | Holds |
   |---|---|---|---|
   | `p_Functions` | String | (empty) | The functions you ticked: `\|People\|Finance\|` |
   | `p_DeptOff` | String | (empty) | The departments you **un**ticked: `\|People>Talent Acquisition\|` |

   Why the second one stores what's left out comes in Step 6.

2. Create:

```
// Function In
[p_Functions] = "" OR CONTAINS([p_Functions], "|" + [function_name] + "|")
```

```
// Dept Key
[function_name] + ">" + [department_name]
```

```
// Dept In
[Function In] AND NOT CONTAINS([p_DeptOff], "|" + [Dept Key] + "|")
```

```
// In Scope
[Dept In]
```

3. On **Try It**, drag `In Scope` to Filters and keep **True**. Right-click the filter > **Apply to Worksheets > All Using This Data Source** is **not** what you want: keep it on Try It only. The lists must always see every option.

**Try it.** Show the parameter control for `p_Functions` (right-click > Show Parameter) and type `|People|`. Try It shows four bars: HR Business Partners 389, Talent Acquisition 388, Total Rewards 221, People Analytics 180. Type `|People|Finance|`: seven bars. Then type `|People>Talent Acquisition|` into `p_DeptOff`: Talent Acquisition goes. Empty both boxes and hide the controls again; from now on clicks will write them.

### Step 5: the function list

**Why.** One click must add the name if it isn't in the string, and take it out if it is. A calculation can build the new string for each mark, and a parameter action writes the string of the mark you clicked.

**Do.**

1. Create:

```
// Function Toggle
IF CONTAINS([p_Functions], "|" + [function_name] + "|")
THEN (IF [p_Functions] = "|" + [function_name] + "|" THEN ""
      ELSE REPLACE([p_Functions], "|" + [function_name] + "|", "|") END)
ELSE (IF [p_Functions] = "" THEN "|" + [function_name] + "|"
      ELSE [p_Functions] + [function_name] + "|" END)
END
```

```
// Function Pick
MIN([Function Toggle])
```

```
// Function Shape
IF [p_Functions] <> "" AND MIN([Function In]) THEN "tick_on" ELSE "tick_off" END
```

```
// Tick X
MIN(0.6)
```

`Tick X` puts every box at the same spot near the left of a 0-to-10 axis, a little in from the edge so the box isn't cut in half.

Reading `Function Toggle` for People: if `|People|` is in the string, remove it (and if it was the only one, leave the string empty); otherwise append it. `Function Pick` wraps it in `MIN()` so the action has one value per mark.

Why the ticks are all empty at the start: with nothing chosen, every function is in, but none is "picked". Empty boxes read as "no choice yet", which is what the capsule's "All functions" says.

2. New sheet **Function List**:
   - Rows `function_name` (header hidden: right-click > untick **Show Header**). Columns `Tick X`; right-click the axis > Edit Axis: Fixed **0 to 10**; then untick **Show Header**.
   - Marks **Shape**, Shape `Function Shape`: assign `tick_on.png` to `tick_on` and `tick_off.png` to `tick_off` (palette Arcadia How-To). Size: one step left of the middle of the slider; keep this size on every list.
   - Label: type two spaces, then insert `function_name`: `  <function_name>`. Tableau Book 10, `#E4E9F0`; alignment left, middle. Under Label, tick **Allow labels to overlap other marks**.
   - Detail `Function Pick`, `zzTrue`, `zzFalse`.
   - Format: shading None, row and column dividers None, grid lines None, zero lines None. Fit **Entire View**. Tooltip off (Tooltip > untick **Show tooltips**).
3. On your dashboard, put **Function List** inside **Org Popover**, under the title, width 200.
4. Actions:

   | Name | Type | Source | Target | Field |
   |---|---|---|---|---|
   | Toggle function | Change Parameter | Function List | p_Functions | Function Pick (aggregation None) |
   | Deselect Function List | Filter | Function List | Function List | `zzTrue` → `zzFalse` |

**You should see** eight empty boxes, Commercial to Technology. Click People: it ticks, and Try It shows only People's four departments. Click Finance: both ticked, seven bars. Click People again: only Finance remains. Click Finance: empty again, 31 bars.

### Step 6: departments that follow their function

**Why.** When you pick People, you expect all four People departments to be in, and then you untick the one you don't want. So the department parameter stores **exclusions**: a department is in when its function is in and it isn't on the "off" list. Every department of a newly picked function starts ticked, with no extra work.

There's one catch. Say you untick Talent Acquisition, then untick People, then pick People again. You'd expect a fresh start, but `|People>Talent Acquisition|` is still in `p_DeptOff`. So a function click also cleans its own departments out of the "off" list. That's what the `>` in `Dept Key` is for: every People department starts with `|People>`, and one regular expression removes them all.

**Do.**

1. Create:

```
// DeptOff Without Function
IF REGEXP_REPLACE([p_DeptOff], "\|" + [function_name] + ">[^|]*", "") = "|" THEN ""
ELSE REGEXP_REPLACE([p_DeptOff], "\|" + [function_name] + ">[^|]*", "") END
```

```
// Function DeptOff Pick
MIN([DeptOff Without Function])
```

```
// Dept Visible
[Function In]
```

```
// Dept Ticked
MIN([Dept In])
```

```
// Dept Toggle
IF CONTAINS([p_DeptOff], "|" + [Dept Key] + "|")
THEN (IF [p_DeptOff] = "|" + [Dept Key] + "|" THEN ""
      ELSE REPLACE([p_DeptOff], "|" + [Dept Key] + "|", "|") END)
ELSE (IF [p_DeptOff] = "" THEN "|" + [Dept Key] + "|"
      ELSE [p_DeptOff] + [Dept Key] + "|" END)
END
```

```
// Dept Pick
MIN([Dept Toggle])
```

```
// Dept Shape
IF [Dept Ticked] THEN "tick_on" ELSE "tick_off" END
```

How the clean-up reads: `"\|People>[^|]*"` matches a bar, `People>`, and everything up to the next bar, which is one People department. Replacing every match with nothing leaves the bars of the other departments. If only a lone `|` is left, the result is empty.

Worked example, with `p_DeptOff` = `|People>Talent Acquisition|Finance>FP&A|`: a click on People leaves `|Finance>FP&A|`. With only `|People>Talent Acquisition|`, it leaves `|`, which becomes empty.

> **Names with special characters.** `REGEXP_REPLACE` reads `( ) [ ] . + * ? ^ $ \` as instructions. None of the Arcadia function names has them. If yours do, escape them first, for example with `REPLACE([name], ".", "\.")`.

2. Add `Function DeptOff Pick` to **Function List**'s Detail, and this action:

   | Name | Type | Source | Target | Field |
   |---|---|---|---|---|
   | Function cleans departments | Change Parameter | Function List | p_DeptOff | Function DeptOff Pick (None) |

   Both actions on Function List run on the same click.

3. New sheet **Dept List**, built like Function List:
   - Filter `Dept Visible` = True. (This filter is fine: it hides departments of unpicked functions, which is what the panel should do.)
   - Rows `Dept Key`, header hidden. Because the key starts with the function, the departments come out sorted by function, so each function's departments sit together. Columns `Tick X`, Fixed 0 to 10, hidden.

     Why not `function_name` then `department_name` as two row headers? A group with a single row loses its heading in Tableau, so in Location (Step 9), every country with one office would show a blank. One flat list, sorted by its key, avoids that everywhere.
   - Shape `Dept Shape` (`tick_on`, `tick_off`); Label `  <department_name>`; Detail `Dept Pick`, `zzTrue`, `zzFalse`.
   - Same format and tooltip-off as Function List.
4. Put **Dept List** in **Org Popover** to the right of Function List (width 420). Actions:

   | Name | Type | Source | Target | Field |
   |---|---|---|---|---|
   | Toggle department | Change Parameter | Dept List | p_DeptOff | Dept Pick (None) |
   | Deselect Dept List | Filter | Dept List | Dept List | `zzTrue` → `zzFalse` |

**You should see** all 31 departments ticked under their functions when nothing is picked. Pick People: only People's four show, all ticked. Untick Talent Acquisition: Try It shows 3 bars, 790 people. Untick People, then pick it again: all four are back. That's the clean-up.

### Step 7: the last one ticked stays

**Why.** Untick every department of a function and the page has nothing to show. Instead, the last ticked department locks: its click writes back the string as it was, so nothing changes.

**Do.**

1. Create:

```
// Dept Scope
SUM(IF [Dept In] THEN [One] END)
```

```
// Scope Total
MIN({ FIXED : SUM(IF [Dept In] THEN [One] END) })
```

```
// Dept Locked
[Dept Ticked] AND ZN([Scope Total]) - ZN([Dept Scope]) = 0
```

`Scope Total` counts everyone in scope across the whole data source (the `{ FIXED : … }` ignores the view's rows). `Dept Scope` counts the people in this department who are in scope. When the two are equal, this department holds everyone in scope, so it is the last one ticked.

2. Edit two fields:

```
// Dept Pick
IF [Dept Locked] THEN [p_DeptOff] ELSE MIN([Dept Toggle]) END
```

```
// Dept Shape
IF [Dept Ticked] THEN "tick_on" ELSE "tick_off" END
```

(`Dept Shape` stays as it is: a locked department is still ticked.)

3. Make the locked name read differently. Create:

```
// Dept Name On
IF NOT [Dept Locked] THEN MIN([department_name]) END
```

```
// Dept Name Locked
IF [Dept Locked] THEN MIN([department_name]) END
```

On **Dept List**, replace the label with two runs on one line: `  <Dept Name On><Dept Name Locked>`. Color the first run `#E4E9F0` and the second `#8FA0B8`. Only one of them has a value for any department, so each name shows once, in the right color.

**You should see** this: pick Legal & Compliance, then untick Legal. Compliance & Risk turns gray, and a click on it changes nothing. Try It still shows its 498 people.

> **Why `ZN()`?** A sum over no rows is NULL in Tableau, not 0. `ZN()` turns it into 0 so the comparison works.

### Step 8: make the capsule talk

**Why.** "All functions" should change to say what you picked, and the capsule should turn white so it's obvious a filter is on.

**Do.**

1. Create:

```
// Org Is All
[p_Functions] = "" AND [p_DeptOff] = ""
```

```
// N Functions In
{ COUNTD(IF [Function In] THEN [function_name] END) }
```

```
// One Function
{ MIN(IF [Function In] THEN [function_name] END) }
```

```
// N Functions
{ COUNTD([function_name]) }
```

```
// N Depts
{ COUNTD([department_name]) }
```

```
// N Depts In
{ COUNTD(IF [Dept In] THEN [department_name] END) }
```

```
// N Depts Offered
{ COUNTD(IF [Function In] THEN [department_name] END) }
```

The curly braces with nothing before the colon are a FIXED level of detail over the whole data source, written short. They give one number however the sheet is built.

2. Edit the two placeholders from Step 1, and add the text fields:

```
// Org Field Text
IF [p_Functions] = "" THEN "All functions"
ELSEIF [N Functions In] = 1 THEN [One Function]
ELSE STR([N Functions In]) + " functions" END
```

```
// Org Capsule Shape
IF [Org Is All] THEN "capsule_dark" ELSE "capsule_light" END
```

```
// Org Text Light
IF NOT [Org Is All] THEN [Org Field Text] END
```

```
// Org Text Dark
IF [Org Is All] THEN [Org Field Text] END
```

```
// Org Sub Text
IF [Org Is All] THEN STR([N Functions]) + " functions · " + STR([N Depts]) + " departments"
ELSE STR([N Depts In]) + " of " + STR([N Depts Offered]) + " departments" END
```

3. On **Org Field**: Shape > assign `capsule_light.png` to `capsule_light`. Replace the label with two runs: `<Org Text Light>` Tableau Semibold 9 navy `#13233A`, then `<Org Text Dark>` Tableau Medium 9 `#E4E9F0`. On the white capsule the text is dark; on the dark capsule it's light.
4. New sheet **Org Sub**: Marks Text, `<Org Sub Text>` Tableau Book 9 `#8A97A8`, left. Detail `zzTrue`, `zzFalse`; tooltip off; deselect action. Put it in the rail under Org Field, height 18.
5. Put a text object `ORGANIZATION` (Tableau Semibold 8, `#B8C4D6`) above the capsule.

**You should see**

| You pick | Capsule | Under it |
|---|---|---|
| Nothing | Dark, "All functions" | 8 functions · 31 departments |
| People | White, "People" | 4 of 4 departments |
| People, Talent Acquisition unticked | White, "People" | 3 of 4 departments |
| People and Finance | White, "2 functions" | 7 of 7 departments |

---

## Part 3: two filters that respect each other

### Step 9: your turn, Location

Build the Location filter yourself, with the same pattern one level deeper: **region > country > office**. Use the hints first; the full answer is below them, and the finished Location sheets are in the downloadable workbook (Loc Field, Region List, Country List, Office List and the rest), so you can open them and compare.

**Hints**

- Three string parameters: `p_Regions` holds picked regions; `p_CountryOff` and `p_OfficeOff` hold exclusions.
- Keys carry their parents: `[region] + ">" + [country_name]`, and `[region] + ">" + [country_name] + ">" + [office_name]`.
- A region click cleans **both** its countries and its offices; a country click cleans its offices.
- `In Scope` becomes `[Dept In] AND [Office In]`.
- The Location capsule reads `All locations`, a region, or `2 regions`; under it `5 regions · 35 offices`, or for a selection `6 countries · 8 of 9 offices`.

<details>
<summary><b>The answer: every Location field</b></summary>

Parameters: `p_Regions`, `p_CountryOff`, `p_OfficeOff`, all String, empty.

```
// Region In
[p_Regions] = "" OR CONTAINS([p_Regions], "|" + [region] + "|")

// Country Key
[region] + ">" + [country_name]

// Country In
[Region In] AND NOT CONTAINS([p_CountryOff], "|" + [Country Key] + "|")

// Office Key
[region] + ">" + [country_name] + ">" + [office_name]

// Office In
[Country In] AND NOT CONTAINS([p_OfficeOff], "|" + [Office Key] + "|")

// In Scope
[Dept In] AND [Office In]

// Region Toggle
IF CONTAINS([p_Regions], "|" + [region] + "|")
THEN (IF [p_Regions] = "|" + [region] + "|" THEN "" ELSE REPLACE([p_Regions], "|" + [region] + "|", "|") END)
ELSE (IF [p_Regions] = "" THEN "|" + [region] + "|" ELSE [p_Regions] + [region] + "|" END) END

// Region Pick
MIN([Region Toggle])

// CountryOff Without Region
IF REGEXP_REPLACE([p_CountryOff], "\|" + [region] + ">[^|]*", "") = "|" THEN ""
ELSE REGEXP_REPLACE([p_CountryOff], "\|" + [region] + ">[^|]*", "") END

// OfficeOff Without Region
IF REGEXP_REPLACE([p_OfficeOff], "\|" + [region] + ">[^|]*", "") = "|" THEN ""
ELSE REGEXP_REPLACE([p_OfficeOff], "\|" + [region] + ">[^|]*", "") END

// Region CountryOff Pick
MIN([CountryOff Without Region])

// Region OfficeOff Pick
MIN([OfficeOff Without Region])

// Region Shape
IF [p_Regions] <> "" AND MIN([Region In]) THEN "tick_on" ELSE "tick_off" END

// Country Visible
[Region In]

// Country Ticked
MIN([Country In])

// Country Toggle
IF CONTAINS([p_CountryOff], "|" + [Country Key] + "|")
THEN (IF [p_CountryOff] = "|" + [Country Key] + "|" THEN "" ELSE REPLACE([p_CountryOff], "|" + [Country Key] + "|", "|") END)
ELSE (IF [p_CountryOff] = "" THEN "|" + [Country Key] + "|" ELSE [p_CountryOff] + [Country Key] + "|" END) END

// OfficeOff Without Country
IF REGEXP_REPLACE([p_OfficeOff], "\|" + [Country Key] + ">[^|]*", "") = "|" THEN ""
ELSE REGEXP_REPLACE([p_OfficeOff], "\|" + [Country Key] + ">[^|]*", "") END

// Country Scope
SUM(IF [Dept In] AND [Office In] THEN [One] END)

// Country Locked
[Country Ticked] AND ZN([Scope Total]) - ZN([Country Scope]) = 0

// Country Pick
IF [Country Locked] THEN [p_CountryOff] ELSE MIN([Country Toggle]) END

// Country OfficeOff Pick
IF [Country Locked] THEN [p_OfficeOff] ELSE MIN([OfficeOff Without Country]) END

// Country Shape
IF [Country Ticked] THEN "tick_on" ELSE "tick_off" END

// Office Visible
[Country In]

// Office Ticked
MIN([Office In])

// Office Toggle
IF CONTAINS([p_OfficeOff], "|" + [Office Key] + "|")
THEN (IF [p_OfficeOff] = "|" + [Office Key] + "|" THEN "" ELSE REPLACE([p_OfficeOff], "|" + [Office Key] + "|", "|") END)
ELSE (IF [p_OfficeOff] = "" THEN "|" + [Office Key] + "|" ELSE [p_OfficeOff] + [Office Key] + "|" END) END

// Office Scope
SUM(IF [Dept In] AND [Office In] THEN [One] END)

// Office Locked
[Office Ticked] AND ZN([Scope Total]) - ZN([Office Scope]) = 0

// Office Pick
IF [Office Locked] THEN [p_OfficeOff] ELSE MIN([Office Toggle]) END

// Office Shape
IF [Office Ticked] THEN "tick_on" ELSE "tick_off" END

// Loc Is All
[p_Regions] = "" AND [p_CountryOff] = "" AND [p_OfficeOff] = ""

// N Regions
{ COUNTD([region]) }

// N Offices
{ COUNTD([office_name]) }

// N Regions In
{ COUNTD(IF [Region In] THEN [region] END) }

// One Region
{ MIN(IF [Region In] THEN [region] END) }

// N Countries In
{ COUNTD(IF [Country In] THEN [country_name] END) }

// N Offices In
{ COUNTD(IF [Office In] THEN [office_name] END) }

// N Offices Offered
{ COUNTD(IF [Region In] THEN [office_name] END) }

// Loc Field Text
IF [p_Regions] = "" THEN "All locations"
ELSEIF [N Regions In] = 1 THEN [One Region]
ELSE STR([N Regions In]) + " regions" END

// Loc Capsule Shape
IF [Loc Is All] THEN "capsule_dark" ELSE "capsule_light" END

// Loc Text Light
IF NOT [Loc Is All] THEN [Loc Field Text] END

// Loc Text Dark
IF [Loc Is All] THEN [Loc Field Text] END

// Loc Sub Text
IF [Loc Is All] THEN STR([N Regions]) + " regions · " + STR([N Offices]) + " offices"
ELSE STR([N Countries In]) + " countries · " + STR([N Offices In]) + " of " + STR([N Offices Offered]) + " offices" END

// Toggle Loc Panel
NOT [p_LocOpen]
```

Also edit, now that Location exists, so a lock counts only the people the page shows:

```
// Dept Scope
SUM(IF [Dept In] AND [Office In] THEN [One] END)

// Scope Total
MIN({ FIXED : SUM(IF [Dept In] AND [Office In] THEN [One] END) })
```

Sheets: **Loc Field**, **Loc Sub**, **Loc Close**, **Region List** (Rows `region`), **Country List** (Filter `Country Visible` = True; Rows `Country Key`, header hidden; label `  <country_name>`), **Office List** (Filter `Office Visible` = True; Rows `Office Key`, header hidden; label `  <ATTR(country_name)> · <office_name>`, the country in `#8FA0B8`), each built like its Organization twin. Locked names use the two-run label of Step 7.

Popover **Loc Popover**: floating at x 216, y 130, w 640, h 720, visibility `p_LocOpen`; Region List 160, Country List 200, Office List 240.

Actions (plus a deselect on every one of these sheets):

| Name | Source | Target | Field |
|---|---|---|---|
| Open loc popover | Loc Field | p_LocOpen | Toggle Loc Panel |
| Loc closes Org | Loc Field | p_OrgOpen | Close Panel |
| Loc popover on ✕ | Loc Close | p_LocOpen | Close Panel |
| Toggle region | Region List | p_Regions | Region Pick |
| Region cleans countries | Region List | p_CountryOff | Region CountryOff Pick |
| Region cleans offices | Region List | p_OfficeOff | Region OfficeOff Pick |
| Toggle country | Country List | p_CountryOff | Country Pick |
| Country cleans offices | Country List | p_OfficeOff | Country OfficeOff Pick |
| Toggle office | Office List | p_OfficeOff | Office Pick |

</details>

**You should see**

| You pick | Capsule | Under it | Try It total |
|---|---|---|---|
| Nothing | Dark, "All locations" | 5 regions · 35 offices | 30,005 |
| Asia Pacific | White, "Asia Pacific" | 6 countries · 9 of 9 offices | 9,005 |
| Asia Pacific, Pune unticked | White, "Asia Pacific" | 6 countries · 8 of 9 offices | 8,527 |
| That, plus People without Talent Acquisition | | | 143 |

To read the total on Try It, turn on **Analysis > Totals > Show Column Grand Totals**.

### Step 10: gray out what's empty

**Why.** Pick Middle East & Africa and untick South Africa, so only Dubai is left. Then open Organization: Analytics Engineering and People Analytics have nobody in Dubai. Ticking them would show nothing, so they should look disabled and do nothing when clicked. The same goes the other way: pick Finance, then open Location, and Portugal has no Finance employees.

The test is the same everywhere: does anybody pass **the other filter**? A department looks at the location filter; a country or office looks at the organization filter.

**Do.**

1. Create:

```
// Function Dim
ZN(SUM(IF [Office In] THEN [One] END)) = 0
```

```
// Dept Dim
ZN(SUM(IF [Office In] THEN [One] END)) = 0
```

```
// Region Dim
ZN(SUM(IF [Dept In] THEN [One] END)) = 0
```

```
// Country Dim
ZN(SUM(IF [Dept In] THEN [One] END)) = 0
```

```
// Office Dim
ZN(SUM(IF [Dept In] THEN [One] END)) = 0
```

2. Edit every **Pick** so a dimmed option writes back the string unchanged:

```
// Function Pick
IF [Function Dim] THEN [p_Functions] ELSE MIN([Function Toggle]) END

// Function DeptOff Pick
IF [Function Dim] THEN [p_DeptOff] ELSE MIN([DeptOff Without Function]) END

// Dept Pick
IF [Dept Locked] OR [Dept Dim] THEN [p_DeptOff] ELSE MIN([Dept Toggle]) END

// Region Pick
IF [Region Dim] THEN [p_Regions] ELSE MIN([Region Toggle]) END

// Region CountryOff Pick
IF [Region Dim] THEN [p_CountryOff] ELSE MIN([CountryOff Without Region]) END

// Region OfficeOff Pick
IF [Region Dim] THEN [p_OfficeOff] ELSE MIN([OfficeOff Without Region]) END

// Country Pick
IF [Country Locked] OR [Country Dim] THEN [p_CountryOff] ELSE MIN([Country Toggle]) END

// Country OfficeOff Pick
IF [Country Locked] OR [Country Dim] THEN [p_OfficeOff] ELSE MIN([OfficeOff Without Country]) END

// Office Pick
IF [Office Locked] OR [Office Dim] THEN [p_OfficeOff] ELSE MIN([Office Toggle]) END
```

3. Give each list a third label run for dimmed names, color `#4F6178`, and drop the dimmed name from the other runs. For departments:

```
// Dept Name On
IF NOT [Dept Locked] AND NOT [Dept Dim] THEN MIN([department_name]) END

// Dept Name Locked
IF [Dept Locked] AND NOT [Dept Dim] THEN MIN([department_name]) END

// Dept Name Dim
IF [Dept Dim] THEN MIN([department_name]) END
```

Label: `  <Dept Name On><Dept Name Locked><Dept Name Dim>`, colors `#E4E9F0`, `#8FA0B8`, `#4F6178`. Do the same for functions (On and Dim), regions, countries and offices.

4. Dimmed boxes: the tick shape stays as it is (an empty box), and the name's dark color does the talking. No new image is needed.

**You should see**

| You pick | Open | Grayed |
|---|---|---|
| Location > Middle East & Africa, South Africa unticked (282 people, all in Dubai) | Organization | Analytics Engineering and People Analytics |
| Organization > Finance | Location > Europe | Portugal and its office, Lisbon |
| Organization > Legal & Compliance | Location | South Korea and its office, Seoul |

Click a grayed name: nothing changes.

---

## Bonus: reset to default view

One button that empties every string parameter and closes every panel.

1. Create:

```
// Empty Text
""
```

```
// Reset Shape
"reset_button"
```

2. New sheet **Reset**: Marks Shape, Shape `Reset Shape` (assign `reset_button.png` to `reset_button`). Detail `Empty Text`, `Close Panel`, `zzTrue`, `zzFalse`. Tooltip `Reset to default view`, command buttons off. Put it in the rail under the Location capsule, height 32.
3. Actions, all from **Reset**, run on Select:

   | Target | Field |
   |---|---|
   | p_Functions, p_DeptOff, p_Regions, p_CountryOff, p_OfficeOff (five actions) | Empty Text |
   | p_OrgOpen, p_LocOpen (two actions) | Close Panel |

   Plus the deselect action.

**You should see** every list back to the start, both capsules dark, both panels closed, and Try It at 30,005.

---

## 5. Put the page together

The finished dashboard, **Multi-select filters**, Fixed 1400 × 850, shading `#F3F3EF`, every item floating:

| Item | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Rail (vertical container) | 0 | 0 | 216 | 850 | Navy `#13233A`, padding 8 left and right |
| Page title (text) | 240 | 16 | 1136 | 56 | "Who works where" Tableau Bold 18 navy, then a line on what the page shows |
| Try It | 240 | 88 | 1136 | 724 | Title hidden |
| Footnote (text) | 240 | 826 | 1136 | 16 | "Arcadia Systems is fictional; all data is synthetic." Book 9 `#5A6170` |
| Org Popover | 216 | 140 | 640 | 700 | Visibility `p_OrgOpen` |
| Loc Popover | 216 | 130 | 640 | 720 | Visibility `p_LocOpen` |

Inside the rail, top to bottom: blank 24 · `arcadia_logo_reverse.png` 200 × 40 · blank 28 · ORGANIZATION 18 · blank 6 · Org Field 32 · Org Sub 18 · blank 24 · LOCATION 18 · blank 6 · Loc Field 32 · Loc Sub 18 · `rail_divider.png` 24 · Reset 32 · flexible blank.

Inside each popover, top to bottom: the title row 44 (title and ✕) · `popover_line.png` 9 · the lists · a footer text 30, Book 9 `#8FA0B8`: "Pick functions; every department starts ticked. The last one ticked can't be unticked; a grayed one has nobody in the chosen locations."

The popovers sit in front of everything; the rail in front of the page.

---

## 6. Checks

Run these in Presentation mode, then again after publishing.

| # | Do | Expect |
|---:|---|---|
| 1 | Nothing | Both capsules dark; "8 functions · 31 departments", "5 regions · 35 offices"; 30,005 |
| 2 | Click every capsule, list row, ✕ and Reset | Nothing stays highlighted |
| 3 | Open Organization, then Location | One panel open at a time |
| 4 | People | "People", "4 of 4 departments"; HR Business Partners 389, Talent Acquisition 388, Total Rewards 221, People Analytics 180 |
| 5 | Untick Talent Acquisition | "3 of 4 departments"; 790 |
| 6 | Untick People, pick it again | All four ticked: the clean-up worked |
| 7 | Legal & Compliance only, untick Legal | Compliance & Risk gray; a click changes nothing; 498 |
| 8 | Reset, then Asia Pacific, untick Pune | "6 countries · 8 of 9 offices"; 8,527 |
| 9 | Add People without Talent Acquisition | 143 |
| 10 | Reset, Middle East & Africa, untick South Africa, open Organization | 282; Analytics Engineering and People Analytics grayed |
| 11 | Reset, Finance, then Location > Europe | Portugal and Lisbon grayed |
| 12 | Reset | Everything as in check 1 |

---

## 7. Why it works this way

- **Why not a regular multi-select filter?** A Tableau filter can't tick its children for you, lock its last option, or gray out options because of another filter's state. It also draws its own control, which can't look like a rail capsule. Parameters plus calculations give you all of that, at the cost of more fields.
- **Why exclusions for children?** Because "everything under a picked parent" is the default you want. Storing exclusions makes the default free and the clean-up one regular expression.
- **Why no context filters?** The lists need to see every option, so the scope tests live inside the formulas (`IF [Office In] THEN …`) rather than as filters. A `FIXED` level of detail runs before ordinary filters, so with the tests inside the formula there is no filter order to remember.
- **Why `MIN()` around the toggles?** A Change Parameter action reads one value per mark. `MIN()` makes the toggle an aggregate, so each mark (one per name) carries exactly one string.
- **Why the deselect trick?** A click on an already-selected mark only unselects it. Clearing the selection right away means every click runs its action.

---

## Files in this folder

| Path | What it is |
|---|---|
| `data/arcadia_employees.csv` | The data: 30,005 rows, one per employee, on Jun 30, 2026 |
| `data/build_arcadia_employees.py` | How the file was made from the Arcadia warehouse (for transparency; you don't need it) |
| `shapes/arcadia_how_to_shapes.zip` | The eight images, in a folder ready for `My Tableau Repository/Shapes/` |
| `shapes/*.png` | The same images, one by one |

### The data, column by column

| Column | Example | Notes |
|---|---|---|
| `employee_id` | W112875 | One row per employee |
| `as_of_date` | 2026-06-30 | The same date on every row |
| `function_name` | Commercial | 8 functions |
| `sub_function` | Client Services | 10 sub-functions |
| `department_name` | Client Success | 31 departments |
| `region` | Asia Pacific | 5 regions |
| `country_name` | Australia | 22 countries |
| `office_name` | Melbourne | 35 offices |
| `job_level` | L5 | L1 to L10 |
| `level_band` | L5–L6 Manager | 4 bands |
| `career_track` | People Manager | Individual Contributor, People Manager, People Leader |
| `job_family` | Client Success | |
| `hire_date` | 2021-01-25 | Original hire date |

Executive officers are excluded, as on every Arcadia dashboard. Someone whose last day is Jun 30, 2026 still counts on that day.
