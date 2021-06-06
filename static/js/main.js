document.addEventListener("DOMContentLoaded", () => {
	const $navbarBurgers = Array.prototype.slice.call(
		document.querySelectorAll(".navbar-burger"),
		0
	);
	if ($navbarBurgers.length > 0) {
		$navbarBurgers.forEach((el) => {
			el.addEventListener("click", () => {
				const target = el.dataset.target;
				const $target = document.getElementById(target);
				el.classList.toggle("is-active");
				$target.classList.toggle("is-active");
			});
		});
	}
	(document.querySelectorAll(".notification .delete") || []).forEach(
		($delete) => {
			const $notification = $delete.parentNode;
			$delete.addEventListener("click", () => {
				$notification.parentNode.removeChild($notification);
			});
		}
	);
});

const fileInput = document.querySelector('#file-js input[type=file]');
  fileInput.onchange = () => {
    if (fileInput.files.length > 0) {
      const fileName = document.querySelector('#file-js-example .file-name');
      fileName.textContent = fileInput.files[0].name;
    }
  }