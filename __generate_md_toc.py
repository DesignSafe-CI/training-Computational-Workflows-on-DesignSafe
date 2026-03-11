import yaml
from pathlib import Path

import nbformat

from urllib.parse import quote

from nbformat.v4 import new_markdown_cell

import os
import glob


# things to go ahead and do
# doTagCells = True
doTagCells = False # 12/28/2025, this should be true, but what does it do? 1/7/26, naw, we don't need to tag notebook cells
doJubHubLinks = True
doAppendTOC = False
addNBicon = False # they are distracting

do_add_intro_markdown = False; # do this only once, but keep here as template.
do_replace_first_markdown = True # 1/7/2026: put back True, but for now we don't have the proper link and we don't want to touch the notebooks # this is good to have since it makes sure the link at the top is good.

# jupyterNotebooksPath_start = f"https://jupyter.designsafe-ci.org/hub/user-redirect/notebooks/"
jupyterNotebooksPath_start = f"https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/"
# jupyterNotebooksPath_mid = f"CommunityData/OpenSees/TrainingMaterial/training-OpenSees-on-DesignSafe/"
jupyterNotebooksPath_mid = f"CommunityData/Training/Computational-Workflows-on-DesignSafe/Jupyter_Notebooks/"

# https://jupyter.designsafe-ci.org/hub/user-redirect/lab/tree/CommunityData/OpenSees/TrainingMaterial/training-OpenSees-on-DesignSafe/Jupyter_Notebooks


def get_notebook_link(notebook_path):
    encoded = quote(f"{jupyterNotebooksPath_mid}{notebook_path}")
    return f"{jupyterNotebooksPath_start}{encoded}"

def generate_jupyterhub_links(notebook_path):
    # encoded = quote(f"{jupyterNotebooksPath_mid}{notebook_path}")
    jupyter_link = get_notebook_link(notebook_path)
    download_link = notebook_path
    # return f"\n      <sub>📂 [Open in JupyterHub]({jupyter_link}) • 💾 [Download]({download_link})</sub>"
    return f"\n      <sub>📂 <a href='{jupyter_link}' target='_blank'>Open in JupyterHub</a></sub>"


from pathlib import Path

def _repo_root() -> Path:
    # robust: folder containing this script (works no matter where you run from)
    return Path(__file__).resolve().parent

def resolve_file_path(basePath: str | Path, toc_file: str) -> Path | None:
    """
    Resolve a toc entry 'file' to a real filesystem path.

    - basePath: the book dir (e.g., books/Computational-Resources-on-DesignSafe)
    - toc_file: what is in _toc.yml (e.g., ../../shared/... or Docs_MD/About.md)
    """
    base = Path(basePath).resolve()
    toc_path = Path(toc_file)

    candidates = []

    # 1) Interpreting toc_file as relative to the book folder
    candidates.append((base / toc_path))

    # 2) Interpreting toc_file as relative to where the script lives (repo root-ish)
    candidates.append((_repo_root() / toc_path))

    # 3) Interpreting toc_file as relative to current working directory
    candidates.append((Path.cwd().resolve() / toc_path))

    for p in candidates:
        try:
            rp = p.resolve()
        except Exception:
            rp = p
        if rp.is_file():
            return rp

    return None



def get_heading_from_file(file_path,link_path):
    # print('---------------- file_path',file_path)
    """Extract the first level-1 Markdown heading from a file."""
    if file_path.endswith(".ipynb") or file_path.endswith(".py"):
        if do_add_intro_markdown:
            add_intro_markdown(file_path,1); # we really only need to do this once
        if do_replace_first_markdown:
            new_text = ''
            new_text += '<a class="reference external" href="'
            new_text += get_notebook_link(link_path)
            new_text += '" target="_blank">\n'
            new_text += '<img alt="Try on DesignSafe" src="https://raw.githubusercontent.com/DesignSafe-Training/pinn/main/DesignSafe-Badge.svg" /></a>'
            # print('new_text',new_text)
            # new_text += '\n'
            # new_text += '<br>\n'
            # new_text += '\n'
            # new_text += 'This notebook is part of the **OpenSees-On-DesignSafe Training Module** -- [CLICK HERE to access the Module](https://designsafe-ci.github.io/training-OpenSees-on-DesignSafe/README.html)'
            replace_first_markdown(file_path, new_text)
        return get_heading_from_notebook(file_path)
    else:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("# "):
                        # print('line',line.strip().lstrip("# ").strip())
                        return line.strip().lstrip("# ").strip()
                # try to look for next level of heading....
                for line in f:
                    if line.strip().startswith("## "):
                        print('two #')
                        return line.strip().lstrip("## ").strip()
        except FileNotFoundError:
            print('FileNotFoundError')
            return Path(file_path).stem  # fallback if file doesn't exist
        return Path(file_path).stem  # fallback if no heading found




