# Bookie

This is a project aimed to automate the process of adding and administrating bookmarks for Firefox.

### Requirements

* Python 3
* Firefox version >= 3

### Usage

`$ python3 app.py [browser] [profile]`

[browser] currently only supports 'firefox'.

[profile] Can be found by browsing `about:profiles`. Looks like `kyy5y7i1.default-release`.

For usage of this script without any modification, Bookie will use the `bookmarks-example.yml` file as reference to which bookmarks to create.

This script will append bookmarks to the existing bookmarks in your filefox profile.

### bookmarks yml file

#### Bookmark

__type__ - [REQUIRED, STRING] "bookmark"

__title__ - [REQURED, STRING] The title of the bookmark.

__url__ - [REQUIRED, STRING] The URL to the website of the bookmark.

__children__ - [LIST] A list of records with bookmarks and/or folders.

Example:

```
  - type: bookmark
    title: Reddit
    url: https://www.reddit.com
```

#### Folder

__type__ - [REQUIRED, STRING] "folder"

__title__ - [REQURED, STRING] The title of the folder.

__children__ - [LIST] A list of records with bookmarks and/or folders.

Example:

```
  - type: folder
    title: work

    children:
      - type: bookmark
        title: Github
        url: https://github.com

      - type: folder
        title: WFH
        children:

          - type: bookmark
            title: jitsi
            url: https://jitsi.org/
```

### What is missing?

* Option to clear all existing bookmarks and populate the bookmarks defined in `bookmarks-example/private.yml`.
* creating other bookmark yml file beside bookmarks-example.yml
