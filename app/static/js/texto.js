  window.onload = function() {
    function editTitle() {
      var title = document.getElementsByTagName('   ')[0];
      var span = title.firstChild;
      span.onmouseover = function() {
        this.title = 'Clique para editar o texto';
        this.style.background = '#f5f5f5';
      }
      span.onmouseout = function() {
        this.title = '';
        this.style.background = '';
      }
      span.onclick = function() {
        var textoAtual = this.firstChild.nodeValue;
        var input = '<input type="text" name="1" value="' + textoAtual + '">';
        this.innerHTML = input;
        var field = this.firstChild;
        this.onclick = null;
        this.onmouseover = null;
        field.focus();
        field.select();
        field.onblur = function() {
          this.parentNode.innerHTML = this.value;
          editTitle();
        }
      }
    }
    editTitle();
  }