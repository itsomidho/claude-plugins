# itsomidho plugins for Claude Code

A [Claude Code](https://claude.com/claude-code) plugin marketplace. Each plugin lives in its own repository and works on its own: install any of them, or all.

| Plugin | |
|---|---|
| [**clawd-statusbar**](https://github.com/itsomidho/clawd-statusbar) | A framed status bar under the prompt: model, context, usage limits with reset times, git state, MR/PR pipeline status, and Clawd frying an egg while Claude works |
| [**clawd-tasks**](https://github.com/itsomidho/clawd-tasks) | A live task board: Claude's plan, and under each task the steps it took, how long it ran, the files it changed and the agents it started |

## Install

In Claude Code, type:

```
/plugin install clawd-statusbar --marketplace itsomidho/claude-plugins
/plugin install clawd-tasks --marketplace itsomidho/claude-plugins
```

Answer `y` to add the marketplace the first time, then choose a scope. Once it is added, `/plugin install <plugin>@itsomidho` is enough.

From a shell:

```
claude plugin install clawd-statusbar --marketplace itsomidho/claude-plugins
claude plugin install clawd-tasks --marketplace itsomidho/claude-plugins
```

In the desktop app: click + next to the prompt box, then Plugins, Add marketplace with `itsomidho/claude-plugins`, then Add plugin.

## Adding a plugin

Add an entry to `.claude-plugin/marketplace.json` whose `source` names the plugin's repository, then check it:

```
claude plugin validate .
```

## License

MIT
