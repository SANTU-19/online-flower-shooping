function showToast(msg) {
  const toast = document.getElementById("toast-message");
  toast.innerText = msg;
  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 1000);
}


function addToCart(productId, productName) {
  fetch(`/cart/add/${productId}/`)
    .then(response => response.json())
    .then(data => {
      const badge = document.getElementById("cart-badge");
      if (badge) {
        badge.innerText = data.cart_count;
        badge.style.display = "inline-block";
      }

      // Show animated toast
      showToast(`${productName} added to cart!`);
    })
    .catch(error => {
      console.error("Error:", error);
      showToast(`Error adding ${productName}`);
    });
}

function openProfile() {
    document.getElementById("profile-drawer").classList.add("active");
    document.getElementById("profile-overlay").classList.add("active");
    document.body.classList.add("blur");
}

function closeProfile() {
    document.getElementById("profile-drawer").classList.remove("active");
    document.getElementById("profile-overlay").classList.remove("active");
    document.body.classList.remove("blur");
}


