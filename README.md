# Ngx (Angular2+) HTML Syntax for SublimeText

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
- in `{{1 + 2}}` interpolations, you should see JS syntax highlighting as well

## And...

Now it supports Angular control flow.

```
@for (item of items) {
  <a [href]="item.link">{{item.title}}</a>
} @empty {
  <p>No Items</p>
}
```

```
@if (users$ | async; as users) {
  {{ users.length }}
}
```

```
@if (a > b) {
  {{a}} is greater than {{b}}
} @else if (b > a) {
  {{a}} is less than {{b}}
} @else {
  {{a}} is equal to {{b}}
}
```

```
@switch (condition) {
  @case (caseA) {
    Case A.
  }
  @case (caseB) {
    Case B.
  }
  @default {
    Default case.
  }
}
```

## How to use

The syntax is listed as `Ngx HTML` in Sublime syntax selection list.

I personaly use [ApplySyntax](https://github.com/facelessuser/ApplySyntax) plugin
with the following setting:

```json
"syntaxes": [
    {
        "syntax": "Ngx HTML/NgxHTML",
        "extensions": ["component.html"],
    },
]
```

You could use it in other ways...
e.g. set it as the default syntax for all html files, since it's a superset of the html syntax anyway.
