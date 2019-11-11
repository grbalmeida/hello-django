(function () {
    const select_variation = document.getElementById('select-variation');
    const variation_price = document.getElementById('variation-price');
    const variation_price_promotional = document.getElementById('variation-price-promotional');

    if (!select_variation || !variation_price) {
        return;
    }

    select_variation.addEventListener('change', function () {
        price = this.options[this.selectedIndex].getAttribute('data-price');
        price_promotional = this.options[this.selectedIndex].getAttribute('data-price-promotional');

        variation_price.innerHTML = price;

        if (variation_price_promotional) {
            variation_price_promotional.innerHTML = price_promotional;
        }
    })
})();
