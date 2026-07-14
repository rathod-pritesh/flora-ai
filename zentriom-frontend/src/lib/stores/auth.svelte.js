import { browser } from '$app/environment';

export const authStore = $state({
	user: null,
	token: null,
	isAuthenticated: false,
	loading: false,
	cachedAvatar: null
});

export async function cacheGoogleAvatar(url) {
	if (!browser || !url) return;
	try {
		const cached = localStorage.getItem('zentriom_avatar_cache');
		if (cached) {
			authStore.cachedAvatar = cached;
			return;
		}

		const response = await fetch(url, { mode: 'cors' });
		if (!response.ok) return;
		const blob = await response.blob();

		const reader = new FileReader();
		reader.onloadend = () => {
			const base64 = reader.result;
			localStorage.setItem('zentriom_avatar_cache', base64);
			authStore.cachedAvatar = base64;
		};
		reader.readAsDataURL(blob);
	} catch (e) {
		console.warn('Could not cache avatar locally:', e);
	}
}

export function setAuth(user, token) {
	authStore.user = user;
	authStore.token = token;
	authStore.isAuthenticated = true;

	localStorage.setItem(
		'auth',
		JSON.stringify({
			user,
			token
		})
	);

	if (user?.picture) {
		cacheGoogleAvatar(user.picture);
	}
}

export function loadAuth() {
	if (!browser) return;
	const stored = localStorage.getItem('auth');

	if (!stored) return;

	try {
		const data = JSON.parse(stored);

		authStore.user = data.user;
		authStore.token = data.token;
		authStore.isAuthenticated = true;
		authStore.cachedAvatar = localStorage.getItem('zentriom_avatar_cache');

		if (data.user?.picture && !authStore.cachedAvatar) {
			cacheGoogleAvatar(data.user.picture);
		}
	} catch (err) {
		console.error('Failed to load auth', err);
		localStorage.removeItem('auth');
		localStorage.removeItem('zentriom_avatar_cache');
	}
}

export function logout() {
	authStore.user = null;
	authStore.token = null;
	authStore.isAuthenticated = false;
	authStore.loading = false;
	authStore.cachedAvatar = null;

	localStorage.removeItem('auth');
	localStorage.removeItem('zentriom_avatar_cache');
}
