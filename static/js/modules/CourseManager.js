/**
 * @fileoverview CourseManager.js
 * Gestión de progreso de lecciones, interactividad LMS en cliente (localStorage),
 * evaluación de cuestionarios (quizzes) e inyección de botones de copiado de código.
 */

import { error as logError } from './logger.js';

export class CourseManager {
    constructor() {
        /** @type {HTMLElement | null} */
        this.layout = document.querySelector('.c-lesson-layout');
        if (!this.layout) return;

        /** @type {string | null} */
        this.courseId = this.layout.getAttribute('data-config-course-id');
        /** @type {string} */
        this.storageKey = `datamaq_course_${this.courseId}_progress`;

        /** @type {HTMLElement | null} */
        this.markBtn = document.getElementById('mark-complete-btn');
        /** @type {HTMLElement | null} */
        this.progressFill = document.getElementById('course-progress-fill');
        /** @type {HTMLElement | null} */
        this.progressText = document.getElementById('course-progress-text');
        /** @type {NodeListOf<HTMLElement>} */
        this.sidebarLessons = document.querySelectorAll('.c-lesson-sidebar-lesson-item');
        
        // Elementos del sidebar móvil
        /** @type {HTMLElement | null} */
        this.sidebar = document.getElementById('lesson-sidebar');
        /** @type {HTMLElement | null} */
        this.sidebarBackdrop = document.getElementById('sidebar-backdrop');
        /** @type {HTMLElement | null} */
        this.toggleSidebarBtn = document.getElementById('toggle-sidebar-btn');
        /** @type {HTMLElement | null} */
        this.closeSidebarBtn = document.getElementById('close-sidebar-btn');

        /** @type {string[]} */
        this.completedLessons = this.loadProgress();
        this.init();
    }

    /**
     * Inicializa los listeners y el estado visual de la lección.
     * @returns {void}
     */
    init() {
        // Inicializar barra lateral móvil
        if (this.sidebar && this.toggleSidebarBtn) {
            this.toggleSidebarBtn.addEventListener('click', () => this.openSidebar());
        }
        if (this.closeSidebarBtn) {
            this.closeSidebarBtn.addEventListener('click', () => this.closeSidebar());
        }
        if (this.sidebarBackdrop) {
            this.sidebarBackdrop.addEventListener('click', () => this.closeSidebar());
        }

        // Inicializar clases de completado en el sidebar según el localStorage
        this.sidebarLessons.forEach(item => {
            const lessonId = item.getAttribute('data-lesson-id');
            if (lessonId && this.completedLessons.includes(lessonId)) {
                item.classList.add('is-completed');
            }
        });

        // Inicializar el botón de marcar completado para la lección actual
        if (this.markBtn) {
            const currentLessonId = this.markBtn.getAttribute('data-lesson-id');
            if (currentLessonId && this.completedLessons.includes(currentLessonId)) {
                this.markBtn.classList.add('is-completed');
            }

            this.markBtn.addEventListener('click', () => {
                if (currentLessonId) {
                    this.toggleLessonComplete(currentLessonId);
                }
            });
        }

        // Inicializar lógica de cuestionario interactivo
        this.initQuiz();

        // Inicializar botones de copiar para bloques de código
        this.initCodeCopyButtons();

        // Actualizar porcentaje y barra de progreso al cargar
        this.updateProgressBar();
    }

