# Contribution Guidelines

## Table of Contents

- [Contribution Guidelines](#contribution-guidelines)
    - [Table of Contents](#table-of-contents)
    - [Branching Strategy](#branching-strategy)
    - [Commit Message Guidelines](#commit-message-guidelines)
    - [Information Update Guidelines](#information-update-guidelines)
    - [Library Update Guidelines](#library-update-guidelines)

## Issue Management

We use Jira to manage issues. Please refer to
the [Jira](https://pi-lab.atlassian.net/jira/software/projects/ASSET/boards/52) board for the list of issues.

## Branching Strategy

The goals of the branching strategy are:

- The `main` branch should always be able to be used by end-users. This implies that the information in the `main`
  branch should be up-to-date and correct in all aspects and at all times.
- The `main` branch should stay active. As we work collaboratively with multiple contributors, we should avoid
  long-lived branches.

The following rules briefly describe the typical workflow:

1. **Create a branch**: Create a new branch from the `main` branch. The branch name should consist of the type of
   the branch and the issue key in Jira.
    - `feature/ASSET-000`: For new features such as adding new information or updating libraries.
    - `fix/ASSET-000`: For bug fixes.
    - `docs/ASSET-000`: For documentation updates.

2. **Work on the branch**: Work on the branch and make the necessary changes.

3. **Create a pull request**: Create a pull request to merge the changes into the `main` branch. The title of the pull
   request should be the issue key in Jira, along with a brief description of the changes.
   (e.g., `[ASSET-000] Add some information on some category`.)
   Furthermore, the CI pipeline should check the changes before merging.

4. **Review the pull request**: The pull request should be reviewed by at least one repository owner.

5. **Merge the pull request**: After the review, the pull request should be merged into the `main` branch.

## Commit Message Guidelines

The commit message should be in the following format:

```
ASSET-000 {{Brief description of the changes}}

{{Some detailed description about the changes}}
```

## Information Update Guidelines

### 1. Update the information

#### 1.1. Choose an element in the directory

Choose an element in the directory that you want to update.
The directory for each type of information is as follows:

- assets (e.g., native coins, ERC20 tokens): `assets`
- networks (e.g., Ethereum, Binance Smart Chain): `networks`
- protocols (e.g., Uniswap, SushiSwap): `protocols`

If the element does not exist, create a new directory with the new unique id of the element.

#### 1.2. Update the `info.json`

Update the information in the `info.json` file of the element.
The model of the `info.json` file is as follows:

- assets: [asset.py](../libraries/models/asset.py)
- networks: [network.py](../libraries/models/network.py)
- protocols: [protocol.py](../libraries/models/protocol.py)

This convention is strictly followed to maintain consistency across all elements.

If the element does not exist, create a new `info.json` file with the above model.

#### 1.3. Update the image

If you need to update the image of the element, update the image in the same directory.
The image should be named `image-{{pixel size}}.png` and `image.svg`.
Each of the images should be square and have the size as follows:

- PNG format: the pixel sizes of its width and height should be the same as the number of its image when it.
  (e.g., `image-128.png` should be 128x128 pixels.)
- SVG format: the size of the image should be 128x128.

### 2. Preprocess before committing

Run the following command to preprocess the information before committing:

```bash
(venv) $ python app.py preprocess
```

### 3. Test the changes

Run the following command to test the changes:

```bash
(venv) $ pytest -vv
```

## Library Update Guidelines

...
