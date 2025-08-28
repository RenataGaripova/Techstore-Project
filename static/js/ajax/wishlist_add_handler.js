document.addEventListener("click", function(e) {
    const csrftokenElem = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrftokenElem) return;
    const csrftoken = csrftokenElem.value;


    if (e.target.classList.contains("add-to-wishlist")) {
        const form = e.target.closest(".cart-form");
        let url = form.dataset.wishlistUrl;
    
        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest"
            },
            body: ""
        })
        .then(res => res.json())
        .then(data => {
            console.log("Wishlist answer:", data);
            alert("✅ " + data.message);
        })
        .catch(err => console.error("Error:", err));
    }
});