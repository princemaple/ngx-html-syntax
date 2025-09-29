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
@let myVar = myObservable | async;
```

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

## Angular Imports Folding

This package now includes functionality to fold import statements and import arrays in Angular TypeScript files to improve code readability.

### Features

- **Optional Automatic Folding**: When enabled, automatically folds import statements and import arrays when opening `.ts` files
- **Separate Control**: Independent commands to fold/unfold import statements vs import arrays
- **Smart Detection**: Groups import statements intelligently and only processes Angular files for import arrays
- **Manual Commands**: Multiple commands for fine-grained control
- **Non-Intrusive**: Auto-folding is disabled by default and must be explicitly enabled

### Usage

#### Enable Auto-Folding

Auto-folding is **disabled by default**. To enable it:

1. Go to `Preferences > Package Settings > NgxHTML > Settings`
2. Set `"auto_fold_angular_imports": true`

#### Manual Commands

Access these commands via Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`):

- **Angular Imports: Fold Import Statements** - Fold import statements at top of file
- **Angular Imports: Fold Import Arrays** - Fold imports arrays in Angular decorators
- **Angular Imports: Fold All Imports** - Fold both import statements and arrays
- **Angular Imports: Unfold Import Statements** - Unfold import statements only
- **Angular Imports: Unfold Import Arrays** - Unfold import arrays only
- **Angular Imports: Unfold All Imports** - Unfold everything

#### How It Works

**Import Statements Folding**:
1. Processes all `.ts` files
2. Finds import statements at the top of the file
3. Groups consecutive imports, separated by blank lines or comments
4. Leaves the first import of each group visible

**Import Arrays Folding**:
1. Looks for `@Component` or `@Directive` decorators
2. Finds `imports: [` patterns within decorators
3. Folds the content between the brackets

#### Examples

**Import Statements (Before)**:
```typescript
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';

import { MyService } from './my-service';
import { UtilsService } from '../utils/utils.service';
```

**Import Statements (After)**:
```typescript
import { CommonModule } from '@angular/common';
[•••]

import { MyService } from './my-service';
[•••]
```

**Import Arrays (Before)**:
```typescript
@Component({
  selector: 'app-example',
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MyComponent
  ],
  templateUrl: './example.component.html'
})
```

**Import Arrays (After)**:
```typescript
@Component({
  selector: 'app-example',
  imports: [•••],
  templateUrl: './example.component.html'
})
```

## How to use syntax

The syntax is listed as `Ngx HTML` in Sublime syntax selection list.

You could use [ApplySyntax](https://github.com/facelessuser/ApplySyntax) plugin
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
e.g. set it as the default syntax for all html files, since it's a superset of the default html syntax anyway.
