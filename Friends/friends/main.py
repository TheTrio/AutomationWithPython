import requests
from bs4 import BeautifulSoup
from pathlib import Path
from argparse import ArgumentParser, BooleanOptionalAction


def get_episode_names(season):
    url = f"http://www.imdb.com/title/tt0108778/episodes?season={season}&ref_=tt_eps_sn_{season}"  # noqa
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return [
        tag.get_attribute_list("title")[0]
        for tag in soup.find_all(itemprop="name")
        if tag.get_attribute_list("title")[0]
    ]


def rename(root, seasons, verbose=False, test=False):
    for season in seasons:
        # left pads the season with 0
        # for example, 1 becomes 01
        season_folder = Path(root / f"S{season:0>2}")
        if not season_folder.exists():
            if verbose:
                print(f'Folder "{season_folder}" for season {season} not found')
            break
        episodes = get_episode_names(season)
        for file in season_folder.iterdir():
            try:
                episode_num = int(file.stem) - 1
                result = (
                    file.parent
                    / f"{episode_num + 1}. {episodes[episode_num]}{file.suffix}"
                )

                if verbose or test:
                    print(f'Renaming "{file.name}" to "{result.name}"')
                if not test:
                    file.rename(result)
            except ValueError:
                # assume its already named
                if verbose:
                    print(
                        f'Invalid file name "{file.stem}". Filename must be a valid integer representing the episode number'  # noqa
                    )
                pass


def main():
    parser = ArgumentParser(description="Renaming Friends episodes made easy")
    parser.add_argument("path", type=Path, help="The folder containing all the seasons")
    parser.add_argument(
        "-S",
        "--seasons",
        nargs="+",
        type=int,
        choices=list(range(1, 11)),
        required=True,
        help="The seasons to run for",
    )
    parser.add_argument("-v", "--verbose", action=BooleanOptionalAction, default=False)
    parser.add_argument(
        "-t",
        "--test",
        action=BooleanOptionalAction,
        help="Logs the changes it will make. No actual files are affected",
    )
    options = parser.parse_args()
    rename(options.path, options.seasons, options.verbose, options.test)


if __name__ == "__main__":
    main()
