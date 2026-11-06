# How-To #3: card zoom, from expand-and-close to grow in any direction

Build a 2 × 2 grid of dashboard cards that zoom. In **Level 1**, each card has one button: click it and the card fills the whole area, click it again and the grid comes back. In **Level 2**, each card can also grow **wide** into its neighbor, **tall** into the card above or below, or **full**, and rows and columns combine freely: 21 layouts from four cards. Every step is a parameter, a calculation, a container or a click in Tableau. There is no SQL and no extension.

**Who it's for:** anyone, including people opening Tableau for the first time. Section 0.5 explains the six moves you'll repeat all through the lesson (make a calculation, make a parameter, put a field on a shelf, filter, add a container, add an action), and every step says exactly where to click.

**What you need:** Tableau Desktop or Tableau Public (the free app), version 2022.3 or later (for showing and hiding containers with a parameter). Plan on about an hour for Level 1 and another for Level 2.

**How the lesson works.** Each step builds one worksheet or one piece of a dashboard. The downloadable workbook on Tableau Public has a sheet per step, named **Step 1 · Icons** to **Step 17 · Test**; each sheet's caption (on its left) holds that step's instructions and every formula to paste. Steps that happen on a dashboard (containers, visibility, actions) have a sheet too, so their instructions sit in a caption like the rest. The workbook has two dashboards: **Level 1 · Expand and close** first, then **Level 2 · Grow in any direction**. Follow this page, the workbook, or both side by side.

**Credit.** Level 1 is the recipe from Jan Kaiser's [Dynamic Zone Zooming in 7 Steps](https://www.thedataschool.de/jan-kaiser/dynamic-zone-zooming-in-7-steps/) (The Data School), from an idea by Samuel Parsons, rebuilt here on Arcadia data with every step explained. Level 2 extends it.

**What you'll learn**

| Steps | Technique | Used for |
|---|---|---|
| 1 | Custom shapes, and a "menu field" that gives a sheet one mark per value | Checking the six icons before you need them |
| 3 | True/False parameters as switches | One switch per card and per row |
| 4 | Calculations that read only parameters | "Are the other cards showing?" and "Are they hidden?" |
| 5–6 | Two button sheets in one slot, each with a mark in one state only | An expand icon that turns into a close icon |
| 7 | Tiled containers, rows inside a column | Room that a hidden card gives to the others |
| 8 | Control visibility using value | Hiding a card, or a whole row, with a parameter |
| 9 | Parameter actions that write a calculation's value | One click that toggles |
| 10 | Reset, and the deselect trick | One click back to the grid; buttons that never stay highlighted |
| 11 | Two container trees in one space | Wide needs rows, tall needs columns |
| 12 | Text parameters that remember an "owner" | Five values that describe 21 layouts |
| 13–15 | Three buttons on one sheet, five actions per click | Wide, tall and full on every card |
| 16–17 | Reset, and a walk through every layout | Checking the whole thing works |

Arcadia Systems is a fictional company. All data is synthetic.

---

## Contents