def replace_first_markdown(notebook_path, new_text):
    try:
        # Load notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        # Find the first markdown cell
        for cell in nb['cells']:
            if cell['cell_type'] == 'markdown':
                cell['source'] = new_text  # Replace its contents
                break  # stop after first markdown cell

        # Save notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)

        print(f"Replaced first markdown cell in {notebook_path}")

    except FileNotFoundError:
        print("FileNotFoundError")
        return Path(notebook_path).stem

def replace_cell_by_index(notebook_path, cell_index, new_text):
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        if 0 <= cell_index < len(nb['cells']):
            nb['cells'][cell_index]['source'] = new_text
        else:
            print(f"Cell index {cell_index} out of range.")

        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)

        print(f"Updated cell {cell_index} in {notebook_path}")

    except FileNotFoundError:
        print("FileNotFoundError")
        return Path(notebook_path).stem




def add_intro_markdown(notebook_path,cellIndexIN):
    intro_text = "This notebook is part of the OpenSees-On-DesignSafe Training Module [CLICK HERE to access the Module](https://designsafe-ci.github.io/training-OpenSees-on-DesignSafe/README.html)"

    try:
        # Load notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        # Create new markdown cell
        new_cell = new_markdown_cell(intro_text)

        # Insert new cell at the top (index 0)
        nb['cells'].insert(cellIndexIN, new_cell)

        # Save the modified notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)

        print(f"Intro markdown cell added to {notebook_path}")

    except FileNotFoundError:
        print("FileNotFoundError")
        return Path(notebook_path).stem


def get_heading_from_notebook(notebook_path):
    functionTagMap = {
        '# Local Utilities Library': 'remove-input',
        'OpsUtils.show_video': 'remove-input',
        'OpsUtils.show_text_file_in_accordion': 'remove-input'
    }
    # Load notebook
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        for idx, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'markdown':
                original_text = cell['source']
                if original_text[0:2] == "# ":
                    lines = cell.source.splitlines()
                    for i, line in enumerate(lines):
                        if line.startswith("# "):
                            return line.strip().lstrip("# ").strip()
    except FileNotFoundError:
        print('FileNotFoundError')
        return Path(file_path).stem  # fallback if file doesn't exist
    return Path(file_path).stem  # fallback if no heading found






def tag_cells(notebook_path):
    functionTagMap = {'# Local Utilities Library':'remove-input','OpsUtils.show_video':'remove-input','OpsUtils.show_text_file_in_accordion':'remove-input'}
    # Load notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    jupyter_link = get_notebook_link(notebook_path)
    myIcon = '📒'
    space = ' '
    myIconLink = f'<a><href="{jupyter_link}" target="_blank">{myIcon}</a> '
    addNBicon_here = addNBicon
    for idx, cell in enumerate(nb['cells']):
        # print(addNBicon_here)
        if addNBicon_here:
            if cell['cell_type'] == 'markdown':
                original_text = cell['source']
                if original_text[0:2] == "# " and not myIcon in original_text:
                    lines = cell.source.splitlines()
                    for i, line in enumerate(lines):
                        if line.startswith("# ") and myIcon not in line:
                            lines[i] = line + " " + myIcon
                            cell.source = "\n".join(lines)
                            addNBicon_here = False
                            break  # Only modify the first heading

        if cell['cell_type'] == 'code':
            for my_function_call,tag_name in functionTagMap.items():
                if my_function_call in cell['source']:
                    # Initialize metadata if missing
                    if 'tags' not in cell['metadata']:
                        cell['metadata']['tags'] = []

                    # Avoid duplicate tags
                    if tag_name not in cell['metadata']['tags']:
                        cell['metadata']['tags'].append(tag_name)
                        # print(f"Tagged cell {idx} with '{tag_name}'")

    # Write back to file
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Updated notebook saved: {notebook_path}")
    


