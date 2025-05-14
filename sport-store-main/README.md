
Built by https://www.blackbox.ai

---

# SPORT STORE

## Project Overview
SPORT STORE is a web application designed for selling sports equipment and apparel. It features a user-friendly interface for browsing products, managing a shopping cart, and processing orders through a seamless checkout system. The application uses JavaScript and local storage to handle cart functionality, ensuring a smooth shopping experience for users.

## Installation
To set up the SPORT STORE application locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sport-store.git
   ```
   
2. Navigate to the project directory:
   ```bash
   cd sport-store
   ```

3. Open `index.html` in your preferred web browser to view the application.

No additional installations are required, as dependencies are included via CDN links.

## Usage
- **Browse Products:** Users can navigate through different product categories and view highlighted products on the homepage.
- **Add to Cart:** Click the shopping cart icon on products to add them to your cart.
- **View Cart:** Users can view their cart at any time by clicking on the cart icon in the header.
- **Checkout:** If the cart is filled, users can proceed to checkout, enter shipping information, select a payment method, and complete their order.

## Features
- Responsive design using **Tailwind CSS** for a modern aesthetic.
- Dynamic cart management utilizing **local storage** to persist cart items across sessions.
- Real-time updates on cart quantity and total price.
- Checkout functionality, allowing users to enter shipping information and select payment methods.
- HTML content is structured for accessibility and usability.

## Dependencies
The project relies on the following external libraries:
- [Tailwind CSS](https://tailwindcss.com/)
- [Font Awesome](https://fontawesome.com/)

These are included via CDN links in the HTML files, so no manual installations are necessary.

## Project Structure
The project directory consists of the following main files:

```
/sport-store
│
├── index.html        # Homepage displaying products and categories
├── cart.html         # View and manage shopping cart
├── checkout.html     # Checkout page for order processing
├── cart.js           # JavaScript file handling cart functionality
├── common.js         # (Unused in this version)
├── styles.css        # (Optional) Custom styles
└── favicon.ico       # Favicon for the website
```

### Key Scripts & Styles
- **cart.js:** Core logic for managing cart items using class-based architecture for maintainability.
- **HTML Files:** Each HTML file is structured with a consistent layout and integrated scripting for dynamic behavior.

## Conclusion
This project provides an intuitive platform for users to browse and purchase sports equipment. It leverages modern web technologies to offer a seamless shopping experience, making it easy for sports enthusiasts to find and buy quality products.