document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('overlay');
  const panel   = document.getElementById('cart-panel');
  const openBtn = document.querySelector('a[href="/cart/"]');
  const closeBtn= panel.querySelector('.cart-close');
  const body    = panel.querySelector('.cart-panel__body');
  const totalEl = document.getElementById('cart-total');

  function toggle(state) {
    overlay.classList.toggle('active', state);
    panel.classList.toggle('active', state);
  }

  async function loadCart() {
    const res = await fetch('/api/cart/');
      const { items, total } = await res.json();
      body.innerHTML = items.map(item => `
        <div class="cart-item-row">
          <img src="${item.image}" alt="${item.name}">
          <div class="info">
            <a href="/${item.id}/">${item.name}</a>
            <p>${item.price} ₽ × ${item.quantity}</p>
          </div>
          <div class="controls">
            <button data-action="dec" data-id="${item.id}">−</button>
            <span>${item.quantity}</span>
            <button data-action="inc" data-id="${item.id}">+</button>
            <button data-action="remove" data-id="${item.id}">×</button>
          </div>
        </div>
        `).join('');
      totalEl.textContent = total;
    attachHandlers();
  }

  function attachHandlers() {
    body.querySelectorAll('button').forEach(btn => {
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
        loadCart();
      });
    });
  }

  if (openBtn) {
    openBtn.addEventListener('click', e => {
      e.preventDefault();
      toggle(true);
      loadCart();
    });
  }
  closeBtn.addEventListener('click', () => toggle(false));
  overlay.addEventListener('click', () => toggle(false));
});
