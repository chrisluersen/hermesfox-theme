-- WezTerm config: HERMES layout variant (Hermes-first)
-- Mirrors wezterm.lua but spawns zellij with --layout hermes (Hermes TUI fills
-- the tab at 100%; nvim summoned as a floating scratchpad via Ctrl+o then e).
-- Used by the "Hermes (Hermes)" shortcuts.
-- Renamed from wezterm-herm.lua 2026-08-12 (layout herm -> hermes).
-- FIXED 2026-08-12: path was double-escaped (C:\\\\Users...), which rendered
-- as a literal double backslash and broke the launcher. Single-escape now.
-- 2026-08-11 (v5): same stack as dev — WezTerm -> zellij -> layout "hermes".
local wezterm = require 'wezterm'

-- Zellij launcher path derived from env (portable — no hardcoded user dir).
local zellij = os.getenv('LOCALAPPDATA') .. '\\Zellij\\zellij.exe'

-- Launch zellij with the hermes layout (Hermes-first research layout).
wezterm.on('gui-startup', function()
  wezterm.mux.spawn_window({
    args = { zellij, '--layout', 'hermes' }
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
