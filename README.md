![Banner.png](Banner.png)
___

# ProjectShop

ProjectShop is an Internet-based store that sells different kinds of electronics, either directly or as the middleman
between other retailers with main functionality via Telegram-bot, where users can log in using telegram data or a
self-created profile.
___
![GitHub issues](https://img.shields.io/github/issues-raw/kolyasalubov/ProjectShop)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/kolyasalubov/ProjectShop?color=green)
![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/kolyasalubov/ProjectShop)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/kolyasalubov/ProjectShop?color=green)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/kolyasalubov/ProjectShop)

* [Installation](#Installation)
    * [Required to install](#Required_to_install)
    * [Clone](#Clone)
    * [How to run](#How_to_run)
* [Git Flow](#Git_Flow)
    * [How we add features](#How_we_add_features)
* [Issue Flow](#Issue_Flow)
* [Developer Team](#Developer_team)

___

## Installation <a name="Installation"></a>

___

### Required to install <a name="Required_to_install"></a>

* Python 3.9
* Django 3.2.6

### Clone <a name="Clone"></a>

Clone this repo to your local machine using:  
`https://github.com/kolyasalubov/ProjectShop.git`

### How to run<a name="How_to_run"></a>

1. Open terminal.
2. Go to the directory ProjectShop.
3. Run `docker-compose up`
4. Open another terminal and go to directory ProjectShop.
5. Run `python manage.py runserver` or `make run`

## Git Flow<a name="Git_Flow"></a>

We have a master(main), development(dev), and feature branches.

All feature branches must be merged into the dev branch!

Only the release should merge into the main branch!!!

![Github flow](https://camo.githubusercontent.com/3e34f7a8d05c9d273965596db7c7b30f111b1d4990aa2ac47cb9792cfcb2b70b/68747470733a2f2f7761632d63646e2e61746c61737369616e2e636f6d2f64616d2f6a63723a62353235396363652d363234352d343966322d623839622d3938373166396565336661342f30332532302832292e7376673f63646e56657273696f6e3d31333132)

All feature branches must be tested before being merged!

All feature branches should start from prefix `feature#XXX-YYY` - where XXX - number of issue and YYY - short
description of the task e.g., feature-#17-Create_README

Don't push features into the main directly!

You should have at least three approves from teammates and final approval from a technical expert before merging your feature.

### How we add features<a name="How_we_add_features"></a>

1. Clone this repo to your local machine using `https://github.com/kolyasalubov/ProjectShop.git`
2. Create a new feature branch from dev.
3. Add some commits to your new branch.
4. Create a new pull request to the dev branch using `https://github.com/kolyasalubov/ProjectShop/compare/`
5. Request review from teammates and wait for at least three approves from teammates
and final approval from a technical expert before merging your feature.
6. Resolve conflicts and merge the feature branch into dev.
7. Run dev to check if all is correct.

___

## Issue Flow<a name="Issue_Flow"></a>

1. Go to [issues](https://github.com/kolyasalubov/ProjectShop/issues) and click `New issue` button.
2. When creating an issue, you should add the name of the issue, description, choose assignee, label, project. If issue is
   a `User Story`, you should link it with corresponding tasks, which should be linked to the issue.
3. If an issue is in work, it should be placed in the right column on the dashboard according to its status.
4. When work on the issue is finished, it should be placed in `Done` column.
___

## Developer Team<a name="Developer_team"></a>

[![@MykhailoGrynenko](https://avatars.githubusercontent.com/u/56480204?s=200&?v=4)](https://github.com/MykhailoGrynenko)
[![OlehHnyp](https://avatars.githubusercontent.com/u/75254063?s=200&?s=200&?v=4)](https://github.com/OlehHnyp)
[![@Maxgioman](https://avatars.githubusercontent.com/u/43215127?s=200&?v=4)](https://github.com/Maxgioman)
[![@v-lavrushko](https://avatars.githubusercontent.com/u/29904652?s=200&?v=4)](https://github.com/v-lavrushko)
[![@ProkhvatylovArtem](https://avatars.githubusercontent.com/u/89210528?s=200&?v=4)](https://github.com/ProkhvatylovArtem)
[![@Andriisas](https://avatars.githubusercontent.com/u/48296925?s=200&?v=4)](https://github.com/Andriisas)
[![@kushnir-tadey](https://avatars.githubusercontent.com/u/74568824?s=200&?v=4)](https://github.com/kushnir-tadey)
[![@CheshirLvova](https://avatars.githubusercontent.com/u/36841164?s=200&?v=4)](https://github.com/CheshirLvova)
[![@Oleg-Smal-git](https://avatars.githubusercontent.com/u/78323776?s=200&?v=4)](https://github.com/Oleg-Smal-git)
[![@ruslanliska](https://avatars.githubusercontent.com/u/78071321?s=200&?v=4)](https://github.com/ruslanliska)
[![@Roman Levytskyi](https://avatars.githubusercontent.com/u/64426960?s=200&?v=4)](https://github.com/l3va)
[![@VladKriuch](https://avatars.githubusercontent.com/u/89203925?s=200&?v=4)](https://github.com/VladKriuch) 
