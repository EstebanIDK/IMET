document.addEventListener('DOMContentLoaded', function() {
  let arrows = document.querySelectorAll(".bxs-chevron-down");
  let sidebar = document.querySelector(".sidebar");
  let sidebarBtn = document.querySelector(".bx-menu");

  if (sidebarBtn) {
      sidebarBtn.addEventListener("click", () => {
          if (sidebar) {
              sidebar.classList.toggle("close");
          }
      });
  }

  arrows.forEach((arrow) => {
      arrow.addEventListener("click", (e) => {
          let arrowParent = e.target.closest('.iocn-link');
          if (arrowParent) {
              arrowParent.classList.toggle("showMenu");
              
              let subMenu = arrowParent.nextElementSibling;
              if (subMenu && subMenu.classList.contains('sub-menu')) {
                  subMenu.style.display = subMenu.style.display === 'block' ? 'none' : 'block';
              }
              
              
              e.target.style.transform = e.target.style.transform === 'rotate(180deg)' ? 'rotate(0deg)' : 'rotate(180deg)';
          }
      });
  });
});