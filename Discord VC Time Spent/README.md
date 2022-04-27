# Discord VC Time Spent Analyzer

Another silly program which I made. Creates a line chart showing the time spent by each user in a voice chat.

# How to Run

```
poetry install --no-dev
poetry run main
```

# Configuration

There's a config file which has to be present in the root of the project

The format is as follows

```py
{
  "names": {
    "id1": "name1",
    "id2": "name2",
    ...
  },
  "title": "VC TIME",
  "dates": {
    "1": "YYYY-MM-DD",
    "2": "YYYY-MM-DD"
    ...
  }
}
```

There's also a data directory in the root of the project. It contains a list of files, all labeled `n.json` where `n` is between 1 and `N`. `N` and the number of dates in the config file must match.

These json files must contain key value pairs of the ID mentioned in the config file and the time spent in the vc. The format is days, seconds

For example

```py
{
  "id1": "1:35614",
  "id2": "2:14167",
}
```

To ignore a user, simply remove their ID from the config file.

If done correctly, you should get a sweet little line graph detailing your adventures
