document.querySelectorAll('.list-group-item').forEach(item => {
    item.addEventListener('mouseenter', function () {
        this.style.backgroundColor = '#f8f9fa';
        this.style.transition = 'background-color 0.2s ease';
    });

    item.addEventListener('mouseleave', function () {
        this.style.backgroundColor = '';
    });
});

// Destacar o item mais recente
const firstItem = document.querySelector('.list-group-item:first-child');
if (firstItem) {
    firstItem.style.borderLeft = '4px solid #007bff';
}