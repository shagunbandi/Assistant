# Setup Python Environment with `pyenv` and `pyenv-virtualenv`

This guide walks you through the steps to set up a new Python environment using `pyenv` and `pyenv-virtualenv`, install dependencies from a `requirements.txt` file, and set up API keys and credentials from GCP.

## Prerequisites

- A Unix-based system (Linux/MacOS) with `bash`, `zsh`, or similar shell.
- Install `pyenv` and `pyenv-virtualenv` for managing Python versions and virtual environments.
- You will also need to set up some API keys and download a `credentials.json` file from GCP.

---

### 1. **Install `pyenv`**

To install `pyenv`, you can follow the official installation steps or use the commands below.

#### For MacOS (with Homebrew)
```bash
brew install pyenv
```

#### For Linux (Using curl)
```bash
curl https://pyenv.run | bash
```

Follow the on-screen instructions for adding `pyenv` to your shell configuration file (usually `~/.bashrc`, `~/.zshrc`, or similar).

After installation, restart your terminal or run:
```bash
source ~/.bashrc   # or ~/.zshrc
```

Verify installation by running:
```bash
pyenv --version
```

---

### 2. **Install `pyenv-virtualenv`**

Install `pyenv-virtualenv` to manage virtual environments.

#### For MacOS (with Homebrew)
```bash
brew install pyenv-virtualenv
```

#### For Linux (using `curl`)
```bash
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
```

Add the following to your shell configuration file (usually `~/.bashrc`, `~/.zshrc`):
```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Then restart your shell or run:
```bash
source ~/.bashrc   # or ~/.zshrc
```

Verify installation by running:
```bash
pyenv virtualenvs
```

---

### 3. **Install Python Version Using `pyenv`**

Use `pyenv` to install a specific version of Python:
```bash
pyenv install 3.11.6
```

---

### 4. **Create a New Virtual Environment**

Create a new virtual environment using `pyenv-virtualenv`:
```bash
pyenv virtualenv 3.11.6 myenv
```

---

### 5. **Activate the Virtual Environment**

Activate the newly created virtual environment:
```bash
pyenv activate myenv
```

Your shell prompt should now show `(myenv)` indicating that the virtual environment is active.

---

### 6. **Install Dependencies from `requirements.txt`**

With the virtual environment active, install the dependencies listed in your `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### 7. **Get API Keys and GCP Credentials**

#### To get the `OPENAI_API_KEY`:
1. Go to [OpenAI API keys](https://platform.openai.com/account/api-keys).
2. Create a new key and copy it to your clipboard.

#### To get `SERVICE_ACCT_EMAILS` (Service Account Email):
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to the **IAM & Admin** section.
3. Select **Service Accounts** from the left sidebar.
4. Find or create a service account with the required permissions and copy the service account email.

#### To get the `NEWS_API_KEY`:
1. Visit [NewsAPI](https://newsapi.org/).
2. Sign up and generate your API key.

#### To get the `credentials.json` from GCP:
1. In Google Cloud Console, go to **IAM & Admin > Service Accounts**.
2. Select the service account you want to use or create a new one.
3. Once the service account is created, click on it, go to **Keys**, and select **Add Key > Create New Key**.
4. Choose **JSON** as the key type.
5. Download the `credentials.json` file and store it securely.

---

### 8. **Deactivate the Virtual Environment**

Once you are done, deactivate the virtual environment by running:
```bash
pyenv deactivate
```

---

## Additional Notes

- If you want to set the virtual environment for a specific project, navigate to your project folder and run:
  ```bash
  pyenv local myenv
  ```
  This will create a `.python-version` file in your project directory to automatically activate the environment when you enter the folder.

- You can list all installed Python versions and environments with:
  ```bash
  pyenv versions
  ```

- Make sure to keep your API keys and `credentials.json` file secure and not commit them to version control.