(function () {
    const select_variations = document.getElementById('select-variations');
    const variation_price = document.getElementById('variation-price');
    const variation_promotional_price = document.getElementById('variation-promotional_price');

    if (!select_variations || !variation_price) {
        return;
    }

    select_variations.addEventListener('change', function () {
        price = this.options[this.selectedIndex].getAttribute('data-price');
        promotional_price = this.options[this.selectedIndex].getAttribute('data-promotional-price');

        variation_price.innerHTML = price;

        if (variation_promotional_price) {
            variation_promotional_price.innerHTML = promotional_price;
        }
    })
})();
