// get CSRF token safely
const csrftoken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute('content');

document.querySelectorAll('.add-cart').forEach(button => {
    button.addEventListener('click', function () {
        const productId = this.dataset.id;

        fetch(`/cart/add/${productId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document.getElementById('cart-count').innerText = data.cart_count;
            }
        })
        .catch(err => console.error("Cart error:", err));
    });
});


