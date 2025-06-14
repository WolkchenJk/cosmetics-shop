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
    <h2>Корзина</h2>
    ${items.map(i => `
      <div>
        ${i.name} × ${i.quantity} = ${i.subtotal} ₽
        <button data-id="${i.id}" class="remove">×</button>
      </div>
    `).join('')}
    <p><strong>Итого:</strong> ${total} ₽</p>
  `;
  container.querySelectorAll('.remove').forEach(btn =>
    btn.addEventListener('click', ()=> removeFromCart(btn.dataset.id))
  );
}

// Навешиваем кнопку «В корзину» на странице товара
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('#add-to-cart').forEach(btn =>
    btn.addEventListener('click', ()=> addToCart(btn.dataset.id))
  );
  renderCart();
});
