# MATHS ISE

## Interactive Discrete Mathematics Computational & Visualization Platform

This project is an interactive platform designed to help visualize and compute various discrete mathematics concepts. It serves as an educational tool for the Discrete Mathematics course.

Course Code: 7MA206  
Walchand College of Engineering, Sangli.

---

## Project Overview

The Maths ISE platform provides a seamless frontend and backend architecture to teach students and users fundamental mathematical operations.
- The **Landing Page** acts as a user-friendly entry point, built purely with HTML and CSS to maintain an academic and clean design.
- The **Mathematical Modules** process operations like logical truth tables, set relations, and relational properties. These modules are implemented using Python.
- **Streamlit** is used to bridge the Python mathematics with an interactive web interface, allowing users to enter mathematical parameters and immediately see visual and calculated results.

---

## Features

### Logic & Proof
- **Basic Logical Operations:** Evaluates logical operators with truth tables.
- **User-Defined Logical Expression:** Evaluates complex custom logical propositions.
- **Conditional Propositions:** Provides analysis and breakdown of condition-based logical statements.

### Set Operations
- **Mathematical Evaluation:** Performs unions, intersections, and other operations on one or multiple sets.
- **Result & Explanation:** Summarizes resulting sets, cardinality, and step-by-step logic.
- **Venn Diagrams:** Visually explores set relations using Matplotlib.

### Relations & Functions
- **Relation Diagram:** Visually maps domain and codomain using directed graphs.
- **Domain, Range, and Codomain analysis:** Identifies elements and their mappings.
- **Relation Properties:** Evaluates reflexivity, symmetry, antisymmetry, and transitivity.
- **Transitive Closure:** Computes and displays the complete transitive closure.
- **Hasse Diagrams:** Visualizes relations that qualify as partial orders.

---

## Technology Stack

**Frontend:**
- HTML5
- CSS3

**Mathematical/Interactive Backend:**
- Python
- Streamlit
- Pandas
- NetworkX
- Matplotlib (and Matplotlib-Venn)

---

## Project Structure

```text
MATHS-ISE/
│
├── index.html
├── style.css
├── README.md
├── requirements.txt
├── .gitignore
├── streamlit_app.py
│
├── assest/
│   └── images.jpg
│
└── Python Files/
    ├── logic.py
    ├── sets.py
    └── relations.py
```

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Chaitanyapakhare7/Maths-ISE.git
```

### 2. Enter the project directory
```bash
cd Maths-ISE
```

### 3. Create a virtual environment
For Windows PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
*(If PowerShell execution policy causes an issue, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` before activating).*

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

This project runs using a local Streamlit server for the math modules and a static web server for the landing page.

**Terminal 1 (Streamlit Backend):**
Start the Streamlit application to serve the mathematical modules.
```bash
streamlit run streamlit_app.py
```
This will start Streamlit (typically on `http://localhost:8501`).

**Terminal 2 (Landing Page):**
Open the `index.html` file in your preferred web browser. You can do this by double-clicking the file or using a local static server.
```bash
# Example using Python's http.server
python -m http.server 8000
```
Navigate to `http://localhost:8000` (or whichever port you opened) in your browser. From the landing page, clicking on any module card will correctly navigate you to the corresponding local Streamlit module.

---

## Module Navigation

| Module | Python File | Purpose |
|---|---|---|
| Logic & Proof | `logic.py` | Evaluates logical operations, truth tables, and conditional propositions. |
| Set Operations | `sets.py` | Computes set logic, relationships, and generates visual Venn diagrams. |
| Relations & Functions | `relations.py` | Evaluates relations, closure, properties, and displays Hasse diagrams. |

---

## How to Contribute

1. Create a branch.
2. Make changes.
3. Test locally.
4. Commit.
5. Push branch.
6. Create Pull Request.

**Example workflow:**
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature

# Make your edits...

git add .
git commit -m "Add new graph visualization feature"
git push origin feature/your-feature
```

---

## Development Guidelines

- **Respect Existing Modules:** Do not modify another person's module unnecessarily.
- **Separation of Concerns:** Keep mathematical logic separated from UI code when expanding.
- **Test Before Committing:** Make sure all interactive components run properly.
- **Virtual Environments:** Do not commit virtual environments (e.g., `.venv`).
- **Secrets:** Do not commit secrets, API keys, or personal tokens.
- **Dependencies:** Keep `requirements.txt` updated if you introduce a new library.
- **Commits:** Use clear and meaningful commit messages.

---

## Team

### Developed By

1. **Chaitanya Pakhare**  
   PRN: 256109010

2. **Sahil Dadmal**  
   PRN: 256109014

3. **Sameer Ramteke**  
   PRN: 256109024

### Under the Guidance Of
**Prof. VA Potadar**

---

## Course Information

**Walchand College of Engineering, Sangli**  
**Course:** Discrete Mathematics  
**Course Code:** 7MA206  

---

## Future Scope

- Integration of additional discrete mathematics modules.
- Improved and highly customizable visualizations.
- Expanded proof tools for symbolic logic.
- Graph theory and traversals.
- Combinatorics and Number theory.
- Complete cloud deployment (e.g., via Streamlit Community Cloud or Vercel).
- Improved accessibility and mobile-friendly interactions for the Python modules.

---

## License

This project is developed as an academic project for the Discrete Mathematics course.
