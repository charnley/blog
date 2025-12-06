---
layout: post
title: "Taking notes - Context Switching Without Losing Your Mind"
date: 2025-12-04
categories: notes, programming
---

> tl;dr. My pitch is,
> you anyway write your notes in Markdown `.md` files,
> why not index and search them with [zk-org](https://github.com/zk-org/zk)?
> And yes, the setup is editor agnostic.

<!-- ## Context switching is productivity killer -->
## Context switching is your problem

In my job, I constantly jump between meetings, problems, and digital fires—all while trying to keep everything under control.
Privately, I’ve always had way too many open projects.

My brain never seems to reload the last task fast enough, and half the stress comes from trying to remember where I left off.
**If you feel a little “ADHD-ish” at work, maybe it’s not you.
Perhaps you need better notes. Or a better note system!**

For a while, I tried solving this with tools:

- Trello for recipes and daily todos
- Notion for project notes
- Emailing myself links to “read later”
- Using [Outlook "To Do"](https://to-do.office.com/tasks/) at work

None of it felt good.
I don’t want a whole application to manage notes or todos.
I don’t need backlinks or [graphs of my notes](https://help.obsidian.md/plugins/graph).
I need something fast, searchable, and in the text/code editor I am already using.
Hence, not [Obsidian](https://obsidian.md/).

So I switched to something extremely simple:
`vim ~/todo/$(date +%Y-%m-%d).md`.
A daily file for meeting notes, tasks, and whatever pops up.
But, when I switch context $$5\cdot10^6$$ times a day, the daily file became pretty chaotic.

Sönke Ahrens says in How to Take Smart Notes:

> We get distracted by open tasks, not finished tasks.
> Convince your brain it will be taken care of by writing it down.

The book is great if you enjoy deconstructing the question "What is a note?",
otherwise… a bit too much.
But a main point is; use cognitive offloading by writing down your thoughts/todo in a note,
if you can easily find it again.
Writing things down frees your brain to work on current task.
Like when you write things down on sticky notes.

My requirements ended up being simple:

- Not another app hanging around.
- Editing notes should happen in my favourite editor.
- Writing a new note for a new context should be fast.
- Searching and finding notes should feel instant.

## The solution you are looking for is "zk"

Obviously the solution is, take notes.
This year I found [zk](https://github.com/zk-org/zk.git),
and it was exactly what I was looking for.
A **terminal tool for indexing and searching Markdown files**.
Having a quick way to write down thoughts/tasks tricks your mind that it will be done later and makes it easier to focus on current task.

![
]({{site.baseurl}}/assets/images/about_zk/zk_demo.gif)

Like Obsidian, it is based around [Zettlekasten](https://en.wikipedia.org/wiki/Zettelkasten),
a note-taking system around making many connected notes.
Again, the book above will go deep into the cult... sorry, I mean the details of the system.

Unlike Obsidian, `zk` is a much more light-weight and practical tool.
The only role it has is to index and search, then the result can be opened in your code editor.
Because it is a CLI tool, you can very easily customize the workflow with standard GNU tools.
I really enjoy building custom commands that work exactly for me.
For example using GNU `date` you can use releative dates to access todo list for other days.

```toml
todo = 'zk new --group todo --no-input --date "$(date -d "$*" +%Y-%m-%d)" "$ZK_NOTEBOOK_DIR/todo" --template todo.md'
```

```bash
zk todo # open today's todo-list
zk todo tomorrow # open tomorrows todo-list
zk todo next monday
zk todo yesterday
```

For the last months working with `zk` I got annoyed I didn't start earlier because I remember I worked on something else
years ago, but don't remember the details. Where is my notes??
I know I worked with this before!

### I don't want to use vim!

Sorry to hear that, but, that is perfectly fine.
The approach is editor agnostic, as `zk` is used to index and search your notes,
it has nothing to do with the editor.

![
VSCode using zk in the terminal to search notes
]({{site.baseurl}}/assets/images/about_zk/vscode_and_zk_resize.png)

They setup works really great with VSCode as well.
Just configure `editor = "code -r"`.

## How I use it at `zk` work

My notes is a folder full of Markdown files that I could be storing on OneDrive,
but I still like to have the history tracking of my notes, so in the end I use Git to manage my notes, and using OneDrive as a "remote" for backup.

```mermaid

%%{init: {
  "theme": "base",
  "themeVariables": {
    "fontFamily": "Mononoki, Monaco, mono",
    "fontSize": "11px",
    "lineHeight": "1.2"
  }
}}%%

flowchart LR
    Editor["Your Editor<br />(VSCode / Vim)"]
    Notes["~/notes<br />(Git Repo)"]
    OneDrive["~/OneDrive<br/>(Remote Backup)"]

    Editor --> Notes
    Notes -->|git push| OneDrive

```

In practise, I 

- Set my daily todo list to try to keep me focused
- Use meeting template, keeping track who was there and what actionable follow is needed
- Tag everything so I can quickly find a meeting / topic
- Search for open Markdown tasks `[ ]`, per tag to know if items are forgotten
- I keep lists of different internal wiki/forum links with my notes, as it is easier to find than a linear bookmark system
- I keep snippets of how to use our internal infrastructure

Since I am at work I don't mind the licensed AI models are reading my stuff,
I can copy-paste the transcript from meetings and use Sonnet to re-write it into Markdown and find follow-ups.
Obviously I use [sst OpenCode](https://github.com/sst/opencode) for my agentic AI work, which works well with our company licensed mondels.

## How I use `zk` privately

Scenarios that kept happening

- I'm in bed, I see a cool Instagram wood project and want to save it for later
- I'm in the supermarket and need my shopping list / recipes
- I'm doing taxes, and forgot what I did last year

So I needed a searchable note system, which is also accessible on my mobile.
In the end I set up a `git` repository at [Linode](https://www.linode.com/) which is then accessible via ssk-key pair.
This would work fine on a private GitHub project, but I didn't want my private notes to be used as AI training data.

```mermaid

%%{init: {
  "theme": "base",
  "themeVariables": {
    "fontFamily": "Mononoki, Monaco, mono",
    "fontSize": "11px",
    "lineHeight": "1.2"
  }
}}%%

flowchart LR

    subgraph Laptop["Laptop/Desktop"]
        LEditor["Editor"]
        LRepo[".git"]
        LEditor --> LRepo
    end

    subgraph Mobile
        GitSync["Git Sync App"]
        Obsidian["Obsidian"]
        MRepo[".git"]
        GitSync --> MRepo
        Obsidian --> MRepo
    end

    Remote["Remote Repo<br/>(Linode/GitHub)"]

    LRepo -- SSH --> Remote
    MRepo -- SSH --> Remote


```

Having all my notes in one setup, it makes it really easy to navigate my projects/private projects.
I'm in the supermarket and I need the grocery list for Lasagne? Pow, just load it on my phone.

Overall I really enjoy the connectivity between having searchable indexed notes between my desktop computer, laptop and phone.
It feels like I can continue whatever I am doing, whenever.

## Setup, installation and configuration

Following
[zk-org.github.io/zk](https://zk-org.github.io/zk/)
easy setup `zk`.
You can compile it by clone and `make`-ing it, with [go](https://go.dev).

    cd $HOME/opt/
    git clone https://github.com/zk-org/zk.git zk.git --depth 1
    cd zk.git
    make build
    ln -s $HOME/opt/zk.git/zk $HOME/bin/zk

or if you are on a Mac, you can;

    brew install zk

With the executable installed, create a note folder `~/notes/` and `git init`.
Inside the folder create a `.zk` for your configuration and templates.
For me the setup is

    .zk
    .zk/templates
    .zk/templates/todo.md
    .zk/templates/default.md
    .zk/templates/meeting.md
    .zk/config.toml
    .zk/.gitignore # ignore .sqlite


A template would look something like this

<details markdown="1">
<summary><b>default_template.md</b></summary>

```markdown
---
date: {{ format-date now 'long' }}
title: {{ title }}
tags: [Untitled]
---

# Untitled

- Untitled
```

</details>

Why have "Untitled" in my template?
Because I sat op my editor [Neovim](https://github.com/neovim/neovim) to jump through "Untitled"
so I can quickly <kbd>c</kbd><kbd>w</kbd> (change word).


<details markdown="1">
<summary><b>config.toml</b></summary>

```toml
[note]
language = "en"
default-title = "Untitled"
filename = "{{format-date now '%Y-%m-%d'}}-{{id}}"
extension = "md"
template = "default.md"
id-charset = "alphanum"
id-length = 8
id-case = "lower"

[group]

[group.todo]
paths = ["todo"]

[group.todo.note]
filename = "{{format-date now '%Y-%m-%d'}}"
extension = "md"
template = "todo.md"

[group.meeting]
paths = ["meetings"]

[group.meeting.note]
filename = "{{format-date now '%Y-%m-%d-%H%M'}}-{{id}}"
extension = "md"
template = "meeting.md"

[format.markdown]
hashtags = true

[tool]
editor = "vim -c \"silent! /Untitled\" -c 'call search(\"Untitled\")' "
pager = "less -FIRX"
fzf-preview = "bat -p --color always {-1}"
fzf-options = "--multi --tiebreak begin --exact --tabstop 4 --height 100% --no-hscroll --color hl:-1,hl+:-1 --preview-window wrap"

[alias]

# Create new note, from templates
n = 'zk new'
today = 'zk new --group todo --no-input "$ZK_NOTEBOOK_DIR/todo" --template todo.md'
meeting = 'zk new --group meeting'
m = 'zk meeting'

# Usage:
# - zk todo next friday
# - zk todo tomorrow
# - zk todo yesterday
todo = 'zk new --group todo --no-input --date "$(date -d "$*" +%Y-%m-%d)" "$ZK_NOTEBOOK_DIR/todo" --template todo.md'

# Find and edit
last = "zk edit --limit 1 --sort modified- $argv"
recent = "zk edit --sort created- --created-after 'last 7 days' --interactive"
recent-month = "zk edit --sort created- --created-after 'last 30 days' --interactive"
ls = "zk edit --interactive --sort created"
t = "zk edit --interactive --tag $(zk tag --quiet | fzf | awk '{print $1}')"
ta = "zk edit --tag $(zk tag --quiet | fzf | awk '{print $1}')"

# Manage the notes
update = "cd $ZK_NOTEBOOK_DIR; git add -A; git commit -am 'updating'; git pull; git push; cd -"
clean = "zk-clean"
clean-dry = "zk-clean --dry-run"
sync = "zk update && zk index"

# Find all unresolved tasks within a zk tag
open-tasks = "cd $ZK_NOTEBOOK_DIR; zk list --tag $(zk tag --quiet | fzf | awk '{print $1}') --format {{path}} --quiet | xargs rg --no-heading --with-filename -F '[ ]'"

```

</details>

Noteable the alias I've setup are

```toml
# Use GNU date to interpret releative dates for todo lists. For example
# - zk todo
# - zk todo tomorrow
# - zk todo yesterday
# - zk todo next friday
# - zk todo 3 months 1 day
# - zk todo 25 dec
todo = 'zk new --group todo --no-input --date "$(date -d "$*" +%Y-%m-%d)" "$ZK_NOTEBOOK_DIR/todo" --template todo.md'

# Use fzf to interactively choose the tag I then want to search in
t = "zk edit --interactive --tag $(zk tag --quiet | fzf | awk '{print $1}')"

# Use git to pull and push, then re-index the zk database
update = "cd $ZK_NOTEBOOK_DIR; git add -A; git commit -am 'updating'; git pull; git push"
sync = "zk update && zk index"

# Find all unresolved Markdown tasks within a zk tag, with fzf and ripgrep
open-tasks = "cd $ZK_NOTEBOOK_DIR; zk list --tag $(zk tag --quiet | fzf | awk '{print $1}') --format {{path}} --quiet | xargs rg --no-heading --with-filename -F '[ ]'"
```

## Mobile Compatiable Setup

On your mobile install

- [obsidian.md/mobile](https://obsidian.md/mobile)
- [gitsync.viscouspotenti.al](https://gitsync.viscouspotenti.al/)

for a nice search and markdown app, and `GitSync` to sync your private git repo to your phone.

For Obsidian Mobile configuration, ensure that "daily" format is the same as with `zk`.

    Settings -> Dailt notes
    - Change Date format
    - Change "new file locaiton"
    - Check "Open daily note on startup"

Tag and search will work out of the box. 

## Conclusion

Just do it.
Setup `zk` for a folder of Markdown files, and use your favourite code editor to continue to write notes.

Thanks to Kristoffer for proofreading again.

## References

- [github.com/charnley/dotfiles](https://github.com/charnley/dotfiles) - my dotfile configuration
- [github.com/zk-org/zk.git](https://github.com/zk-org/zk.git) - the main CLI tool to search and index your notes
- [Obsidian](https://obsidian.md/) - Overkill Zettlekasten-based not taking application
- [ViscousPot/GitSync](https://github.com/ViscousPot/GitSync) - Sync git repos on your phone
- [en.wikipedia.org/wiki/Cognitive_load](https://en.wikipedia.org/wiki/Cognitive_load) - Cognitive offloading
