-- WezTerm config for Chris: NOTES layout variant (minimalist md/txt editor)
-- Mirrors wezterm.lua but spawns zellij with --layout notes
-- (yazi file viewer LEFT, nvim editor MIDDLE, glow markdown preview RIGHT).
-- Used by the "Hermes (Notes)" Start Menu shortcut. Kept separate from
-- wezterm.lua so the daily dev launch (default_layout "dev") stays untouched.
-- 2026-08-11 (v1): work-mode layout for reading/writing notes and markdown.
local wezterm = require 'wezterm'

-- Launch zellij with the notes layout (yazi | nvim | glow).
wezterm.on('gui-startup', function()
  wezterm.mux.spawn_window({
    args = { 'C:\\Users\\chris\\AppData\\Local\\Zellij\\zellij.exe', '--layout', 'notes' }
  })
end)

return {
  -- Hermes pet/kitty protocol detection (TERM_PROGRAM is not set by Windows WezTerm)
  set_environment_variables = {
    TERM_PROGRAM = 'wezterm',
  },

  font_size = 10.0,
  font = wezterm.font('Hack Nerd Font Mono', { weight = 'Regular' }),
  enable_kitty_graphics = true, -- kitty protocol (iTerm2 path used by hermes pet; kitty a=T broken in 20240203)
  color_scheme = 'carbonfox', -- matches nvim + zellij carbonfox theme
  initial_cols = 170,
  initial_rows = 45,
  window_decorations = 'RESIZE | TITLE',
  window_close_confirmation = 'NeverPrompt',
  default_cwd = wezterm.home_dir,
}
