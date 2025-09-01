document.addEventListener('DOMContentLoaded', function() {
  // Busca na tabela
  const buscaInput = document.getElementById('busca');
  const noResultsMessage = document.getElementById('no-results-message');
  
  if (buscaInput) {
    buscaInput.addEventListener('input', function(e) {
      const termo = e.target.value.toLowerCase();
      const tabela = document.getElementById('tabela-resultados');
      
      if (tabela) {
        const linhas = tabela.querySelectorAll('tbody tr');
        let visiveisCount = 0;
        
        linhas.forEach(linha => {
          const texto = linha.textContent.toLowerCase();
          const visivel = texto.includes(termo);
          linha.style.display = visivel ? '' : 'none';
          if (visivel) visiveisCount++;
        });
        
        // Mostrar ou esconder a mensagem de "nenhum resultado"
        if (noResultsMessage) {
            noResultsMessage.style.display = visiveisCount === 0 ? 'block' : 'none';
        }
        
        updateSearchCounter(visiveisCount, linhas.length);
      }
    });
  }

  // Animação nos cards de estatísticas
  const cards = document.querySelectorAll('.card');
  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-2px)';
      this.style.transition = 'transform 0.2s ease';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });

  // Tooltip para botões (se você usar)
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});

function updateSearchCounter(visiveis, total) {
  let counter = document.getElementById('search-counter');
  if (!counter) {
    counter = document.createElement('small');
    counter.id = 'search-counter';
    counter.className = 'text-muted ms-2';
    // Garante que o contador seja adicionado ao lugar certo
    const headerTitle = document.querySelector('.card-header h5');
    if (headerTitle) {
      headerTitle.appendChild(counter);
    }
  }
  
  if (visiveis === total || document.getElementById('busca').value === '') {
    counter.textContent = '';
  } else {
    counter.textContent = `(${visiveis} de ${total} resultados)`;
  }
}