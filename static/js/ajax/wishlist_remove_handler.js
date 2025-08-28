document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".remove-from-wishlist").forEach(button => {
        button.addEventListener("click", function() {
            let form = this.closest(".cart-form");
            let url = form.dataset.removeUrl;
            let csrfToken = form.querySelector("input[name=csrfmiddlewaretoken]").value;
            let wishlistId = this.dataset.wishlistId;

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
                    let wishlistWrapper = document.getElementById(`wishlist-wrapper-${wishlistId}`);
                    if (wishlistWrapper) {
                        wishlistWrapper.remove();
                    }
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error when deleting product from the wishlist.");
            })
        });
    });
});