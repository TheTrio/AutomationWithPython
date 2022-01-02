from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import json
import matplotlib.dates as mdates
from matplotlib import pyplot as plt


# This creates a line graph of how much time each member has spent in the VC
# There's a config file which has to be present in the root of the project
# The format is as follows
# {
#   "names": {
#     "id1": "name1",
#     "id2": "name2",
#     ...
#   },
#   "title": "VC TIME",
#   "dates": {
#     "1": "YYYY-MM-DD",
#     "2": "YYYY-MM-DD"
#     ...
#   }
# }
# There's also a data directory in the root of the project. It contains
# a list of files, all labeled "n.json" where n is between 1 and N.
# N and the number of dates in the config file must match.
# These json files must contain key value pairs of the ID mentioned in the config
# file and the time spent in the vc. The format is days, seconds
# Example
# {
#   "id1": "1:35614",
#   "id2": "2:14167",
# }
# To ignore a user, simply remove their ID from the config file
# if done correctly, you should get a sweet little line graph detailing your adventures

root = Path(__file__).parent.parent  # change as per your wish


def sort_default_dict(d: dict):
    """Returns a sorted default dict created from the provided dictionary"""
    return defaultdict(
        lambda: timedelta(days=0, seconds=0),
        {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)},
    )


def main():
    data = defaultdict(list)

    with open(root / "config.json") as f:
        config: dict = json.load(f)

    names_data = config["names"]
    months: list[datetime] = []

    for date in config["dates"].values():
        months.append(datetime.strptime(date, "%Y-%m-%d"))

    for discord_id, name in names_data.items():
        for index in range(1, len(months) + 1):
            with open(root / f"data/{index}.json") as f:
                curr_json_data: dict = json.load(f)
            if discord_id in curr_json_data:
                days, seconds = list(map(int, curr_json_data[discord_id].split(":")))
                data[name].append(timedelta(days=days, seconds=seconds).total_seconds())
            else:
                data[name].append(0)

    # sorting the data
    data = sort_default_dict(data)
    for name, days in data.items():
        plt.plot(months, days, label=name)

    # setting date formatters
    locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
    formatter = mdates.ConciseDateFormatter(locator)
    ax = plt.gca()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    # converting seconds to days
    yticks = plt.yticks()[0]
    plt.yticks(yticks, list(map(lambda v: v // (24 * 60 * 60), yticks)))

    # other configuration
    plt.xlabel("Month")
    plt.ylabel("Days spent in VC")
    plt.title(config["title"])
    ax.set_ylim([0, None])
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
