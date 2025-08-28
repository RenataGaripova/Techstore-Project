document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".remove-from-cart").forEach(button => {
        button.addEventListener("click", function() {
            let form = this.closest(".cart-form");
            let url = form.dataset.removeUrl;
            let csrfToken = form.querySelector("input[name=csrfmiddlewaretoken]").value;
            let cartId = this.dataset.cartId;

            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type":"application/x-www-form-urlencoded",
                    "X-CSRFToken": csrfToken
                },
                body: new URLSearchParams({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    form.remove();
                    let cartWrapper = document.getElementById(`cart-wrapper-${cartId}`);
                    if (cartWrapper) {
                        cartWrapper.remove();
                    }
                    let cartTotalEl = document.getElementById("cart-total");
                    if (cartTotalEl) {
                        cartTotalEl.textContent = data.cart_total + " $";
                    }
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error when deleting product from the cart.");
            })
        });
    });
});