def format_link(file_fs_path, link_path):
    """
    file_fs_path: real file on disk (Path or str)
    link_path: path to use in markdown link + JupyterHub link (string from _toc.yml)
    """
    file_fs_path = str(file_fs_path)
    title = get_heading_from_file(file_fs_path,link_path)

    # print('link_path',link_path)

    if title == 'Table of Contents':
        return ''

    link_line = f"[{title}]({link_path})"

    if file_fs_path.endswith(".ipynb") or file_fs_path.endswith(".py"):
        if doJubHubLinks:
            # IMPORTANT: JupyterHub link should be built from the *link path* (toc/book-relative),
            # not from the filesystem path.
            link_line += generate_jupyterhub_links(link_path)
        if doTagCells:
            tag_cells(file_fs_path)

    return link_line



def process_chapters(chapters, indent=0, basePath=''):
    lines = []
    if not chapters:
        return lines

    prefix = "  " * indent + "- "
    for chapter in chapters:
        if 'file' in chapter:
            toc_file = chapter['file']               # what is written in _toc.yml
            # print('toc_file',toc_file)
            file_fs = resolve_file_path(basePath, toc_file)
            # print('file_fs',file_fs)
            # print('Path(basePath).resolve()',Path(basePath).resolve())

            if file_fs is not None:
                link_line = format_link(file_fs, link_path=toc_file)
                if link_line:
                    lines.append(prefix + link_line)
            else:
                # keep your debug print, but show the normalized candidates for clarity
                base = Path(basePath).resolve()
                # print('base',base)
                print(f"The file does NOT exist: {base / toc_file}")

        if 'sections' in chapter:
            lines.extend(process_chapters(chapter['sections'], indent + 1, basePath))

    return lines


def generate_markdown_toc(toc_yaml_path="_toc.yml",basePath=''):
    with open(toc_yaml_path, "r", encoding="utf-8") as f:
        toc = yaml.safe_load(f)

    if doAppendTOC:
        lines = ["\n## Table of Contents\n"]
    else:
        lines = ["\n# Table of Contents\n"]

    # print('basePath',basePath)
    if 'parts' in toc:
        for part in toc['parts']:
            if 'caption' in part:
                if part['caption'] == 'Table of Contents':
                    continue
                if doAppendTOC:
                    lines.append(f"### {part['caption']}")
                else:
                    lines.append(f"## {part['caption']}")
            lines.extend(process_chapters(part.get('chapters', []),0,basePath))
            lines.append("")
    elif 'chapters' in toc:
        lines.extend(process_chapters(toc['chapters'],0,basePath))

    return "\n".join(lines)


def generate_tocfile(readme0_path="", toc_yaml_path="_toc.yml",
                   output_toc_path="generated_toc.md",
                   github_readme_path="README.md",basePath=''):

    # Generate ToC
    toc_md = generate_markdown_toc(toc_yaml_path,basePath).strip()

    # Save ToC for Jupyter Book `{include}`
    with open(output_toc_path, "w", encoding="utf-8") as f:
        f.write(toc_md + "\n")
    print(f"✅ Wrote {output_toc_path}")

    # Generate GitHub-friendly README
    # Read intro
    ## you could use readme0_path = "readme0.md"
    if len(readme0_path)>0:
        with open(readme0_path, "r", encoding="utf-8") as f:
            intro = f.read().strip()   
            
        with open(github_readme_path, "w", encoding="utf-8") as f:
            if doAppendTOC:
                f.write(intro + "\n\n" + toc_md + "\n")
            else:
                f.write(intro)
        print(f"✅ Wrote {github_readme_path} (for GitHub)")

# Run the generator
if __name__ == "__main__":
    import glob
    booksFolder = 'books'
    dirs = [d for d in glob.glob(os.path.join(booksFolder, "**/"), recursive=False) if os.path.isdir(d)]
    dirs = [os.path.normpath(d) for d in dirs] # remove the ending / if there

    print('dirs',dirs)
    for thisBookDir in dirs:
        print('-------------------------------- thisBookDir',thisBookDir)
        toc_yaml_path = f'{thisBookDir}/_toc.yml'
        print('toc_yaml_path',toc_yaml_path)
        if os.path.isfile(toc_yaml_path):
            output_toc_path = f'{thisBookDir}/generated_toc.md'
            print('output_toc_path',output_toc_path)
            generate_tocfile(readme0_path="", toc_yaml_path=toc_yaml_path,
                       output_toc_path=output_toc_path,
                       github_readme_path="README.md",
                            basePath = thisBookDir)

