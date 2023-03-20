const baseUrl = "http://localhost:8080";
const authData = { sessionToken: null, company: null };

async function blockLoginPage() {
  if (await userLogged()) {
    window.location.href = "comandas.html";
  }
}

async function submitLogin(event) {
  event.preventDefault(); // Evita que o formulário seja enviado da forma tradicional
  if (!(await userLogged())) {
    // Obtém os valores dos campos do formulário
    const username = document.querySelector('input[name="username"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const company = document.querySelector('input[name="company"]').value;

    // Cria um objeto com os dados do login
    const data = {
      username,
      password,
      company,
    };
    // Faz a requisição de login para a API usando o Axios
    axios
      .get(baseUrl + "/auth/user", { params: data })
      .then((response) => {
        // Se a requisição for bem-sucedida, redireciona o usuário para a página de dashboard
        saveUserData(response.data, company);
        window.location.href = "comandas.html";
      })
      .catch((error) => {
        // Se houver um erro na requisição, exibe uma mensagem de erro para o usuário
        alert("Erro ao fazer login: " + error.message);
      });
  } else {
    alert("Já há um usuário logado!");
    window.location.href = "comandas.html";
  }
}

function saveUserData(userData, company) {
  userData.company = company;
  authData.sessionToken = userData.sessionToken;
  authData.company = userData.company;
  localStorage.setItem("userData", JSON.stringify(userData));
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
  logged = false
  if (params.receiver) {
    logged = await axios({
      method: "get",
      url: baseUrl + "/users/notifications",
      headers: loadAuthData(),
      params: params,
    }).then((response) => {
      return true;
    });
  }

  return logged || false;
}

blockLoginPage();
