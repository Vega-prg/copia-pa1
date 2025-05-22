document.addEventListener('DOMContentLoaded', function() {
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');

    sidebarCollapse.addEventListener('click', function() {
        sidebar.classList.toggle('active');
        content.classList.toggle('active');
    });
});