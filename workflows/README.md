# Comfy Anything Workflow Submission Guide

## Introduction

This guide provides step-by-step instructions on how to submit your ComfyUI workflow requests to Comfy Anything. The key requirement is to organize your workflow files properly to avoid any confusion. Specifically, each workflow should be contained within its own folder, which will include a `workflow.json` file exported from ComfyUI.

[Hugging Face Repo Docs](https://huggingface.co/docs/hub/repositories)

## Example Directory Structure

workflows/ <br>
├── username-my-awesome-workflow/ <br>
........└── your-workflow.json

## Steps to Submit Your Workflow Request (in browser)

### 1. Export Your Workflow from ComfyUI

1. Open ComfyUI.
2. Build your workflow as needed.
3. Export your workflow by selecting `Save > Save as JSON`.
4. Save the exported file with a meaningful name, e.g., `your-workflow.json`.

### 2. Create a Folder for Your Workflow and Paste the JSON

1. Create a new folder inside /workflows.
   - The folder name should be indicative of your workflow to avoid any confusion. For example, `username-awesome-workflow`.

2. Paste the exported `.json` file inside the editor.

3. Commit changes.

![Visual Example](https://i.imgur.com/NGBGY9c.png)

### 3. I'll review your submission and get back to you.

Happy hacking! 🚀