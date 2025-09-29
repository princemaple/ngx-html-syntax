import sublime
import sublime_plugin
import re


class FoldAngularImportsListener(sublime_plugin.EventListener):
    """
    Sublime Text plugin that optionally folds imports in Angular TypeScript files.

    When auto-folding is enabled and opening a .ts file that contains @Component or @Directive decorator,
    it will:
    1. Find and fold the imports array in the decorator to keep the file more readable
    2. Find and fold consecutive chunks of import statements at the top of the file

    Import chunks are automatically detected and grouped (e.g., Angular imports,
    library imports, local project imports) based on blank lines or comment separators.
    """

    def on_load_async(self, view):
        """Called when a file is loaded"""
        if self.should_auto_fold(view):
            self.fold_angular_imports(view)

    def on_activated_async(self, view):
        """Called when a view gains input focus"""
        # Only fold if not already processed and auto-folding is enabled
        if self.should_auto_fold(view) and not view.settings().get("angular_imports_folded", False):
            self.fold_angular_imports(view)

    def should_auto_fold(self, view):
        """Check if auto-folding should be enabled for this view"""
        # Check package settings for auto-folding preference
        settings = sublime.load_settings("NgxHTML.sublime-settings")
        auto_fold_enabled = settings.get("auto_fold_angular_imports", False)
        
        if not auto_fold_enabled:
            return False
            
        # Check if it's a TypeScript file
        return self.is_typescript_file(view)

    def fold_angular_imports(self, view):
        """Main method to detect Angular files and fold imports array"""
        # Check if it's a TypeScript file
        if not self.is_typescript_file(view):
            return

        # Get the entire file content
        file_content = view.substr(sublime.Region(0, view.size()))

        folded_something = False

        # Find and fold the imports array (only in Angular files)
        if self.is_angular_file(file_content):
            imports_region = self.find_imports_array(view, file_content)
            if imports_region:
                view.fold(imports_region)
                view.settings().set("import_arrays_folded", True)
                folded_something = True
        
        # Find and fold import statement chunks at the top (for all TypeScript files)
        import_chunks = self.find_import_chunks(view, file_content)
        if import_chunks:
            for chunk in import_chunks:
                view.fold(chunk)
            view.settings().set("import_statements_folded", True)
            folded_something = True
        
        if folded_something:
            view.settings().set("angular_imports_folded", True)

    def is_typescript_file(self, view):
        """Check if the current file is a TypeScript file"""
        file_name = view.file_name()
        if not file_name:
            return False
        return file_name.endswith(".ts")

    def is_angular_file(self, content):
        """Check if the file contains @Component or @Directive decorators"""
        return bool(re.search(r"@(Component|Directive)\s*\(", content))

    def find_imports_array(self, view, content):
        """Find the imports array and return its region for folding"""
        # Pattern to match the imports array line
        imports_pattern = r"(\s+imports:\s*\[)"

        match = re.search(imports_pattern, content)
        if not match:
            return None

        # Get the position of the opening bracket
        bracket_start = match.end() - 1  # Position of the opening bracket '['
        
        # Find the matching closing bracket
        bracket_count = 0
        pos = bracket_start  # Start from the opening bracket

        while pos < len(content):
            char = content[pos]
            if char == "[":
                bracket_count += 1
            elif char == "]":
                bracket_count -= 1
                if bracket_count == 0:
                    # Found the matching closing bracket
                    # Fold from after the opening bracket to before the closing bracket
                    fold_start = bracket_start + 1  # After the '['
                    fold_end = pos  # Before the ']'
                    
                    # Only fold if there's content between brackets
                    if fold_end > fold_start:
                        return sublime.Region(fold_start, fold_end)
                    else:
                        return None
            pos += 1

        return None

    def find_import_chunks(self, view, content):
        """Find chunks of import statements and return regions for folding"""
        lines = content.split('\n')
        chunks = []
        current_chunk_start = None
        current_chunk_end = None
        in_multiline_import = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped_line = line.strip()
            
            # Check if this is a single-line import
            is_single_line_import = (stripped_line.startswith('import ') and 
                                   ' from ' in stripped_line and
                                   not stripped_line.startswith('//') and
                                   not stripped_line.startswith('/*'))
            
            # Check if this starts a multi-line import
            is_multiline_import_start = (stripped_line.startswith('import ') and 
                                       ' from ' not in stripped_line and
                                       '{' in stripped_line and
                                       not stripped_line.startswith('//') and
                                       not stripped_line.startswith('/*'))
            
            # Check if we're continuing a multi-line import
            is_multiline_import_continuation = in_multiline_import
            
            # Check if this ends a multi-line import
            is_multiline_import_end = in_multiline_import and ' from ' in stripped_line
            
            is_import_line = (is_single_line_import or 
                            is_multiline_import_start or 
                            is_multiline_import_continuation or
                            is_multiline_import_end)
            
            # Update multiline import state
            if is_multiline_import_start:
                in_multiline_import = True
            elif is_multiline_import_end:
                in_multiline_import = False
            
            if is_import_line:
                if current_chunk_start is None:
                    # Start of a new chunk
                    current_chunk_start = i
                current_chunk_end = i
            else:
                # Check if this is a blank line or comment that could separate chunks
                is_separator = (stripped_line == '' or 
                              stripped_line.startswith('//') or 
                              stripped_line.startswith('/*') or
                              stripped_line.startswith('*'))
                
                if current_chunk_start is not None and not is_separator:
                    # End of current chunk - create fold if chunk has multiple lines
                    if current_chunk_end > current_chunk_start:
                        chunk_region = self.lines_to_region(view, content, current_chunk_start, current_chunk_end)
                        if chunk_region:
                            chunks.append(chunk_region)
                    current_chunk_start = None
                    current_chunk_end = None
                    
                    # Stop if we hit substantial non-import content (not just separators)
                    if not is_separator:
                        break
                elif current_chunk_start is not None and is_separator:
                    # We're in a chunk and hit a separator - end current chunk and prepare for next
                    if current_chunk_end > current_chunk_start:
                        chunk_region = self.lines_to_region(view, content, current_chunk_start, current_chunk_end)
                        if chunk_region:
                            chunks.append(chunk_region)
                    current_chunk_start = None
                    current_chunk_end = None
            
            i += 1
        
        # Handle case where file ends with imports
        if current_chunk_start is not None and current_chunk_end > current_chunk_start:
            chunk_region = self.lines_to_region(view, content, current_chunk_start, current_chunk_end)
            if chunk_region:
                chunks.append(chunk_region)
        
        return chunks

    def lines_to_region(self, view, content, start_line, end_line):
        """Convert line numbers to a Sublime Text region, leaving first import visible"""
        lines = content.split('\n')
        
        # Only fold if there's more than one import (need at least 2 lines to fold)
        if end_line <= start_line:
            return None
            
        # Find where the first import statement ends
        first_import_end = start_line
        in_multiline_import = False
        
        for i in range(start_line, end_line + 1):
            line = lines[i].strip()
            
            # Check if this starts a multi-line import
            if line.startswith('import ') and '{' in line and ' from ' not in line:
                in_multiline_import = True
            
            # If we're in a multi-line import, keep going until we find the 'from' line
            if in_multiline_import:
                if ' from ' in line:
                    first_import_end = i
                    break
            else:
                # Single line import - this line is the complete import
                if line.startswith('import ') and ' from ' in line:
                    first_import_end = i
                    break
        
        # Start folding from the line after the first complete import
        fold_start_line = first_import_end + 1
        
        # Make sure we have something to fold
        if fold_start_line > end_line:
            return None
        
        # Calculate character positions
        fold_start_pos = sum(len(lines[i]) + 1 for i in range(fold_start_line))  # +1 for newline
        fold_end_pos = sum(len(lines[i]) + 1 for i in range(end_line + 1)) - 1  # -1 to not include final newline
        
        # Only fold if there's actual content
        if fold_end_pos > fold_start_pos:
            return sublime.Region(fold_start_pos, fold_end_pos)
        
        return None


