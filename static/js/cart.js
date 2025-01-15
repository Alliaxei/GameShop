document.addEventListener("DOMContentLoaded", function () {
    const cartIcons = document.querySelectorAll('.cart-icon');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    // Добавление/Удаление из корзины
    cartIcons.forEach(function (icon) {
        icon.addEventListener('click', function (e) {
            console.log("Добавление объекта в корзину");
            e.preventDefault();
            e.stopPropagation();

            const gameId = icon.getAttribute('data-game-id');
            const addToCartUrl = icon.getAttribute('data-add-to-cart-url');
            const checkmarkUrl = icon.getAttribute('data-checkmark-url');
            const cartIconSrc = icon.src;
            const removeFromCartUrl = icon.getAttribute('data-remove-url');
            const cartIconDefaultUrl = icon.getAttribute('data-cart-url');

            //Добавление
            if (cartIconSrc.includes('cart.png')) {
                console.log("Настоящее добавление в корзину");

                icon.disabled = true;

                fetch( addToCartUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': csrfToken,
                    },
                    body: new URLSearchParams({
                        'game_id': gameId,
                })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert("Ошибка " + data.error);
                    }
                    else {
                        icon.src = checkmarkUrl;
                    }
                })
                    .catch(error => {
                        console.error('Ошибка при добавлении в корзину ' + error.message);
                })
                    .finally(() => {
                        icon.disabled = false;
                    });
                //Удаление
                } else {

                    fetch(removeFromCartUrl, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken,
                        },
                        body: JSON.stringify({game_id: gameId}),
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            alert(data.error);
                        } else {
                            icon.src = cartIconDefaultUrl;
                        }
                    })
                    .catch(error => {
                        console.error('Ошибка при удалении из корзины ' + error.message);
                    });
            }
        });
    });

    function handleRemoveClick(e) {
        e.preventDefault();
        //Передача необходимых данных из кнопки, а не из img внутри
        const btn = e.target.closest('.remove-btn');
        if (!btn) return;

        const gameId = btn.getAttribute('data-game-id');
        const removeUrl = btn.getAttribute('data-remove-url');

         fetch( removeUrl, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({game_id: gameId}),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            }
            else {
                // alert(data.message);
                const row = btn.closest('tr');
                row.remove();

                //checkEmptyCart();
            }
        })
        .catch(error => {
            console.error(error);
        });
    }

    // function checkEmptyCart() {
    //     const cartContainer = document.querySelector('.cart-items-container')
    //     const cartRows = document.querySelectorAll('tr');
    //
    //         if (cartRows.length === 0) {
    //             cartContainer.innerHTML = '<p>Корзина пуста</p>';
    //     }
    // }

    function setRemoveButtonsEventListeners() {
        const removeBtns = document.querySelectorAll('.remove-btn');
       removeBtns.forEach(btn => {
            btn.addEventListener('click', handleRemoveClick);
        });
    }

    //Не работает
    //checkEmptyCart();

    setRemoveButtonsEventListeners();
});