// Markdown Editor with Toolbar
document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('markdown-editor');
    if (!textarea) return;

    // Create editor container
    const container = document.createElement('div');
    container.className = 'w-full';

    // Create toolbar
    const toolbar = document.createElement('div');
    toolbar.className = 'flex flex-wrap items-center gap-1 p-3 bg-primary rounded-t-lg';
    toolbar.innerHTML = `
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('**', '**')" title="Bold">
            <strong>B</strong>
        </button>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('*', '*')" title="Italic">
            <em>I</em>
        </button>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('~~', '~~')" title="Strikethrough">
            <s>S</s>
        </button>
        <div class="divider divider-horizontal mx-1 h-6"></div>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('# ', '')" title="Heading 1">
            H1
        </button>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('## ', '')" title="Heading 2">
            H2
        </button>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('### ', '')" title="Heading 3">
            H3
        </button>
        <div class="divider divider-horizontal mx-1 h-6"></div>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('> ', '')" title="Quote">
            " "
        </button>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('- ', '')" title="List">
            •
        </button>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('1. ', '')" title="Numbered List">
            1.
        </button>
        <div class="divider divider-horizontal mx-1 h-6"></div>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('[', '](url)')" title="Link">
            <i class="ti ti-link"></i>
        </button>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('![', '](url)')" title="Image">
            <i class="ti ti-photo"></i>
        </button>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('\`', '\`')" title="Code">
            &lt;/&gt;
        </button>
        <button type="button" class="btn btn-ghost btn-sm text-primary-content hover:bg-primary-content/20" onclick="insertText('\`\`\`\\n', '\\n\`\`\`')" title="Code Block">
            { }
        </button>
    `;

    // Create status bar
    const statusBar = document.createElement('div');
    statusBar.className = 'flex justify-between px-3 py-2 bg-base-300 rounded-b-lg text-xs text-base-content/60';
    statusBar.innerHTML = '<span id="char-count">0 characters</span><span>Markdown supported</span>';

    // Style the textarea
    textarea.classList.add('rounded-none', 'border-x-0', 'focus:outline-none');
    textarea.classList.remove('textarea-bordered');

    // Insert toolbar before textarea
    textarea.parentNode.insertBefore(container, textarea);
    container.appendChild(toolbar);
    container.appendChild(textarea);
    container.appendChild(statusBar);

    // Add placeholder
    textarea.placeholder = `Write your amazing blog post here...

## Start writing!

Use **bold**, *italic*, and other markdown features.

### Tips:
- Use # for headings
- Use **text** for bold
- Use *text* for italic
- Use [text](url) for links
- Use ![alt](url) for images`;

    // Character count
    function updateCharCount() {
        const count = textarea.value.length;
        document.getElementById('char-count').textContent = count + ' characters';
    }

    textarea.addEventListener('input', updateCharCount);
    updateCharCount();

    // Global function for toolbar buttons
    window.insertText = function(before, after) {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const selectedText = textarea.value.substring(start, end);
        const newText = before + selectedText + after;

        textarea.value = textarea.value.substring(0, start) + newText + textarea.value.substring(end);

        // Set cursor position
        const newCursorPos = start + before.length + selectedText.length;
        textarea.setSelectionRange(newCursorPos, newCursorPos);
        textarea.focus();
        updateCharCount();
    };

    // Keyboard shortcuts
    textarea.addEventListener('keydown', function(e) {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'b':
                    e.preventDefault();
                    insertText('**', '**');
                    break;
                case 'i':
                    e.preventDefault();
                    insertText('*', '*');
                    break;
                case 'k':
                    e.preventDefault();
                    insertText('[', '](url)');
                    break;
            }
        }

        // Tab support
        if (e.key === 'Tab') {
            e.preventDefault();
            insertText('    ', '');
        }
    });
});