class FoldImportStatementsCommand(sublime_plugin.TextCommand):
    """Command to manually fold import statements only"""

    def run(self, edit):
        if not self.is_typescript_file():
            return

        content = self.view.substr(sublime.Region(0, self.view.size()))
        listener = FoldAngularImportsListener()
        
        # Find and fold import statement chunks only
        import_chunks = listener.find_import_chunks(self.view, content)
        for chunk in import_chunks:
            self.view.fold(chunk)
        
        if import_chunks:
            self.view.settings().set("import_statements_folded", True)

    def is_enabled(self):
        return self.is_typescript_file()
    
    def is_typescript_file(self):
        file_name = self.view.file_name()
        return file_name and file_name.endswith(".ts")


class FoldImportArraysCommand(sublime_plugin.TextCommand):
    """Command to manually fold imports arrays in Angular decorators only"""

    def run(self, edit):
        if not self.is_angular_file():
            return

        content = self.view.substr(sublime.Region(0, self.view.size()))
        listener = FoldAngularImportsListener()
        
        # Find and fold the imports array only
        imports_region = listener.find_imports_array(self.view, content)
        if imports_region:
            self.view.fold(imports_region)
            self.view.settings().set("import_arrays_folded", True)

    def is_enabled(self):
        return self.is_angular_file()
    
    def is_angular_file(self):
        file_name = self.view.file_name()
        if not file_name or not file_name.endswith(".ts"):
            return False

        content = self.view.substr(sublime.Region(0, self.view.size()))
        return bool(re.search(r"@(Component|Directive)\s*\(", content))


