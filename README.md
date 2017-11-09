# Ngx/Angular2 HTML Syntax for SublimeText

based on the official sublime html syntax

### Features

So that it's not broken when there are

- `[input]`
- `[@animation]`
- `(output)`
- `(@animation.event)`
- `#reference`
- `*template`
- `[(bananaBox)]`

attributes on the tags

### How to use

The syntax is listed as `Ngx HTML` in Sublime syntax selection list.

I personaly use [ApplySyntax](https://github.com/facelessuser/ApplySyntax) plugin
with the following setting:

```json
"syntaxes": [
    {
        "syntax": "Angular2 HTML Syntax/Angular2HTML",
        "extensions": ["component.html"],
    },
]
```

You could use it in other way...
e.g. set it as the default syntax for all html files, since it's a superset of the html syntax anyway.

### Package name

The package was created during the Angular 2 time, hence the name.
I will eventually rename it to `Ngx` in package control.
