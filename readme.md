# Bookie

This is a project aimed to automate the process of adding and administrating bookmarks for Firefox.

### Requirements

* Python 3
* Firefox version >= 3

### Usage

`$ python3 app.py [browser] [profile]`

For usage of this script without any modification, Bookie will use the `bookmarks-example.yml` file as reference to which bookmarks to create.

This script will append bookmarks to the existing bookmarks in your filefox profile.

### What is missing?

* Option to clear all existing bookmarks and populate the bookmarks defined in `bookmarks-example/private.yml`.
* Creating folders.
* Placing bookmarks in folders.

### bookmarks yml file

#### Bookmarks

__type__ - [REQUIRED, STRING] This defines if the current row is of type "bookmark" when defining a bookmark. This field exists for future development of "folders" when defining folders.

__title__ - [REQURED, STRING] The title of the bookmark.

__url__ - [REQUIRED, STRING] The URL to the website of the bookmark.
