# Banker's Algorithm GUI – Python

A Python-based **Graphical User Interface (GUI)** implementation of the **Banker's Algorithm** for deadlock avoidance in operating systems.  
This project was built using **Tkinter** and demonstrates:  

- Resource Allocation & Safety Algorithm  
- Need Matrix calculation  
- Safe Sequence detection  
- Handling **Resource Requests** using Banker's request algorithm  

---

## Features
- **Interactive GUI** with input tables for:  
  - Allocation Matrix  
  - Max Matrix  
  - Available Vector  
- **Dynamic table resizing**: set the number of processes (`n`) and resources (`m`) and rebuild input grids.  
- **Load Sample Data**: Quickly load a classic textbook example.  
- **Compute Safety**:  
  - Shows the Need Matrix  
  - Displays whether the system is in a **Safe or Unsafe state**  
  - Provides the Safe Sequence if one exists  
- **Resource Requests**:  
  - Submit a request for a process  
  - Banker’s Algorithm checks if it can be safely granted  
  - Updates Allocation and Available if approved  

---

## 🚀 How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/bankers-algorithm-gui.git
   cd bankers-algorithm-gui