- [0. Get ready](#0-get-ready)
- [Part 1: the pieces](#part-1-the-pieces)
   - [Step 1: the icons](#step-1-the-icons)
   - [Step 2: the four cards](#step-2-the-four-cards)
- [Part 2: Level 1, expand and close](#part-2-level-1-expand-and-close)
   - [Step 3: six switches](#step-3-six-switches)
   - [Step 4: eight calculations](#step-4-eight-calculations)
   - [Step 5: the Open buttons](#step-5-the-open-buttons)
   - [Step 6: the Close buttons](#step-6-the-close-buttons)
   - [Step 7: the layout](#step-7-the-layout)
   - [Step 8: control visibility](#step-8-control-visibility)
   - [Step 9: sixteen parameter actions](#step-9-sixteen-parameter-actions)
   - [Step 10: reset, and test every card](#step-10-reset-and-test-every-card)
- [Part 3: Level 2, grow in any direction](#part-3-level-2-grow-in-any-direction)
   - [Step 11: two trees in one space](#step-11-two-trees-in-one-space)
   - [Step 12: five owners, twelve visibility calculations](#step-12-five-owners-twelve-visibility-calculations)
   - [Step 13: three buttons on one sheet](#step-13-three-buttons-on-one-sheet)
   - [Step 14: five actions for one card](#step-14-five-actions-for-one-card)
   - [Step 15: the other seven button sheets](#step-15-the-other-seven-button-sheets)
   - [Step 16: reset Level 2](#step-16-reset-level-2)
   - [Step 17: test all 21 layouts](#step-17-test-all-21-layouts)
- [Use it on your own data](#use-it-on-your-own-data)
- [Checks](#checks)
- [Why it works this way](#why-it-works-this-way)

---

## 0. Get ready

### 0.1 Download the files

Download **[card-zoom-files.zip](https://github.com/thialp/tableau-how-to/raw/main/03-card-zoom/card-zoom-files.zip)** and unzip it (double-click it on a Mac; on Windows right-click > **Extract All**). You get:

- `arcadia_employees.csv`: one row per employee on Jun 30, 2026 (30,005 people, executive officers excluded), the same file as How-To #1;
- a folder **Arcadia How-To** with the images, including the six buttons this lesson uses.

### 0.2 Install the shapes

Tableau looks for custom shapes in one place on your computer. Move the folder **Arcadia How-To** into:

- Windows: `Documents\My Tableau Repository\Shapes\`
- Mac: `Documents/My Tableau Repository/Shapes/`

If you did How-To #1 or #2, replace the old folder: this one holds all their images plus six new ones.

| File | Size (px) | What it draws |
|---|---|---|
| `icon_expand.png` | 48 × 48 | Expand: two arrows pointing out |
| `icon_close.png` | 48 × 48 | Close: × |
| `icon_right.png` | 48 × 48 | → (Level 2: grow right) |
| `icon_left.png` | 48 × 48 | ← (Level 2: grow left) |
| `icon_up.png` | 48 × 48 | ↑ (Level 2: grow up) |
| `icon_down.png` | 48 × 48 | ↓ (Level 2: grow down) |
| `reset_button.png` | 600 × 96 | "Reset to default view" (Steps 10 and 16) |

The icons are drawn at twice their on-screen size (24 × 24), so they stay sharp on high-resolution screens. If Tableau was open, close it and open it again, so it sees the new folder.

### 0.3 Connect the data

1. Open Tableau. On the start page, under **Connect > To a File**, click **Text file**, and pick `arcadia_employees.csv`.
2. Tableau shows the Data Source page with a preview of the rows. At the bottom left, click **Sheet 1**.
3. **File > Save As**, and name it `Card zoom.twbx` (Tableau Public saves to your profile instead; that's fine).

**You should see** the **Data pane** on the left of Sheet 1, listing 13 fields such as `Department Name` and `Level Band`, plus `arcadia_employees.csv (Count)` at the bottom.

### 0.4 One helper field

```
// Employees
COUNT([employee_id])
```

It counts employees: one row per person, so counting the IDs counts the people. Section 0.5 shows how to create it.

### 0.5 The six moves you'll repeat

**Make a calculated field.** Every formula box in this guide starts with a `//` line: that's the field's name.

1. Top menu **Analysis > Create Calculated Field**.
2. In the box at the top of the window (it says "Calculation1"), type the name from the `//` line, for example `Employees`.
3. Click in the big box below, delete anything there, and paste the formula: everything after the `//` line. (Pasting the `//` line too is harmless: Tableau treats it as a comment.)
4. Check the message at the bottom: **The calculation is valid.** If it says something else, a name is misspelled: field names in square brackets must match exactly, capitals and spaces included.
5. Click **OK**. The new field appears in the Data pane.

**Make a parameter.** A parameter is a value you can change on the page, like a switch or a setting.

1. In the Data pane, click the small arrow (▾) at the top right, next to the search box, and pick **Create Parameter**.
2. Type the **Name**, choose the **Data type**, set the **Current value**, and for a list of values pick **Allowable values: List** and type each value on its own line.
3. Click **OK**. Parameters show at the bottom of the Data pane, under **Parameters**.

To see and change a parameter while you build, right-click it in the Data pane > **Show Parameter**: a small control appears on the right of the sheet.

**Put a field on a shelf or the Marks card.** Drag the field from the Data pane and drop it on the target: **Columns** and **Rows** are the long shelves at the top of the sheet; **Filters** is the box on the left; the **Marks card** below it has squares named **Color**, **Size**, **Label**, **Detail**, **Tooltip** and **Shape**. The dropdown at the top of the Marks card (it starts as **Automatic**) sets the mark type: **Bar**, **Text**, **Shape** and so on. Dropping a field on **Detail** puts it in the view without drawing anything: that's how a click can carry a value without showing it.

**Filter to one value.** Drag the field to **Filters**. A window opens with a list of the field's values: tick only the ones to keep, then **OK**. For a True/False field, keep **True** or **False**.

**Add a container on a dashboard.** On a dashboard, the left panel has an **Objects** list: **Horizontal**, **Vertical**, **Text**, **Image** and so on. Drag **Horizontal** or **Vertical** onto the dashboard to add a container: an empty box that lays out whatever you drop inside it side by side (horizontal) or one under the other (vertical). Switch the left panel to **Layout** to see the **Item hierarchy**, a tree of everything on the dashboard; that's the easiest place to select a container and to rename it (double-click its name).

**Add a parameter action.** Top menu **Dashboard > Actions** (on a worksheet, **Worksheet > Actions**). Click **Add Action** > **Change Parameter**. A window opens: give it a name, tick the source sheets, pick what triggers it (**Select** means a click), pick the **Target Parameter** and the **Source Field** whose value it writes. Click **OK**, then **OK** again to close the list of actions.

---

## Part 1: the pieces

### Step 1: the icons

**Why.** The buttons in this lesson are pictures, and a picture only shows if Tableau finds it in your Shapes folder. Before anything else, put all six on one sheet: if one is missing, you'll know now, not in the middle of Step 5.

A sheet draws one mark per value of the fields in the view. There's no column that holds "expand, close, right…", so you make one: a **menu field** that relabels six values of a column you already have. Job levels L1 to L6 are just a convenient list of six.

```
// Icon Name
CASE [job_level]
WHEN "L1" THEN "icon_expand"
WHEN "L2" THEN "icon_close"
WHEN "L3" THEN "icon_right"
WHEN "L4" THEN "icon_left"
WHEN "L5" THEN "icon_up"
WHEN "L6" THEN "icon_down"
END
```

How to read it: `CASE` looks at the job level of each row; when it's "L1" the result is "icon_expand", and so on. Levels L7 to L10 match no line, so they get no value at all, which Tableau calls **Null**.

1. Rename Sheet 1: double-click its tab at the bottom and type **Step 1 · Icons**.
2. Create the calculated field `Icon Name` (section 0.5).
3. Drag `Icon Name` to **Columns**. You get seven columns: six icon names and one called **Null**.
4. Drag `Icon Name` to **Filters**. In the list, untick **Null** and click **OK**. Six columns are left.
5. On the Marks card, change **Automatic** to **Shape**. Drag `Icon Name` from the Data pane onto the **Shape** square.
6. Click the **Shape** square. In the window, open **Select Shape Palette** and pick **Arcadia How-To**. Then, on the left, click `icon_expand` and click the matching picture on the right; do the same for the other five. Click **OK**.
7. Click the **Size** square and drag the slider to about the middle.

**You should see** six icons in a row: expand, ×, →, ←, ↑, ↓, each on a light rounded square. If a value shows a plain circle or square instead, its picture wasn't found: check the folder name and restart Tableau.

---

### Step 2: the four cards

**Why.** The lesson is about the zoom, not the charts, so the four cards come ready-made in the downloadable workbook. If you're building from scratch, make them now: four simple sheets, one per corner of the grid. **TL, TR, BL and BR** stand for top left, top right, bottom left and bottom right; you'll meet these four letters in every name from here on.

For the hire-year card, make one calculation first:

```
// Hire Year
YEAR([hire_date])
```

`YEAR()` takes a date and keeps only its year. Right-click `Hire Year` in the Data pane > **Convert to Discrete**, so each year becomes its own column instead of a number axis.

Make each card on a new sheet (the **New Worksheet** icon at the bottom, right of the tabs), and name the tab as in the table:

| Sheet | Rows | Columns | Mark | Sort |
|---|---|---|---|---|
| **TL · Departments** | `department_name` | `Employees` | Bar | Descending by `Employees` |
| **TR · Hire years** | `Employees` | `Hire Year` | Bar | By year |
| **BL · Level mix** | `level_band` | `Employees` | Bar | By band, L1–L2 to L7+ |
| **BR · Countries** | | | Map | |

- For the **sort** on TL: click the department header, then the **Sort descending** button in the toolbar (bars from longest to shortest).
- For **BR · Countries**: double-click `country_name` in the Data pane. Tableau knows these are countries and draws a map. On the Marks card pick **Map**, then drag `Employees` to **Color**: darker countries have more people.
- On every card: drag `Employees` to **Label** so each bar shows its number; right-click each axis > untick **Show Header** to hide it; **Format > Lines** > Grid Lines: **None**.
- Tooltip (the box that appears when you hover a mark): click **Tooltip** on the Marks card and write the name in bold on the first line and "<Employees> employees" below. Untick **Include command buttons** at the bottom.

The cards are deliberately plain; the point is how they move.

**You should see**

| Card | Shows | Check |
|---|---|---|
| TL | 31 bars | Core Platform Engineering is the largest, 2,566 |
| TR | One bar per hire year, 2001 to 2026 | 2025 is the tallest, 4,049. 2001 holds the founding group (197). 2026 is a half year: 2,517 up to Jun 30 |
| BL | 4 bars | L3–L4 Senior 12,778, L5–L6 Manager 9,511, L1–L2 Associate 7,302, L7+ 414 |
| BR | 22 countries | United States 9,362, India 6,967 |

TR counts **today's** employees by the year they joined, not everyone ever hired: people who joined in 2005 and left are not in the file.

---

## Part 2: Level 1, expand and close

The goal: each card gets one button in its top-right corner. In the grid it shows **expand**. Click it, and the other three cards disappear so the card fills the area, and the button turns into **×**. Click × and the grid comes back.

You'll build it in this order, for all four cards at once:

1. the **switches** (parameters) that say what's visible;
2. the **calculations** that read the switches;
3. the **button sheets**;
4. on the dashboard: the **containers**, their **visibility**, and the **actions** that flip the switches.

### Step 3: six switches

**Why.** A dashboard container can be shown or hidden by a True/False parameter. So each card gets a parameter that means "show me". Hiding a card isn't quite enough, though: when you hide both cards of the bottom row, the row's empty height stays on the page. So each row gets a parameter too. Four cards plus two rows: six switches, all True at the start, which is the grid.

Create six parameters (section 0.5), all with:

- **Data type:** Boolean (that's Tableau's word for True/False)
- **Current value:** True
- Leave the aliases as they are

| Parameter name | What it shows |
|---|---|
| `Show TL` | The top-left card |
| `Show TR` | The top-right card |
| `Show BL` | The bottom-left card |
| `Show BR` | The bottom-right card |
| `Show Top Row` | The row holding TL and TR |
| `Show Bottom Row` | The row holding BL and BR |

To watch them while you build, make a sheet that prints them. Create this calculated field:

```
// Switches Now
"TL " + STR([Show TL]) + " · TR " + STR([Show TR]) + " · BL " + STR([Show BL]) + " · BR " + STR([Show BR])
+ " · Top row " + STR([Show Top Row]) + " · Bottom row " + STR([Show Bottom Row])
```

How to read it: text in quotes is printed as it is; `STR()` turns True or False into text; `+` glues the pieces together.

1. New worksheet, named **Step 3 · Switches**.
2. Marks card: **Text**. Drag `Switches Now` to **Text**.
3. In the Data pane, right-click each of the six parameters > **Show Parameter**.

**You should see** "TL True · TR True · BL True · BR True · Top row True · Bottom row True". In the `Show BL` control on the right, pick False: the line follows. Set it back to True.

---

### Step 4: eight calculations

**Why.** Each card's button has to answer two questions, and each answer is a calculation that reads only the switches.

- **Which icon should I show?** In the grid, the other three cards are showing, so show **expand**. When the other three are hidden, this card is the one zoomed, so show **×**. That's the **Button Filter**: True means "the others are showing".
- **What should a click write?** In the grid, a click must hide the others, so it writes False. Zoomed, a click must bring them back, so it writes True. That's exactly the answer to "are the others hidden?": False in the grid, True when zoomed. That's the **Button Switch**, and the actions in Step 9 write its value straight into the other cards' switches.

So one click toggles, with no IF anywhere: the value to write is always the opposite of the current state, and the Switch already is that opposite.

Create the eight calculated fields in this order. Each card looks at the **other three** cards. `AND` means "all of these are true"; `NOT` flips True into False and False into True.

```
// TL Button Filter
[Show TR] AND [Show BL] AND [Show BR]
```

```
// TL Button Switch
NOT [Show TR] AND NOT [Show BL] AND NOT [Show BR]
```

```
// TR Button Filter
[Show TL] AND [Show BL] AND [Show BR]
```

```
// TR Button Switch
NOT [Show TL] AND NOT [Show BL] AND NOT [Show BR]
```

```
// BL Button Filter
[Show TL] AND [Show TR] AND [Show BR]
```

```
// BL Button Switch
NOT [Show TL] AND NOT [Show TR] AND NOT [Show BR]
```

```
// BR Button Filter
[Show TL] AND [Show TR] AND [Show BL]
```

```
// BR Button Switch
NOT [Show TL] AND NOT [Show TR] AND NOT [Show BL]
```

Notice what's missing: a card never looks at its own switch. While TL is zoomed, `Show TL` stays True; only the others change.

Watch them too:

```
// Buttons Now
"TL " + IIF([TL Button Filter], "expand", IIF([TL Button Switch], "×", "–"))
+ " · TR " + IIF([TR Button Filter], "expand", IIF([TR Button Switch], "×", "–"))
+ " · BL " + IIF([BL Button Filter], "expand", IIF([BL Button Switch], "×", "–"))
+ " · BR " + IIF([BR Button Filter], "expand", IIF([BR Button Switch], "×", "–"))
```

How to read it: `IIF(test, a, b)` gives a when the test is true and b when it's false. So for each card: "expand" if its Filter is True, otherwise "×" if its Switch is True, otherwise "–" (hidden, no button).

New worksheet **Step 4 · Buttons Now**: Marks card **Text**, drag `Buttons Now` to **Text**.

**You should see** "TL expand · TR expand · BL expand · BR expand": the grid. Now play TL's click by hand: with the parameter controls (Step 3), set `Show TR`, `Show BL` and `Show BR` to False. The line reads "TL × · TR – · BL – · BR –": TL shows ×, and the other three show nothing at all, because they're hidden. Set the three back to True.

---

### Step 5: the Open buttons

**Why.** A button is a sheet with one mark: give the mark a picture and a click action, and it looks and works like a button. Each card needs two pictures, expand and ×, so it gets two sheets in the same spot: an **Open** sheet that has its mark only when the Filter is True, and a **Close** sheet that has its mark only when the Filter is False. At any moment one of them is empty, and an empty sheet takes no room.

**TL Open**, a new worksheet (in the downloaded workbook its tab reads **Step 5 · TL Open**):

1. Drag `TL Button Filter` to **Filters**, keep **True** only, **OK**. The sheet has one mark when the other three cards are showing, and none otherwise.
2. Marks card: change **Automatic** to **Shape**. Drag `TL Button Filter` onto the **Shape** square too.
3. Click **Shape** > **Select Shape Palette: Arcadia How-To**. Click **True** on the left and pick `icon_expand`; click **False** and pick `icon_close`. **OK**. Only True shows on this sheet; False is for Step 6. Tableau remembers a field's shapes for every sheet, so TL's Close sheet will get the × by itself.
4. Drag `TL Button Switch` onto the **Detail** square. Nothing changes on screen: Detail only carries the value, which is what the click will write in Step 9.
5. Click **Size** and set it so the icon is small, about a quarter of the slider (it will sit in a 32 × 32 slot).
6. Click **Tooltip** and type "Expand this card"; untick **Include command buttons**; **OK**.

Then the other three:

1. Right-click the **TL Open** tab > **Duplicate**. Rename the copy **TR Open**.
2. Swap each TL field for its TR twin: drag `TR Button Filter` from the Data pane and drop it **exactly on top of** the `TL Button Filter` pill in Filters (Tableau replaces it and asks which values to keep: **True**). Do the same on the Shape square, then assign the same two icons (True = expand, False = ×). Drop `TR Button Switch` on top of `TL Button Switch` on Detail.
3. Repeat for **BL Open** and **BR Open**.

**You should see** on each of the four Open sheets one expand icon. Set `Show BR` to False: TL, TR and BL Open go empty (their "others" aren't all showing any more), while BR Open still shows expand, since BR's others are all showing. Set it back to True.

---

### Step 6: the Close buttons

**Why.** The mirror of Step 5: the × sheet, with a mark only when the card is zoomed.

1. Right-click the **TL Open** tab > **Duplicate**, and rename the copy **TL Close** (its tab in the downloaded workbook reads **Step 6 · TL Close**).
2. In Filters, click the arrow on the `TL Button Filter` pill > **Edit Filter**, untick True, tick **False**, **OK**. The shape follows by itself: False is ×.
3. Tooltip: "Back to the grid".
4. Do the same for **TR Close**, **BL Close** and **BR Close**, duplicating each card's own Open sheet.

Why two sheets instead of one sheet whose shape changes? Because a clicked mark normally stays **selected** (highlighted), and a second click on a selected mark only unselects it instead of running the action. Here, after a click the sheet you clicked goes empty (the Filter flips), and the other one appears with a fresh mark. A selection on a mark that's gone can't block the next click, so **these buttons need no deselect trick**. You'll need one in Level 2, where a button sheet keeps its marks.

**You should see** the four Close sheets empty in the grid. Set `Show TR`, `Show BL` and `Show BR` to False: TL Close shows ×, and TL Open is empty. Set them back to True.

---

### Step 7: the layout

**Why.** Hiding works only if the space is handed over: in a **tiled** container, when one item hides, the others grow to fill the room. So the cards sit in containers inside containers: a column of two rows, and each row holds two cards.

Create a dashboard: the **New Dashboard** icon at the bottom (the second of the three icons right of the tabs). Name its tab **Level 1 · Expand and close**. On the left, under **Size**, pick **Fixed size** and type 1400 × 850.

Build the containers, all **tiled** (the default; the **Tiled / Floating** switch sits under the Objects list):

1. Drag a **Vertical** container onto the empty dashboard. In the Item hierarchy (left panel, **Layout** tab), double-click its name and call it **Cards**.
2. Drag a **Horizontal** container *into* Cards, then a second Horizontal *below* the first (a dark line shows where it will land). Name them **Top Row** and **Bottom Row**.
3. Drag a **Vertical** container into Top Row, and a second one to its right. Name them **TL Card** and **TR Card**. Do the same in Bottom Row: **BL Card** and **BR Card**.
4. Inside each card container, from top to bottom:
   - a **Horizontal** container for the title row. Select it, and in the Layout tab set its **Height** (under Size) to 40 px and tick **Fixed**. Inside it, a **Text** object with the card's title (for example "Employees by department"), then drag the card's **Open** sheet and **Close** sheet from the Sheets list to its right end; give each a fixed width of 32 px.
   - the card's sheet (**TL · Departments** in TL Card, and so on), dropped under the title row.
5. On every worksheet on the dashboard: click it, open its menu (the small arrow at its top right) > **Hide Title**.
6. Check the names in the Item hierarchy: Cards, Top Row, Bottom Row, TL Card, TR Card, BL Card, BR Card. The next step picks containers by name.

Select **Cards** and each of the two rows, open the container's menu (the small arrow at its top right) and pick **Distribute Contents Evenly**, so the grid splits into equal halves. Leave it off on the four card containers and on the title rows: their items are sized by hand (a 40 px title row, then the chart), and an evenly split card would give the title half the height.

**You should see** the four cards in a 2 × 2 grid, each with its title and an expand icon at the top right. Nothing happens on a click yet.

---

### Step 8: control visibility

**Why.** This is where the switches meet the containers. Since Tableau 2022.3, any dashboard item can be shown or hidden by a True/False parameter or calculation: True shows it, False hides it.

For each of the six containers below:

1. Click it in the Item hierarchy (Layout tab), so it's selected on the dashboard.
2. In the Layout tab, under **Visibility**, tick **Control visibility using value**.
3. In the dropdown under it, open **Parameters** and pick the parameter in the table.

| Container | Value |
|---|---|
| TL Card | `Show TL` |
| TR Card | `Show TR` |
| BL Card | `Show BL` |
| BR Card | `Show BR` |
| Top Row | `Show Top Row` |
| Bottom Row | `Show Bottom Row` |

Put the visibility on the **containers**, not on the sheets: a container hides the card's title row, its buttons and its chart together.

Test before any button works: go to **Step 3 · Switches**, change values in its parameter controls, and come back to the dashboard to see the result.

**You should see**

| Set to False | The dashboard |
|---|---|
| `Show BL` | BR grows to the full width of the bottom row |
| `Show BL` and `Show BR` | An empty bottom row: its height stays on the page |
| `Show BL`, `Show BR` and `Show Bottom Row` | The top row fills the area |
| `Show TR`, `Show BL`, `Show BR`, `Show Bottom Row` | TL alone, full size, with × at its top right |

The second row of that table is why rows have switches of their own. Set everything back to True.

---

### Step 9: sixteen parameter actions

**Why.** A click on TL's button must write TL's Switch into the other three cards' switches, and into the other row's switch: four writes. A parameter action writes one parameter, so TL needs four actions, and the four cards need sixteen. They all run on **Select**, which in Tableau means "on click".

On the dashboard, top menu **Dashboard > Actions > Add Action > Change Parameter**. For TL's first action, fill the window like this:

- **Name:** TL → Show TR
- **Source Sheets:** the dropdown shows the dashboard's name; under it, untick everything, then tick **TL Open** and **TL Close** only.
- **Run action on:** Select
- **Target Parameter:** `Show TR`
- **Source Field:** `TL Button Switch` (it may show as ATTR(TL Button Switch); that's fine, the sheet has one mark).
- **Aggregation:** None
- **Clearing the selection will:** Keep current value

Click **OK**. Then **Add Action** again for the next one. The sixteen, card by card (each card's two button sheets are the source of its own four actions):

| Card | Source sheets | Source field | Target parameters (one action each) |
|---|---|---|---|
| TL | TL Open, TL Close | `TL Button Switch` | `Show TR`, `Show BL`, `Show BR`, `Show Bottom Row` |
| TR | TR Open, TR Close | `TR Button Switch` | `Show TL`, `Show BL`, `Show BR`, `Show Bottom Row` |
| BL | BL Open, BL Close | `BL Button Switch` | `Show TL`, `Show TR`, `Show BR`, `Show Top Row` |
| BR | BR Open, BR Close | `BR Button Switch` | `Show TL`, `Show TR`, `Show BL`, `Show Top Row` |

A top card hides the **bottom** row, and a bottom card hides the **top** row: always the row it isn't in.

Why "Keep current value": a click on an empty spot of a button sheet clears the selection. Keeping the value means that stray click changes nothing.

**You should see** a click on TL's expand: TR, BL and BR disappear, TL fills the area, and its icon turns into ×. Click ×: the grid is back. Do the same with TR, BL and BR.

---

### Step 10: reset, and test every card

**Why.** A dashboard opens in whatever state it was saved in. Save it with BR zoomed, and every visitor starts zoomed. A Reset button writes True into all six switches, so the grid is one click away, and it's a good habit to click it before you save.

Create these calculated fields:

```
// Reset True
TRUE
```

```
// Reset Shape
"reset_button"
```

Two more for the **deselect trick**. The Reset sheet keeps its mark after a click, so the mark would stay selected and the next click would only unselect it. The trick clears the selection right after every click:

```
// zzTrue
TRUE
```

```
// zzFalse
FALSE
```

New worksheet **L1 Reset** (tab **Step 10 · Reset** in the downloaded workbook):

1. Marks card **Shape**. Drag `Reset Shape` to **Shape**; click Shape, palette **Arcadia How-To**, assign `reset_button`.
2. Drag `Reset True`, `zzTrue` and `zzFalse` to **Detail**.
3. **Size**: large enough to fill the slot. Tooltip "Back to the grid", command buttons off.
4. Put it on the dashboard at 200 × 32 (on the finished page it sits in the rail on the left).

Six actions from **L1 Reset** (**Dashboard > Actions > Add Action > Change Parameter**, source sheet **L1 Reset** only, run on **Select**, source field `Reset True`, keep current value), one per target parameter: `Show TL`, `Show TR`, `Show BL`, `Show BR`, `Show Top Row`, `Show Bottom Row`.

Then the deselect: **Dashboard > Actions > Add Action > Filter**:

- **Source Sheets:** L1 Reset only; **Run action on:** Select
- **Target Sheets:** L1 Reset only
- **Clearing the selection will:** Show all values
- **Filter:** Selected Fields, then the field pair **zzTrue** (source) → **zzFalse** (target)

On every click it asks Tableau for rows where TRUE equals FALSE. There are none, so the selection drops at once, and because the action clears to "Show all values", nothing on the sheet disappears. Every click is a fresh click.

**You should see**

| Do | The dashboard |
|---|---|
| Click TL's expand | TL alone, × at its top right |
| Click Reset | The grid, four expand icons |
| Click BR's expand, then its × | BR alone, then the grid |
| Click TR's expand, then Reset | TR alone, then the grid |
| With a card zoomed, look for the other buttons | They're hidden with their cards: × or Reset first |

Click Reset before you save.

---

## Part 3: Level 2, grow in any direction

Level 1 has five layouts: the grid and four zoomed cards. Level 2 gives every card three buttons:

- **wide** (→ or ←): take the whole row, pushing its neighbor out;
- **tall** (↓ or ↑): take the whole column, pushing the card above or below out;
- **full** (expand): take the whole area.

The button for the layout you're in turns into ×, which undoes that move. Rows and columns combine: TL can be wide while BR is wide too, or TL tall while TR is tall. With the grid, that's 21 layouts. Six Boolean switches can't describe them; Level 2 needs a better idea.

### Step 11: two trees in one space

**Why.** In Level 1 the cards sit in rows: a column of two rows. In that tree, a card can take its row (hide its neighbor) or the whole area (hide the other row), but it can never take a column: TL and BL live in different rows, and no row can reach into another. To grow tall, the cards must sit in columns instead: a row of two columns, each holding two cards. So Level 2 builds **both trees** in the same space and shows one at a time: the **rows tree** for wide and full, the **columns tree** for tall.

A worksheet can appear only once on a dashboard. The rows tree uses the four card sheets you already have (a sheet can be on several dashboards, so Level 1's cards work here too); the columns tree needs a copy of each: right-click each card tab > **Duplicate**, and rename the copies **TL · Departments (col)**, **TR · Hire years (col)**, **BL · Level mix (col)** and **BR · Countries (col)**.

New dashboard **Level 2 · Grow in any direction**, Fixed size 1400 × 850. Containers, all tiled:

1. A **Vertical** container named **Area**.
2. Inside Area, two containers one under the other:
   - **Rows Tree**, Vertical, holding two Horizontal containers **Top Row 2** and **Bottom Row 2**; Top Row 2 holds **TL Card 2** and **TR Card 2**, Bottom Row 2 holds **BL Card 2** and **BR Card 2** (Vertical containers, built like Level 1's cards).
   - **Columns Tree**, Horizontal, holding two Vertical containers **Left Col** and **Right Col**; Left Col holds **TL Card (col)** above **BL Card (col)**, Right Col holds **TR Card (col)** above **BR Card (col)**.
3. Each card container: a 40 px title row (title text, then the card's **Buttons** sheet from Step 13, 96 px wide) and the card's sheet below (the `(col)` copies in the columns tree).
4. **Distribute Contents Evenly** on Area, Rows Tree, Columns Tree, the two rows and the two columns; not on the cards.

For now both trees show, each in half the space. Step 12 makes only one show at a time.

**You should see** two grids, one above the other: the top one built by rows, the bottom one by columns. They look the same, and that's the point: the difference only shows when a card grows.

---

### Step 12: five owners, twelve visibility calculations

**Why.** Instead of a switch per card, Level 2 asks one question per row, per column and for the whole area: **who owns it?** The top row is owned by "both" cards (the grid), or by TL alone (TL is wide), or by TR alone. The same for the bottom row, the two columns and the full area. Five text parameters describe every layout, and twelve calculations turn them into show/hide for the containers.

Create five parameters (section 0.5), **Data type: String**, **Allowable values: List**, with these values, each on its own line:

| Parameter | Values (current value first) | Meaning |
|---|---|---|
| `p_Top` | both, TL, TR | Who owns the top row |
| `p_Bottom` | both, BL, BR | Who owns the bottom row |
| `p_Left` | both, TL, BL | Who owns the left column |
| `p_Right` | both, TR, BR | Who owns the right column |
| `p_Full` | none, TL, TR, BL, BR | Who owns the whole area |

Set the current value to the first one: **both** for the four rows and columns, **none** for full.

Now the twelve visibility calculations. Each reads only the parameters, so it has one True/False value for the whole dashboard, which is what **Control visibility using value** needs. `=` means "equals", `<>` means "is not", `OR` means "either one is true".

Which tree shows:

```
// L2 Rows Tree
[p_Left] = "both" AND [p_Right] = "both"
```

```
// L2 Columns Tree
NOT ([p_Left] = "both" AND [p_Right] = "both")
```

The rows tree shows unless a column has an owner; the columns tree is its exact opposite, so exactly one of them is always on.

In the rows tree, a row hides when a card in the **other** row goes full:

```
// L2 Top Row
[p_Full] = "none" OR [p_Full] = "TL" OR [p_Full] = "TR"
```

```
// L2 Bottom Row
[p_Full] = "none" OR [p_Full] = "BL" OR [p_Full] = "BR"
```

In the rows tree, a card hides when its row neighbor owns the row, or goes full:

```
// L2 TL
NOT ([p_Top] = "TR" OR [p_Full] = "TR")
```

```
// L2 TR
NOT ([p_Top] = "TL" OR [p_Full] = "TL")
```

```
// L2 BL
NOT ([p_Bottom] = "BR" OR [p_Full] = "BR")
```

```
// L2 BR
NOT ([p_Bottom] = "BL" OR [p_Full] = "BL")
```

The row containers do half the work: when BL goes full, hiding the top row already hides TL and TR, so each card only needs to watch its own neighbor.

In the columns tree, a card hides when the card above or below owns the column:

```
// L2 TL (col)
[p_Left] <> "BL"
```

```
// L2 BL (col)
[p_Left] <> "TL"
```

```
// L2 TR (col)
[p_Right] <> "BR"
```

```
// L2 BR (col)
[p_Right] <> "TR"
```

Then, on the Level 2 dashboard, set **Control visibility using value** (Step 8's three clicks) on twelve containers. This time the dropdown's value is a calculated field, not a parameter: look for it under the data source's name.

| Container | Value |
|---|---|
| Rows Tree | `L2 Rows Tree` |
| Columns Tree | `L2 Columns Tree` |
| Top Row 2 | `L2 Top Row` |
| Bottom Row 2 | `L2 Bottom Row` |
| TL Card 2, TR Card 2, BL Card 2, BR Card 2 | `L2 TL`, `L2 TR`, `L2 BL`, `L2 BR` |
| TL Card (col), BL Card (col), TR Card (col), BR Card (col) | `L2 TL (col)`, `L2 BL (col)`, `L2 TR (col)`, `L2 BR (col)` |

To watch the five owners, one more text sheet:

```
// Owners Now
"Top " + [p_Top] + " · Bottom " + [p_Bottom] + " · Left " + [p_Left] + " · Right " + [p_Right] + " · Full " + [p_Full]
```

New worksheet **Step 12 · Owners**: Marks **Text**, `Owners Now` on Text; right-click each of the five parameters > **Show Parameter**.

**You should see** "Top both · Bottom both · Left both · Right both · Full none", and on the dashboard only the rows tree, as a grid. Test with the parameter controls before any button exists, then set each back:

| Set | The dashboard |
|---|---|
| `p_Top` = TL | TL takes the top row |
| `p_Top` = TL and `p_Bottom` = BR | TL wide on top, BR wide below |
| `p_Left` = TL | The columns tree: TL takes the left column, TR and BR on the right |
| `p_Left` = TL and `p_Right` = BR | TL tall on the left, BR tall on the right |
| `p_Full` = BL | BL alone |

---

### Step 13: three buttons on one sheet

**Why.** Each card needs three buttons: wide, tall and full. Three marks on one sheet do it, one per button, and the click on a mark tells the actions which button it was. Once again, no column holds "wide, tall, full", so a menu field makes one: three level bands relabeled.

```
// Kind
CASE [level_band]
WHEN "L1–L2 Associate" THEN "wide"
WHEN "L3–L4 Senior" THEN "tall"
WHEN "L5–L6 Manager" THEN "full"
END
```

(The band names use an en dash, "–", not a hyphen: copy them from here.)

```
// Kind No
CASE [Kind] WHEN "wide" THEN 1 WHEN "tall" THEN 2 WHEN "full" THEN 3 END
```

`Kind No` puts the three buttons in a fixed order, left to right.

Each card's icon depends on its position (TL grows right and down, BR grows left and up) and on whether that move is already on (then it shows ×):

```
// TL Icon
IF [Kind] = "wide" THEN IIF([p_Top] = "TL", "icon_close", "icon_right")
ELSEIF [Kind] = "tall" THEN IIF([p_Left] = "TL", "icon_close", "icon_down")
ELSE IIF([p_Full] = "TL", "icon_close", "icon_expand") END
```

```
// TR Icon
IF [Kind] = "wide" THEN IIF([p_Top] = "TR", "icon_close", "icon_left")
ELSEIF [Kind] = "tall" THEN IIF([p_Right] = "TR", "icon_close", "icon_down")
ELSE IIF([p_Full] = "TR", "icon_close", "icon_expand") END
```

```
// BL Icon
IF [Kind] = "wide" THEN IIF([p_Bottom] = "BL", "icon_close", "icon_right")
ELSEIF [Kind] = "tall" THEN IIF([p_Left] = "BL", "icon_close", "icon_up")
ELSE IIF([p_Full] = "BL", "icon_close", "icon_expand") END
```

```
// BR Icon
IF [Kind] = "wide" THEN IIF([p_Bottom] = "BR", "icon_close", "icon_left")
ELSEIF [Kind] = "tall" THEN IIF([p_Right] = "BR", "icon_close", "icon_up")
ELSE IIF([p_Full] = "BR", "icon_close", "icon_expand") END
```

How to read TL Icon: on the wide mark, show × if TL already owns the top row, otherwise →; on the tall mark, × if TL owns the left column, otherwise ↓; on the full mark, × if TL owns the area, otherwise expand.

And a tooltip line for each mark:

```
// Kind Tip
CASE [Kind]
WHEN "wide" THEN "Grow wide: take the whole row"
WHEN "tall" THEN "Grow tall: take the whole column"
ELSE "Full: take the whole area"
END
```

New worksheet **TL Buttons** (tab **Step 13 · TL Buttons** in the downloaded workbook):

1. Drag `Kind` to **Filters**, untick **Null**, **OK**: three values left.
2. Drag `Kind No` to **Columns**. Right-click it > **Convert to Discrete** if it shows as an axis: you want three separate columns. Right-click its header > untick **Show Header**.
3. Marks card **Shape**. Drag `TL Icon` to **Shape**; click Shape, palette **Arcadia How-To**, and assign each value to the picture with the same name (`icon_right`, `icon_down`, `icon_expand`, `icon_close`).
4. Drag `Kind` to **Detail**. Then drag `zzTrue` and `zzFalse` to **Detail** (the deselect trick, Step 10: this sheet keeps its marks after a click).
5. Tooltip: `<Kind Tip>` on the first line (use **Insert** in the tooltip editor to add a field), "Click again to undo." on the second. Command buttons off.
6. **Size**: small, like Level 1's buttons.

**You should see** three icons side by side: →, ↓ and expand. Set `p_Top` to TL: the first one turns into ×. Set it back to both.

---

### Step 14: five actions for one card

**Why.** One click must update all five owners at once, because a move in one direction clears the others: going wide while you were tall gives the column back. Each owner gets a **source calculation**: a formula that says what this card's click writes into that owner, depending on which of the three marks was clicked. Five source calculations, five parameter actions, all from the same sheet.

TL's five, created in this order:

```
// TL to Top
IF [Kind] = "wide" THEN IIF([p_Top] = "TL", "both", "TL") ELSE "both" END
```

The wide button claims the top row for TL, or gives it back if TL already has it; the other two buttons give it back.

```
// TL to Bottom
IF [Kind] = "wide" THEN [p_Bottom] ELSE "both" END
```

The wide button leaves the bottom row as it is (so BR can stay wide below TL); the other buttons give it back.

```
// TL to Left
IF [Kind] = "tall" THEN IIF([p_Left] = "TL", "both", "TL") ELSE "both" END
```

```
// TL to Right
IF [Kind] = "tall" THEN [p_Right] ELSE "both" END
```

The same two ideas for the columns: tall claims or releases the left column, and keeps the right column as it is.

```
// TL to Full
IF [Kind] = "full" THEN IIF([p_Full] = "TL", "none", "TL") ELSE "none" END
```

Drag all five to **Detail** on **TL Buttons**.

Then five actions (**Dashboard > Actions > Add Action > Change Parameter**), all with **Source Sheets: TL Buttons** only, **Run action on: Select**, **Aggregation: None**, **Keep current value**:

| Name | Target parameter | Source field |
|---|---|---|
| TL to Top | `p_Top` | `TL to Top` |
| TL to Bottom | `p_Bottom` | `TL to Bottom` |
| TL to Left | `p_Left` | `TL to Left` |
| TL to Right | `p_Right` | `TL to Right` |
| TL to Full | `p_Full` | `TL to Full` |

And the deselect, as in Step 10: **Add Action > Filter**, source and target **TL Buttons**, run on Select, clearing shows all values, selected fields zzTrue → zzFalse.

Why "keep the other row" creates the combined layouts: with TL wide (`p_Top` = TL), a click on BL's → writes BL into `p_Bottom`, and its "to Top" source writes the current `p_Top` back into `p_Top`, unchanged. So TL stays wide on top and BL goes wide below, with no extra rule.

**You should see** on the Level 2 dashboard: TL's → makes TL take the top row, and the → turns into ×; × gives the grid back. TL's ↓ switches to the columns tree with TL taking the left column. TL's expand fills the area with TL.

---

### Step 15: the other seven button sheets

**Why.** Every card needs its own buttons, and each card exists twice (rows tree and columns tree), so there are eight button sheets: TL, TR, BL, BR, and the same four with "(col)". A click on any of them must do the same thing, so the `(col)` sheets are plain copies.

First the source calculations for the other three cards. Each card claims its own row and its own column:

| Card | Its row | Other row | Its column | Other column |
|---|---|---|---|---|
| TR | `p_Top` | `p_Bottom` | `p_Right` | `p_Left` |
| BL | `p_Bottom` | `p_Top` | `p_Left` | `p_Right` |
| BR | `p_Bottom` | `p_Top` | `p_Right` | `p_Left` |

```
// TR to Top
IF [Kind] = "wide" THEN IIF([p_Top] = "TR", "both", "TR") ELSE "both" END
```

```
// TR to Bottom
IF [Kind] = "wide" THEN [p_Bottom] ELSE "both" END
```

```
// TR to Right
IF [Kind] = "tall" THEN IIF([p_Right] = "TR", "both", "TR") ELSE "both" END
```

```
// TR to Left
IF [Kind] = "tall" THEN [p_Left] ELSE "both" END
```

```
// TR to Full
IF [Kind] = "full" THEN IIF([p_Full] = "TR", "none", "TR") ELSE "none" END
```

```
// BL to Bottom
IF [Kind] = "wide" THEN IIF([p_Bottom] = "BL", "both", "BL") ELSE "both" END
```

```
// BL to Top
IF [Kind] = "wide" THEN [p_Top] ELSE "both" END
```

```
// BL to Left
IF [Kind] = "tall" THEN IIF([p_Left] = "BL", "both", "BL") ELSE "both" END
```

```
// BL to Right
IF [Kind] = "tall" THEN [p_Right] ELSE "both" END
```

```
// BL to Full
IF [Kind] = "full" THEN IIF([p_Full] = "BL", "none", "BL") ELSE "none" END
```

```
// BR to Bottom
IF [Kind] = "wide" THEN IIF([p_Bottom] = "BR", "both", "BR") ELSE "both" END
```

```
// BR to Top
IF [Kind] = "wide" THEN [p_Top] ELSE "both" END
```

```
// BR to Right
IF [Kind] = "tall" THEN IIF([p_Right] = "BR", "both", "BR") ELSE "both" END
```

```
// BR to Left
IF [Kind] = "tall" THEN [p_Left] ELSE "both" END
```

```
// BR to Full
IF [Kind] = "full" THEN IIF([p_Full] = "BR", "none", "BR") ELSE "none" END
```

Then the sheets:

1. Duplicate **TL Buttons** three times: **TR Buttons**, **BL Buttons**, **BR Buttons**. On each, drop the card's own Icon calculation on top of `TL Icon` on Shape (and assign its pictures), and drop its five source calculations on top of TL's five on Detail.
2. Duplicate each of the four once more and add " (col)" to the name: **TL Buttons (col)** and so on.
3. Put each sheet in its card's title row on the Level 2 dashboard: the plain ones in the rows tree, the "(col)" ones in the columns tree.

The actions: five per sheet, eight sheets, **forty** parameter actions, plus a deselect per sheet. Each sheet's five actions are exactly like Step 14's, with that sheet as the only source:

| Source sheet | Writes `p_Top` from | `p_Bottom` from | `p_Left` from | `p_Right` from | `p_Full` from |
|---|---|---|---|---|---|
| TL Buttons, TL Buttons (col) | TL to Top | TL to Bottom | TL to Left | TL to Right | TL to Full |
| TR Buttons, TR Buttons (col) | TR to Top | TR to Bottom | TR to Left | TR to Right | TR to Full |
| BL Buttons, BL Buttons (col) | BL to Top | BL to Bottom | BL to Left | BL to Right | BL to Full |
| BR Buttons, BR Buttons (col) | BR to Top | BR to Bottom | BR to Left | BR to Right | BR to Full |

Name them after the sheet and the target ("TR (col) to Left"), so the list stays readable.

**You should see** every card's three buttons working, in both trees.

---

### Step 16: reset Level 2

**Why.** As in Level 1: one click back to the grid, and the state to save the workbook in.

```
// Reset Both
"both"
```

```
// Reset None
"none"
```

New worksheet **L2 Reset** (tab **Step 16 · Reset** in the downloaded workbook): a copy of L1 Reset (right-click its tab > **Duplicate**), with `Reset Both` and `Reset None` on Detail instead of `Reset True`. Put it in the Level 2 rail.

Five actions from **L2 Reset**: `Reset Both` into `p_Top`, `p_Bottom`, `p_Left` and `p_Right`; `Reset None` into `p_Full`. Plus its deselect (source and target L2 Reset, zzTrue → zzFalse).

**You should see** the grid after any layout. Click Reset before you save.

---

### Step 17: test all 21 layouts

**Why.** Twenty-one layouts and twelve buttons make 252 possible clicks; a short tour covers every kind of move.

| Do | The dashboard |
|---|---|
| TL → | TL takes the top row (×), BL and BR below |
| then BR ← | TL wide on top, BR wide below |
| then TL × | The top row is back to two cards; BR still wide |
| Reset, then TL ↓ | Columns: TL takes the left column, TR and BR on the right |
| then BR ↑ | TL tall on the left, BR tall on the right |
| then TL → | Wide clears tall: back to rows, TL wide on top, BL and BR below |
| then BL expand | BL alone |
| then BL × | The grid |
| TR expand, then TL expand | Full moves straight from TR to TL |

The 21 layouts: the grid; 4 wide (each card takes its row); 4 tall (each card takes its column); 4 full; 4 with both rows taken (TL or TR on top, with BL or BR below); 4 with both columns taken (TL or BL on the left, with TR or BR on the right).

---

## Use it on your own data

The zoom doesn't care what's inside the cards: swap any card sheet for one of yours and every button keeps working. Keep the names (TL · …, TR · …) or rename them; the containers, parameters and actions don't read the sheet names. For more than four cards, Level 1 needs one switch and one Filter/Switch pair per card, and every card's calculations grow; Level 2's owners grow by one value per card in each row or column.

## Checks

| Check | Value |
|---|---|
| Employees, every card | 30,005 |
| TL departments | 31; Core Platform Engineering 2,566 |
| TR hire years | 2001 to 2026; 2025 4,049; 2001 197; 2026 2,517 |
| BL bands | 7,302 / 12,778 / 9,511 / 414 |
| BR countries | 22; United States 9,362 |
| Level 1 layouts | 5 (grid + 4 zoomed) |
| Level 2 layouts | 21 |
| Parameters | 6 Boolean (Level 1) + 5 String (Level 2) |
| Parameter actions | 16 + 6 Reset (Level 1); 40 + 5 Reset (Level 2) |
| Containers shown or hidden | 6 (Level 1); 12 (Level 2) |

## Why it works this way

- **Booleans for five layouts, owners for 21.** Level 1's switches say what's visible; each card asks "are the others showing?". That's simple for one move per card. Level 2's moves overlap (a card can be wide while another is wide below it), so instead of a switch per container it stores who owns each row, column and the area, and calculations work out what's visible.
- **Two trees, not one.** A container can only hand space to its own children. Rows can merge cards side by side, columns can merge them top to bottom; no single tree does both, so Level 2 keeps both and shows one.
- **Every visibility calculation reads only parameters.** "Control visibility using value" needs one True/False value for the whole dashboard. A calculation on data rows could have a different value per row; one that reads only parameters can't.
- **Two sheets per button in Level 1, one sheet with a deselect in Level 2.** Level 1's clicked sheet empties itself, so nothing stays selected. Level 2's sheet keeps three marks, so it needs the zzTrue → zzFalse filter action to clear the click.
