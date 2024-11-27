Aqui está a versão atualizada do README, incluindo as instruções sobre o uso do ambiente virtual (venv) e a instalação com **pipenv**:

---

<p align="center">
  <a href="#-about-the-project">About</a> •
  <a href="#-features">Features</a> •
  <a href="#-layout">Layout</a> • 
  <a href="#-how-to-run-the-project">How to Run</a> • 
  <a href="#-technologies">Technologies</a> • 
  <a href="#-how-to-contribute-to-the-project">Contribute</a> • 
  <a href="#-license">License</a> • 
  <a href="#-contributors">Contributors</a>
</p>

## 💻 About the project

**pythonVim** is a simple code editor and a custom programming language built with Python. The project is designed to be beginner-friendly, focusing on simplicity and ease of use. The editor enables users to write, test, and run code in the custom language directly in an online environment, using **OnlineGDB** as the primary platform.

---

## ⚙️ Features

- **Simple Code Editor**: A minimalist interface for writing and testing code.
- **Custom Language**: A lightweight programming language designed for ease of understanding.
- **Code Execution**: Run your code directly in the editor and view the results instantly.
- **Intuitive Interface**: A clean and distraction-free design, ideal for beginners learning to code.

---

## 🎨 Layout

The editor's layout is straightforward and functional, comprising the following:

- **Code Editing Area**: A space to write code.
- **Output Area**: Displays the execution results, including outputs and error messages.

The interface is designed to help users focus on coding and immediate feedback.

---

## 🚀 How to Run the Project

1. **Clone the repository**:  

   To run the project locally, clone the repository:

   ```bash
   git clone https://github.com/oVitorio-ac/pythonVim.git
   cd pythonVim
   ```

2. **Set up a virtual environment**:  

   Create and activate a virtual environment using `pipenv` to manage dependencies:

   ```bash
   # Install pipenv if not already installed
    python -m venv .venv
    .\.venv\Scripts\activate
    pip install --upgrade pip
    pip install pipenv
    # Create and activate the virtual environment
    pipenv install
   ```

3. **Run the Python script**:  

   Execute the Python script to start using the editor:

   ```bash
   python main.py
   ```

4. **Optional: Use OnlineGDB**:  

   If you'd prefer an online solution, you can upload the script to [OnlineGDB](https://www.onlinegdb.com/_www_7lvb?classId=ca4e133a-0236-4601-b403-6bd1ba97a369&assignmentId=d435f079-f0ae-4d22-9a64-ca87f42cf98e&submissionId=10b584aa-071e-b61c-c94a-238688755fa3) and run it there.

---

## 🛠 Technologies

- **Python**: Used to develop the code editor and the custom programming language.
- **pipenv**: For managing project dependencies and creating a virtual environment.
- **OnlineGDB**: Online IDE for running and testing the project.

---

## 🤝 How to Contribute to the Project

1. Fork the repository.  
2. Create a branch for your feature: `git checkout -b feature/your-feature-name`.  
3. Commit your changes: `git commit -m "Add some feature"`.  
4. Push to the branch: `git push origin feature/your-feature-name`.  
5. Open a Pull Request.

All contributions are welcome! Please feel free to suggest improvements, new features, or report issues.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 👥 Contributors

- [oVitorio-ac](https://github.com/oVitorio-ac)  

