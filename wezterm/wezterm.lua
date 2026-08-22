-- WezTerm config for Chris (Hermes Agent TUI host)
-- 2026-08-11: added to make Hermes' kitty-graphics detection fire on Windows.
--   Hermes checks TERM_PROGRAM == "wezterm" / WEZTERM_PANE (agent/pet/render.py);
--   the Windows stable build doesn't set them by default, so we inject them here.
-- 2026-08-11 (v5): FINAL STACK = WezTerm -> zellij -> layout. zellij is the
--   multiplexer. Its default_layout "dev" (AppData/Roaming/Zellij/config) opens
--   neovim LEFT 60% + hermes --tui RIGHT 40%. Per-mode variants (herm/review/notes)
--   live in wezterm-<mode>.lua, each spawning `zellij --layout <mode>`.
local wezterm = require 'wezterm'

-- Launch the zellij workspace on GUI start. zellij reads default_layout "dev"
-- from C:\Users\chris\AppData\Roaming\Zellij\config\config.kdl.
wezterm.on('gui-startup', function()
  wezterm.mux.spawn_window({ args = { 'C:\\Users\\chris\\AppData\\Local\\Zellij\\zellij.exe' } })
end)

return {
  -- Hermes pet/kitty protocol detection (see above)
  set_environment_variables = {
    TERM_PROGRAM = 'wezterm',
  },

  font_size = 10.0,
  font = wezterm.font('Hack Nerd Font Mono', { weight = 'Regular' }),
  enable_kitty_graphics = true, -- kitty protocol (iTerm2 path used by hermes pet; kitty a=T broken in 20240203)
  color_scheme = 'carbonfox', -- matches nvim nightfox/carbonfox + zellij carbonfox theme
  -- 2026-08-12: open generous (170x45) so the dev 55/45 split gives hermes
  -- enough width for un-wrapped lines. Fits the 2560x1440 panel at DPI scale.
  initial_cols = 170,
  initial_rows = 45,
  -- Windows Terminal-ish feel: dark, no title noise
  window_decorations = 'RESIZE | TITLE',
  window_close_confirmation = 'NeverPrompt',
  default_cwd = wezterm.home_dir,
}
