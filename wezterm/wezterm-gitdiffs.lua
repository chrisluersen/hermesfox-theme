-- WezTerm config for Chris: GITDIFFS layout variant (PR/MR diff review)
-- Mirrors wezterm.lua but spawns zellij with --layout gitdiffs
-- (nvim+lazygit LEFT, hermes --tui RIGHT for drafting the review).
-- Used by the "Hermes (Git Diffs)" Start Menu shortcut. Kept separate from
-- wezterm.lua so the daily dev launch (default_layout "dev") stays untouched.
-- 2026-08-11 (v1, as review): work-mode layout for reviewing GitHub PR/MR diffs.
-- 2026-08-12: renamed review -> gitreview, then gitreview -> gitdiffs.
local wezterm = require 'wezterm'

-- Launch zellij with the gitdiffs layout (nvim+lazygit left, hermes right).
wezterm.on('gui-startup', function()
  wezterm.mux.spawn_window({
    args = { 'C:\\\\Users\\\\chris\\\\AppData\\\\Local\\\\Zellij\\\\zellij.exe', '--layout', 'gitdiffs' }
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
