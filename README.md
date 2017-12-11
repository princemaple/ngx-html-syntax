# Ngx/Angular2 HTML Syntax for SublimeText

based on the official sublime html syntax

## Features

So that it's not broken when there are

- `[input]`
- `[@animation]`
- `(output)`
- `(@animation.event)`
- `#reference`
- `*template`
- `[(bananaBox)]`

attributes on the tags

## Plus

Highlighting the JS part as JS. So,

- in `[myBinding]="myVar"`, you should see `myVar` as an JS variable instead of string content
    - i.e. `myVar` should be highlighted differently from `"`s
- in `*ngFor="let column of columns"`, you should see `let` and `of` highlighted as keywords
- in `(change)="update()"`, you should see `update` as function name
- in `a && b` within an Angular expression, you should see `&&` correctly highlighted as the JS operator instead of an error you would see in normal HTML syntax.

## How to use

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

## Package name

The package was created during the Angular 2 time, hence the name.
I will eventually rename it to `Ngx` in package control.
