# Palette and source lineage

Tokencat is an upgraded **Carbonfox-derived** bundle, not a pixel-perfect Lualine port. `palette.json` preserves the shipped Carbonfox reference at theme revision `793dcd583c873a7512c6d2a5222d4d0b697f704c`; `palettes/tokencat.json` preserves every one of those base values and adds named roles. The original reference already includes adaptations. It must not be described as identical to every upstream Nightfox value.

## Pinned source chain

Original inspiration: [Carbonfox Lualine entry](https://github.com/EdenEast/nightfox.nvim/blob/main/lua/lualine/themes/carbonfox.lua).

Pinned Nightfox revision: `4dacd3f0185a2227bdf3b6c0975a8f0bf87cac9a`:

- [Lualine wrapper](https://github.com/EdenEast/nightfox.nvim/blob/4dacd3f0185a2227bdf3b6c0975a8f0bf87cac9a/lua/lualine/themes/carbonfox.lua)
- [Shared Lualine adapter](https://github.com/EdenEast/nightfox.nvim/blob/4dacd3f0185a2227bdf3b6c0975a8f0bf87cac9a/lua/nightfox/util/lualine.lua)
- [Carbonfox palette and generated spec](https://github.com/EdenEast/nightfox.nvim/blob/4dacd3f0185a2227bdf3b6c0975a8f0bf87cac9a/lua/nightfox/palette/carbonfox.lua)
- [Upstream license](https://github.com/EdenEast/nightfox.nvim/blob/4dacd3f0185a2227bdf3b6c0975a8f0bf87cac9a/LICENSE), copied completely to [nightfox-MIT.txt](../licenses/nightfox-MIT.txt).

The wrapper delegates to the adapter. Its active mode band uses dark `s.bg0` text on a mode color, the secondary band blends that color into `s.bg0`, and inactive bands use dark background with subdued text. Normal uses blue; insert uses green; visual uses `p.magenta.base` (Carbonfox purple `#be95ff`). Command, replace and terminal use upstream yellow, red and orange respectively. Hermes has semantic status states, not Vim editing modes: Tokencat retains a dark status background, readable light text and distinct status accents rather than inventing modes or copying inverted bands into unrelated states. These are documented adaptations, not proven Lualine rendering equivalence.

## Deliberate differences

| Role | Preserved reference | Tokencat use |
|---|---|---|
| Muted source | `muted: #7f8489` | `muted_accessible: #97999b` for readable secondary text/comments and selected dark surfaces |
| Reasoning source | `thinking: #8c6fb9` | `thinking_accessible: #a184d0` for reasoning on background and raised surface |
| Warning extension | `orange: #ff9e64` | Keep the shipped warm warning; Nightfox's token named orange is teal `#3ddbd9` |
| Success green | Shipped `green: #25be6a` | Preserved; matches pinned Nightfox's base green |
| Word-diff backgrounds | Existing reference values unchanged | `diff_add_word_bg: #1a3525` / `diff_remove_word_bg: #462535` in VS Code preserve body and syntax-comment readability; added words have an explicit green border |
| VS Code suggestion selection | Legacy export unchanged | Explicit selected text uses `foreground: #f2f4f8`; focused matches use `cyan_bright: #3ddbd9` on `border: #525253`, while unfocused matches retain blue |
| Decorative borders | `border: #525253` | Not falsely treated as body-text AA; focus uses blue |
| Dashboard | No legacy export exists | Separate YAML with explicit semantic overrides; backend normalization must retain them |

The palette includes additional explicit ANSI and editor-role tokens because app schemas differ. `exports` maps every authored hex leaf to a base token, rejects drift and unmapped colors, and shares strict duplicate-key-aware JSON/YAML parsers. No runtime generator or new theming framework is introduced. Dashboard `warmGlow` is the intentional non-hex exception: transparent `rgba(0, 0, 0, 0)`, with zero noise; tests pin both.

Contrast tests calculate WCAG sRGB luminance for named normal-text, diff-word and VS Code suggestion-state pairs in both upgrade exports. Word-diff guards cover every emitted syntax foreground, including comments, against both opaque word backgrounds. The added-word border clears 3:1 against both word and line backgrounds so the darker green highlight remains distinguishable. Focused suggestion matches use `editorSuggestWidget.focusHighlightForeground`, not the unfocused `highlightForeground` role; selected-state colors are explicit rather than assumed from host defaults. Tests are not a guarantee for every terminal rendering, anti-aliasing mode or effective UI state. Runtime/selection-state checks remain separate. Legacy files intentionally retain their original appearance and limitations.
