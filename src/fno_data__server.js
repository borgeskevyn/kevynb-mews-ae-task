const express = require('express');
const fs = require('fs');
const app = express();
const port = 3000;

console.log(`
--------------------------------------------------------------------------------
--                                      Mews                                  --
--------------------------------------------------------------------------------

Job: Analytics Engineer
Org: FnO.Data

API server starting...
`);

const nestedCategories = [];

// Load data once at startup (sync for simplicity)
let jsonData;
try {
    const raw = fs.readFileSync('./data/mock_data.json', 'utf8');
    jsonData = JSON.parse(raw);
} catch (error) {
    console.error('Failed to read JSON file:', error);
    process.exit(1);
}

// Simple request logger
app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
});

// List all top-level categories
app.get('/', (req, res) => {
    res.json(Object.keys(jsonData));
});

// List subcategories for a category
app.get('/:category', (req, res) => {
    const { category } = req.params;
    const cat = jsonData[category];
    if (!cat) return res.status(404).send('Not Found');
    res.json(Object.keys(cat));
});

// List subcategory data or nested keys
app.get('/:category/:subCategory', (req, res) => {
    const { category, subCategory } = req.params;
    const sub = jsonData[category]?.[subCategory];
    if (!sub) return res.status(404).send('Not Found');
    if (nestedCategories.includes(category)) {
        res.json(Object.keys(sub));
    } else {
        res.json(sub);
    }
});

// List year data or nested keys
app.get('/:category/:subCategory/:year', (req, res) => {
    const { category, subCategory, year } = req.params;
    const yearObj = jsonData[category]?.[subCategory]?.[year];
    if (!yearObj) return res.status(404).send('Not Found');
    if (nestedCategories.includes(category)) {
        res.json(Object.keys(yearObj));
    } else {
        res.json(yearObj);
    }
});

// List month data or nested keys
app.get('/:category/:subCategory/:year/:month', (req, res) => {
    const { category, subCategory, year, month } = req.params;
    const monthObj = jsonData[category]?.[subCategory]?.[year]?.[month];
    if (!monthObj) return res.status(404).send('Not Found');
    if (nestedCategories.includes(category)) {
        res.json(Object.keys(monthObj));
    } else {
        res.json(monthObj);
    }
});

// Return day data
app.get('/:category/:subCategory/:year/:month/:day', (req, res) => {
    const { category, subCategory, year, month, day } = req.params;
    const dayObj = jsonData[category]?.[subCategory]?.[year]?.[month]?.[day];
    if (!dayObj) return res.status(404).send('Not Found');
    res.json(dayObj);
});

app.listen(port, () => {
    console.log(`
--------------------------------------------------------------------------------

API server is running.

http://localhost:${port}

Good luck!
    `);
});
