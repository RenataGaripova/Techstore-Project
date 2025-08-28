document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".increase-item, .decrease-item").forEach(button => {
        button.addEventListener("click", function() {
            let form = this.closest(".cart-form");
            let url = form.dataset.url;
            let csrfToken = form.querySelector("input[name=csrfmiddlewaretoken]").value;
            let input = form.querySelector("input[name=quantity]");
            let currentQuantity = parseInt(input.value);
            let maxQuantity = parseInt(form.querySelector(".quantity-wrapper").dataset.max);

            if (this.classList.contains("increase-item")) {
                if (currentQuantity < maxQuantity) {
                    currentQuantity++;
                }
            } else {
                if (currentQuantity > 1) {
                    currentQuantity--;
                }
            }

            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type":"application/x-www-form-urlencoded",
                    "X-CSRFToken": csrfToken
                },
                body: new URLSearchParams({
                    quantity: currentQuantity
                })
            })
            .then(response => response.json())
            .then(data => {
                input.value = currentQuantity;

                if (data.cart_total) {
                    let cartTotalEl = document.getElementById("cart-total");
                    if (cartTotalEl) {
                        cartTotalEl.textContent = data.cart_total + " $";
                    }
                }
                if (data.product_total) {
                    let itemTotalEl = document.getElementById(`product-total-${data.cart_id}`);
                    if (itemTotalEl) {
                        itemTotalEl.textContent = "Subtotal: " + data.product_total + " $";
                    }
                }
            })
            .catch(error => {
                console.error("Ошибка:", error);
                alert("Ошибка при обновлении корзины");
            })
        });
    });
});