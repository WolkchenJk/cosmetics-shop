(function($) {
  $(function(){
    var cat = $('#id_category');
    var priceRow = $('.form-row.field-price');
    if (!cat.length || !priceRow.length) return;

    function toggle() {
      var name = cat.find('option:selected').text().trim().toLowerCase();
      // если текст пункта = "ароматы"
      if (name === 'ароматы') {
        priceRow.hide();
      } else {
        priceRow.show();
      }
    }

    // вешаем на изменение селектора и сразу вызываем
    cat.on('change', toggle);
    toggle();
  });
})(django.jQuery);

