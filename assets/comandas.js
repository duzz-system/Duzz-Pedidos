const baseUrl = "http://localhost:8080";
const authData = { sessionToken: null, company: null };
const sessions = [];
const products = {};

// Obtém o modal e o botão
var modalNovaComanda = document.getElementById("modal");
var modalComanda = document.getElementById("modal-comandas");
var botao = document.querySelector(".botao-flutuante");

async function exibirComanda(comanda) {
  modalComanda.style.display = "block";
  comandaId = comanda.lastElementChild;
  if (!comandaId) {
    comandaId = comanda.parentElement.lastElementChild;
  }
  comandaData = await getComandas(comandaId.value);
  comandaData = comandaData[0];

  modalComanda.firstElementChild.firstElementChild.innerHTML =
    comandaData.identifier;
  productsTable =
    modalComanda.firstElementChild.getElementsByTagName("table")[0]
      .lastElementChild;
  console.log(comandaData);
  for (value of comandaData.sale_metadata.products) {
    itemQuantidade = JSON.parse(comandaData.products);
    produto = await getProductName(value.item);
    console.log(produto);
    productsTable.innerHTML += `
    <tr>
      <td>${value.item}</td>
      <td>${produto.name}</td>
      <td>${itemQuantidade[value.item]}</td>
      <td>R$ ${produto.value}</td>
      <td>R$ ${value.gain}</td>
    </tr>`;
  }
}

function ocultarComanda() {
  productsTable =
    modalComanda.firstElementChild.getElementsByTagName("table")[0]
      .lastElementChild;
  productsTable.innerHTML = "";
}

// Quando o botão é clicado, exibe o modal
botao.onclick = function () {
  modalNovaComanda.style.display = "block";
};

// Quando o usuário clica fora do modal, ele é fechado
window.onclick = function (event) {
  if (event.target == modalNovaComanda || event.target == modalComanda) {
    modalNovaComanda.style.display = "none";
    modalComanda.style.display = "none";
    ocultarComanda();
  }
};

async function generateComandas() {
  container = document.getElementById("cards");
  const comandas = await getComandas();
  comandas.map((values) => {
    if (!sessions.includes(values.session_id)) {
      container.innerHTML += `
      <div class="card">
      <div class="card-title">${values.identifier}</div>
      <div class="card-title">R$ ${values.sale_metadata.total}</div>
      <div class="card-content">${values.responsible}</div>
      <input value="${values.session_id}" type="hidden">
      </div>
      `;
      sessions.push(values.session_id);
    }
  });

  comandasElements = document.getElementsByClassName("card");
  for (let comanda of comandasElements) {
    comanda.addEventListener("click", (event) => {
      el = event.srcElement;
      exibirComanda(el);
    });
  }
}

async function showComandaData(comanda) {}

async function getComandas(comandaId) {
  comandas = [];
  if (await userLogged()) {
    comandas = await axios({
      method: "get",
      url: baseUrl + "/sales/sessions",
      headers: loadAuthData(),
      params: { session_id: comandaId },
    }).then((response) => {
      return response.data;
    });
  } else {
    window.location.href = "index.html";
  }
  return comandas;
}

function getUserData() {
  return JSON.parse(localStorage.getItem("userData")) || {};
}

function loadAuthData() {
  if (!authData.sessionToken) {
    userData = getUserData();
    authData.company = userData.company;
    authData.sessionToken = userData.sessionToken;
  }
  return authData;
}

async function userLogged() {
  userData = getUserData();
  params = { receiver: userData.id };
  logged = false;
  if (params.receiver) {
    logged = await axios({
      method: "get",
      url: baseUrl + "/users/notifications",
      headers: loadAuthData(),
      params: params,
    })
      .then((response) => {
        return true;
      })
      .catch((error) => {
        return false;
      });
  }

  return logged || false;
}

async function getProductName(product) {
  if (!products[product]) {
    produto = await axios({
      method: "get",
      url: baseUrl + "/products",
      headers: loadAuthData(),
      params: { id: product },
    }).then((response) => {
      return response.data;
    });
    products[produto[0].id] = produto[0];
  }
  return products[product];
}
generateComandas();
// setInterval(generateComandas, 1000);
