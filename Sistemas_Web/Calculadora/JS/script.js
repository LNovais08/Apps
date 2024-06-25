var lista = [];

function numeroEscolhido(num) {
    var result = document.getElementById('result');
    result.value += num;
}

// Função para registrar o operador escolhido
function operadorEscolhido(operador) {
    var result = document.getElementById('result');
    lista.push(result.value);
    lista.push(operador);
    result.value += " " + operador + " ";
}

// Função para calcular o resultado
function calcular() {
    var result = document.getElementById('result');
    lista.push(result.value.split(" ").pop()); // Pega o último número inserido após o operador
    
    var num1 = parseFloat(lista[0]);
    var operador = lista[1];
    var num2 = parseFloat(lista[2]);
    var resultado = 0;

    switch (operador) {
        case '+':
            resultado = num1 + num2;
            break;
        case '-':
            resultado = num1 - num2;
            break;
        case '*':
            resultado = num1 * num2;
            break;
        case '/':
            resultado = num1 / num2;
            break;
    }

    result.value = resultado;
    lista = [];
}

// Função para limpar a tela e a lista
function limpar() {
    var result = document.getElementById('result');
    result.value = '';
    lista = [];
}
