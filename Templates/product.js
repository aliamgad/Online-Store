// Array of products (example data, should be replaced with actual data)
const products = [
    {
        id: 1,
        name: 'Product 1',
        image: 'https://via.placeholder.com/600x400',
        price: '$29.99',
        description: 'Description for Product 1',
        related: [2, 3]
    },
    {
        id: 2,
        name: 'Product 2',
        image: 'https://via.placeholder.com/600x400',
        price: '$49.99',
        description: 'Description for Product 2',
        related: [1, 3]
    },
    {
        id: 3,
        name: 'Product 3',
        image: 'https://via.placeholder.com/600x400',
        price: '$19.99',
        description: 'Description for Product 3',
        related: [1, 2]
    }
];

function getProductById(id) {
    return products.find(product => product.id == id);
}

function displayProductDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    const product = getProductById(productId);
    const productDetails = document.getElementById('product-details');
    const relatedProductList = document.getElementById('related-product-list');

    if (product) {
        productDetails.innerHTML = `
            <div class="product-detail-container">
                <div class="product-image">
                    <img src="${product.image}" alt="${product.name}">
                </div>
                <div class="product-info">
                    <h1>${product.name}</h1>
                    <p class="price">${product.price}</p>
                    <p class="description">${product.description}</p>
                    <button id="toggle-cart">${isProductInCart(productId) ? 'Remove from Cart' : 'Add to Cart'}</button>
                </div>
            </div>
        `;

        // Display related products
        const relatedProducts = product.related.map(id => getProductById(id)).filter(Boolean);
        relatedProducts.forEach(relatedProduct => {
            const relatedProductDiv = document.createElement('div');
            relatedProductDiv.className = 'product';

            relatedProductDiv.innerHTML = `
                <a href="product.html?id=${relatedProduct.id}">
                    <img src="${relatedProduct.image}" alt="${relatedProduct.name}">
                    <h3>${relatedProduct.name}</h3>
                    <p class="price">${relatedProduct.price}</p>
                </a>
            `;

            relatedProductList.appendChild(relatedProductDiv);
        });

        document.getElementById('toggle-cart').addEventListener('click', () => {
            toggleCartStatus(productId);
        });
    } else {
        productDetails.innerHTML = `<p>Product not found.</p>`;
    }
}

function isProductInCart(productId) {
    // Mock function to check if the product is in the cart
    return false; // Placeholder
}

function toggleCartStatus(productId) {
    // Mock function to add/remove product from cart
    alert(`Product ${productId} cart status toggled.`);
}

document.addEventListener('DOMContentLoaded', displayProductDetails);
