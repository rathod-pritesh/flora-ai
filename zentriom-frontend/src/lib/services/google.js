let initialized = false;

export function initGoogleLogin(callback, buttonElementId) {
	if (typeof window === 'undefined') return;

	const checkAndInit = () => {
		if (!window.google || !window.google.accounts || !window.google.accounts.id) {
			// Check again in 50ms if script is still loading
			setTimeout(checkAndInit, 50);
			return;
		}

		if (!initialized) {
			window.google.accounts.id.initialize({
				client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
				callback: (response) => {
					if (callback) callback(response);
				}
			});
			initialized = true;
		}

		if (buttonElementId) {
			const btnElement = document.getElementById(buttonElementId);
			if (btnElement) {
				window.google.accounts.id.renderButton(btnElement, {
					theme: 'outline',
					size: 'large',
					text: 'continue_with',
					shape: 'rectangular',
					width: btnElement.offsetWidth || 382
				});
			}
		}
	};

	checkAndInit();
}
