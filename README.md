## Introduction

`graphview` is a CLI tool to help you navigate your markdown notes. Running it will
display a navigatable list of related notes.

```bash
graphview index build
graphview search text "Vector databases"
```

Graphview works best when used with your favorite code editor. Use it as part of script to
automatically search using what you currently have open in the editor.

```bash
graphview search file --line-number 50 my_note.md
```

## Installation

```bash
pipx install git+https://github.com/kylediaz/graphview.git
```

## Zed

Add an entry to `tasks.json` that executes the following command:

```bash
{
  "label": "Local graph view current file",
  "command": "graphview search file",
  "args": ["--line-number", "$ZED_ROW", "$ZED_RELATIVE_FILE"]
}
```
