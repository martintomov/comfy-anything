# ComfyUI Experiments

ComfyUI workflows and nodes I experiment with.

## Installing ComfyUI on Mac OS

This guide walks you through the process of setting up ComfyUI on a Mac computer running on M1, M2, or M3 processors. ComfyUI is a powerful tool for creating custom workflows and leveraging AI capabilities for image and animation generation.

## Prerequisites

Before you begin, ensure you have the following:

- Mac computer with M1, M2, or M3 processor
- Homebrew (a package manager for macOS)

## Installation Steps

### 1. Create a dedicated folder for ComfyUI

Open a Finder window and navigate to your home directory. Create a new folder named AI (for example). This folder will serve as the base directory for ComfyUI setup.

### 2. Install Homebrew

> **Skip step if you already have Homebrew installed.**

Homebrew is a package manager that simplifies the installation of software packages on macOS. Open Terminal and paste the following command to install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the on-screen instructions to complete the installation.

### 3. Install Python 3.11

ComfyUI requires Python 3.11. Install Python 3.11 using Homebrew by running the following command:

```bash
brew install python@3.11
```

### 4. Install PyTorch (Nightly)

PyTorch is a deep learning framework required by ComfyUI. Install PyTorch by following the instructions provided on the [PyTorch website](https://pytorch.org/get-started/locally/).

**Or, just run:**

```bash
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
```

### 5. Clone the ComfyUI repository

Clone the ComfyUI GitHub repository into the "Ai" folder created earlier. In Terminal, navigate to the "Ai" folder and run the following command:

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
```

### 6. Install dependencies

Navigate into the ComfyUI directory using Terminal and install the dependencies listed in the `requirements.txt` file:

```bash
cd comfy-ui
pip3 install -r requirements.txt
```

### 7. Run ComfyUI

Run ComfyUI by executing the `main.py` file within the ComfyUI directory:

```bash
python3.11 main.py
```

Once ComfyUI is running, open your web browser and enter the provided URL to access the ComfyUI interface.

### 8. Install ComfyUI Manager (recommended)

ComfyUI Manager simplifies the management of ComfyUI missing nodes and models. Download the ComfyUI Manager from the [ComfyUI Manager GitHub page](https://github.com/ltdrdata/ComfyUI-Manager) and follow the installation instructions.


## Troubleshooting

If you encounter any issues during the installation process, refer to the troubleshooting section of the ComfyUI documentation or seek assistance from the ComfyUI community.

## Contributing

Contributions to this workflow/node repository are welcome! If you have suggestions for improvements or encounter any issues, please submit a pull request or open an issue on GitHub.

## Acknowledgments

Thanks to the ComfyUI community for providing the tools and support needed to make this project possible.

## License

This project is licensed under the Apache-2.0 License.