**Role:** You are an expert Full Stack Developer and Data Visualization specialist.

**Goal:** Build a 'landing page with information and a Fantasy Football Analytics dashboard using a single `index.html` file and vanilla JavaScript.

**Landing Page** 

The landing page should be simple and clean. It should document the scraping process done in `scrape-weekly-stats.py`. It should use `explanaition.md` to explain the SQL queries in `data/queries.sql`. And it should explain the following web application

## App

**Architecture & Data Loading:**
The website must run client-side.
Use the `sql.js` library to load the `data/weekly.db` file directly in the browser.

**UI Layout:**
1.  **Header:** Title of the project.
2.  **Controls Section:**
    * **Position Dropdown:** Options: All, Flex (RB/WR/TE), QB, RB, WR, TE.
    * **Week Dropdown:** A selector for the Week number.
3.  **Data Display:** A clean, sortable HTML table.

**Functionality & Logic:**
1.  **Filtering:**
    * When a user selects a Position, filter the table to show only that position (or the specific "Flex" group).
    * **Critical:** When a user selects a "Week" (e.g., Week 5), the app must filter out any data from the future (Week 6+). However, it should use historical data (Week 1-4) to calculate averages.
2.  **Columns to Display:**
    * Player Name
    * Position
    * Avg Points (All season up to selected week)
    * Var Coef (Coefficient of Variation)
    * Points Scored (In the specifically selected week)
    * Rolling Average (Last 3 weeks)
    * Trend ([Explain logic: e.g., Is current week higher than average?])
    * Next Week Projection ([Explain logic: e.g., Weighted average of last 3 games])

**Design Requirements:**
* Use Bootstrap 5 for responsiveness and a dark theme.
* Ensure the table is responsive on mobile devices.

**Deliverables:**
1.  The complete `index.html` file (containing CSS and JS).
2.  [If Option 1] The updated Python script to export JSON.

---

Perfect.

Now under the psudocode web scraping section I'd like to display the actual code from scrape-weekly-stats.py

---

Good.

Now create a new section called 'AI Prompts Used' and include the 3 prompts used in `ui_prompt.md` in that section. 

> Note that the prompts are separated by '---'