# Mu: A Python Code Editor

![Mu's logo](logo.png "Code with Mu!")

This is an experimental version of [Mu](https://codewith.mu) made with
Microsoft's [Monaco code editor](https://microsoft.github.io/monaco-editor/).
Packaged via [Electron](https://www.electronjs.org/).


```eval_rst
.. note::

    **This documentation is NOT for users of Mu**. Rather, it is for software
    developers who want to improve Mu. Read on if that's you!

    For tutorials, how-to guides and user related discussion, please see the
    project's website for users of Mu at: https://codewith.mu/

    If you're interested in the fun, educational, inspiring and sometimes
    hilarious ways in which people use Mu, check out: https://madewith.mu/
```

## Developer Setup

You must have `node` and `npm` installed for your operating system. We use
Python (3.6+) for scripting various aspects of the project, so this will also
need to be installed.

1. Make a Python virtualenv and install the Python requirements via pip:
   `pip install -r requirements.txt`
2. Use the `make` command to install the Electron dependencies: `make setup`
3. Check everything works by running the test suite: `make test`
4. Run the application locally with: `make run`

Most other aspects of developing the project are scripted via the `make`
command. Typing `make` on its own will give you a list of all available
commands.

## What?

Mu is a very simple Python editor for kids, teachers and beginner programmers.
It's written in Python and works on Windows, OSX, Linux and the web.

> "[Papert] realized, 'Oh, we could take the real content out here as a
> version in the child's world that is still the real thing.' It's not a fake
> version of math. It's kind of like little league, or even T-ball. In sports
> they do this all the time. In music, they do it all the time. The idea is,
> you never let the child do something that isn't the real thing -- but you
> have to work your ass off to figure out what the real thing is in the
> context of the way their minds are working at that developmental level."
> -- [Alan Kay](https://www.fastcompany.com/40435064/what-alan-kay-thinks-about-the-iphone-and-technology-now)

Mu aspires to be "the real thing" as a development environment for beginner
programmers taking their first steps with Python.

As a rule of thumb, if you're able to ask "why doesn't Mu have [feature X]?"
then you're probably too advanced for using Mu as a development environment. In
which case, you should graduate to a more advanced editor.

## Why?

There isn't a cross platform Python code editor that is:

* Easy to use;
* Available on all major platforms;
* Well documented (even for beginners);
* Simply coded;
* Currently maintained; and,
* Thoroughly tested.

Mu addresses these needs.

## How?

Mu's outlook is:

* Less is more (remove all unnecessary distractions);
* Keep it simple (so Mu is easy to understand);
* Walk the path of least resistance (Mu should be easy to use);
* Have fun (learning should be a positive experience).

## Who?

**You!**

Contributions are welcome without prejudice from *anyone* irrespective of
age, gender, religion, race or sexuality. If you're thinking, "but they don't
mean me", *then we especially mean YOU*. Good quality code and engagement
with respect, humour and intelligence wins every time.

Read about [contributing](contributing.md) and perhaps try out some
[first-steps](first-steps.md).

We want the Mu community to be a friendly place. Therefore, we expect
contributors to abide by the spirit of our
[Code of Conduct](code_of_conduct.md).

## Contents

```eval_rst
.. toctree::
   :maxdepth: 2

   contributing.md
   code_of_conduct.md
   first-steps.md
   user-experience.md
   architecture.md
   translations.md
   website.md
   authors.md
   copyright.md
```
