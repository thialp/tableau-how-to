# tableau-how-to

Step-by-step Tableau lessons built on **Arcadia Systems**, a fictional company with synthetic data. Each lesson rebuilds one technique from the [Arcadia dashboards on Tableau Public](https://public.tableau.com/app/profile/thialp) from an empty workbook, with every calculation made in Tableau, a "you should see" check after each step, and the data and images to download.

| # | Lesson | You'll build | Level |
|---|---|---|---|
| 1 | [Multi-select filters with clicks and images](01-multi-select-filters/) | A rail button that opens a panel, tick lists with a parent-to-child cascade, a guard on the last option, and options that gray out across two filters | Intermediate |
| 2 | Period selection *(coming next)* | Year over year, year to date, quarter and month comparisons from one picker | Intermediate |

## How each lesson is laid out

```
01-multi-select-filters/
├── README.md            the guide, step by step
├── data/                the CSV (and how it was made)
└── shapes/              the button and tick images, zipped for My Tableau Repository/Shapes
```

The finished workbook for each lesson is on Tableau Public with **download on**, so you can open every step's sheet and compare it with yours.

## The data

Every lesson uses the same company: 30,005 employees across 8 functions, 31 departments, 5 regions, 22 countries and 35 offices. Column names stay the same from lesson to lesson, so the calculations you build in one paste straight into the next.

Arcadia Systems is fictional and all data is synthetic. Any resemblance to a real company or person is a coincidence.

## The look

The images follow the Arcadia design system, published as the [Arcadia Analytics · Tableau UI Kit](https://www.figma.com/community/file/1690422855000144024) on Figma. Restyle them there if you like; you never need Figma to follow a lesson.

## License

Code and data under the [MIT License](LICENSE).
