-- ═══════════════════════════════════════════════════════════════════════
-- Neovim Config — AI Terminal Stack (zellij + nvim + herm)
-- Plugin manager: lazy.nvim
-- ═══════════════════════════════════════════════════════════════════════

-- Set C compiler for tree-sitter parser compilation (MinGW GCC, not MSVC)
vim.env.CC = "gcc"

-- Leader (must be set before lazy so mappings use it)
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- ── Basic options ─────────────────────────────────────────────────────
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.expandtab = true
vim.opt.shiftwidth = 2
vim.opt.tabstop = 2
vim.opt.smartindent = true
vim.opt.termguicolors = true
vim.opt.guifont = "Hack Nerd Font Mono:h10"
vim.opt.signcolumn = "yes"
vim.opt.updatetime = 250
vim.opt.splitright = true
vim.opt.splitbelow = true
-- Clipboard: use clip.exe + PowerShell on native Windows (no win32yank needed)
vim.g.clipboard = {
  name = "Windows",
  copy  = { ["+"] = "clip.exe",                                 ["*"] = "clip.exe" },
  paste = { ["+"] = 'powershell.exe -NoProfile -Command "Get-Clipboard -Raw"',
            ["*"] = 'powershell.exe -NoProfile -Command "Get-Clipboard -Raw"' },
  cache_enabled = 0,
}
vim.opt.clipboard = "unnamedplus"
vim.opt.mouse = "a"
vim.opt.timeoutlen = 300
vim.opt.scrolloff = 8

-- ── Bootstrap lazy.nvim ────────────────────────────────────────────────
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  local out = vim.fn.system({
    "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath,
  })
  if vim.v.shell_error ~= 0 then
    vim.api.nvim_echo(
      { { "Failed to clone lazy.nvim:\n", "ErrorMsg" }, { out, "WarningMsg" },
        { "\nPress any key to exit...", "MoreMsg" } }, true, { err = true })
    vim.fn.getchar()
    vim.cmd.quit()
  end
end
vim.opt.rtp:prepend(lazypath)

-- ── dadbod settings (must be set before plugin loads) ──────────────────
vim.g.db_ui_save_location = vim.fn.stdpath("config") .. "/db_queries"
vim.g.db_ui_use_nerd_fonts = 1
vim.g.db_ui_auto_execute_table_helpers = 1
vim.g.db_ui_show_database_icon = 1
vim.g.db_ui_win_position = "right"
vim.g.db_ui_winwidth = 40
-- Predefined connections (edit/extend as needed — also addable via :DBUI with `+`)
-- Example uses a per-user path: sqlite:///C:/Users/<USER>/db/test.sqlite
vim.g.dbs = {
  test_sqlite = "sqlite:///C:/Users/<USER>/db/test.sqlite",
}

