-- lazy module
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
        vim.fn.system({
                "git","clone","--filter=blob:none",
                "https://github.com/folke/lazy.nvim.git",
                "--branch=stable", lazypath,
        })
end
vim.opt.rtp:prepend(lazypath)


require("lazy").setup({
        -- 1. nvim-dap
        -- DAP Client
        { "mfussenegger/nvim-dap" },

        -- 2. nvim-dap-python
        -- Python Addapter
        { "mfussenegger/nvim-dap-python",
                dependencies = { "mfussenegger/nvim-dap" },
                config = function()
                        require("dap-python").setup(vim.fn.expand("~/anaconda3/bin/python"))
                end,
        },

        -- 3. nvim-dap-ui
        -- DAP UI
        {
                "rcarriga/nvim-dap-ui", -- dap ui
                dependencies = { "mfussenegger/nvim-dap", "nvim-neotest/nvim-nio" },
                config = function()
                        local dap, dapui = require("dap"), require("dapui")
                        dapui.setup()
                        dap.listeners.after.event_initialized["dapui"] = function() dapui.open() end
                        dap.listeners.before.event_terminated["dapui"] = function() dapui.close() end
                        dap.listeners.before.event_exited["dapui"] = function() dapui.close() end
                end,
        },

        -- 4. nvim-dap-virtual-text
        -- Inline Result
        {
                "theHamsta/nvim-dap-virtual-text",
                dependencies = { "nvim-treesitter/nvim-treesitter" },
                config = function()
                        require("nvim-dap-virtual-text").setup()
                end,
        },

        -- 5. nvim-treesitter
        -- Readablitiy up
        {
                "nvim-treesitter/nvim-treesitter",
                build = ":TSUpdate",
                config = function()
                        require("nvim-treesitter.configs").setup({
                                ensure_installed = { "python" },
                                auto_install = true,
                                highlight = { enable = true },
                        })
                end,
        },

        -- 6. debugpy.nvim
        -- :Debugpy module app.main, :Debugpy program app foo bar, :Debugpy attach 127.0.0.1 5678
        {
                "HiPhish/debugpy.nvim",
                dependencies = { "mfussenegger/nvim-dap" },
                cmd = "Debugpy"
        },


})

local dap = require("dap")

-- command
local dapui_ok, dapui = pcall(require, "dapui")

local function map(lhs, rhs, desc)
        vim.keymap.set("n", lhs, rhs, { silent = true, noremap = true, desc = desc })
end

map("<F2>", function() dap.toggle_breakpoint() end, "Breakpoint")
map("<S-F2>", function()
        local cond = vim.fn.input("Condition : ")
        if cond ~= "" then dap.set_breakpoint(cond) end
end, "Conditional Breakpoint")
map("<C-F2>", function()
        if dap.restart then
                dap.restart()
        else
                dap.terminate(); vim.defer_fn(function() dap.run_last() end, 100)
        end
end, "Restart")
map("<M-F2>", function() dap.terminate() end, "Terminate") -- M -> Alt
map("<F4>", function() dap.run_to_cursor() end, "Run to Cursor")
map("<F7>", function() dap.step_info() end, "Step Info")
map("<F8>", function() dap.step_over() end, "Step Over")
map("<S-F8>", function() dap.step_out() end, "Step Out")
map("<F9>", function() dap.continue() end, "Contiune / Run")
map("<F12>", function() dap.continue() end, "Pause")
