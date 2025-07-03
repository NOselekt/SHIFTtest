// Function to hash the password using SHA-256
async function hashPassword(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
}

// Event listener for the "Get Token" button
document.getElementById('getTokenBtn').addEventListener('click', async () => {
  const login = document.getElementById('login').value.trim();
  const password = document.getElementById('password').value;

  if (!login || !password) return alert('Введите логин и пароль');

  const hashedPassword = await hashPassword(password);

  const formData = new FormData();
  formData.append('login', login);
  formData.append('password', hashedPassword);

  try {
    const response = await fetch('/employee_salary/login', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (response.ok && data.token) {
      var oldEle = document.getElementById("getTokenBtn");
      var newEle = document.createElement("div");
      newEle.className = "new-token";
      newEle.innerHTML = data.token + "<br>(Скопировано в буфер обмена)";
      navigator.clipboard.writeText(data.token);
      oldEle.parentNode.replaceChild(newEle, oldEle);
      document.getElementById('tokenInput').value = data.token;
      document.getElementById('tokenInput').value = data.token;
    } else {
      alert(data.detail);
    }
  } catch (err) {
    alert('Ошибка соединения с сервером');
  }
});

// Event listener for the "Get Data" button
document.getElementById('getDataBtn').addEventListener('click', async () => {
  const token = document.getElementById('tokenInput').value.trim();
  if (!token) return alert('Введите токен');

  const formData = new FormData();
  formData.append('token', token);

  try {
    const response = await fetch('/employee_salary/token', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (response.ok) {
      document.getElementById('tokenStatus').textContent = 'Токен верный';
      document.getElementById('salary').textContent = data.salary + ' ₽';
      document.getElementById('nextSalaryIncrease').textContent = data.next_salary_increase;
    } else {
      document.getElementById('tokenStatus').textContent = 'Неверный токен';
      document.getElementById('tokenStatus').style.color = 'red';
    }
  } catch (err) {
    alert('Ошибка запроса');
  }
});
