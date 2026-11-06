# Free stuff nearby

A map of free drinking water, toilets, parking, Wi‑Fi and defibrillators, using OpenStreetMap data.

Every Monday, GitHub downloads the latest OpenStreetMap data for the countries in `countries.txt`, keeps only the places this app shows, and publishes the app together with that data. Outside those countries, the app falls back to the public Overpass servers.

## Put it online (one time, about 15 minutes, needs a computer)

1. **Create a free GitHub account** at github.com, if you don’t have one.
2. **Create a repository.** Click **+** (top right) → **New repository**. Name it `free-stuff-nearby`, choose **Public**, and click **Create repository**.
3. **Upload the files.** On the new repository page, click **uploading an existing file**. Unzip this project on your computer, open the folder, select everything inside it and drag it onto the page. Include the `.github` folder: on a Mac it’s hidden, so press **Cmd + Shift + .** in Finder to show it. Click **Commit changes**.
4. **Turn on GitHub Pages.** Go to **Settings** → **Pages**. Under **Source**, choose **GitHub Actions**.
5. **Run the first build.** Go to the **Actions** tab → **Build app and place data** → **Run workflow**. It takes about 10 minutes. (A build may already have failed right after step 3, because Pages wasn’t on yet. That’s fine.)
6. **Open your app** at `https://YOUR-USERNAME.github.io/free-stuff-nearby/`. On your phone, open it in the browser and choose **Add to Home screen**.

After that, the data refreshes by itself every Monday.

## Adding a country

Open `countries.txt` on GitHub, click the pencil icon, and remove the `#` in front of a country (or add a line using a name from download.geofabrik.de, such as `europe/france`). Click **Commit changes**; a new build starts automatically.

## Changing the app

Replace `index.html` with a new version (**Add file** → **Upload files**). Each upload publishes the app again.

## Files

- `index.html` – the app
- `countries.txt` – which areas get prepared data
- `scripts/build_data.py` – turns OpenStreetMap data into small files the app loads quickly
- `.github/workflows/build.yml` – the weekly automation

Map data © OpenStreetMap contributors (ODbL). Base map by OpenFreeMap. Data downloads from Geofabrik.
