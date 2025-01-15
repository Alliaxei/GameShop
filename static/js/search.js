document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");
    const resultContainer = document.querySelector(".catalog-games-grid");

    searchInput.addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();

            const query = searchInput.value.trim(); //trim удаляет пробелы в начале и конце строки

        if (query.length>= 0) {
            fetch(`/catalog/ajax/search/?search=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    resultContainer.innerHTML = '';

                    if (data.games.length > 0) {
                        data.games.forEach((game) => {
                            const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
                            console.log("Переданный game_id:", game.id);
                            const cardHTML = `
                                    <form method="post" action="/add_to_cart/">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <button type="submit">
                                            <div class="catalog-game-card">
                                                <img src="${game.image}" alt="${game.name}" class="catalog-game-image">
                                                <h3>${game.name}</h3>
                                                <p><strong>Цена:</strong> $${game.price}</p>
                                                <img
                                                    src="${game.in_cart ? '/static/images/checkmark.png' : '/static/images/cart.png'}"
                                                    alt="Корзина" 
                                                    class="cart-icon"
                                                    data-game-id="${game.id}"
                                                    data-add-to-cart-url="/cart/add/"
                                                    data-checkmark-url="/static/images/checkmark.png"
                                                    data-cart-url="/static/images/cart.png"
                                                    data-remove-url="/cart/remove/">   
                                               </div>
                                            <input type="hidden" name="game_id" value="${game.id}">
                                        </button>
                                    </form>
                                `;
                            resultContainer.insertAdjacentHTML('beforeend',  cardHTML);

                        });
                    } else {
                        resultContainer.innerHTML = "Игры не найдено";

                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    resultContainer.innerHTML = '<p>Произошла ошибка</p>';
                });
            } else {
             resultContainer.innerHTML = '';
        }
        }
    });
});