from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import json
import matplotlib.dates as mdates
from matplotlib import pyplot as plt

root = Path(__file__).parent.parent  # change as per your wish


def sort_dict(d: dict):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}


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
    data = sort_dict(data)
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
