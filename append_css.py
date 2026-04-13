css_append = """

/* ---- Dropdown Menus ---- */
.dropdown-wrapper {
  position: relative;
  display: inline-block;
}

.dropdown-menu {
  display: none;
  position: absolute;
  top: 100%;
  right: -10px;
  width: 250px;
  background: var(--bg-surface-hover);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 15px;
  box-shadow: var(--shadow-float);
  z-index: 1000;
  animation: slideUp 0.3s var(--ease-out-expo);
}

.dropdown-wrapper:hover .dropdown-menu {
  display: block;
}

/* ---- Floating Copilot ---- */
.floating-copilot {
  position: fixed;
  bottom: 20px;
  left: 90px;
  width: 320px;
  background: var(--bg-surface);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-float);
  z-index: 900;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s var(--ease-out-expo);
  transform-origin: bottom left;
}

.floating-copilot--collapsed {
  transform: translateY(calc(100% - 40px));
}

.floating-copilot__header {
  padding: 10px 15px;
  background: rgba(139, 92, 246, 0.15);
  border-bottom: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 13px;
  color: var(--text-primary);
  cursor: pointer;
}

.floating-copilot__body {
  padding: 10px;
}

/* Scrollbar hides for chips */
.copilot-chips::-webkit-scrollbar {
  display: none;
}
"""

with open('css/stadium-os.css', 'a', encoding='utf-8') as f:
    f.write(css_append)
print("CSS appended.")
