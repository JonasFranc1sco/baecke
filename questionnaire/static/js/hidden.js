document.addEventListener('DOMContentLoaded', function () {
    function isTruthyValue(val) {
        if (val === null || val === undefined) return false;
        const s = String(val).trim().toLowerCase();
        return ['true', '1', 'on', 'yes', 'sim'].includes(s);
    }

    function getControlValue(name) {
        const checked = document.querySelector(`input[name="${name}"]:checked`);
        if (checked) return checked.value;
        // Se não houver nenhum input marcado, NÃO devolvemos o value do primeiro
        // elemento encontrado (isso fazia com que um select vazio ou um radio
        // não marcado ainda retornasse um valor e mostrasse os blocos).
        // Apenas para controles não-radio/checkbox (ex: select, input text)
        // podemos devolver seu value padrão; caso contrário retornamos null.
        const el = document.querySelector(`[name="${name}"]`);
        if (el) {
            const type = el.type || el.tagName.toLowerCase();
            if (type === 'checkbox') return el.checked ? el.value || 'true' : null;
            if (type === 'select-one' || el.tagName.toLowerCase() === 'select' || type === 'text' || type === 'hidden') {
                return el.value || null;
            }
        }
        return null;
    }

    function wireBoolean(groupName, containerClasses) {
        const boolName = `${groupName}_boolean`;

        function toggle() {
            const val = getControlValue(boolName);
            const show = isTruthyValue(val);

            containerClasses.forEach(containerClass => {
                document.querySelectorAll(`.${containerClass}`).forEach(node => {
                    node.style.display = show ? 'block' : 'none';
                });
            });
        }

        // Sempre inicia ocultando
        containerClasses.forEach(containerClass => {
            document.querySelectorAll(`.${containerClass}`).forEach(node => {
                node.style.display = 'none';
            });
        });

        // Observa mudanças
        document.querySelectorAll(`[name="${boolName}"]`).forEach(el => {
            el.addEventListener('change', toggle);
        });

        // Aplica estado inicial correto
        toggle();
    }

    // 1️⃣ Quando question_9_boolean = false → esconde tudo (inclusive 9_other)
    // Aqui o controle principal só mostra/oculta o bloco principal. O bloco
    // "other" será controlado pelo seu próprio booleano. Quando o principal
    // ficar false nós também garantimos que o bloco "other" permaneça oculto.
    wireBoolean('question_9', ['question-9-condicional']);

    // 2️⃣ Quando question_9_other_boolean = false → esconde apenas o grupo "outro"
    wireBoolean('question_9_other', ['question-9-other-condicional']);

    // Garantir que quando o controle principal for alterado para false, o
    // bloco "other" seja forçado a esconder. Quando for alterado para true,
    // reavaliamos o estado do booleano interno (disparando change) para que
    // o seu toggle mostre/oculte corretamente o conteúdo interno.
    document.querySelectorAll(`[name="question_9_boolean"]`).forEach(el => {
        el.addEventListener('change', function () {
            const val = getControlValue('question_9_boolean');
            const showMain = isTruthyValue(val);
            if (!showMain) {
                document.querySelectorAll('.question-9-other-condicional').forEach(node => node.style.display = 'none');
            } else {
                // Re-dispara change nos radios internos para que sua lógica
                // toggle() seja aplicada (vai esconder, pois nada está marcado).
                document.querySelectorAll(`[name="question_9_other_boolean"]`).forEach(n => {
                    n.dispatchEvent(new Event('change'));
                });
            }
        });
    });
});
