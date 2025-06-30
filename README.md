
<h1 align="center">📦 Order Management System</h1>

<div align="center">
  <table>
    <tr>
      <td width="55%">
        <h3><b>About the Project</b></h3>
        <p>
          The <strong>Order Management System</strong> is a dynamic, interactive web application built using <strong>Streamlit</strong> that allows users to efficiently <strong>place orders</strong>, manage <strong>inventory</strong> across warehouses, and analyze <strong>sales patterns</strong>. 
          It includes intelligent <strong>warehouse allocation logic</strong> based on city and availability — ensuring optimal logistics and cost efficiency.
        </p>
        <p>
          🔗 <strong>Live Project:</strong> <a href="https://ordermanage.streamlit.app/" target="_blank">https://ordermanage.streamlit.app/</a>
        </p>
      </td>
      <td width="45%">
        <img src="https://media.giphy.com/media/26xBwdIuRJiAIqHwA/giphy.gif" width="100%">
      </td>
    </tr>
  </table>
</div>

---

## ✅ Features

- 🔍 Search and place orders by city and product
- 🧠 Intelligent warehouse allocation to minimize delivery cost
- 📦 Auto-invoice generation upon successful order
- 📊 Inventory analytics and restocking interface
- 🔒 Orders are validated to ensure all required details are entered correctly
- 📈 Sales analysis by city, product frequency, trending patterns, and order cost visualized through graphs

---

## 🧰 Tech Stack Used

| Category        | Tools / Libraries                         |
|----------------|--------------------------------------------|
| 🐍 Programming  | Python 3.x                                 |
| 🖼️ UI Framework | Streamlit                                  |
| 📊 Data Handling| Pandas                                     |
| 💾 Storage      | JSON (for inventory & order tracking)      |
| 📦 Deployment   | Streamlit Cloud                            |

---

## 📁 Project Structure

```bash
order_management-system/
├── app.py                 # Streamlit UI main script
├── logic/
│   ├── allocator.py       # Core logic for order allocation
│   └── utils.py           # Utility functions
├── data/
│   ├── inventory.json     # Product and warehouse data
│   └── orders.json        # Logged order data
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## ▶️ How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Technicalarpan/order_management-system.git
cd order_management-system
```

### 2. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

OR (alternative):

```bash
python -m streamlit run app.py
```

---

## 💡 How It Works

| Tab             | Functionality                                                                 |
|------------------|------------------------------------------------------------------------------|
| 📦 **Place Order** | Select a city, product, and quantity. The system automatically chooses the most optimal warehouse based on stock availability. |
| 🔄 **Restock**     | Easily add new inventory to any warehouse using an intuitive form.         |
| 📈 **Analytics**   | View graphs and metrics on order trends, top cities, most-ordered items, and revenue. |

---

## 🔮 Future Enhancements

- 🔐 Implement admin login for restricted actions (e.g., restocking)
- 📤 Export order history as CSV or Excel
- 🧩 Integrate a persistent database like SQLite or PostgreSQL
- 🗺️ Real-time map-based warehouse routing system

---

## 🙌 Contributions

Contributions and suggestions are welcome!  
If you'd like to improve the project:

```bash
# Fork the repository
git clone <your-fork-url>

# Create your feature branch
git checkout -b feature/your-feature

# Commit and push your changes
git push origin feature/your-feature
```

Open a Pull Request for review!

---

## 📜 License

This project is licensed under the **MIT License**.  
You're free to use, distribute, and modify the codebase.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

---

<h3 align="center">💼 Built with ❤️ by <a href="https://github.com/Technicalarpan" target="_blank">Arpan Mukherjee</a> 💼</h3>