    /**
     * Inicializa los manejadores de eventos para los cuestionarios (quizzes).
     * @returns {void}
     */
    initQuiz() {
        const quizContainer = document.getElementById('quiz-container');
        if (!quizContainer) return;

        const submitBtn = /** @type {HTMLButtonElement | null} */ (document.getElementById('quiz-submit-btn'));
        const resetBtn = /** @type {HTMLButtonElement | null} */ (document.getElementById('quiz-reset-btn'));
        const form = /** @type {HTMLFormElement | null} */ (document.getElementById('quiz-form'));
        /** @type {HTMLElement | null} */
        const resultContainer = document.getElementById('quiz-result');
        /** @type {HTMLElement | null} */
        const resultScore = document.getElementById('quiz-result-score');
        /** @type {NodeListOf<HTMLElement>} */
        const questionCards = quizContainer.querySelectorAll('.c-quiz-question-card');

        if (!form) return;

        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                // Verificar que se hayan respondido todas las preguntas
                const allAnswered = Array.from(questionCards).every(card => {
                    const questionId = card.getAttribute('data-question-id');
                    const checked = form.querySelector(`input[name="question_${questionId}"]:checked`);
                    return checked !== null;
                });

                if (!allAnswered) {
                    alert('Por favor, responde todas las preguntas antes de verificar.');
                    return;
                }

                let correctAnswersCount = 0;

                questionCards.forEach(card => {
                    const questionId = card.getAttribute('data-question-id');
                    const correctOption = parseInt(card.getAttribute('data-correct-option') || '0', 10);
                    const selectedInput = /** @type {HTMLInputElement | null} */ (form.querySelector(`input[name="question_${questionId}"]:checked`));
                    const selectedValue = selectedInput ? parseInt(selectedInput.value, 10) : NaN;
                    
                    const feedbackContainer = document.getElementById(`feedback_${questionId}`);
                    const badgeCorrect = feedbackContainer?.querySelector('.feedback-badge-correct');
                    const badgeIncorrect = feedbackContainer?.querySelector('.feedback-badge-incorrect');
                    
                    // Mostrar feedback
                    if (feedbackContainer) {
                        feedbackContainer.style.display = 'block';
                    }
                    if (selectedValue === correctOption) {
                        correctAnswersCount++;
                        if (badgeCorrect) /** @type {HTMLElement} */ (badgeCorrect).style.display = 'inline-flex';
                        if (badgeIncorrect) /** @type {HTMLElement} */ (badgeIncorrect).style.display = 'none';
                    } else {
                        if (badgeCorrect) /** @type {HTMLElement} */ (badgeCorrect).style.display = 'none';
                        if (badgeIncorrect) /** @type {HTMLElement} */ (badgeIncorrect).style.display = 'inline-flex';
                    }

                    // Deshabilitar opciones
                    /** @type {NodeListOf<HTMLInputElement>} */
                    const inputs = form.querySelectorAll(`input[name="question_${questionId}"]`);
                    inputs.forEach(input => { input.disabled = true; });
                });

                // Calcular e imprimir resultado
                const scorePercentage = Math.round((correctAnswersCount / questionCards.length) * 100);
                if (resultScore) {
                    resultScore.textContent = `Obtuviste ${scorePercentage}% (${correctAnswersCount} de ${questionCards.length} correctas)`;
                }
                if (resultContainer) {
                    resultContainer.style.display = 'block';
                }

                submitBtn.style.display = 'none';
                if (resetBtn) resetBtn.style.display = 'inline-flex';
                
                // Opcional: Marcar automáticamente la lección (quiz) como completada al verificarla
                const currentLessonId = this.markBtn ? this.markBtn.getAttribute('data-lesson-id') : null;
                if (currentLessonId && !this.completedLessons.includes(currentLessonId)) {
                    this.toggleLessonComplete(currentLessonId);
                }
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                // Habilitar y desmarcar opciones
                questionCards.forEach(card => {
                    const questionId = card.getAttribute('data-question-id');
                    /** @type {NodeListOf<HTMLInputElement>} */
                    const inputs = form.querySelectorAll(`input[name="question_${questionId}"]`);
                    inputs.forEach(input => {
                        input.disabled = false;
                        input.checked = false;
                    });

                    const feedbackContainer = document.getElementById(`feedback_${questionId}`);
                    if (feedbackContainer) {
                        feedbackContainer.style.display = 'none';
                    }
                });

                if (resultContainer) {
                    resultContainer.style.display = 'none';
                }

                resetBtn.style.display = 'none';
                if (submitBtn) submitBtn.style.display = 'inline-flex';
            });
        }
    }

    /**
     * Carga la lista de IDs de lecciones completadas desde localStorage.
     * @returns {string[]} Lista de identificadores de lecciones completadas.
     */
    loadProgress() {
        try {
            const data = localStorage.getItem(this.storageKey);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            logError('[CourseManager] Error cargando progreso:', e);
            return [];
        }
    }

    /**
     * Guarda la lista de IDs de lecciones completadas en localStorage.
     * @returns {void}
     */
    saveProgress() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.completedLessons));
        } catch (e) {
            logError('[CourseManager] Error guardando progreso:', e);
        }
    }

    /**
     * Marca o desmarca una lección como completada y actualiza el estado visual del LMS.
     * @param {string} lessonId - Identificador único de la lección.
     * @returns {void}
     */
    toggleLessonComplete(lessonId) {
        const index = this.completedLessons.indexOf(lessonId);
        let completed = false;

        if (index === -1) {
            this.completedLessons.push(lessonId);
            completed = true;
        } else {
            this.completedLessons.splice(index, 1);
        }

        this.saveProgress();

        // Actualizar el estado del botón en la interfaz
        if (this.markBtn && this.markBtn.getAttribute('data-lesson-id') === lessonId) {
            if (completed) {
                this.markBtn.classList.add('is-completed');
            } else {
                this.markBtn.classList.remove('is-completed');
            }
        }

        // Actualizar el item del sidebar correspondiente
        const sidebarItem = document.querySelector(`.c-lesson-sidebar-lesson-item[data-lesson-id="${lessonId}"]`);
        if (sidebarItem) {
            if (completed) {
                sidebarItem.classList.add('is-completed');
            } else {
                sidebarItem.classList.remove('is-completed');
            }
        }

        // Actualizar barra de progreso global
        this.updateProgressBar();
    }

    /**
     * Calcula y actualiza la barra de progreso y el texto de porcentaje.
     * @returns {void}
     */
    updateProgressBar() {
        const totalLessonsCount = this.sidebarLessons.length;
        if (totalLessonsCount === 0) return;

        const completedCount = this.completedLessons.length;
        const percentage = Math.round((completedCount / totalLessonsCount) * 100);

        if (this.progressFill) {
            this.progressFill.style.width = `${percentage}%`;
        }

        if (this.progressText) {
            this.progressText.textContent = `${percentage}% completado`;
        }
    }

    /**
     * Abre el sidebar de navegación en dispositivos móviles.
     * @returns {void}
     */
    openSidebar() {
        if (this.sidebar) this.sidebar.classList.add('is-open');
        if (this.sidebarBackdrop) this.sidebarBackdrop.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    }

    /**
     * Cierra el sidebar de navegación en dispositivos móviles.
     * @returns {void}
     */
    closeSidebar() {
        if (this.sidebar) this.sidebar.classList.remove('is-open');
        if (this.sidebarBackdrop) this.sidebarBackdrop.classList.remove('is-open');
        document.body.style.overflow = '';
    }

    /**
     * Inyecta distintivos visuales y botones de copia diferenciando comandos CLI de salidas de terminal.
     * @returns {void}
     */
    initCodeCopyButtons() {
        const codeBlocks = document.querySelectorAll('.c-lesson-body pre, .markdown-body pre, pre');
        if (!codeBlocks.length) return;

        const outputLanguages = ['text', 'output', 'console', 'plain', 'raw', 'log', 'stdout', 'stderr'];
        const inputLanguages = ['bash', 'sh', 'shell', 'zsh', 'powershell', 'cmd'];

        codeBlocks.forEach((pre) => {
            if (pre.querySelector('.c-code-copy-btn') || pre.querySelector('.c-code-badge')) return;

            const codeElement = /** @type {HTMLElement} */ (pre.querySelector('code') || pre);
            const classList = Array.from(codeElement.classList).concat(Array.from(pre.classList));
            const langClass = classList.find(c => c.startsWith('language-') || c.startsWith('lang-')) || '';
            const lang = langClass.replace(/^(language-|lang-)/, '').toLowerCase();

            const rawText = (codeElement.innerText || codeElement.textContent || '').trim();

            // Heurística para detectar si el bloque es una salida de terminal (Output)
            const isOutputBlock = outputLanguages.includes(lang) || 
                rawText.startsWith('Output:') || 
                rawText.startsWith('Completed At:') ||
                rawText.startsWith('HTTP/1.1') ||
                rawText.startsWith('=============================') ||
                (lang === '' && (rawText.includes('INFO:') || rawText.includes('error:') || rawText.includes('WARN:')));

            if (isOutputBlock) {
                // Configurar como bloque de Salida (Sin botón de copiar)
                pre.classList.add('c-code-block--output');
                const outputBadge = document.createElement('span');
                outputBadge.className = 'c-code-badge c-code-badge--output';
                outputBadge.innerHTML = '<i class="bi bi-terminal"></i> Salida de Terminal';
                pre.appendChild(outputBadge);
                return;
            }

            // Si es un bloque de Comando CLI (Input)
            const isCliInput = inputLanguages.includes(lang) || rawText.startsWith('$ ') || rawText.startsWith('> ');

            if (isCliInput) {
                const inputBadge = document.createElement('span');
                inputBadge.className = 'c-code-badge c-code-badge--input';
                inputBadge.innerHTML = '<i class="bi bi-terminal-fill"></i> Ejecutar en Terminal';
                pre.appendChild(inputBadge);
            }

            // Inyectar Botón de Copiado para comandos y código ejecutable
            const copyBtn = document.createElement('button');
            copyBtn.type = 'button';
            copyBtn.className = 'c-code-copy-btn';
            copyBtn.setAttribute('aria-label', 'Copiar código al portapapeles');
            copyBtn.setAttribute('title', 'Copiar al portapapeles');
            copyBtn.innerHTML = '<i class="bi bi-clipboard"></i> <span>Copiar</span>';

            copyBtn.addEventListener('click', async () => {
                let textToCopy = codeElement.innerText || codeElement.textContent || '';

                // Si es comando de consola, limpiar los símbolos de prompt ($ o >) al copiar
                if (isCliInput) {
                    textToCopy = textToCopy
                        .split('\n')
                        .map(line => line.replace(/^[\$\>]\s?/, ''))
                        .join('\n');
                }

                try {
                    await navigator.clipboard.writeText(textToCopy.trim());
                    copyBtn.classList.add('is-copied');
                    copyBtn.innerHTML = '<i class="bi bi-check2"></i> <span>¡Copiado!</span>';

                    setTimeout(() => {
                        copyBtn.classList.remove('is-copied');
                        copyBtn.innerHTML = '<i class="bi bi-clipboard"></i> <span>Copiar</span>';
                    }, 2000);
                } catch (err) {
                    logError('[CourseManager] Error al copiar texto al portapapeles:', err);
                }
            });

            pre.appendChild(copyBtn);
        });
    }
}

// Inicialización automática robusta
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new CourseManager());
} else {
    new CourseManager();
}
