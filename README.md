# tableau-how-to

Step-by-step Tableau lessons built on **Arcadia Systems**, a fictional company with synthetic data. Each lesson rebuilds one technique from the [Arcadia dashboards on Tableau Public](https://public.tableau.com/app/profile/thialp) from an empty workbook, with every calculation made in Tableau, a "you should see" check after each step, and the data and images to download.

| # | Lesson | You'll build | Level |
|---|---|---|---|
| 1 | [Multi-select filters from shapes](01-multi-select-filters/) · [live](https://public.tableau.com/app/profile/thialp/viz/HowtoBuildMulti-SelectFiltersfromShapesArcadiaHow-To/Multi-selectfilters) | A rail button that opens a panel, tick lists with a parent-to-child cascade, a guard on the last option, and options that gray out across two filters | Intermediate |
| 2 | [Period selection](02-period-selection/) · [live](https://public.tableau.com/app/profile/thialp/viz/HowtoBuildaPeriodPickerforYoYYTDQuarterandMonthArcadiaHow-To/Periodselection) | One picker for year, year to date, quarter and month, today or any closed month-end, with a fair "to date" rule, shaded comparison windows and a last-year / prior-period toggle | Intermediate |

## How each lesson is laid out

Each lesson has its own folder. Open it and the first thing you see is a **Download everything** link: one zip with the data and the images. Below that, three lines to get started, and a link to the full step-by-step guide.

```
01-multi-select-filters/
├── README.md                          download link and how to start
├── GUIDE.md                           every step, with the reasons behind it
├── multi-select-filters-files.zip     the data and the images, in one download
├── data/                              the CSV, to preview here
└── shapes/                            the images, to preview here
```

The finished workbook for each lesson is on Tableau Public with **download on**: every step is a tab, and each tab's caption holds its instructions.

## The data

Every lesson uses the same company: 30,005 employees on Jun 30, 2026 across 8 functions, 31 departments, 5 regions, 22 countries and 35 offices. Lesson 1 has one row per employee on that date; lesson 2 has employee counts on every day from Jun 2021 to Jul 5, 2026. Column names stay the same from lesson to lesson, so the calculations you build in one paste straight into the next.

Arcadia Systems is fictional and all data is synthetic. Any resemblance to a real company or person is a coincidence.

## The look

The images follow the Arcadia design system, published as the [Arcadia Analytics · Tableau UI Kit](https://www.figma.com/community/file/1690422855000144024) on Figma. Restyle them there if you like; you never need Figma to follow a lesson.

## License

Code and data under the [MIT License](LICENSE). How the data was made from the Arcadia warehouse is in [`tools/`](tools/); you don't need it for any lesson.
