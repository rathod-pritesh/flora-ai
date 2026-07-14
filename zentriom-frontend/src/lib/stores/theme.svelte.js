import { browser } from '$app/environment';

class ThemeStore {
	theme = $state('light'); // 'light' | 'dark' | 'system'

	constructor() {
		if (browser) {
			const saved = localStorage.getItem('zentriom_theme');
			if (saved === 'light' || saved === 'dark' || saved === 'system') {
				this.theme = saved;
			} else {
				this.theme = 'light';
			}
			this.applyTheme(this.theme);

			// Listen for system color scheme changes in real-time
			const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
			mediaQuery.addEventListener('change', () => {
				if (this.theme === 'system') {
					this.applyTheme('system');
				}
			});
		}
	}

	setTheme(newTheme) {
		this.theme = newTheme;
		if (browser) {
			localStorage.setItem('zentriom_theme', newTheme);
			this.applyTheme(newTheme);
		}
	}

	applyTheme(theme) {
		if (!browser) return;

		let isDark = false;
		if (theme === 'dark') {
			isDark = true;
		} else if (theme === 'light') {
			isDark = false;
		} else {
			// System theme logic
			isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
		}

		if (isDark) {
			document.documentElement.classList.add('dark');
		} else {
			document.documentElement.classList.remove('dark');
		}
	}
}

export const themeStore = new ThemeStore();
