# Install DataCanvas EDU

Skill name: `datacanvas-edu`. The installable directory is [skills/datacanvas-edu](../skills/datacanvas-edu/). Its `SKILL.md`, scripts, and references belong together.

These setup routes follow the official documentation reviewed on 2026-09-08. The DataCanvas EDU package has not yet completed installation and conversational execution trials on every host. Record your tool, version or surface, and observed outcome when testing. Account availability and organization settings can affect the interfaces below.

## Claude app

1. Download [datacanvas-edu-v0.1.1.zip](../dist/datacanvas-edu-v0.1.1.zip) from this repository. On its GitHub file page, use the download control.
2. Enable code execution and file creation in your Claude environment if needed.
3. Open **Customize > Skills**, choose the option to create a Skill, and select **Upload a skill**.
4. Upload the ZIP and enable it.
5. In a new conversation, ask Claude to use DataCanvas EDU with your teaching brief.

The ZIP has one top-level `datacanvas-edu/` directory containing `SKILL.md` and the supporting resources. Use this Skill ZIP rather than the whole-repository download, which includes an extra repository structure.

References: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude), [Create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

## Claude Code

Download or clone this public repository. Copy `skills/datacanvas-edu/` into one of these locations:

- Personal: `~/.claude/skills/datacanvas-edu/`.
- Project: `.claude/skills/datacanvas-edu/` inside the project where you want to use it.

For a new installation on macOS/Linux, these commands run from the repository root and stop if the destination already exists:

```sh
python3 -c "from pathlib import Path; import shutil; shutil.copytree('skills/datacanvas-edu', Path.home() / '.claude/skills/datacanvas-edu')"
```

Start or reopen Claude Code in your working project, then invoke:

```text
/datacanvas-edu
```

Provide your teaching brief, or ask Claude to propose a suitable scenario. The Agent needs permission to write project files and run Python. Reference: [Claude Code Skills](https://code.claude.com/docs/en/skills).

## Codex local tools

Copy the same Skill folder into a supported discovery location:

- Personal: `~/.agents/skills/datacanvas-edu/`.
- Project: `.agents/skills/datacanvas-edu/` inside your working project.

For a new personal installation from the repository root:

```sh
python3 -c "from pathlib import Path; import shutil; shutil.copytree('skills/datacanvas-edu', Path.home() / '.agents/skills/datacanvas-edu')"
```

Use the Skill selector or, in Codex CLI/IDE, include `$datacanvas-edu` in your prompt. If the new Skill is not visible, restart the tool. Reference: [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills).

## ChatGPT

For accounts and surfaces with Skills support, open **Plugins > Skills > Create > Upload from your computer** and follow the upload interface. Use the supported Skill package/file selection offered by that surface. Account and workspace permissions determine availability; a GitHub connector or ordinary chat attachment is not itself a persistent Skill installation.

After installation, select the Skill in the interface or explicitly ask ChatGPT to use DataCanvas EDU. Test that it can read the supporting resources, execute the Python workflow, and return the complete teaching package. Record any packaging or runtime adjustments needed rather than assuming a successful upload establishes full compatibility.

References: [Skills in ChatGPT](https://help.openai.com/en/articles/20001066), [Build skills](https://learn.chatgpt.com/docs/build-skills).

## Runtime and updates

The numerical helper uses Python 3.10+ and its standard library. Reference charts use Matplotlib; WindowDash also needs NumPy and pandas. The Agent may install appropriate dependencies within the host's permitted environment. No separate API key or paid API service is required by the helper itself; your chosen Agent tool has its own access requirements.

Folder copies and downloaded ZIPs are version snapshots. Updating this GitHub repository does not automatically replace a manually installed copy. Keep the prior version for comparison and use the host's update or replacement process after reviewing the changelog. Plugin packaging and easier update distribution remain planned work.
