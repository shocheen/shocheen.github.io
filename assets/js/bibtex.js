document.querySelectorAll('.copy-bibtex').forEach(function (button) {
  button.hidden = false;
  button.addEventListener('click', async function () {
    var panel = button.closest('.bibtex-panel');
    var code = panel.querySelector('code');
    var status = panel.querySelector('.bibtex-status');
    status.textContent = '';
    try {
      await navigator.clipboard.writeText(code.textContent);
      status.textContent = 'Copied!';
    } catch (error) {
      var selection = window.getSelection();
      var range = document.createRange();
      range.selectNodeContents(code);
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = 'Text selected. Copy it with your keyboard.';
    }
  });
});
