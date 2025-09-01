document.getElementById('uploadForm').addEventListener('submit', function(e) {
  const submitBtn = document.getElementById('submitBtn');
  const fileInput = document.getElementById('arquivo_excel');

  if (!fileInput.files.length) {
    e.preventDefault();
    return;
  }

  submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processando...';
  submitBtn.disabled = true;

  document.querySelector('.card').classList.add('processing');
});

setTimeout(function() {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function(alert) {
    const bsAlert = new bootstrap.Alert(alert);
    bsAlert.close();
  });
}, 5000);