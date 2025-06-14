// Вспомогательная функция — если CSRF без exempt:
function getCookie(name) {
  const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return v ? v.pop() : '';
}

async function updateCartOnServer(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      //'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(body)
  });
  return res.json();
}

async function addToCart(id, qty = 1) {
  const data = await updateCartOnServer('/api/cart/add/', { product_id: id, quantity: qty });
  console.log('Cart after add:', data.cart || data);  // для дебага
  renderCart();  
}

async function removeFromCart(id) {
  const data = await updateCartOnServer('/api/cart/remove/', { product_id: id });
  console.log('Cart after remove:', data.cart || data);
  renderCart();
}

async function renderCart() {
  const res = await fetch('/api/cart/');
  const { items, total } = await res.json();
  const container = document.getElementById('cart');
  if (!container) return;
  container.innerHTML = `
    <h1>Корзина</h1>
    ${items.map(item => `
      <div class="cart-item-row">
        <img src="${item.product.image || item.product.images[0]}" alt="${item.product.name}">
        <div class="info">
          <a href="/${item.product.id}/">${item.product.name}</a>
          <p>${item.price} ₽ × ${item.quantity}</p>
        </div>
        <div class="controls">
          <button data-action="dec" data-id="${item.product.id}">−</button>
          <span>${item.quantity}</span>
          <button data-action="inc" data-id="${item.product.id}">+</button>
          <button data-action="remove" data-id="${item.product.id}">×</button>
        </div>
      </div>
    `).join('')}
    <div class="cart-total">Итого: ${total} ₽</div>
  `;
  container.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.id;
      const action = btn.dataset.action;
      let url = '/api/cart/';
      let method = 'POST';
      let bodyData = { product_id: id, quantity: 1 };

      if (action === 'inc') {
        url = '/api/cart/add/';
      } else if (action === 'dec') {
        url = '/api/cart/add/';
        bodyData.quantity = -1;
      } else if (action === 'remove') {
        url = '/api/cart/remove/';
      }
      await fetch(url, {
        method,
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(bodyData)
      });
      renderCart();
    });
  });
}

// Навешиваем кнопку «В корзину» на странице товара
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('#add-to-cart').forEach(btn =>
    btn.addEventListener('click', ()=> addToCart(btn.dataset.id))
  );
  renderCart();
});
