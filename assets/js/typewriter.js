/**
 * Typewriter Effect
 * Simulates typing animation with cursor blink
 */

class Typewriter {
    constructor(element, options = {}) {
        this.element = typeof element === 'string' ? document.querySelector(element) : element;
        if (!this.element) return;

        this.texts = options.texts || ['Software Architect', '软件架构师'];
        this.typingSpeed = options.typingSpeed || 80;
        this.deletingSpeed = options.deletingSpeed || 50;
        this.pauseDelay = options.pauseDelay || 2000;
        this.cursor = options.cursor !== false;

        this.textIndex = 0;
        this.charIndex = 0;
        this.isDeleting = false;
        this.isPaused = false;

        if (this.cursor) {
            this.addCursor();
        }

        this.type();
    }

    addCursor() {
        const cursor = document.createElement('span');
        cursor.className = 'typewriter-cursor';
        cursor.textContent = '|';
        this.element.appendChild(cursor);
    }

    getCurrentText() {
        return this.texts[this.textIndex];
    }

    type() {
        const currentText = this.getCurrentText();

        if (this.isDeleting) {
            // Delete one character
            this.charIndex--;
            this.element.childNodes[0].textContent = currentText.substring(0, this.charIndex);

            if (this.charIndex === 0) {
                this.isDeleting = false;
                this.textIndex = (this.textIndex + 1) % this.texts.length;
            }
        } else {
            // Type one character
            this.charIndex++;
            this.element.childNodes[0].textContent = currentText.substring(0, this.charIndex);

            if (this.charIndex === currentText.length) {
                this.isDeleting = true;
                this.isPaused = true;
                setTimeout(() => {
                    this.isPaused = false;
                    this.type();
                }, this.pauseDelay);
                return;
            }
        }

        if (!this.isPaused) {
            const speed = this.isDeleting ? this.deletingSpeed : this.typingSpeed;
            setTimeout(() => this.type(), speed);
        }
    }
}

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    const typewriterEl = document.querySelector('.typing-text');
    if (typewriterEl) {
        const lang = window.CURRENT_LANG || 'cn';
        const texts = lang === 'cn'
            ? ['软件架构师 · 技术极客', '120+ 专利持有者', '10年+ 互联网经验']
            : ['Software Architect · Tech Geek', '120+ Patent Holder', '10+ Years Experience'];

        window.typewriter = new Typewriter(typewriterEl, {
            texts: texts,
            typingSpeed: 100,
            deletingSpeed: 60,
            pauseDelay: 2500
        });
    }
});
