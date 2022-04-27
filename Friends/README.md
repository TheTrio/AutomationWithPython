# Friends Episode Renamer

A program that I spent way too much time on

# How to Install

The easiest and simplest way to install the program is through the `tar.gz` file. Download it from the releases section and then do

```
pip install friends-0.1.0.tar.gz
```

Then you can run it as

```
friends-renamer --help
```

# How to Rename

- Create a folder for all the seasons. Inside, each season should have a folder. The expected format is `S01`, `S02`, ... and `S10`
- Rename the files to their episode numbers. For example, `1.mkv` or `1.mp4` for the first episode of the season and so on.

And that's about it! To rename the files for the 1st season for example, do

```
friends-renamer /path/to/folder -S 1
```

Adding a `-v` flag makes the program more verbose, while the `-t` flag is used to test the changes it will make without actually writing anything to disk

To see the complete manual, do

```
friends-renamer --help
```
