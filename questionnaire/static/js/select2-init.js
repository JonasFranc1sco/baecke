$(document).ready(function () {
    $('#id_question_1, #id_question_9, #id_question_9_other').select2({
        placeholder: 'Digite para buscar uma opção...',
        allowClear: true,
        width: '100%',
        minimumResultsForSearch: 0,
        language: {
            noResults: function() { return "Nenhuma opção encontrada"; }
        }
    });

    $('select:not(#id_question_1, #id_question_9, #id_question_9_other)').select2({
        placeholder: 'Selecionar',
        minimumResultsForSearch: Infinity,
        width: '100%',
        allowClear: true
    });
});
