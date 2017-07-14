/**
 * Created by Aggelos on 7/14/2017.
 */
(function($) {
    $(document).ready(function() {
        $('#id_director').on('change', function() {
            var $directorId = $(this).find('option:selected').val();

            $('#id_users')
                .find('option')
                .css('display', '')
                .filter('[value=' + $directorId + ']')
                .css('display', 'none');
        });
    });
})(django.jQuery);
