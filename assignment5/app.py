import datetime
from typing import List, Optional
import uvicorn

import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# `GET /` should render the `strompris.html` template
# with inputs:
# - request
# - location_codes: location code dict
# - today: current date

@app.get("/")
def get_template(request: Request, 
                 location_codes: dict = LOCATION_CODES, 
                 today: datetime.date = datetime.date.today()
                 ):
    return templates.TemplateResponse(
        "strompris.html",
        {
            "request": request,
            "location_codes": location_codes,
            "today": today
        }
    )


# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)

@app.get("/plot_prices.json")
def plot(locations: Optional[list] = Query(default=list(LOCATION_CODES.keys())), 
         end: Optional[datetime.date] = datetime.date.today(), 
         days: Optional[int] = 7):
    df = fetch_prices(end_date=end, days=days, locations=locations)
    return alt.vconcat(plot_prices(df), plot_daily_prices(df)).to_dict()

# Task 5.6:
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date

...

# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)

...


# mount your docs directory as static files at `/help`

...

if __name__ == "__main__":
    # use uvicorn to launch your application on port 5000

    uvicorn.run(app, host="127.0.0.1", port=5000)
