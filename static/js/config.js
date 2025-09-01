document.addEventListener('DOMContentLoaded', function() {
    const keywordsTextarea = document.getElementById('keywords');
    const suggestions = document.querySelectorAll('.add-keyword');

    // Função para adicionar sugestão ao textarea
    function addKeyword(keyword) {
        if (keywordsTextarea.value.trim() === '') {
            keywordsTextarea.value = keyword;
        } else {
            // Evita adicionar vírgula se o campo já terminar com uma
            if (keywordsTextarea.value.trim().slice(-1) !== ',') {
                keywordsTextarea.value += ', ';
            }
            keywordsTextarea.value += keyword;
        }
        keywordsTextarea.focus();
    }

    // Adiciona evento de clique para cada sugestão
    suggestions.forEach(badge => {
        badge.addEventListener('click', function() {
            addKeyword(this.textContent);
        });
    });
});