document.addEventListener("submit", (event) => {
  const form = event.target;
  const dangerButton = event.submitter;

  if (dangerButton && dangerButton.classList.contains("btn-outline-danger")) {
    const ok = window.confirm("Confirmar esta acao?");
    if (!ok) {
      event.preventDefault();
    }
  }
});
