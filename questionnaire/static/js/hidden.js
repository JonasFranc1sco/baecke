
$(document).ready(function () {
    const mainBoolean = $("[name='question_9_boolean']");
    const otherBoolean = $("[name='question_9_other_boolean']");

    const mainFields = $(".question-9-main-field");
    const otherFields = $(".question-9-other-field");

    const mainBooleanBlock = $("#question-9-boolean-block");
    const otherBooleanBlock = $("#question-9-other-boolean-block");

    // choice_002 corresponde a "Sim"
    function isYes(field) {
        return field.filter(":checked").val() === "choice_002";
    }

    function setVisibility(elements, visible) {
        elements.each(function () {
            const element = $(this);
            element.prop("hidden", !visible);
            element.toggle(visible);
            element.find("input, select, textarea").each(function () {
                const field = $(this);

                field.prop("disabled", !visible);

                if (!visible) {
                    if (field.is(":radio, :checkbox")) {
                        field.prop("checked", false);
                    } else {
                        field.val("");
                    }

                    if (field.hasClass("select2-hidden-accessible")) {
                        field.trigger("change");
                    }
                }
            });
        });
    }

    function updateVisibility() {
        const showMain = isYes(mainBoolean);

        // Pergunta principal: question_9, question_9_time e question_9_proportion
        setVisibility(mainFields, showMain);

        // Pergunta sobre a realização de outro exercício
        setVisibility(otherBooleanBlock, showMain);

        const showOther = showMain && isYes(otherBoolean);

        // Campos do segundo exercício
        setVisibility(otherFields, showOther);
    }

    $(document).on(
        "change",
        "[name='question_9_boolean'], [name='question_9_other_boolean']",
        updateVisibility
    );

    // Define a visibilidade inicial ao abrir a página
    updateVisibility();
});
