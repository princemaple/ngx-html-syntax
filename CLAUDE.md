# Project: Ngx HTML Syntax for Sublime Text

## Overview
A Sublime Text syntax highlighting package for Angular 2+ HTML templates. Extends the default HTML syntax to support Angular-specific features.

## Key Files
- `NgxHTML.sublime-syntax` - Main syntax definition (YAML 1.2 format)
- `tests/syntax_test_scopes.component.html` - Syntax test file
- `Embeddings/*.sublime-syntax` - Embedded syntax definitions for CSS, HTML, RegExp in template strings

## Syntax File Structure
The syntax file (`NgxHTML.sublime-syntax`) is organized into sections:
- HTML Customizations (extends base HTML)
- Angular Directives (`*ngIf`, `[bind]`, `(event)`, `[(twoWay)]`, `#ref`)
- Angular Declarations (`@let`)
- Angular Statements (`@if`, `@for`, `@switch`, `@case`, `@defer`, etc.)
- Angular Expressions (arrays, objects, functions, operators, literals)
- Angular Variables and property access

## Testing
- Tests run via GitHub Actions using `SublimeText/syntax-test-action@v2`
- Test file uses Sublime Text syntax test format with `<!-- ^ scope.name -->` assertions
- Column positions in test assertions must align exactly with the code being tested
- The `^` marker points to the same column in the line above (1-indexed)

## Scope Naming Conventions
- `keyword.operator.spread.ngx` - Spread operator `...`
- `keyword.control.conditional.*.ngx` - Control flow keywords
- `punctuation.section.*.ngx` - Brackets and delimiters
- `punctuation.separator.*.ngx` - Commas and separators
- `variable.other.*.ngx` - Variables
- `meta.*.ngx` - Meta scopes for regions

## Build/CI
- GitHub Actions workflow in `.github/`
- Uses Sublime Text build 4180 for syntax tests
- No local test runner required; tests run in CI

## Common Patterns
When adding new syntax support:
1. Add pattern to appropriate section in `NgxHTML.sublime-syntax`
2. Use `include: ng-<context>` to compose contexts
3. Add tests in `tests/syntax_test_scopes.component.html`
4. Ensure test `^` markers align with exact column positions
