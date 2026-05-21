# 🍔 E-Menu Telegram Food Ordering Bot

A fully functional, feature-rich Telegram Bot for food ordering and restaurant management. Built with Python and SQLite, this bot provides a seamless ordering experience for customers and a powerful management interface for restaurant owners.

## ✨ Features

### For Customers (Users)
* **🛒 Interactive Menu:** Browse categories like Pizza 🍕, Burger 🍔, Seafood 🦞, Korean 🍜, Steak 🥩, and Drinks 🥤 using inline keyboards.
* **📦 Smart Shopping Cart:** Add items, adjust quantities, view cart, and clear cart easily.
* **💾 Profile Memory:** Automatically remembers the customer's phone number and delivery address for faster checkout on future orders.
* **📜 Order History & Reorder:** Customers can view their latest 5 orders and instantly re-add items to their cart with a single click.
* **💳 Flexible Payment:** Supports Cash on Delivery (COD) and QR Code Payment.

### For Restaurant Owners (Admin)
* **🛎️ Instant Notifications:** Receive new orders directly in the Admin's Telegram chat.
* **⚙️ Quick Action Buttons:** Accept, Reject, or mark orders as "Delivering" directly from the chat.
* **📢 Broadcast System:** Send promotional messages or images to all customers who have interacted with the bot using a secret `/broadcast` command.

### Technical & System
* **🗄️ Local Database (SQLite):** Lightweight, fast, and auto-generates tables upon first run.
* **🔄 Auto-Reconnect Logic:** Built-in infinite polling loop to automatically recover from proxy drops or temporary network disconnections.
* **☁️ Cloud-Ready:** Optimized for free hosting platforms like PythonAnywhere.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Library:** `pyTelegramBotAPI` (Telebot)
* **Database:** SQLite3
* **Environment Management:** `python-dotenv`

---

## 🚀 Installation & Setup

Follow these steps to run the bot on your local machine or server:

### 1. Clone the repository
```bash
git clone [https://github.com/DUC2026-PGB-HNKSR-CloudServer/emenu-bot.git](https://github.com/DUC2026-PGB-HNKSR-CloudServer/emenu-bot.git)
cd emenu-bot