-- ═══════════════════════════════════════════════════════════════════════
-- Plugins
-- ═══════════════════════════════════════════════════════════════════════
require("lazy").setup({

  -- ── Core ────────────────────────────────────────────────────────────
  { "nvim-lua/plenary.nvim" },

  -- ── Theme ───────────────────────────────────────────────────────────
  {
    "EdenEast/nightfox.nvim",
    priority = 1000,
    config = function()
      require("nightfox").setup({})
      vim.cmd.colorscheme("carbonfox")
    end,
  },

  -- ── LSP & Completion ────────────────────────────────────────────────
  {
    "williamboman/mason.nvim",
    config = function()
      require("mason").setup()
    end,
  },
  {
    "williamboman/mason-lspconfig.nvim",
    dependencies = { "williamboman/mason.nvim" },
    config = function()
      require("mason-lspconfig").setup({
        ensure_installed = {
          "lua_ls", "pyright", "rust_analyzer",
          "ts_ls", "bashls", "yamlls", "jsonls", "sqls",
        },
      })
    end,
  },
  {
    "neovim/nvim-lspconfig",
    dependencies = { "williamboman/mason-lspconfig.nvim" },
    config = function()
      -- Neovim 0.11+ API: vim.lsp.config() + vim.lsp.enable()
      -- (replaces deprecated require("lspconfig").server.setup())
      vim.lsp.config("lua_ls", {
        settings = { Lua = { diagnostics = { globals = { "vim" } } } },
      })
      vim.lsp.config("pyright", {})
      vim.lsp.config("rust_analyzer", {})
      vim.lsp.config("ts_ls", {})
      vim.lsp.config("bashls", {})
      vim.lsp.config("yamlls", {})
      vim.lsp.config("jsonls", {})
      vim.lsp.config("sqls", {})
      -- Enable all configured servers
      vim.lsp.enable({
        "lua_ls", "pyright", "rust_analyzer", "ts_ls",
        "bashls", "yamlls", "jsonls", "sqls",
      })
    end,
  },
  {
    "hrsh7th/nvim-cmp",
    dependencies = {
      "hrsh7th/cmp-nvim-lsp",
      "L3MON4D3/LuaSnip",
      "saadparwaiz1/cmp_luasnip",
      "rafamadriz/friendly-snippets",
    },
    config = function()
      local cmp = require("cmp")
      cmp.setup({
        snippet = {
          expand = function(args)
            require("luasnip").lsp_expand(args.body)
          end,
        },
        mapping = cmp.mapping.preset.insert({
          ["<C-Space>"] = cmp.mapping.complete(),
          ["<CR>"] = cmp.mapping.confirm({ select = true }),
          ["<Tab>"] = cmp.mapping.select_next_item(),
          ["<S-Tab>"] = cmp.mapping.select_prev_item(),
        }),
        sources = cmp.config.sources({
          { name = "nvim_lsp" },
          { name = "luasnip" },
        }),
      })
      -- Load friendly-snippets
      require("luasnip.loaders.from_vscode").lazy_load()
    end,
  },

  -- ── Telescope (fuzzy finder) ────────────────────────────────────────
  {
    "nvim-telescope/telescope.nvim",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "nvim-telescope/telescope-fzf-native.nvim",
    },
    cmd = "Telescope",
    keys = {
      { "<leader>ff", "<cmd>Telescope find_files<cr>", desc = "Find files" },
      { "<leader>fg", "<cmd>Telescope live_grep<cr>",  desc = "Live grep" },
      { "<leader>fb", "<cmd>Telescope buffers<cr>",    desc = "Buffers" },
      { "<leader>fh", "<cmd>Telescope help_tags<cr>",  desc = "Help tags" },
    },
    config = function()
      require("telescope").setup({})
      -- fzf-native is optional — works without it, just slower
      pcall(require("telescope").load_extension, "fzf")
    end,
  },
  {
    "nvim-telescope/telescope-fzf-native.nvim",
    build = "make",
    -- If make fails on Windows, telescope still works (just without fzf optimization)
  },

  -- ── Treesitter (syntax highlighting & parsing) ─────────────────────
  -- Neovim 0.11+: highlighting is built-in via vim.treesitter.start()
  -- which activates automatically when a parser is installed.
  -- nvim-treesitter just provides parser installation (:TSInstall).
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    config = function()
      require("nvim-treesitter").setup({})
      -- Ensure key parsers are installed (async, runs in background)
      local wanted = {
        "lua", "vim", "vimdoc", "bash", "python", "javascript",
        "typescript", "go", "rust", "sql", "markdown", "yaml", "json",
      }
      local installed = require("nvim-treesitter").get_installed()
      local missing = {}
      for _, lang in ipairs(wanted) do
        if not vim.tbl_contains(installed, lang) then
          table.insert(missing, lang)
        end
      end
      if #missing > 0 then
        vim.cmd("TSInstall " .. table.concat(missing, " "))
      end
    end,
  },
  { "nvim-treesitter/nvim-treesitter-textobjects" },

  -- ── Git ─────────────────────────────────────────────────────────────
  { "tpope/vim-fugitive" },
  {
    "lewis6991/gitsigns.nvim",
    config = function() require("gitsigns").setup() end,
  },
  {
    "kdheepak/lazygit.nvim",
    cmd = { "LazyGit", "LazyGitCurrentFile" },
    dependencies = { "nvim-lua/plenary.nvim" },
    keys = {
      { "<leader>gg", "<cmd>LazyGit<cr>", desc = "Open LazyGit" },
    },
  },

  -- ── File Manager (Yazi integration) ────────────────────────────────
  {
    "mikavilpas/yazi.nvim",
    event = "VeryLazy",
    keys = {
      { "<leader>e", "<cmd>Yazi<cr>", desc = "Open Yazi" },
    },
    opts = { open_for_directories = true },
  },

  -- ── Markdown ────────────────────────────────────────────────────────
  {
    "MeanderingProgrammer/render-markdown.nvim",
    ft = { "markdown", "codecompanion" },
    opts = { render_modes = true },
  },
  {
    "iamcco/markdown-preview.nvim",
    cmd = { "MarkdownPreview", "MarkdownPreviewToggle" },
    build = "cd app && npm install",
    ft = { "markdown" },
  },

  -- ── Database ────────────────────────────────────────────────────────
  { "tpope/vim-dadbod", cmd = { "DB", "DBUI" } },
  {
    "kristijanhusak/vim-dadbod-ui",
    cmd = { "DBUI", "DBUIToggle", "DBUIFindBuffer" },
    keys = {
      { "<leader>D", "<cmd>DBUIToggle<CR>", desc = "Toggle DB UI" },
    },
  },
  { "kristijanhusak/vim-dadbod-completion", ft = { "sql", "mysql", "plsql" } },

  -- ── Quality of Life ─────────────────────────────────────────────────
  {
    "windwp/nvim-autopairs",
    event = "InsertEnter",
    config = function() require("nvim-autopairs").setup() end,
  },
  {
    "numToStr/Comment.nvim",
    lazy = false,
    config = function() require("Comment").setup() end,
  },
  {
    "kylechui/nvim-surround",
    version = "*",
    event = "VeryLazy",
    config = function() require("nvim-surround").setup() end,
  },
  {
    "lukas-reineke/indent-blankline.nvim",
    main = "ibl",
    event = "VeryLazy",
    config = function()
      require("ibl").setup({ scope = { enabled = true } })
    end,
  },
  {
    "folke/todo-comments.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
    event = "VeryLazy",
    config = function() require("todo-comments").setup() end,
  },
  {
    "folke/trouble.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    cmd = { "Trouble", "TroubleToggle" },
    keys = {
      { "<leader>xx", "<cmd>TroubleToggle<cr>", desc = "Diagnostics" },
      { "<leader>xq", "<cmd>TroubleToggle quickfix<cr>", desc = "Quickfix" },
    },
    config = function() require("trouble").setup() end,
  },
  {
    "stevearc/oil.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    keys = {
      { "-", "<cmd>Oil<cr>", desc = "Open parent dir (Oil)" },
    },
    config = function() require("oil").setup() end,
  },
  -- Seamless nvim-window <-> zellij-pane navigation (Ctrl+hjkl). Pairs with the
  -- zellij-autolock wasm plugin: when nvim is focused zellij is Locked, so these
  -- keys reach nvim; at an nvim window edge Neolij calls `zellij action move-focus`
  -- to hop into the adjacent zellij pane (e.g. the hermes TUI). Uses autolock mode
  -- (NOT vim-zellij-navigator), so vim_zellij_navigator stays false/default.
  {
    "y2w8/neolij.nvim",
    event = "VeryLazy",
    opts = {}, -- important even if empty
    keys = {
      { "<C-h>", ":NeolijLeftTab<CR>", mode = { "n", "t" }, desc = "Nav left / prev tab", silent = true },
      { "<C-j>", ":NeolijDown<CR>",    mode = { "n", "t" }, desc = "Nav down",             silent = true },
      { "<C-k>", ":NeolijUp<CR>",      mode = { "n", "t" }, desc = "Nav up",               silent = true },
      { "<C-l>", ":NeolijRightTab<CR>", mode = { "n", "t" }, desc = "Nav right / next tab", silent = true },
      { "<leader>zp", ":NeolijNewPane -d right<CR>", desc = "New zellij pane right", silent = true },
      { "<leader>zP", ":NeolijNewPane -d down<CR>",  desc = "New zellij pane down",  silent = true },
      { "<leader>zf", ":NeolijNewPane -f<CR>",       desc = "New zellij floating pane", silent = true },
      { "<leader>zt", ":NeolijNewTab<CR>",           desc = "New zellij tab", silent = true },
    },
    config = function() require("neolij").setup({}) end,
  },
  {
    "stevearc/conform.nvim",
    event = "BufWritePre",
    keys = {
      { "<leader>cf", function() require("conform").format({ async = true }) end, desc = "Format buffer" },
    },
    config = function()
      -- NOTE: formatters come from two sources — portability caveat.
      --   ruff      -> PATH binary (winget: astral-sh.ruff). Not Mason-managed.
      --   stylua/sqlfluff/prettierd -> Mason-managed (nvim-data/mason/bin).
      -- Reproducing this on a new machine needs BOTH: `winget install astral-sh.ruff`
      -- plus `:MasonInstall stylua sqlfluff prettierd` (or mason-tool-installer).
      require("conform").setup({
        formatters_by_ft = {
          lua = { "stylua" },
          python = { "ruff_fix", "ruff_format", "ruff_organize_imports" },
          javascript = { "prettierd", "prettier", stop_after_first = true },
          typescript = { "prettierd", "prettier", stop_after_first = true },
          json = { "prettierd", "prettier", stop_after_first = true },
          yaml = { "prettierd", "prettier", stop_after_first = true },
          markdown = { "prettierd", "prettier", stop_after_first = true },
          sql = { "sqlfluff" },
        },
        format_on_save = { timeout_ms = 500, lsp_fallback = true },
      })
    end,
  },

  -- ── UI ──────────────────────────────────────────────────────────────
  {
    "nvim-lualine/lualine.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("lualine").setup({
        options = { theme = "nightfox" }, -- auto-picks carbonfox via colors_name
      })
    end,
  },
  {
    "folke/which-key.nvim",
    event = "VeryLazy",
    config = function() require("which-key").setup() end,
  },
  {
    "folke/noice.nvim",
    event = "VeryLazy",
    dependencies = {
      "MunifTanjim/nui.nvim",
      "rcarriga/nvim-notify",
    },
    config = function() require("noice").setup() end,
  },

}, {
  install = { missing = true },
  checker = { enabled = false },
})

-- ═══════════════════════════════════════════════════════════════════════
-- Keymaps & Autocmds
-- ═══════════════════════════════════════════════════════════════════════

-- SQL file niceties
vim.api.nvim_create_autocmd("FileType", {
  pattern = { "sql", "mysql", "plsql" },
  callback = function()
    local opts = { buffer = true, silent = true }
    vim.keymap.set("n", "<leader>r", "<Plug>(DBExec)", opts)
    vim.keymap.set("x", "<leader>r", "<Plug>(DBExec)", opts)
    vim.keymap.set("n", "<leader>rl", "<Plug>(DBExecLine)", opts)
  end,
})