class FoldAllImportsCommand(sublime_plugin.TextCommand):
    """Command to manually fold both import statements and import arrays"""

    def run(self, edit):
        listener = FoldAngularImportsListener()
        listener.fold_angular_imports(self.view)

    def is_enabled(self):
        file_name = self.view.file_name()
        return file_name and file_name.endswith(".ts")


class UnfoldImportStatementsCommand(sublime_plugin.TextCommand):
    """Command to unfold import statements only"""

    def run(self, edit):
        # Unfold all regions, but this is a limitation - Sublime doesn't allow selective unfolding
        # In practice, this will unfold everything, but we'll track the state
        self.view.unfold(sublime.Region(0, self.view.size()))
        self.view.settings().set("import_statements_folded", False)
        
        # Re-fold import arrays if they were previously folded
        if self.view.settings().get("import_arrays_folded", False):
            content = self.view.substr(sublime.Region(0, self.view.size()))
            listener = FoldAngularImportsListener()
            imports_region = listener.find_imports_array(self.view, content)
            if imports_region:
                self.view.fold(imports_region)

    def is_enabled(self):
        file_name = self.view.file_name()
        return file_name and file_name.endswith(".ts")


class UnfoldImportArraysCommand(sublime_plugin.TextCommand):
    """Command to unfold import arrays only"""

    def run(self, edit):
        # Unfold all regions, but this is a limitation - Sublime doesn't allow selective unfolding
        self.view.unfold(sublime.Region(0, self.view.size()))
        self.view.settings().set("import_arrays_folded", False)
        
        # Re-fold import statements if they were previously folded
        if self.view.settings().get("import_statements_folded", False):
            content = self.view.substr(sublime.Region(0, self.view.size()))
            listener = FoldAngularImportsListener()
            import_chunks = listener.find_import_chunks(self.view, content)
            for chunk in import_chunks:
                self.view.fold(chunk)

    def is_enabled(self):
        file_name = self.view.file_name()
        if not file_name or not file_name.endswith(".ts"):
            return False

        content = self.view.substr(sublime.Region(0, self.view.size()))
        return bool(re.search(r"@(Component|Directive)\s*\(", content))


class UnfoldAllImportsCommand(sublime_plugin.TextCommand):
    """Command to unfold all imports (both statements and arrays)"""

    def run(self, edit):
        # Unfold all regions in the current view
        self.view.unfold(sublime.Region(0, self.view.size()))
        self.view.settings().set("angular_imports_folded", False)
        self.view.settings().set("import_statements_folded", False)
        self.view.settings().set("import_arrays_folded", False)

    def is_enabled(self):
        file_name = self.view.file_name()
        return file_name and file_name.endswith(".ts")