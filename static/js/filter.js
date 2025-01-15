document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("apply-filters").addEventListener("click", async ()=>{
    const filters = {
        price_max: document.getElementById("price-range").value,
    }

    try {
        const response = await fetch("/apply_filters/", {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(filters),
        });
        if (!response.ok) {
             throw new Error(`Ошибка: ${response.status}`);
        }

        const data = await response.json();
        updateGames(data.games);
    } catch (error) {
        console.error("Ошибка запроса:", error);
    }
})

    function updateGames(games) {
        const container = document.querySelector(".catalog-games-grid");
        container.innerHTML = "";

        if (games.length === 0) {
            container.innerHTML = "<p>Игры не найдены.</p>";
            return;
        }
        games.forEach(game => {
            const gameCard = document.createElement("form");
            gameCard.method = "post";
            gameCard.action = `extended_info${game.id}/`;
            gameCard.innerHTML = `
                <input type="hidden" name="csrfmiddlewaretoken" value="${getCsrfToken()}">
                <button type="submit" class="game-details-link">
                    <div class="catalog-game-card">
                        <img 
                            src="${game.image ? game.image : '/static/images/cart.png'}" 
                            alt="${game.name}" 
                            class="catalog-game-image">
                        <h3>${game.name}</h3>
                        <p><strong>Цена:</strong> $${game.price}</p>
                        <img 
                            src="${game.in_cart ? '/static/images/checkmark.png' : '/static/images/cart.png'}" 
                            alt="Корзина"
                            class="cart-icon"
                            data-game-id="${game.id}"
                            data-add-to-cart-url="/add_to_cart/"
                            data-checkmark-url="/static/images/checkmark.png"
                            data-cart-url="/static/images/cart.png"
                            data-remove-url="/remove_from_cart/">
                    </div>
                </button>
            `;
            container.appendChild(gameCard);
        })

    }
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function getCsrfToken() {
        const csrfElement =  document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfElement) {
            return csrfElement.value;
        }
         console.warn("CSRF токен не найден!");
        return "";
    }
})


